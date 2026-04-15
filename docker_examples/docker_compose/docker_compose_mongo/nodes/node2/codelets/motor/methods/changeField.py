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

root_codelet_dir = os.getenv('ROOT_CODELET_DIR')


def change_field(field, value):
	with open(root_codelet_dir + '/fields.json', 'r+') as json_data:
		jsonData = json.load(json_data)
		jsonData[field] = value
		print(jsonData[field])
		
		json_data.seek(0) #rewind
		json.dump(jsonData, json_data)
		json_data.truncate()


def add_entry(field, data):
	with open(root_codelet_dir + '/fields.json', 'r+') as json_data:
		jsonData = json.load(json_data)
		vector = jsonData[field]
		vector.append(json.loads(data))
		jsonData[field] = vector
		
		print(jsonData[field])
		
		json_data.seek(0) #rewind
		json.dump(jsonData, json_data)
		json_data.truncate()


def remove_entry(field, name):
	with open(root_codelet_dir + '/fields.json', 'r+') as json_data:
		jsonData = json.load(json_data)
		vector = jsonData[field]

		for i in vector:
			for k, v in i.items():
				if (v == name):
					vector.remove(i)
					return i

		jsonData[field] = vector
		print(jsonData[field])
		
		json_data.seek(0) #rewind
		json.dump(jsonData, json_data)
		json_data.truncate()

		
def set_field_list(field, dataList):
	jsonList = []
	for dataString in dataList:
		jsonList.append(json.loads(dataString))

	with open(root_codelet_dir + '/fields.json', 'r+') as json_data:
		jsonData = json.load(json_data)
		jsonData[field] = jsonList
		print(jsonData[field])
		
		json_data.seek(0) #rewind
		json.dump(jsonData, json_data)
		json_data.truncate()


def convert(string):
	li = list(string.split(";"))
	return li


if __name__ == '__main__':
	args = sys.argv[1:]
	if len(args) == 2:
		field = args[0]
		value = args[1]
		change_field(field, value)
	
	elif len(args) == 3:
		if args[0] == 'add':
			field = args[1]
			data = args[2]
			add_entry(field, data)

		elif args[0] == 'remove':
			field = args[1]
			data = args[2]
			remove_entry(field, data)
		
		elif args[0] == 'list':
			field = args[1]
			dataList = convert(args[2])
			set_field_list(field, dataList)

	else:
		print(len(args))
		print('Error! Wrong number of arguments!')
		sys.exit()

