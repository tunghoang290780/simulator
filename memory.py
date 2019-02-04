from construct import *
import utils

import os
import array
import numpy as np

class Memory(Construct):
    """
        Memory
    """

    # NOTE large I/O could speed things up.
    # Reading files in parallel may speed things up.
    # FIXME this load and store is just simple implementation
    # that is not complete
    def load8(self, inputs, outputs, arguments):
        #print 'load8 {} {}'.format(outputs, arguments)
        assert os.path.exists(self.get_cid()+'_hex'), 'file for memory missing'
        mem_fd = os.open(self.get_cid()+'_hex', os.O_RDWR)
        os.lseek(mem_fd, arguments[0], 0)
        val = np.array(array.array('b', os.read(mem_fd, arguments[1] * arguments[2])), dtype=np.int8)
        self.push_output(outputs[0], val.reshape(arguments[1], arguments[2]))
    
    def load16(self, inputs, outputs, arguments):
        #print 'load16 {} {}'.format(outputs, arguments)
        assert os.path.exists(self.get_cid()+'_hex'), 'file for memory missing'
        mem_fd = os.open(self.get_cid()+'_hex', os.O_RDWR)
        os.lseek(mem_fd, arguments[0], 0)
        val = np.array(array.array('h', os.read(mem_fd, arguments[1] * arguments[2])), dtype=np.int16)
        self.push_output(outputs[0], val.reshape(arguments[1], arguments[2]))
    
    def store8(self, inputs, outputs, arguments):
        #print 'store8 {} {}'.format(inputs, arguments)
        if not os.path.exists(self.get_cid()+'_hex'):
            utils.make_file(self.get_cid()+'_hex', 32*1024)
        mem_fd = os.open(self.get_cid()+'_hex', os.O_RDWR)
        os.lseek(mem_fd, arguments[0], 0)
        val = self.pop_input(inputs[0]).astype(np.int8)
        assert val.size == (arguments[1] * arguments[2]), 'size not matching'
        os.write(mem_fd, val[:])

    def store16(self, inputs, outputs, arguments):
        #print 'store16 {} {}'.format(inputs, arguments)
        if not os.path.exists(self.get_cid()+'_hex'):
            utils.make_file(self.get_cid()+'_hex', 32*1024)
        mem_fd = os.open(self.get_cid()+'_hex', os.O_RDWR)
        os.lseek(mem_fd, arguments[0], 0)
        val = self.pop_input(inputs[0]).astype(np.int16)
        assert val.size == (arguments[1] * arguments[2]), 'size not matching'
        os.write(mem_fd, val[:])

    def __init__(self, name, store_time, load_time):
        super(Memory, self).__init__(name)
        
        #                command,   time,       function,     inputs, outputs, arguments 
        self.set_command('load8',   load_time,  self.load8,   [],     [0],     [1, 2, 3])
        self.set_command('load16',  load_time,  self.load16,  [],     [0],     [1, 2, 3])
        self.set_command('store8',  store_time, self.store8,  [0],    [],      [1, 2, 3])
        self.set_command('store16', store_time, self.store16, [0],    [],      [1, 2, 3])
    
if __name__ == '__main__':
    # build constructs to check
    mem = Memory('mem', 80, 40)
    pe = Construct('pe')

    # add connections
    mem.add_output(pe) # mem --> pe
    pe.add_input('mem')
    pe.add_output(mem) # pe --> mem
    mem.add_input('pe')
    
    # add commands
    mem.command = ['store8   pe 0x400 8 4', \
                   'store8   pe 0x420 8 4', \
                   'load8    pe 0x410 8 4']
    
    # force data in Memory queue for testing purpose
    mem.input_list['pe'].append((10.0, np.array([1, 2, 3, 4, \
                                                 5, 6, 7, 8, \
                                                 9, 10, 11, 12, \
                                                 13, 14, 15, 16, \
                                                 17, 18, 19, 20, \
                                                 21, 22, 23, 24, \
                                                 25, 26, 27, 28, \
                                                 29, 30, 31, 32])))
    mem.input_list['pe'].append((40.0, np.array([1, 2, 3, 4, \
                                                 5, 6, 7, 8, \
                                                 9, 10, 11, 12, \
                                                 13, 14, 15, 16, \
                                                 17, 18, 19, 20, \
                                                 21, 22, 23, 24, \
                                                 25, 26, 27, 28, \
                                                 29, 30, 31, 32])))

    # run quantums for test
    mem.run_quantum()
    mem.run_quantum()
    mem.run_quantum()

    # print to check 
    print pe.input_list['mem'][0]

    # remove temporary file
    os.remove('mem_file')
