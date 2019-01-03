from engine import *    # SIMULATION ENGINE
from construct import *
from memory import *    # MEMORY
from pe import *        # PE
import utils

import array
import numpy as np

if __name__ == '__main__':
    test_engine = SimulationEngine(value_aware=True)

    # build constructs to check
    test_engine.add_construct(Memory('ifmem', 80, 40))
    test_engine.add_construct(Memory('kmem', 80, 40))
    test_engine.add_construct(Memory('ofmem', 80, 40))
    test_engine.add_construct(ProcessingElement('pe', 200, 20))

    # add connections
    test_engine.add_connection('ifmem', 'pe')
    test_engine.add_connection('pe', 'ifmem') # to save initial values
    test_engine.add_connection('kmem', 'pe')
    test_engine.add_connection('pe', 'kmem') # to save initial values
    test_engine.add_connection('pe', 'ofmem')
    
    # force data in Memory for testing purpose
    test_engine.feed_command('ifmem', ['load8     pe    0x000 8 4'])
    test_engine.feed_command('kmem',  ['load8     pe    0x000 8 4'])
    test_engine.feed_command('pe',    ['matmul8   ofmem ifmem kmem 8 4 8'])
    test_engine.feed_command('ofmem', ['store16   pe    0x000 8 8'])

    """
    # force test data to test
    test_engine.get_construct('ifmem')\
               .input_list['pe']\
               .append((20.0, np.array([1, 2, 3, 4, \
                                        5, 6, 7, 8, \
                                        9, 10, 11, 12, \
                                        13, 14, 15, 16, \
                                        17, 18, 19, 20, \
                                        21, 22, 23, 24, \
                                        25, 26, 27, 28, \
                                        29, 30, 31, 32])))
    test_engine.get_construct('kmem')\
               .input_list['pe']\
               .append((40.0, np.array([1, 2, 3, 4, \
                                        5, 6, 7, 8, \
                                        9, 10, 11, 12, \
                                        13, 14, 15, 16, \
                                        17, 18, 19, 20, \
                                        21, 22, 23, 24, \
                                        25, 26, 27, 28, \
                                        29, 30, 31, 32])))
    """

    # run test
    test_engine.run()
    
    """
    # run quantums for test
    print test_engine.all_command_empty()
    test_engine.get_construct('ifmem').run_quantum(value_aware)
    test_engine.get_construct('kmem').run_quantum(value_aware)
    test_engine.get_construct('ifmem').run_quantum(value_aware)
    test_engine.get_construct('kmem').run_quantum(value_aware)
    test_engine.get_construct('pe').run_quantum(value_aware)
    print test_engine.get_construct('ofmem').input_list['pe'][0] # print the queue before it gets popped
    test_engine.get_construct('ofmem').run_quantum(value_aware)

    print test_engine.all_command_empty()
    """
    # remove temporary file
    #os.remove('ifmem_file')
    #os.remove('kmem_file')
    #os.remove('ofmem_file')
