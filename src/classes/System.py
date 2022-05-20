#!/usr/bin/env python
# ----------------------------------------------------------------------------------------------------
# Implements an System Handler class for the Acceptance Test Generator
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

import re
import spacy
import time
from spacy import displacy
from classes.Interface import Interface
from classes.Requirement import Requirement
from classes.Network import Network
from classes.Settings import Settings
from classes.Output import Output

class System:
    """
    System Handler Class
    """

    def __init__( self ) -> None:
        """
        Initialise a System class

        Parameters: 
            - self: the current class instance

        Returns:
            - A System instance
        """

        self.interface = Interface()
        self.requirements = {}
        self.relationships = {}
        self.network = Network( self.relationships )
        self.chains = ()
        self.feedback = ""
        self.main_menu_input = ""
        self.nlp = None
        self.tic = None
        self.toc = None

        # Load system settings
        self.settings = Settings( self.interface )
        self.settings.readSettingFile()

    def mainMenu( self ) -> None:
        """
        Start the system main menu

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        self.main_menu_input = ""

        # Load NLP pipeline
        if not self.loadPipeline():
            return

        # Iterate until user input exit code
        while self.main_menu_input != "0":
            self.interface.clear()

            # Display main menu
            self.main_menu_input = self.interface.displayMainMenu( self.requirements, self.relationships, self.network, self.chains, self.feedback )

            # Execute system functionality
            getattr( self, {
                "0": "goodbye",
                "1": "quickRun",
                "2": "settingMenu",
                "3": "createAcceptanceNetworks",
                "4": "viewRequirements",
                "5": "viewAcceptanceNetworks",
                "6": "viewAcceptanceTests",
                "7": "exportAcceptanceTests"
            }.get( self.main_menu_input, "invalidInput" ), self.invalidInput )()
    
    def settingMenu( self ) -> None:
        """
        Update system setting values

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        input_value = ""
        self.reset()

        # Iterate until user input exit code
        while input_value != "0":
            self.interface.clear()

            # Display main menu
            # Execute system functionality
            input_value = self.interface.displaySettingMenu( self.settings.values, self.feedback )
            getattr( self, {
                "0": "back",
                "1": "defineInputFile",
                "2": "defineOutputFile",
                "3": "definePipeline",
                "4": "definePatternStyle",
                "5": "defineChainStyle",
                "6": "defineGraphStyle",
                "7": "defineLemmaChaining"
            }.get( input_value, "invalidInput" ), self.invalidInput )()

    def goodbye( self ) -> None:
        """
        Print a goodbye message

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        self.interface.clear()
        print( "Goodbye!" )

    def reset( self ) -> None:
        """
        Reset the system

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        self.requirements = {}
        self.relationships = {}
        self.network = Network( self.relationships )
        self.chains = ()

    def back( self ) -> None:
        """
        Return to the main menu

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        self.feedback = "Returned to main menu"

    def invalidInput( self ) -> None:
        """
        Set feedback message on invalid input by user

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        self.feedback = "ERROR: Please enter a valid number!"

    def defineInputFile( self ) -> None:
        """
        Get the user to define the name of the input file 

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        self.interface.clear()
        self.settings.updateInputFile( self )
        self.settings.saveSettings()
        self.feedback = "Defined input file: {}".format( self.settings.values[ "input_file" ] )

    def defineOutputFile( self ) -> None:
        """
        Get the user to define the name of the output file 

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        self.interface.clear()
        self.settings.updateOutputFile()
        self.settings.saveSettings()
        self.feedback = "Defined output file: {}".format( self.settings.values[ "output_file" ] )

    def definePipeline( self ) -> None:
        """
        Get the user to select a nlp pipeline 

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        self.interface.clear()
        self.settings.updatePipeline()
        self.settings.saveSettings()
        self.loadPipeline()

    def definePatternStyle( self ) -> None:
        """
        Get the user to select a pattern style 

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        self.interface.clear()
        self.settings.updatePatternStyle()
        self.settings.saveSettings()
        self.feedback = "Defined pattern style: {}".format( self.settings.values[ "pattern_style" ] )

    def defineChainStyle( self ) -> None:
        """
        Get the user to select a chain style 

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        self.interface.clear()
        self.settings.updateChainStyle()
        self.settings.saveSettings()
        self.feedback = "Defined chain style: {}".format( self.settings.values[ "chain_style" ] )

    def defineGraphStyle( self ) -> None:
        """
        Get the user to select a graph style  

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        self.interface.clear()
        self.settings.updateGraphStyle()
        self.settings.saveSettings()
        self.feedback = "Defined graph style: {}".format( self.settings.values[ "graph_style" ] )

    def loadPipeline( self ) -> bool:
        """
        Load the NLP pipeline  

        Parameters: 
            - self: the current class instance

        Returns:
            - Success boolean
        """

        # Clear current pipeline
        self.tic = time.perf_counter()
        self.nlp = None 
        self.interface.clear()

        # Load new pipeline
        print( "Loading NLP Pipeline..." )
        try:
            self.nlp = spacy.load( self.settings.values[ "pipeline" ] )
            self.toc = time.perf_counter() 
            self.feedback = "Loaded {} pipeline in: {:.2f}ms".format( self.settings.values[ "pipeline" ], ( self.toc - self.tic ) * 1000 )
            return True

        # Failed to load pipeline
        except Exception:
            self.feedback = "ERROR: Failed to load NLP pipeline. Please run `python -m spacy download {}`".format( self.settings.values[ "pipeline" ] )
            return False

    def quickRun( self ) -> None:
        """
        Run the system from start to finish and exit 

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        # Create relationship network
        if not self.createAcceptanceNetworks():
            return

        # Export acceptance tests
        self.exportAcceptanceTests()

        # Allow main menu to exit
        self.main_menu_input = "0"
        self.interface.clear()
        print( self.feedback )

    def readInputFile( self ) -> bool:
        """
        Read the defined input file content 

        Parameters: 
            - self: the current class instance

        Returns:
            - Success boolean
        """

        self.reset()
        try:

            # Open and iterate input file
            with open( self.settings.values[ "input_file" ], "r" ) as input_file:
                for line_content in input_file: 
                    self.tic = time.perf_counter()

                    # Sanitise line
                    line_content = re.sub( r"\s*\r?\n|\s*\r", "", line_content )
                    line_content = re.sub( r"\s{2,}", " ", line_content )
                    line_content = line_content.strip()

                    # Verify line format and content
                    if line_content.startswith( "#" ) or len( line_content ) == 0:
                        continue
                    if not line_content.endswith( "." ):
                        self.reset()
                        self.feedback = "ERROR: Requirement {} does not end with a fullstop: {}".format( len( self.requirements ) + 1, line_content )
                        return False
                    if match := re.search( r".* (\w+n't).*", line_content, re.IGNORECASE ):
                        self.reset()
                        self.feedback = "ERROR: Requirement {} contains the contraction: {}".format( len( self.requirements ) + 1, match.group( 1 ) )
                        return False
                    if line_content in self.requirements:
                        self.reset()
                        self.feedback = "ERROR: Duplicate requirement found: {}".format( line_content )
                        return False
                        
                    # Add requirement line to requirement list
                    self.requirements[ line_content ] = None
                    self.toc = time.perf_counter() 
                    print( "Loaded requirement {} in: {:.2f}ms".format( len( self.requirements ), ( self.toc - self.tic ) * 1000 ) )

        # Catch errors
        except FileNotFoundError:
            self.reset()
            self.feedback = "ERROR: Input file could not be found: {}".format( self.settings.values[ "input_file" ] )
            return False
        
        # File read success
        # Update feedback message
        self.interface.clear()
        self.feedback = "Read {} requirements from input file: {}".format( len( self.requirements ), self.settings.values[ "input_file" ] )
        return True

    def createAcceptanceNetworks( self ) -> bool:
        """
        Create a relationship network and retrieve its chains 

        Parameters: 
            - self: the current class instance

        Returns:
            - Success boolean
        """

        self.reset()

        # Ensure NLP pipeline is loaded
        if self.nlp == None:
            if not self.loadPipeline():
                return False

        # Read requirements file
        if not self.readInputFile():
            return False

        # Check if requirements exist
        if len( self.requirements ) == 0:
            self.feedback = "ERROR: No requirements in input file"
            return False

        # Create and save requirement relationships
        self.interface.clear()
        if self.createRelationships():

            # Create semantic network and link chains
            # Update feedback message
            self.tic = time.perf_counter()
            self.network = Network( self.relationships )
            self.chains = self.network.getChains( self.settings.values[ "chain_style" ] )
            self.toc = time.perf_counter()
            self.feedback = "Created semantic network with {} chains from {} requirements in: {:.2f}ms".format( len( self.chains ), len( self.requirements ), ( self.toc - self.tic ) * 1000 )
            return True

        # Clear system on fail
        else:
            self.reset()
            return False

    def createRelationships( self ) -> bool:
        """
        Create requirement classes and their relationships 

        Parameters: 
            - self: the current class instance

        Returns:
            - Success boolean
        """

        # Iterate requirements list
        for requirement_index, requirement_string in enumerate( self.requirements ):
            self.tic = time.perf_counter()

            # Ensure requirement follows MoSCoW format
            if match := re.search( r"^[\w\d\s]+ (must|should|could|will not) .*\.", requirement_string, re.IGNORECASE ):
                requirement_priority = match.group( 1 )
                requirement_number = requirement_index + 1
                
                # Exempt "will not" requirements as they are technically for a future iteration
                if requirement_priority != "will not":
                
                    # Create requirement handler
                    requirement_handler = Requirement( requirement_number, requirement_priority, requirement_string, self.nlp )
                    print( "\nAssessing requirement {}: {}".format( requirement_number, requirement_string ) )

                    # Find relationships in requirement
                    requirement_relationships = requirement_handler.getRelationships( self.settings.values[ "pattern_style" ] )
                    print( "Found {} relationships in requirement {}".format( len( requirement_relationships ), requirement_number ) )

                    # Iterate requirement relationships
                    for relationship_identifier in requirement_relationships:
                        print( "> {}: {}".format( relationship_identifier, requirement_relationships[ relationship_identifier ][ "pattern" ] ) )

                        # Create relationship structure if it does not exist
                        if relationship_identifier not in self.relationships:
                            self.relationships[ relationship_identifier ] = { 
                                "tokens": requirement_relationships[ relationship_identifier ][ "tokens" ], 
                                "requirements": [], 
                                "priorities": [],
                                "patterns": [] 
                            }

                        # Update relationship structure with info from requirement and relationship
                        self.relationships[ relationship_identifier ][ "requirements" ].append( requirement_number )
                        self.relationships[ relationship_identifier ][ "priorities" ].append( requirement_priority )
                        self.relationships[ relationship_identifier ][ "patterns" ].append( requirement_relationships[ relationship_identifier ][ "pattern" ] )

                    # Add requirement handler to list of requirements
                    self.requirements[ requirement_string ] = requirement_handler

                    # Finished this requirement
                    # Move onto the next
                    self.toc = time.perf_counter() 
                    print( "Parsed requirement {} in: {:.2f}ms".format( requirement_number, ( self.toc - self.tic ) * 1000 ) )

                # Skip "will not" requirements
                else:
                    print( print( "\nSkipping requirement {}: {}".format( requirement_number, requirement_string ) ) )

            # Line does not follow MoSCoW formatting
            else:
                self.reset()
                self.feedback = "ERROR: Requirement {} does not follow 'MoSCoW' formatting: {}".format( requirement_index + 1, requirement_string )
                return False 

        # Return success
        return True 

    def viewRequirements( self ) -> None:
        """
        Get the user to select a requirement graph to display 

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        input_value = ""
        self.feedback = ""

        # Check if chains exist
        if len( self.requirements ) == 0:
            self.feedback = "ERROR: Please execute: Create Acceptance Network"
            return 

        # Create list of requirements for indexing
        requirements_list = [ requirement for requirement in self.requirements ]

        # Iterate until user input exit code
        while input_value != "0":
            self.interface.clear()

            # Display main menu
            input_value = self.interface.displayRequirementsMenu( self.requirements, self.feedback )

            # Validate selected index
            if input_value == "0":
                self.feedback = "Returned to main menu"
                return
            elif not input_value.isdigit() or int( input_value ) > len( self.requirements ):
                self.invalidInput()
                continue

            # Handle user input
            requirement_index = int( input_value ) - 1
            selected_requirement = self.requirements[ requirements_list[ requirement_index ] ]

            # Display chosen requirement
            displacy.serve( selected_requirement.doc, style = "dep" )

    def viewAcceptanceNetworks( self ) -> None:
        """
        Get the user to select an acceptance network to display 

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        input_value = ""
        self.feedback = ""

        # Check if requirements exist
        if len( self.network.data ) == 0:
            self.feedback = "ERROR: Please execute: Create Acceptance Network"
            return 

        # Display complete graph
        if self.settings.values[ "graph_style" ] == "complete":
            self.network.displayCompleteNetwork()
            self.feedback = "Displayed complete network"

        # Display default or linked graph
        else: 

            # Iterate until user input exit code
            while input_value != "0":
                self.interface.clear()

                # Display network menu
                input_value = self.interface.displayNetworkMenu( self.network, self.feedback )

                # Validate selected index
                if input_value == "0":
                    self.feedback = "Returned to main menu"
                    return
                elif not input_value.isdigit() or int( input_value ) > len( self.network.data ):
                    self.invalidInput()
                    continue

                # Handle user input
                network_index = int( input_value ) - 1
                selected_network_key = [ head_node for head_node in self.network.data ][ network_index ]

                # Display selected default network
                if self.settings.values[ "graph_style" ] == "default":
                    self.network.displayDefaultNetwork( selected_network_key )
                    self.feedback = "Displayed default network: {}".format( " ".join( selected_network_key ) )

                # Display selected linked network
                elif self.settings.values[ "graph_style" ] == "linked":
                    self.network.displayLinkedNetwork( selected_network_key )
                    self.feedback = "Displayed linked network: {}".format( " ".join( selected_network_key ) )

    def viewAcceptanceTests( self ) -> None:
        """
        Get the user to select an acceptance test to display 

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        input_value = ""
        self.feedback = ""

        # Check if chains exist
        if len( self.chains ) == 0:
            self.feedback = "ERROR: Please execute: Create Acceptance Network"
            return 

        # Iterate until user input exit code
        while input_value != "0":
            self.interface.clear()

            # Display main menu
            input_value = self.interface.displayTestMenu( self.chains, self.feedback )

            # Validate selected index
            if input_value == "0":
                self.feedback = "Returned to main menu"
                return
            elif not input_value.isdigit() or int( input_value ) > len( self.chains ):
                self.invalidInput()
                continue

            # Handle user input
            test_number = int( input_value )
            selected_test = self.chains[ test_number - 1 ]

            # Display chosen network
            self.interface.clear()
            output_handler = Output( self.nlp, self.requirements, self.relationships )
            output_handler.displayTest( test_number, selected_test )
            self.feedback = "Displayed acceptance test: {}".format( test_number )
            input( "\nENTER TO CONTINUE " )

    def exportAcceptanceTests( self ) -> None:
        """
        Get the user to select an output file and export the tests 

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        self.interface.clear()

        # Create output handler
        self.tic = time.perf_counter()
        output_handler = Output( self.nlp, self.requirements, self.relationships )
        output_handler.createWriter( self.settings.values[ "output_file" ] )

        # Add chains to file as sheets
        for chain_index, chain in enumerate( self.chains ):
            output_handler.addTest( chain_index + 1, chain )

        # Save output file
        output_handler.saveWriter()
        self.toc = time.perf_counter()
        self.feedback = "Exported {} acceptance tests to file '{}' in: {:.2f}ms".format( len( self.chains ), self.settings.values[ "output_file" ], ( self.toc - self.tic ) * 1000 )
