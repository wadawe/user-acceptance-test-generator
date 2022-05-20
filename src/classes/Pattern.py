#!/usr/bin/env python
# ----------------------------------------------------------------------------------------------------
# Implements an Pattern Handler class for the Acceptance Test Generator
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

class Pattern:
    """
    Pattern Handler Class
    """

    def __init__( self, operator: str ) -> None:
        """
        Initialise a Pattern class

        Parameters: 
            - self: the current class instance
            - operator: The relational operator to use

        Returns:
            - A Pattern instance
        """

        # Create patterns dictionary
        self.patterns = {}

        # --------------------------------------------------------------------------------------------

        self.patterns[ "NOUN-ADJ" ] = ( [ 
            { "RIGHT_ID": "dep1", "RIGHT_ATTRS": { 
                "POS": { "IN": [ "NOUN", "PROPN" ] }
            } },
            { "RIGHT_ID": "dep2", "LEFT_ID": "dep1", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": "ADJ", 
                "DEP": "amod"
            } },
        ], [ [ 0 ], [ "is" ], [ 1 ] ] )

        # --------------------------------------------------------------------------------------------

        self.patterns[ "NOUN-NOUN" ] = ( [ 
            { "RIGHT_ID": "dep1", "RIGHT_ATTRS": { 
                "POS": { "IN": [ "NOUN", "PROPN" ] }
            } },
            { "RIGHT_ID": "dep2", "LEFT_ID": "dep1", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": { "IN": [ "NOUN", "PROPN" ] },
                "DEP": "compound"
            } },
        ], [ [ 1 ], [ "has" ], [ 0 ] ] )

        # --------------------------------------------------------------------------------------------

        self.patterns[ "VERB-NOUN-ADJ" ] = ( [ 
            { "RIGHT_ID": "dep1", "RIGHT_ATTRS": { 
                "POS": "VERB"
            } },
            { "RIGHT_ID": "dep2", "LEFT_ID": "dep1", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": { "IN": [ "NOUN", "PROPN" ] }, 
                "DEP": { "IN": [ "nsubj", "nsubjpass" ] }
            } },
            { "RIGHT_ID": "dep3", "LEFT_ID": "dep1", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": "ADJ", 
                "DEP": "acomp",
                "LEMMA": { "NOT_IN": [ "able" ] } 
            } },
        ], [ [ 1 ], [ "is" ], [ 2 ] ] )

        # --------------------------------------------------------------------------------------------

        self.patterns[ "VERB-NOUN-VERB" ] = ( [ 
            { "RIGHT_ID": "dep1", "RIGHT_ATTRS": { 
                "POS": "VERB"
            } },
            { "RIGHT_ID": "dep2", "LEFT_ID": "dep1", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": { "IN": [ "NOUN", "PROPN" ] }, 
                "DEP": { "IN": [ "nsubj", "nsubjpass" ] }
            } },
            { "RIGHT_ID": "dep3", "LEFT_ID": "dep1", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": "VERB", 
                "DEP": "acomp",
                "LEMMA": { "NOT_IN": [ "able" ] } 
            } },
        ], [ [ 1 ], [ "is" ], [ 2 ] ] )

        # --------------------------------------------------------------------------------------------

        self.patterns[ "have-NOUN-NOUN" ] = ( [ 
            { "RIGHT_ID": "dep1", "RIGHT_ATTRS": { 
                "LEMMA": { "IN": [ "have" ] } 
            } },
            { "RIGHT_ID": "dep2", "LEFT_ID": "dep1", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": { "IN": [ "NOUN", "PROPN" ] }, 
                "DEP": { "IN": [ "nsubj", "nsubjpass" ] }
            } },
            { "RIGHT_ID": "dep3", "LEFT_ID": "dep1", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": { "IN": [ "NOUN", "PROPN" ] }, 
                "DEP": { "IN": [ "dobj", "pobj" ] }
            } },
        ], [ [ 1 ], [ "has" ], [ 2 ] ] )

        # --------------------------------------------------------------------------------------------

        self.patterns[ "VERB-NOUN-NOUN" ] = ( [ 
            { "RIGHT_ID": "dep1", "RIGHT_ATTRS": { 
                "POS": "VERB",
                "LEMMA": { "NOT_IN": [ "have" ] }
            } },
            { "RIGHT_ID": "dep2", "LEFT_ID": "dep1", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": { "IN": [ "NOUN", "PROPN" ] }, 
                "DEP": { "IN": [ "nsubj", "nsubjpass" ] }
            } },
            { "RIGHT_ID": "dep3", "LEFT_ID": "dep1", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": { "IN": [ "NOUN", "PROPN" ] }, 
                "DEP": { "IN": [ "dobj", "pobj" ] }
            } },
        ], [ [ 1 ], [ 0 ], [ 2 ] ] )

        # --------------------------------------------------------------------------------------------

        self.patterns[ "VERB-NOUN-ADP-NOUN" ] = ( [ 
            { "RIGHT_ID": "dep1", "RIGHT_ATTRS": { 
                "POS": "VERB"
            } }, 
            { "RIGHT_ID": "dep2", "LEFT_ID": "dep1", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": { "IN": [ "NOUN", "PROPN" ] }, 
                "DEP": { "IN": [ "nsubj", "nsubjpass" ] }
            } }, 
            { "RIGHT_ID": "dep3", "LEFT_ID": "dep1", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": "ADP", 
                "DEP": "prep"
            } }, 
            { "RIGHT_ID": "dep4", "LEFT_ID": "dep3", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": { "IN": [ "NOUN", "PROPN" ] }, 
                "DEP": { "IN": [ "dobj", "pobj" ] }
            } }, 
        ], [ [ 1 ], [ 0, 2 ], [ 3 ] ] )

        # --------------------------------------------------------------------------------------------

        self.patterns[ "NOUN-VERB-ADP-NOUN" ] = ( [ 
            { "RIGHT_ID": "dep1", "RIGHT_ATTRS": { 
                "POS": { "IN": [ "NOUN", "PROPN" ] }
            } },
            { "RIGHT_ID": "dep2", "LEFT_ID": "dep1", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": "VERB", 
                "DEP": "acl"
            } },
            { "RIGHT_ID": "dep3", "LEFT_ID": "dep2", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": "ADP", 
                "DEP": "prep"
            } }, 
            { "RIGHT_ID": "dep4", "LEFT_ID": "dep3", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": { "IN": [ "NOUN", "PROPN" ] },
                "DEP": { "IN": [ "dobj", "pobj" ] }
            } }, 
        ], [ [ 0 ], [ 1, 2 ], [ 3 ] ] )

        # --------------------------------------------------------------------------------------------

        self.patterns[ "VERB-NOUN-ADJ-ADP-NOUN" ] = ( [ 
            { "RIGHT_ID": "dep1", "RIGHT_ATTRS": { 
                "POS": "VERB"
            } },
            { "RIGHT_ID": "dep2", "LEFT_ID": "dep1", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": { "IN": [ "NOUN", "PROPN" ] }, 
                "DEP": { "IN": [ "nsubj", "nsubjpass" ] }
            } }, 
            { "RIGHT_ID": "dep3", "LEFT_ID": "dep1", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": "ADJ", 
                "DEP": "acomp"
            } }, 
            { "RIGHT_ID": "dep4", "LEFT_ID": "dep3", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": "ADP", 
                "DEP": "prep"
            } }, 
            { "RIGHT_ID": "dep5", "LEFT_ID": "dep4", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": { "IN": [ "NOUN", "PROPN" ] }, 
                "DEP": { "IN": [ "dobj", "pobj" ] }
            } }, 
        ], [ [ 1 ], [ 2, 3 ], [ 4 ] ] )

        # --------------------------------------------------------------------------------------------

        self.patterns[ "VERB-NOUN-ADJ-VERB-NOUN" ] = ( [ 
            { "RIGHT_ID": "dep1", "RIGHT_ATTRS": { 
                "POS": "VERB"
            } },
            { "RIGHT_ID": "dep2", "LEFT_ID": "dep1", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": { "IN": [ "NOUN", "PROPN" ] }, 
                "DEP": { "IN": [ "nsubj", "nsubjpass" ] }
            } }, 
            { "RIGHT_ID": "dep3", "LEFT_ID": "dep1", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": "ADJ", 
                "DEP": "acomp"
            } },
            { "RIGHT_ID": "dep4", "LEFT_ID": "dep3", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": "VERB", 
                "DEP": "xcomp"
            } },
            { "RIGHT_ID": "dep5", "LEFT_ID": "dep4", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": { "IN": [ "NOUN", "PROPN" ] }, 
                "DEP": { "IN": [ "dobj", "pobj" ] }
            } }, 
        ], [ [ 1 ], [ 3 ], [ 4 ] ] )

        # --------------------------------------------------------------------------------------------

        self.patterns[ "VERB-NOUN-NOUN-ADP-NOUN" ] = ( [ 
            { "RIGHT_ID": "dep1", "RIGHT_ATTRS": { 
                "POS": "VERB"
            } }, 
            { "RIGHT_ID": "dep2", "LEFT_ID": "dep1", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": { "IN": [ "NOUN", "PROPN" ] }, 
                "DEP": { "IN": [ "nsubj", "nsubjpass" ] }
            } }, 
            { "RIGHT_ID": "dep3", "LEFT_ID": "dep1", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": { "IN": [ "NOUN", "PROPN" ] }, 
                "DEP": { "IN": [ "dobj", "pobj" ] }
            } }, 
            { "RIGHT_ID": "dep4", "LEFT_ID": "dep1", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": "ADP", 
                "DEP": "prep"
            } }, 
            { "RIGHT_ID": "dep5", "LEFT_ID": "dep4", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": { "IN": [ "NOUN", "PROPN" ] }, 
                "DEP": { "IN": [ "dobj", "pobj" ] }
            } }, 
        ], [ [ 1 ], [ 0, 2 ], [ 3, 4 ] ] )

        # --------------------------------------------------------------------------------------------

        self.patterns[ "VERB-NOUN-ADJ-VERB-ADP-NOUN" ] = ( [ 
            { "RIGHT_ID": "dep1", "RIGHT_ATTRS": { 
                "POS": "VERB", 
                "DEP": { "IN": [ "ROOT", "ccomp" ] }
            } },
            { "RIGHT_ID": "dep2", "LEFT_ID": "dep1", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": { "IN": [ "NOUN", "PROPN" ] }, 
                "DEP": { "IN": [ "nsubj", "nsubjpass" ] }
            } }, 
            { "RIGHT_ID": "dep3", "LEFT_ID": "dep1", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": "ADJ", 
                "DEP": "acomp"
            } },
            { "RIGHT_ID": "dep4", "LEFT_ID": "dep3", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": "VERB", 
                "DEP": "xcomp"
            } }, 
            { "RIGHT_ID": "dep5", "LEFT_ID": "dep4", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": "ADP", 
                "DEP": "prep"
            } }, 
            { "RIGHT_ID": "dep6", "LEFT_ID": "dep5", "REL_OP": operator, "RIGHT_ATTRS": { 
                "POS": { "IN": [ "NOUN", "PROPN" ] }, 
                "DEP": { "IN": [ "dobj", "pobj" ] }
            } }, 
        ], [ [ 1 ], [ 3, 4 ], [ 5 ] ] )

        # --------------------------------------------------------------------------------------------
