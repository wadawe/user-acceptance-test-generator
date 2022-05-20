#!/usr/bin/env python
# ----------------------------------------------------------------------------------------------------
# Implements an Interface Handler class for the Acceptance Test Generator
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

from classes.Network import Network

class Interface:
    """
    Interface Handler Class
    """

    def clear( self ):
        """
        Clear the console output

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """
        
        print( "\n" * 50 )

    def getInput( self, prompt: str ) -> str:
        """
        Get an input value from the user 

        Parameters: 
            - self: the current class instance
            - prompt: The prompt to display to the user

        Returns:
            - The user input string value
        """

        # Retrieve input from user
        print( prompt )
        return str( input( " > " ) )

    def displayMainMenu( self, requirements: dict, relationships: dict, network: Network, chains: tuple, feedback: str ) -> str:
        """
        Display the system main menu 

        Parameters: 
            - self: the current class instance
            - requirements: The system requirements structure
            - relationships: The system relationships structure
            - network: The system network handler
            - chains: The system chains structure
            - feedback: The menu feedback string

        Returns:
            - A user input string value
        """

        print( "=" * 150 )
        print( "MAIN MENU" )
        print( "=" * 150 )
        print( "" )
        print( "{:>6}: {:<90}".format( 1, "Quick Run" ) )
        print( "{:>6}: {:<90}".format( 2, "Edit System Settings" ) )
        print( "" )
        print( "{:>6}: {:<90} {:>50}".format( 3, "Create Acceptance Network", str( len( relationships ) ) + " Semantic Links" ) )
        print( "{:>6}: {:<90} {:>50}".format( 4, "View Requirement(s)", str( len( requirements ) ) + " Requirements" ) )
        print( "{:>6}: {:<90} {:>50}".format( 5, "View Acceptance Network(s)", str( len( network.data ) ) + " Starting Nodes" ) )
        print( "{:>6}: {:<90} {:>50}".format( 6, "View Acceptance Test(s)", str( len( chains ) ) + " Acceptance Chains" ) )
        print( "" )
        print( "{:>6}: {:<90}".format( 7, "Export Acceptance Tests" ) )
        print( "" )
        print( "{:>6}: {:<90}".format( 0, "Exit" ) )
        print( "" )
        if len( feedback ) > 0:
            print( "=" * 150 )
            print( feedback )
        print( "=" * 150 )
        return self.getInput( "Enter selection:" )

    def displaySettingMenu( self, settings: dict, feedback: str ) -> str:
        """
        Display the system setting menu 

        Parameters: 
            - self: the current class instance
            - settings: The global setting values
            - feedback: The menu feedback string

        Returns:
            - A user input string value
        """

        print( "=" * 150 )
        print( "SETTING MENU" )
        print( "=" * 150 )
        print( "" )
        print( "{:>6}: {:<90} {:>50}".format( 1, "Define Input File", settings[ "input_file" ] ) )
        print( "{:>6}: {:<90} {:>50}".format( 2, "Define Output File", settings[ "output_file" ] ) )
        print( "{:>6}: {:<90} {:>50}".format( 3, "Define NLP Pipeline", settings[ "pipeline" ] ) )
        print( "{:>6}: {:<90} {:>50}".format( 4, "Define Pattern Style", settings[ "pattern_style" ] ) )
        print( "{:>6}: {:<90} {:>50}".format( 5, "Define Chain Style", settings[ "chain_style" ] ) )
        print( "{:>6}: {:<90} {:>50}".format( 6, "Define Graph Style", settings[ "graph_style" ] ) )
        print( "" )
        print( "{:>6}: {:<90}".format( 0, "Back" ) )
        print( "" )
        if len( feedback ) > 0:
            print( "=" * 150 )
            print( feedback )
        print( "=" * 150 )
        return self.getInput( "Enter selection:" )

    def displayUpdateMenu( self, setting_name: str, setting_value: str ) -> str:
        """
        Display the setting update menu 

        Parameters: 
            - self: the current class instance
            - setting_name: The setting name to update
            - setting_value: The current setting value

        Returns:
            - A user input string value
        """

        print( "=" * 150 )
        print( "SETTING MENU" )
        print( "=" * 150 )
        print( "" )
        print( "{:>20}: {}".format( "Setting Name", setting_name ) )
        print( "{:>20}: {}".format( "Current Value", setting_value ) )
        print( "" )
        print( "=" * 150 )
        return self.getInput( "Enter new value:" )

    def displayPipelineMenu( self ) -> str:
        """
        Display the pipeline selection menu 

        Parameters: 
            - self: the current class instance

        Returns:
            - A user input string value
        """

        print( "=" * 150 )
        print( "PIPELINE SELECTION" )
        print( "=" * 150 )
        print( "" )
        print( "{:>6}: {:<90} {:>50}".format( 1, "en_core_web_sm", "~89.9% Accuracy | FASTEST" ) )
        print( "{:>6}: {:<90} {:>50}".format( 2, "en_core_web_md", "~90.2% Accuracy | FAST   " ) )
        print( "{:>6}: {:<90} {:>50}".format( 3, "en_core_web_lg", "~90.3% Accuracy | SLOW   " ) )
        print( "{:>6}: {:<90} {:>50}".format( 4, "en_core_web_trf", "~92.5% Accuracy | SLOWEST" ) )
        print( "" )
        print( "=" * 150 )
        return self.getInput( "Enter selection:" )

    def displayPatternMenu( self ) -> str:
        """
        Display the pattern selection menu 

        Parameters: 
            - self: the current class instance

        Returns:
            - A user input string value
        """

        print( "=" * 150 )
        print( "PATTERN SELECTION" )
        print( "=" * 150 )
        print( "" )
        print( "{:>6}: {:<90} {:>50}".format( 1, "default", "Immediate Dependency Matching" ) )
        print( "{:>6}: {:<90} {:>50}".format( 2, "gibberish", "Nested Chain Matching" ) )
        print( "" )
        print( "=" * 150 )
        return self.getInput( "Enter selection:" )

    def displayChainMenu( self ) -> str:
        """
        Display the chain selection menu 

        Parameters: 
            - self: the current class instance

        Returns:
            - A user input string value
        """

        print( "=" * 150 )
        print( "CHAIN SELECTION" )
        print( "=" * 150 )
        print( "" )
        print( "{:>6}: {:<90} {:>50}".format( 1, "default", "Group-based Chaining" ) )
        print( "{:>6}: {:<90} {:>50}".format( 2, "advanced", "Last-word-based Chaining" ) )
        print( "" )
        print( "=" * 150 )
        return self.getInput( "Enter selection:" )

    def displayGraphMenu( self ) -> str:
        """
        Display the graph selection menu 

        Parameters: 
            - self: the current class instance

        Returns:
            - A user input string value
        """

        print( "=" * 150 )
        print( "GRAPH SELECTION" )
        print( "=" * 150 )
        print( "" )
        print( "{:>6}: {:<90} {:>50}".format( 1, "default", "Display Direct Connections" ) )
        print( "{:>6}: {:<90} {:>50}".format( 2, "linked", "Display Linked Connections" ) )
        print( "{:>6}: {:<90} {:>50}".format( 3, "complete", "Display All Connections" ) )
        print( "" )
        print( "=" * 150 )
        return self.getInput( "Enter selection:" )

    def displayRequirementsMenu( self, requirements: dict, feedback: str ) -> str:
        """
        Display the requirements selection menu 

        Parameters: 
            - self: the current class instance
            - requirements: The system requirements structure
            - feedback: The menu feedback string

        Returns:
            - A user input string value
        """

        print( "=" * 150 )
        print( "REQUIREMENTS MENU" )
        print( "=" * 150 )
        print( "" )
        for requirement_index, requirement in enumerate( requirements ): 
            relationships_text = "n/a"
            if requirements[ requirement ] != None:
                relationships_text = str( len( requirements[ requirement ].relationships ) ) + " Relationship(s)"
            print( "{:>6}: {:<90} {:>50}".format( requirement_index + 1, requirement, relationships_text ) )
        print( "" )
        print( "{:>6}: {:<90}".format( 0, "Back" ) )
        print( "" )
        if len( feedback ) > 0:
            print( "=" * 150 )
            print( feedback )
        print( "=" * 150 )
        return self.getInput( "Enter selection:" )

    def displayNetworkMenu( self, network: Network, feedback: str ) -> str:
        """
        Display the network selection menu 

        Parameters: 
            - self: the current class instance
            - network: The system network handler
            - feedback: The menu feedback string

        Returns:
            - A user input string value
        """

        print( "=" * 150 )
        print( "NETWORK MENU" )
        print( "=" * 150 )
        print( "" )
        for node_index, head_node in enumerate( network.data ): 
            node_connections = str( len( network.data[ head_node ] ) ) + " Node Connection(s)"
            print( "{:>6}: {:<90} {:>50}".format( node_index + 1, " ".join( head_node ), node_connections ) )
        print( "" )
        print( "{:>6}: {:<90}".format( 0, "Back" ) )
        print( "" )
        if len( feedback ) > 0:
            print( "=" * 150 )
            print( feedback )
        print( "=" * 150 )
        return self.getInput( "Enter selection:" )

    def displayTestMenu( self, chains: tuple, feedback: str ) -> str:
        """
        Display the acceptance test selection menu 

        Parameters: 
            - self: the current class instance
            - chains: The system chains structure
            - feedback: The menu feedback string

        Returns:
            - A user input string value
        """

        print( "=" * 150 )
        print( "ACCEPTANCE TEST MENU" )
        print( "=" * 150 )
        print( "" )
        for chain_index in range( 0, len( chains ) ):
            print( "{:>6}: {:<90}".format( chain_index + 1, "Display Acceptance Test #{}".format( chain_index + 1 ) ) )
        print( "" )
        print( "{:>6}: {:<90}".format( 0, "Back" ) )
        print( "" )
        if len( feedback ) > 0:
            print( "=" * 150 )
            print( feedback )
        print( "=" * 150 )
        return self.getInput( "Enter selection:" )
