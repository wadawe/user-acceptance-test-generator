#!/usr/bin/env python
# ----------------------------------------------------------------------------------------------------
# Implements an Output Handler class for the Acceptance Test Generator
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

from pandas import ExcelWriter, DataFrame
from spacy.language import Language
import xlsxwriter

class Output:
    """
    Output Handler Class
    """

    def __init__( self, nlp: Language, requirements: dict, relationships: dict ) -> None:
        """
        Initialise an Output class

        Parameters: 
            - self: the current class instance
            - nlp: The nlp pipeline processor
            - requirements: List of requirement strings and their handlers
            - relationships: Dictionary of relationships

        Returns:
            - An Output instance
        """

        self.nlp = nlp 
        self.requirements = requirements
        self.relationships = relationships
        self.writer = None
        self.summary = {}

    def displayTest( self, test_number: int, chain: tuple ) -> None:
        """
        Display a chosen acceptance test table in the console

        Parameters: 
            - self: the current class instance
            - test_number: The acceptance test number
            - chain: A chain of acceptance steps for the test table

        Returns:
            - None
        """

        # Display table header
        print( "=" * 150 )
        print( "ACCEPTANCE TEST #{}".format( test_number ).center( 150 ) )
        print( "=" * 150 )
        print( "{:>6} | {:<60} | {:<30} | {:<20} | {:<20} |".format( "Step", "Action", "Observation", "Requirements", "Priority" ) )
        print( "=" * 150 )

        # Display table steps
        for link_index, chain_link in enumerate( chain ):
            action_text = self.getActionText( chain_link )
            observation_text = self.getObservationText( chain_link )
            source_text = self.getRequirementsText( chain_link )
            priority_text = self.getPriorityText( chain_link )
            print( "{:>6} | {:<60} | {:<30} | {:<20} | {:<20} |".format( link_index + 1, action_text, observation_text, source_text, priority_text ) )
        print( "=" * 150 )

    def getActionText( self, chain_link: tuple ) -> str:
        """
        Create the action text for an acceptance test step

        Parameters: 
            - self: the current class instance
            - chain_link: A step tuple for the test

        Returns:
            - An action string
        """

        chain_tokens = self.relationships[ chain_link ][ "tokens" ]
        return " ".join( [ token.text for group in chain_tokens for token in group ] )

    def getObservationText( self, chain_link: tuple ) -> str:
        """
        Create the observation text for an acceptance test step

        Parameters: 
            - self: the current class instance
            - chain_link: A step tuple for the test

        Returns:
            - An observation string
        """

        chain_tokens = self.relationships[ chain_link ][ "tokens" ]
        return " ".join( [ token.text for token in chain_tokens[ 2 ] ] ) + " " + " ".join( [ token.text for token in chain_tokens[ 1 ] ] )

    def getRequirementsText( self, chain_link: tuple ) -> str:
        """
        Create the requirements text for an acceptance test step

        Parameters: 
            - self: the current class instance
            - chain_link: A step tuple for the test

        Returns:
            - A requirements string
        """

        return ", ".join( [ str( requirement_number ) for requirement_number in self.relationships[ chain_link ][ "requirements" ] ] )

    def getPriorityText( self, chain_link: tuple ) -> str:
        """
        Create the priority text for an acceptance test step

        Parameters: 
            - self: the current class instance
            - chain_link: A step tuple for the test

        Returns:
            - A priority string
        """

        # Find highest priority value from requirement priorities for the relationship
        for priority in [ "must", "should", "could", "will not" ]:
            if priority in self.relationships[ chain_link ][ "priorities" ]:
                return priority

        # Highest priority could not be found
        # Shouldn't hit this value
        return "error"

    def createWriter( self, name: str ) -> None:
        """
        Create a excel writer for use in test exporting

        Parameters: 
            - self: the current class instance
            - name: The file name to export to

        Returns:
            - None
        """

        self.writer = ExcelWriter( name, engine="xlsxwriter" )
        print( "Created writer for file: {}".format( name ) )

        # Create a dictionary of empty arrays for the summary sheet data
        self.summary = { "": [] }
        for requirement_index in range( 0, len( self.requirements ) ):
            self.summary[ "Req #" + str( requirement_index + 1 ) ] = []

    def addTest( self, test_number: int, chain: tuple ) -> None:
        """
        Add a test to the exporting excel writer

        Parameters: 
            - self: the current class instance
            - test_number: The acceptance test number
            - chain: A chain of acceptance steps for the test table

        Returns:
            - None
        """

        test_data = { "Step": [], "Action": [], "Observation": [], "Requirements": [], "Priority": [] }

        # Iterate test chain links
        # Save link features as test step
        for link_index, chain_link in enumerate( chain ):
            test_data[ "Step" ].append( str( link_index + 1 ) )
            test_data[ "Action" ].append( self.getActionText( chain_link ) )
            test_data[ "Observation" ].append( self.getObservationText( chain_link ) )
            test_data[ "Requirements" ].append( self.getRequirementsText( chain_link ) )
            test_data[ "Priority" ].append( self.getPriorityText( chain_link ) )

        # Add test to summary
        self.updateSummary( test_number, chain )

        # Add test chain to output file
        test_data = DataFrame( test_data )
        test_data.to_excel( self.writer, sheet_name = "Test #" + str( test_number ) )
        print( "> Exported test: {}".format( test_number ) )

    def updateSummary( self, test_number: int, chain: tuple ) -> None:
        """
        Add a test to the summary sheet

        Parameters: 
            - self: the current class instance
            - test_number: The acceptance test number
            - chain: A chain of acceptance steps for the test table

        Returns:
            - None
        """

        # Add the current test as a row to the summary table
        self.summary[ "" ].append( "Test #" + str( test_number ) )
        requirements_list = []

        # Create list of requirement numbers for whole test chain
        for chain_link in chain:
            for requirement_number in self.relationships[ chain_link ][ "requirements" ]:
                if requirement_number not in requirements_list:
                    requirements_list.append( requirement_number )

        # Update summary table
        # Column has "X" if requirement is a part of the current test
        # Column has "-" if requirement is not a part of the current test
        for requirement_index in range( 0, len( self.requirements ) ):
            self.summary[ "Req #" + str( requirement_index + 1 ) ].append( "X" if requirement_index + 1 in requirements_list else "-" )

    def saveWriter( self ) -> None:
        """
        Save the excel writer to the defined file

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        # Add summary sheet to workbook
        summary_data = DataFrame( self.summary )
        summary_data.to_excel( self.writer, sheet_name = "Summary" )

        # Move summary sheet to start of workbook
        worksheet_length = len( self.writer.book.worksheets_objs )
        self.writer.book.worksheets_objs.insert( 0, self.writer.book.worksheets_objs.pop( worksheet_length - 1 ) )

        # Save workbook
        self.writer.save()
        print( "Exported test file!" )
