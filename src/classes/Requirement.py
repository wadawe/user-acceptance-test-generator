#!/usr/bin/env python
# ----------------------------------------------------------------------------------------------------
# Implements an Requirement Handler class for the Acceptance Test Generator
#
# Copyright (C) 2021 wadawe
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>
# ----------------------------------------------------------------------------------------------------

from spacy.tokens.token import Token
from spacy.language import Language
from spacy.matcher import DependencyMatcher
from classes.Pattern import Pattern

class Requirement:
    """
    Requirement Handler Class
    """
    
    def __init__( self, identifier: int, priority: str, text: str, nlp: Language ) -> None:
        """
        Initialise a Requirement class

        Parameters: 
            - self: the current class instance
            - identifier: The requirement number
            - priority: The requirement MoSCoW priority
            - text: The full requirement string
            - nlp: The nlp pipeline processor

        Returns:
            - A Requirement instance
        """

        self.identifier = identifier
        self.priority = priority
        self.text = text 
        self.nlp = nlp
        self.doc = None 
        self.relationships = {}

    def getRelationships( self, pattern_style: str ) -> dict:
        """
        Get relationships from the current requirement

        Parameters: 
            - self: the current class instance
            - pattern_style: The match style to use

        Returns:
            - A list of relationship tuples
        """

        self.relationships = {}

        # Create the nlp doc
        if self.doc == None:
            self.doc = self.nlp( self.text.lower() )

        # Execute pattern handling method
        # Operator ">" matches direct word links
        # Operator ">>" matches nested word links 
        pattern_operator = ">" if pattern_style == "default" else ">>"
        pattern_handler = Pattern( pattern_operator )
        for pattern_identifier, pattern in pattern_handler.patterns.items():
            pattern_structure, index_groups = pattern
            found_relationsips = self.findPattern( pattern_identifier, pattern_structure, index_groups )

            # Add found relationships to list of requirement relationships
            for relationship_identifier in found_relationsips:
                if relationship_identifier not in self.relationships:
                    self.relationships[ relationship_identifier ] = found_relationsips[ relationship_identifier ] 

        # Return created relationships
        return self.relationships

    def findPattern( self, pattern_identifier: str, pattern_structure: tuple, index_groups: list ) -> dict:
        """
        Search the doc for a relationship pattern

        Parameters: 
            - self: the current class instance
            - pattern_identifier: The idenfitier for the given pattern
            - pattern_structure: The pattern to search for
            - index_groups: The pattern index groups to create a relationship from

        Returns:
            - Found Relationships
        """

        found_relationsips = {}
        
        # Create dependency matcher
        matcher = DependencyMatcher( self.nlp.vocab )
        matcher.add( "SEARCH", [ pattern_structure ] )
        requirement_matches = matcher( self.doc ) 

        # Iterate requirement pattern matches
        for match in requirement_matches:
            found_relationship = []
            matched_token_identifiers = match[ 1 ]

            # Iterate pattern index groups
            for index_group in index_groups:
                group_tokens = [] 

                # Iterate token indexes in index group
                for token_index in index_group:

                    # Add token and its compounds to relationship
                    if str( token_index ).isdigit():
                        group_tokens.extend( self.getCompounds( self.doc[ matched_token_identifiers[ token_index ] ] ) )
                        group_tokens.append( self.doc[ matched_token_identifiers[ token_index ] ] )

                    # Token index is actually string value for relationship
                    else:
                        group_tokens.extend( token for token in self.nlp( token_index.lower() ) )

                # Add text group to relationship
                found_relationship.append( tuple( text for text in group_tokens ) )

            # Add relationship to list of relationships
            found_relationship = tuple( relationship_group for relationship_group in found_relationship )
            tuple_identifier = tuple( tuple( token.lemma_ for token in token_group ) for token_group in found_relationship )
            if tuple_identifier not in found_relationsips:
                found_relationsips[ tuple_identifier ] = { "pattern": pattern_identifier, "tokens": found_relationship }
        
        # Return found relationships
        return found_relationsips

    def getCompounds( self, token: Token ):
        """
        Recursive handle to retrieve prefixed compound dependencies of a token

        Parameters: 
            - self: the current class instance
            - token: The token to parse

        Returns:
            - List of token compounds
        """

        print( type(token ))
        token_compounds = []
        print( "> Assessing token: (TEXT={}) (POS={}) (DEP={}) (TAG={})".format( token.text, token.pos_, token.dep_, token.tag_ ) )

        # Iterate token dependencies
        # Look for relevant token compounds
        for child in token.children:
            print( "  - Child found: (TEXT={}) (POS={}) (DEP={}) (TAG={})".format( child.text, child.pos_, child.dep_, child.tag_ ) )
            if child.pos_ == "NUM" and child.dep_ == "nummod":
                token_compounds.extend( self.getCompounds( child ) )
                token_compounds.append( child )
            elif child.pos_ == "VERB" and child.dep_ == "amod":
                token_compounds.extend( self.getCompounds( child ) )
                token_compounds.append( child )
            elif child.pos_ == "NOUN" and child.dep_ == "compound":
                token_compounds.extend( self.getCompounds( child ) )
                token_compounds.append( child )
            elif child.pos_ == "ADV" and child.dep_ == "advmod":
                token_compounds.extend( self.getCompounds( child ) )
                token_compounds.append( child )
            elif child.pos_ == "ADJ" and child.dep_ == "amod":
                token_compounds.extend( self.getCompounds( child ) )
                token_compounds.append( child )
            elif child.pos_ == "NOUN" and child.dep_ == "npadvmod":
                token_compounds.extend( self.getCompounds( child ) )
                token_compounds.append( child )
            elif child.pos_ == "PART" and child.dep_ == "neg":
                token_compounds.extend( self.getCompounds( child ) )
                token_compounds.append( child )
            elif child.pos_ == "SCONJ" and child.dep_ == "quantmod":
                token_compounds.extend( self.getCompounds( child ) )
                token_compounds.append( child )
        
        # Return linked compounds
        return token_compounds
