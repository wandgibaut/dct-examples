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
import time
import os
import threading
import dct


class PerceptualCodelet(dct.codelets.PythonCodelet):

    def calculate_activation(self):
        # print("new Activation")
        return 0.0

    def proc(self, activation):
        mem = dct.get_memory_objects_by_name(self.root_codelet_dir, 'perceptual-sensory-memory', 'inputs')[0]
        # print(mem['I'])
        #dct.set_memory_objects_by_name(self.root_codelet_dir, 'behavioral-perceptual-memory', 'I', mem['I'], 'outputs')
        #pass


if __name__ == '__main__':
   #  print(os.getenv('ROOT_CODELET_DIR'))
    codelet = PerceptualCodelet(name='perceptualCodelet',root_codelet_dir=os.getcwd()+'/codelets/perceptual')
    threading.Thread(target=codelet.run).start()
    # codelet.run()
