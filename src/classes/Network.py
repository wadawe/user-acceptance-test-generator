#!/usr/bin/env python
# ----------------------------------------------------------------------------------------------------
# Implements an Network Handler class for the Acceptance Test Generator
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
from collections import defaultdict
import networkx as netx
import matplotlib.pyplot as plt
from networkx.classes.multidigraph import MultiDiGraph

class Network:
    """
    Network Handler Class
    """

    def __init__( self, relationships: dict ) -> None:
        """
        Initialise a Network class

        Parameters: 
            - self: the current class instance
            - relationships: Dictionary of relationship classes

        Returns:
            - A Network instance
        """

        self.relationships = relationships
        self.chains = ()
        self.data = defaultdict( set )
        self.labels = {}
        self.handled = []
        self.createNetwork()

    def createNetwork( self ) -> None:
        """
        Create the network data structure from the relationships

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        # Iterate requirement relationships
        for relationship_identifier in self.relationships:

            # Pull tokens from relationship structure
            first_group = self.relationships[ relationship_identifier ][ "tokens" ][ 0 ]

            # Create network identifier from first group in relationship
            network_identifier = tuple( token.lemma_ for token in first_group )

            # Add relationship to network structure
            self.data[ network_identifier ].add( relationship_identifier )

    def getChains( self, chain_style: str ) -> tuple:
        """
        Use bredth-first search on relationship network to create a list of relationship chains

        Parameters: 
            - self: the current class instance
            - chain_style: The chain style to use

        Returns:
            - Tuple of relationship chains
        """

        self.chains = ()

        # Iterate network identifier keys
        for network_identifier in self.data:

            # Iterate network node relationship values
            for relationship in self.data[ network_identifier ]:
                relationship_tokens = self.relationships[ relationship ][ "tokens" ]

                # Recursively find relationship chains
                found_chains = self.findSubchains( ( relationship, ), relationship_tokens, chain_style )

                # Save new found chains
                for node_chain in found_chains:
                    if node_chain not in self.chains:
                        self.chains += ( node_chain, )

        # Return created chains
        return self.chains 

    def findSubchains( self, chain: tuple, tail_tokens: tuple, chain_style: str ) -> list:
        """
        Recursive function to generate network sub-chains by adding relationships to the end of a chain

        Parameters: 
            - self: the current class instance
            - chain: The starting chain tuple to create chains from
            - tail_tokens: The token values for the relationship at the tail of the chain
            - chain_style: The chain style to use

        Returns:
            - Tuple of relationship chains
        """

        found_subchains = [ chain ]

        # Create search term to look for in other relationships
        search_term = self.getSearchTerm( tail_tokens, chain_style )

        # Iterate network identifier keys and relationships
        # Search for relationships that start with the search term
        for network_identifier in self.data:
            for relationship in self.data[ network_identifier ]:
                relationship_tokens = self.relationships[ relationship ][ "tokens" ]

                # Ensure relationship is not already in the chain
                # Stops infinite loops
                if relationship not in chain:

                    # Create a test term from the relationship
                    test_term = self.getTestTerm( relationship_tokens, chain_style )

                    # Compare search term and test term
                    # Checks if the chains tail matches the head of the relationship being tested
                    if search_term == test_term:

                        # Add new relationship to the end of the chain
                        new_chain = chain + ( relationship, )

                        # Recursively find and save subchains of the new chain
                        # Save found subchains
                        found_subchains.extend( self.findSubchains( new_chain, relationship_tokens, chain_style ) )

        # Return list of found subchains
        return found_subchains

    def getSearchTerm( self, tokens: tuple, chain_style: str ) -> str:
        """
        Generate a search term based on the system chain style by looking at a relationships last group

        Parameters: 
            - self: the current class instance
            - tokens: The token group to pull the term from
            - chain_style: The chain style to use

        Returns:
            - Search term value
        """

        # Use whole node if chain style is default
        if chain_style == "default":
            return " ".join( tuple( token.lemma_ for token in tokens[ len( tokens ) - 1 ] ) )

        # Use group last word 
        return tokens[ len( tokens ) - 1 ][ len( tokens[ len( tokens ) - 1 ] ) - 1 ].lemma_

    def getTestTerm( self, tokens: tuple, chain_style: str ) -> str:
        """
        Generate a test term based on the system chain style by looking at the relationships first group

        Parameters: 
            - self: the current class instance
            - tokens: The token group to pull the term from
            - chain_style: The chain style to use

        Returns:
            - Test term value
        """

        # Use whole node if chain style is default
        if chain_style == "default":
            return " ".join( tuple( token.lemma_ for token in tokens[ 0 ] ) )

        # Use node last word 
        return tokens[ 0 ][ len( tokens[ 0 ] ) - 1 ].lemma_

    def displayDefaultNetwork( self, starting_node: tuple ) -> None:
        """
        Display a chosen default acceptance network

        Parameters: 
            - self: the current class instance
            - starting_node: The network node to link from

        Returns:
            - None
        """

        # Create network graph
        # Add head node to network
        network = netx.MultiDiGraph()
        self.labels = {}
        head_text = " ".join( starting_node )
        network.add_node( head_text )

        # Iterate node connections
        for relationship in self.data[ starting_node ]:
            link_text = " ".join( relationship[ 1 ] )
            tail_text = " ".join( relationship[ 2 ] )

            # Add tail node to network
            network.add_node( tail_text )
            network.add_edge( head_text, tail_text )

            # Create and store node connections and labels
            label_identifier = ( head_text, tail_text )
            self.labels[ label_identifier ] = self.labels[ label_identifier ] + "\n{}".format( link_text ) if label_identifier in self.labels else link_text

        # Configure and display network graph
        node_pos = netx.spring_layout( network )
        plt.figure( "Default Network: {}".format( head_text ), figsize = ( 16, 8 ) ) 
        plt.subplots_adjust( left = 0, right = 1, top = 1, bottom = 0 )
        netx.draw_networkx( 
            network, pos = node_pos, font_weight = "bold", font_size = 6, 
            node_color = "paleturquoise", node_size = 1800, arrowsize = 20, edge_color = "dodgerblue"
        )
        netx.draw_networkx_edge_labels( network, pos = node_pos, edge_labels = self.labels, font_size = 6 )
        plt.show( block = False )

    def displayLinkedNetwork( self, starting_node: tuple ) -> None:
        """
        Display a chosen linked acceptance network

        Parameters: 
            - self: the current class instance
            - starting_node: The network node to link from

        Returns:
            - None
        """

        # Create network graph
        network = netx.MultiDiGraph()
        self.labels = {}
        self.handled = []
        
        # Recursively add nodes to network from starting node
        self.buildLinkedNetwork( network, starting_node )

        # Configure and display network graph
        node_pos = netx.spring_layout( network )
        plt.figure( "Linked Network: {}".format( " ".join( starting_node ) ), figsize = ( 16, 8 ) ) 
        plt.subplots_adjust( left = 0, right = 1, top = 1, bottom = 0 )
        netx.draw_networkx( 
            network, pos = node_pos, font_weight = "bold", font_size = 6, 
            node_color = "paleturquoise", node_size = 1800, arrowsize = 20, edge_color = "dodgerblue"
        )
        netx.draw_networkx_edge_labels( network, pos = node_pos, edge_labels = self.labels, font_size = 6 )
        plt.show( block = False )

    def buildLinkedNetwork( self, network: MultiDiGraph, starting_node: tuple ) -> None:
        """
        Recursively build a linked acceptance network

        Parameters: 
            - self: the current class instance
            - network: The network to build on
            - starting_node: The network node to link from

        Returns:
            - None
        """

        # Add starting node to network
        head_text = " ".join( starting_node )
        network.add_node( head_text )

        # Validate whether node has connections
        if starting_node in self.data:

            # Check whether node has already been handled
            # If not, mark it as handled and check its connections
            if head_text not in self.handled:
                self.handled.append( head_text )

                # Iterate node connections
                for relationship in self.data[ starting_node ]:
                    tail_node = relationship[ 2 ]
                    tail_text = " ".join( tail_node )

                    # Ensure connecting node has not already been handled
                    if tail_text not in self.handled:
                        network.add_node( tail_text )
                        network.add_edge( head_text, tail_text )
                        link_text = " ".join( relationship[ 1 ] )

                        # Create and store node connections and labels
                        label_identifier = ( head_text, tail_text )
                        self.labels[ label_identifier ] = self.labels[ label_identifier ] + "\n{}".format( link_text ) if label_identifier in self.labels else link_text

                        # Recursively move on to connecting nodes as starting node
                        self.buildLinkedNetwork( network, tail_node )

    def displayCompleteNetwork( self ) -> None:
        """
        Display the complete acceptance network

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        # Create network graph
        network = netx.MultiDiGraph()
        self.labels = {}

        # Iterate root nodes in network
        # Add root node to network
        for starting_node in self.data:
            head_text = " ".join( starting_node )
            network.add_node( head_text )

            # Iterate node connections
            for relationship in self.data[ starting_node ]:
                link_text = " ".join( relationship[ 1 ] )
                tail_text = " ".join( relationship[ 2 ] )

                # Add tail node to network
                network.add_node( tail_text )
                network.add_edge( head_text, tail_text )

                # Create and store node connections and labels
                label_identifier = ( head_text, tail_text )
                self.labels[ label_identifier ] = self.labels[ label_identifier ] + "\n{}".format( link_text ) if label_identifier in self.labels else link_text

        # Configure and display network graph
        node_pos = netx.spring_layout( network )
        plt.figure( "Complete Network", figsize = ( 16, 8 ) ) 
        plt.subplots_adjust( left = 0, right = 1, top = 1, bottom = 0 )
        netx.draw_networkx( 
            network, pos = node_pos, font_weight = "bold", font_size = 6, 
            node_color = "paleturquoise", node_size = 1800, arrowsize = 20, edge_color = "dodgerblue"
        )
        netx.draw_networkx_edge_labels( network, pos = node_pos, edge_labels = self.labels, font_size = 6 )
        plt.show( block = False )
