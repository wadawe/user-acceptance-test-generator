#!/usr/bin/env python
# ----------------------------------------------------------------------------------------------------
# Implements an Settings Handler class for the Acceptance Test Generator
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

from classes.Interface import Interface

class Settings:
    """
    Setting Handler Class
    """

    def __init__( self, interface: Interface ):
        """
        Initialise a Settings class

        Parameters: 
            - self: the current class instance

        Returns:
            - A Settings instance
        """

        self.interface = interface

        # Define setting default values
        self.values = {
            "input_file": "input.txt",
            "output_file": "Output.xlsx",
            "pipeline": "en_core_web_md",
            "pattern_style": "default",
            "chain_style": "default",
            "graph_style": "default"
        }

        # Define setting restrictions
        self.restrictions = {
            "pipeline": [ "en_core_web_sm", "en_core_web_md", "en_core_web_lg", "en_core_web_trf" ],
            "pattern_style": [ "default", "gibberish" ],
            "chain_style": [ "default", "advanced" ],
            "graph_style": [ "default", "linked", "complete" ]
        }

    def readSettingFile( self ) -> None:
        """
        Read the setting file and load its values

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """
        
        try:

            # Open and iterate setting file
            with open( ".settings", "r+" ) as setting_file:
                for line_content in setting_file:

                    # Sanitise and split line into key-value pair
                    line_content = re.sub( r"\s+|\s*\r?\n|\s*\r", "", line_content )
                    line_setting = line_content.split( "=" )

                    # Validate line is key-value pair
                    if len( line_setting ) == 2:
                        setting_key, setting_value = line_setting

                        # Validate setting key and value
                        if self.validateSetting( setting_key, setting_value ):
                            self.values[ setting_key ] = setting_value
        
        # Catch error when file does not exist
        except IOError:
            print( "Setting file does not exist; creating it!" )

        # Save loaded settings
        self.saveSettings()
          
    def validateSetting( self, setting_key: str, setting_value: str ) -> bool:
        """
        Validate a given setting key and value

        Parameters: 
            - self: the current class instance
            - setting_key: The setting key to validate
            - setting_value: The setting value to validate

        Returns:
            - State boolean
        """
        
        # Ensure setting key is valid
        if setting_key in self.values:

            # Check if setting has restrictions
            if setting_key in self.restrictions:

                # Validate setting value
                if setting_value in self.restrictions[ setting_key ]:
                    return True

                # Setting value is not valid
                else:
                    return False

            # Setting does not have restrictions
            else:
                return True

        # Setting key is not valid
        else:
            return False

    def saveSettings( self ) -> None:
        """
        Save the current settings into the setting file

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        # Create contents to write to the setting file
        file_content = ""
        for setting_key in self.values:
            setting_value = self.values[ setting_key ]
            file_content += "{}={}\n".format( setting_key, setting_value )

        # Write the file content
        with open( ".settings", "w+" ) as setting_file:
            setting_file.write( file_content )

    def updateValue( self, setting_key: str ) -> None:
        """
        Update a global setting value

        Parameters: 
            - self: the current class instance
            - setting_key: The setting key to update

        Returns:
            - None
        """

        # Display setting menu
        input_value = self.interface.displayUpdateMenu( setting_key, self.values[ setting_key ] )

        # Retrieve and update user defined setting value
        if self.validateSetting( setting_key, input_value ):
            self.values[ setting_key ] = input_value or self.values[ setting_key ]

    def updateInputFile( self ) -> None:
        """
        Update the input file setting value

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        self.updateValue( "input_file" )
        if not self.values[ "input_file" ].endswith( ".txt" ):
            self.values[ "input_file" ] += ".txt"

    def updateOutputFile( self ) -> None:
        """
        Update the output file setting value

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        self.updateValue( "output_file" )
        if not self.values[ "output_file" ].endswith( ".xlsx" ):
            self.values[ "output_file" ] += ".xlsx"

    def updatePipeline( self ) -> None:
        """
        Update the pipeline setting value

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        input_value = self.interface.displayPipelineMenu()

        # Retrieve and update user defined pipeline value
        if input_value == "1":
            self.values[ "pipeline" ] = "en_core_web_sm"
        elif input_value == "2":
            self.values[ "pipeline" ] = "en_core_web_md"
        elif input_value == "3":
            self.values[ "pipeline" ] = "en_core_web_lg"
        elif input_value == "4":
            self.values[ "pipeline" ] = "en_core_web_trf"

    def updatePatternStyle( self ) -> None:
        """
        Update the pattern style setting value

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        input_value = self.interface.displayPatternMenu()

        # Retrieve and update user defined pattern value
        if input_value == "1":
            self.values[ "pattern_style" ] = "default"
        elif input_value == "2":
            self.values[ "pattern_style" ] = "gibberish"

    def updateChainStyle( self ) -> None:
        """
        Update the chain style setting value

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        input_value = self.interface.displayChainMenu()

        # Retrieve and update user defined chain value
        if input_value == "1":
            self.values[ "chain_style" ] = "default"
        elif input_value == "2":
            self.values[ "chain_style" ] = "advanced"

    def updateGraphStyle( self ) -> None:
        """
        Update the graph style setting value

        Parameters: 
            - self: the current class instance

        Returns:
            - None
        """

        input_value = self.interface.displayGraphMenu()

        # Retrieve and update user defined graph value
        if input_value == "1":
            self.values[ "graph_style" ] = "default"
        elif input_value == "2":
            self.values[ "graph_style" ] = "linked"
        elif input_value == "3":
            self.values[ "graph_style" ] = "complete"
