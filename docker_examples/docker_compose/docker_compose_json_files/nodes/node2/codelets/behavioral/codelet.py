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
import threading
import os
import dct


class BehavioralCodelet(dct.codelets.PythonCodelet):

    def calculate_activation(self):
        # print("new Activation")
        return 0.0

    def proc(self, activation):
        mem = dct.get_memory_objects_by_name(self.root_codelet_dir, 'behavioral-perceptual-memory', 'inputs')[0]
        dct.set_memory_objects_by_name(self.root_codelet_dir, 'motor-behavioral-memory', 'I', mem['I'], 'outputs')


if __name__ == '__main__':
    codelet = BehavioralCodelet(name='behavioralCodelet',root_codelet_dir=os.getcwd()+'/codelets/behavioral')
    threading.Thread(target=codelet.run).start()
    # codelet.run()
