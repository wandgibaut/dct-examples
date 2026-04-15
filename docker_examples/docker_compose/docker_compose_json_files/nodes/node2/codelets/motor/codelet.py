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


class MotorCodelet(dct.codelets.PythonCodelet):

    def calculate_activation(self):
        # print("new Activation")
        return 0.0

    def proc(self, activation):
        mem = dct.get_memory_objects_by_name(self.root_codelet_dir, 'motor-behavioral-memory', 'inputs')[0]
        # dct.set_memory_objects(self.root_codelet_dir, 'final-memory', 'I', mem['I'], 'outputs')
        print(mem['I'])


if __name__ == '__main__':
    codelet = MotorCodelet(name='motorCodelet',root_codelet_dir=os.getcwd()+'/codelets/motor')
    threading.Thread(target=codelet.run).start()
    # codelet.run()
