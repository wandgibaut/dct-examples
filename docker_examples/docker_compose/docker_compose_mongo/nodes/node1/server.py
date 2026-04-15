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
import socket
import sys
import json
import threading
import os
import glob
import configparser
root_node_dir = os.getenv('ROOT_NODE_DIR')
# root_node_dir = '/home/wander/OtherProjects/dct_pack/dct/devel/mind_test/nodes/node1'


class CodeletTCPHandler(socketserver.BaseRequestHandler):
    # TODO: improve
    def get_memory(self, memory_name):
        file_memory = None
        for filename in glob.iglob(root_node_dir + '/**', recursive=True):
            if filename.__contains__(memory_name + '.json'):
                file_memory = filename
        with open(file_memory, 'r+') as json_data:
            memory = json.dumps(json.load(json_data))
            return memory

    def set_memory(self, memory_name, field, value):
        file_memory = None
        for filename in glob.iglob(root_node_dir + '/**', recursive=True):
            if filename.__contains__(memory_name + '.json'):
                file_memory = filename
        with open(file_memory, 'r+') as json_data:
            jsonData = json.load(json_data)
            jsonData[field] = value
            json_data.seek(0) # rewind
            json.dump(jsonData, json_data)
            json_data.truncate()

    def get_codelet_info(self, codelet_name):
        file_fields = None
        for filename in glob.iglob(root_node_dir + '/**', recursive=True):
            if filename.__contains__(codelet_name + '/fields.json'):
                file_fields = filename
        with open(file_fields, 'r+') as json_data:
            fields = json.dumps(json.load(json_data))
            return fields

    def get_node_info(self):
        print('a')
        number_of_codelets = 0
        input_ips = []
        output_ips = []
        for filename in glob.iglob(root_node_dir + '/**', recursive=True):
            if filename.__contains__('fields.json'):
                number_of_codelets += 1
                with open(filename, 'r+') as json_data:
                    fields = json.load(json_data)
                    add_inputs = [item['ip/port'] for item in fields['inputs']]
                    add_outputs = [item['ip/port'] for item in fields['outputs']]
                    for entry in add_inputs:
                        if entry not in input_ips:
                            input_ips.append(entry)
                    for entry in add_outputs:
                        if entry not in output_ips:
                            output_ips.append(entry)

        answer = {'number_of_codelets': number_of_codelets, 'input_ips': input_ips, 'output_ips': output_ips}
        return json.dumps(answer)

    @staticmethod
    def convert(string):
        li = list(string.split("_"))
        return li

    def read_param(self):
        config = configparser.ConfigParser()
        config.read(root_node_dir + '/param.ini', encoding='utf-8')
        return config

    def set_param(self, section, field, value):
        config = self.read_param()
        config.set(section, field, value)
        with open(root_node_dir + '/param.ini', 'w') as configfile:
            config.write(configfile)

    def remove_param(self, section, field):
        config = self.read_param()
        config.remove_option(section, field)
        with open(root_node_dir + '/param.ini', 'w') as configfile:
            config.write(configfile)

    def kill_codelet(self, codelet_name):
        self.remove_param('active_codelets', codelet_name)
        return 0

    def run_codelet(self, codelet_name):
        config = self.read_param()
        if config.has_option('internal_codelets', codelet_name):
            self.set_param('active_codelets', codelet_name, codelet_name)
        return 0

    def config_death(self):
        config = self.read_param()
        self.death_threshold = int(config.get('signals', 'death_threshold'))
        self.death_votes = 0

    def vote_kill(self, ip_port):
        data = 'vote_' + ip_port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to server and send data
            splited = split(ip_port)
            sock.connect((splited[0], int(splited[1])))
            sock.sendall(bytes(data + "\n", "utf-8"))
            # Receive data from the server and shut down
            received = str(sock.recv(1024), "utf-8")
            return received  # a string confirming the vote

    def listen_death_democracy(self, node_ip):
        if not hasattr(self, 'death_threshold'):
            self.config_death()

        config = self.read_param()
        for i in range(self.death_threshold):
            if config.has_option('signals', 'voter_' + str(i)):
                if config.get('signals', 'voter_' + str(i)) == 'node_ip':
                    return 'vote already listened!'

        self.set_param('signals', 'voter_' + str(self.death_votes), node_ip)
        self.death_votes += 1

        if self.death_votes >= self.death_threshold:
            self.set_param('signals', 'suicide_note', 'true')
            return 'node will die!'

        return 'vote computed!'

    def listen_death_authority(self):
        self.set_param('signals', 'suicide_note', 'true')
        return 0

    # TODO: implement this method
    def listen_internal_codelet(self):
        return 0

    # TODO: implement ifs
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        list_data = self.convert(self.data.decode())
        if list_data[0] == 'get':
            self.request.sendall(bytes(self.get_memory(list_data[1]), "utf-8"))
            
        if list_data[0] == 'set':
            self.set_memory(list_data[1], list_data[2], list_data[3])
            self.request.sendall(bytes('success!', "utf-8"))

        if list_data[0] == 'info':
            print('Ok!')
            if len(list_data) == 2:
                self.request.sendall(bytes(self.get_codelet_info(list_data[1]), "utf-8"))
            else:
                self.request.sendall(bytes(self.get_node_info(), "utf-8"))

        if list_data[0] == 'kill-codelet':
            self.kill_codelet(list_data[1])
            self.request.sendall(bytes('codelet killed!', "utf-8"))

        if list_data[0] == 'run-codelet':
            self.run_codelet(list_data[1])
            self.request.sendall(bytes('codelet will run soon!', "utf-8"))

        if list_data[0] == 'vote-kill':
            self.vote_kill(list_data[1])
            # self.request.sendall(bytes('codelet killed!', "utf-8"))

        if list_data[0] == 'die':
            self.listen_death_democracy(list_data[1])
            self.request.sendall(bytes('vote computed!', "utf-8"))

        if list_data[0] == 'die-now':
            self.listen_death_authority()
            self.request.sendall(bytes('will die soon! Good bye... :(', "utf-8"))


def split(string): 
    li = list(string.split(":")) 
    return li 


if __name__ == "__main__":
    args = sys.argv[1:]
    HOST = split(args[0])[0]
    PORT = int(split(args[0])[1])
    server = socketserver.TCPServer((HOST, PORT), CodeletTCPHandler)
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    threading.Thread(target=server.serve_forever).start()
    # server.serve_forever()
