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

# usage: ./removeOutput.sh <field> <value>
# example: ./removeOutput.sh ip/port 127.0.0.1:6000


if [ $# -eq 0 ]
    then
        echo "No argument supplied!

usage: ./removeOutput.sh <arg>"
    else
        python3 $root_codelet_dir/methods/changeField.py remove outputs $1
fi

