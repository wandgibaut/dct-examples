# ****************************************************************************#
# Copyright (c) 2020  Wandemberg Gibaut                                       #
# All rights reserved. This program and the accompanying materials            #
# are made available under the terms of the MIT License                       #
# which accompanies this distribution, and is available at                    #
# https://opensource.org/licenses/MIT                                         #
#                                                                             #
# Contributors:                                                               #
#      W. Gibaut                                                              #
#                                                                             #
# ****************************************************************************#

import socketserver
import sys
import json
import threading
import os
import glob

ROOT_NODE_DIR = os.getcwd()


def get_connections():
	with open('connections.json', 'r+') as json_data:  # abrir o fields
		return json.load(json_data)


def add_connection(connection, field):
	field_file = None
	for filename in glob.iglob('./nodes/**', recursive=True):
		if filename.__contains__(connection[field] + '/fields'):
			field_file = filename
	with open(field_file, 'r+') as json_data:
		jsonData= json.load(json_data)
		if field == 'in':
			jsonData['inputs'].append(create_connection(connection))
		elif field == 'out':
			jsonData['outputs'].append(create_connection(connection))

		json_data.seek(0)  # rewind
		json.dump(jsonData, json_data)
		json_data.truncate()


def create_json_memory(connection, name):
	memory_dir = None
	for filename in glob.iglob('./nodes/**', recursive=True):
		if filename.__contains__(connection['out'] + '/memories'):
			if os.path.isdir(filename):
				memory_dir = filename
	with open(memory_dir + '/' + name + '.json', 'w') as json_data:

		mem = {
			"name": name,
			"ip/port": connection['ip/port'],
			"type": connection['type'],
			"I": "0",
			"eval": 0.0}

		json.dump(mem, json_data)


def create_connection(connection):
	if (connection['type'] == 'tcp')  or (connection['type'] == 'local'):
		name = connection['in'] + '-' + connection['out'] + '-' + 'memory'
		create_json_memory(connection, name)
	else:
		name = connection['in'] + '-input-memories/' + connection['out'] + '-' + 'memory'

	conn = {
		"ip/port": connection['ip/port'],
		"type": connection['type'],
		"name": name
	}
	return conn


def clear_connection(connection, field):
	field_file = None
	for filename in glob.iglob('./nodes/**', recursive=True):
		if filename.__contains__(connection[field] + '/fields'):
			field_file = filename
	with open(field_file, 'r+') as json_data:
			jsonData= json.load(json_data)

			jsonData['inputs'].clear()
			jsonData['outputs'].clear()

			json_data.seek(0)  # rewind
			json.dump(jsonData, json_data)
			json_data.truncate()


def fill_connections():
	connections = get_connections()
	for connection in connections['connections']:
		add_connection(connection, 'in')
		add_connection(connection, 'out')


def clear():
	connections = get_connections()
	for connection in connections['connections']:
		clear_connection(connection, 'in')
		clear_connection(connection, 'out')


def test():
	for filename in glob.iglob('./nodes/**', recursive=True):
		if filename.__contains__('fields'):
			print(filename)
		if filename.__contains__('sensory/codelet/fields'):
			print('here')


if __name__ == '__main__':
	args = sys.argv[1:]

	if len(args) != 0:
		if args[0] == 'clear':
			clear()
			sys.exit()
		elif args[0] == 'reset':
			clear()
			fill_connections()
			sys.exit()

	fill_connections()
