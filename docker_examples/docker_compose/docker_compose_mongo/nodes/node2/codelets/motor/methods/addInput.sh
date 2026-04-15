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

# usage: ./addInput.sh <arg>
# where <arg> is a string with the inputs to set
# example: ./addInput.sh '{"key": "value"}'


if [ $# -eq 0 ]
    then
        echo "No argument supplied!

usage: ./setInputs.sh <arg>"
    else
        python3 $root_codelet_dir/methods/changeField.py add inputs "$1"
fi


# must format like this: '{"key": "value"}' when called
