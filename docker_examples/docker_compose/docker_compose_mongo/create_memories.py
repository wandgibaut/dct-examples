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

import json
import sys
import glob
from pymongo import MongoClient
import redis
import os

os.chdir(os.path.dirname(__file__))
current_dir = os.getcwd()
# mount : receber lista de codelets
# verificar inputs, outputs e tipo de codelet
# montar metodos de acesso e ligar tudo 

#padrão pra nome da base e da collection
# base: 'database-raw-memory'
# collection: '<tipo: sensory, perceptual...>-<anotação: nome do codelet, grupo de codelets...>-input-memories'


def mount(list_of_codelets):
    for codelet in list_of_codelets:
        field_file = None
        for filename in glob.iglob(current_dir + '/nodes/**', recursive=True):
            if filename.__contains__(codelet + '/fields'):
                field_file = filename
        with open(field_file, 'r+') as json_data:  # abrir o fields
            jsonData = json.load(json_data)
            inputs = jsonData['inputs']
            outputs = jsonData['outputs']
            codelet_name = jsonData['name']
            
            for inputMemory in inputs:
                try:
                    if inputMemory['type'] == 'mongo':
                        client = MongoClient(inputMemory['ip/port']) # METODO: vai no ip
                        base = client['database-raw-memory']
                        inMem = base[convert(inputMemory['name'])[0]] # define base, collection (input name)
                        #debug
                        print(inputMemory['name'])
                        print(convert(inputMemory['name']))
                        mem = inMem.find_one(
                            {'name': convert(inputMemory['name'])[1]}) # e checa se existe uma memoria com esse name

                        if(mem == None):  # se sim, deixa quieto, se não, cria
                            memory = {'name': convert(inputMemory['name'])[1],'ip/port': inputMemory['ip/port'],'type': 'mongo', 'group': [], 'I': None,'eval': 0.0}
                            inMem.insert_one(memory)
                            print(memory)
                        
                    if inputMemory['type'] == 'redis':
                        client = redis.Redis(host=convert_alt(inputMemory['ip/port'])[0], port=convert_alt(inputMemory['ip/port'])[1])
                        
                        mem = {'name': convert(inputMemory['name'])[1],'ip/port': inputMemory['ip/port'],'type': 'redis', 'group': [],'I': None,'eval': 0.0}
                        client.set(convert(inputMemory['name'])[1], json.dumps(mem))
                    
                    if inputMemory['type'] == 'tcp':
                        #subprocess.check_call()
                        print('tcp')
                except: 
                    print('an error has occurred!!')
       

def convert(string): 
    li = list(string.split("/")) 
    return li 


def convert_alt(string): 
    li = list(string.split(":")) 
    return li 


if __name__ == '__main__':
    args = sys.argv[1:]
    list_of_codelets = args
    
    mount(list_of_codelets)


