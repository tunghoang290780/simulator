from construct import *
import utils

import array
import numpy as np

class ProcessingElement(Construct):
    """
        Processing Element
    """

    # ifmap:  np x k (np: number of patches) in INT8
    # kernel: nk x k (nk: number of kernels) in INT8
    # ofmap <-- ifmap * kernel': np x nk in INT16
    # NOTE this is to make it easier to load kernels
    def matmul8(self, inputs, outputs, arguments):
        #print 'matmul {} {} {}'.format(outputs, inputs, arguments)
        ifmap = self.pop_input(inputs[0]).astype(np.int16)
        kernel = self.pop_input(inputs[1]).astype(np.int16)
        assert ifmap.shape[1] == kernel.shape[1], 'shape error for matmul'
        ofmap = np.matmul(ifmap, kernel.T)
        assert ifmap.shape[0] == ofmap.shape[0], 'output not correct shape'
        assert kernel.shape[0] == ofmap.shape[1], 'output not correct shape'
        self.push_output(outputs[0], ofmap)

    def add8(self, inputs, outputs, arguments):
        #print 'add {} {} {}'.format(outputs, inputs, arguments)
        mat0 = self.pop_input(inputs[0]).astype(np.int8)
        mat1 = self.pop_input(inputs[1]).astype(np.int8)
        assert mat0.shape == (arguments[0], arguments[1]), 'shape error for add'
        assert mat0.shape == mat1.shape, 'shape error for add'
        out = mat0 + mat1
        self.push_output(outputs[0], out)
    
    # TODO value dependent timing calculation has to be implemented later
    def __init__(self, name, matmul8_time, add8_time):
        super(ProcessingElement, self).__init__(name)
        
        #                command,   time,         function,     inputs, outputs, arguments 
        self.set_command('matmul8', matmul8_time, self.matmul8, [1, 2], [0],     [3, 4, 5])
        self.set_command('add8',    add8_time,    self.add8,    [1, 2], [0],     [3, 4])

if __name__ == '__main__':
    # import memory to help test pe
    from memory import *

    # build constructs to check
    ifmem = Memory('ifmem', 80, 40)
    kmem = Memory('kmem', 80, 40)
    ofmem = Memory('ofmem', 80, 40)
    pe = ProcessingElement('pe', 200, 20)

    # add connections
    ifmem.add_output(pe) # ifmem --> pe
    pe.add_input('ifmem')
    
    pe.add_output(ifmem) # pe --> ifmem (to save initial values)
    ifmem.add_input('pe')
    
    kmem.add_output(pe) # kmem --> pe
    pe.add_input('kmem')

    pe.add_output(kmem) # pe --> kmem (to save initial values)
    kmem.add_input('pe')

    pe.add_output(ofmem) # pe --> ofmem
    ofmem.add_input('pe')
    
    # force data in Memory for testing purpose
    ifmem.feed_command(['store8    pe    0x000 8 4', \
                        'load8     pe    0x000 8 4'])
    kmem.feed_command( ['store8    pe    0x000 8 4', \
                        'load8     pe    0x000 8 4'])
    pe.feed_command(   ['matmul8   ofmem ifmem kmem 8 4 8'])
    ofmem.feed_command(['store16   pe    0x000 8 8'])
    ifmem.input_list['pe'].append((20.0, np.array([1, 2, 3, 4, \
                                                   5, 6, 7, 8, \
                                                   9, 10, 11, 12, \
                                                   13, 14, 15, 16, \
                                                   17, 18, 19, 20, \
                                                   21, 22, 23, 24, \
                                                   25, 26, 27, 28, \
                                                   29, 30, 31, 32])))
    kmem.input_list['pe'].append((40.0, np.array([1, 2, 3, 4, \
                                                  5, 6, 7, 8, \
                                                  9, 10, 11, 12, \
                                                  13, 14, 15, 16, \
                                                  17, 18, 19, 20, \
                                                  21, 22, 23, 24, \
                                                  25, 26, 27, 28, \
                                                  29, 30, 31, 32])))

    # run quantums for test
    value_aware = True
    ifmem.run_quantum(value_aware)
    ifmem.run_quantum(value_aware)
    kmem.run_quantum(value_aware)
    kmem.run_quantum(value_aware)
    pe.run_quantum(value_aware)
    print ofmem.input_list['pe'][0] # print the queue before it gets popped
    ofmem.run_quantum(value_aware)

    # remove temporary file
    if value_aware:
        os.remove('ifmem_file')
        os.remove('kmem_file')
        os.remove('ofmem_file')
