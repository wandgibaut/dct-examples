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
import json
import sys
import os

root_codelet_dir= os.getenv('ROOT_CODELET_DIR')


def read_field(field):
	with open(root_codelet_dir +'/fields.json', 'r') as json_data:
		jsonData = json.load(json_data)
		value = jsonData[field]
	return value


def read_field_with_name(field, name):
	with open(root_codelet_dir + '/fields.json', 'r') as json_data:
		jsonData = json.load(json_data)
		vector = jsonData[field]
		for i in vector:
			for k, v in i.items():
				if (v == name):
					return i
	return "none"


if __name__ == '__main__':
	args = sys.argv[1:]
	if len(args) == 1:
		field = args[0]
		print(read_field(field))
	elif len(args) == 2:
		field = args[0]
		name = args[1]
		print(read_field_with_name(field, name))

	#elif len(args) == 3:
	#	field = args[0]
	#	name = args[1]
	#	index = args[2]
	#	print(read_field_with_name(field, name))

	else:
		print('Error! Wrong number of arguments!')

	sys.exit()

