#!/bin/bash

#*****************************************************************************#
# Copyright (c) 2020  Wandemberg Gibaut                                       #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the MIT License                       #
# which accompanies this distribution, and is available at                    #
# https://opensource.org/licenses/MIT                                         #
#                                                                             #
# Contributors:                                                               #
#      W. Gibaut                                                              #
#                                                                             #
#*****************************************************************************#


if [ $# -ne 0 ] 
    then
        echo "initiating servers!"
        for var in "$@"
        do
            python3 $ROOT_CODELET_DIR/server.py "$var"  &
        done
fi



    
python3 $ROOT_CODELET_DIR/codelet.py 

   
