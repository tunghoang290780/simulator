from engine import *    # SIMULATION ENGINE
from construct import * # CONSTRUCT
from memory import *    # MEMORY
from pe import *        # PE

if __name__ == '__main__':
    test_engine = SimulationEngine(value_aware=True)

    # build constructs to check
    test_engine.add_construct(Memory('ifmem', 80, 40))
    test_engine.add_construct(Memory('kmem', 80, 40))
    test_engine.add_construct(Memory('ofmem', 80, 40))
    test_engine.add_construct(ProcessingElement('pe', 200, 20))

    # add connections
    test_engine.add_connection('ifmem', 'pe')
    test_engine.add_connection('kmem', 'pe')
    test_engine.add_connection('pe', 'ofmem')
    
    # force data in Memory for testing purpose
    test_engine.feed_command('ifmem', ['load8     pe    0x000 8 4'])
    test_engine.feed_command('kmem',  ['load8     pe    0x000 8 4'])
    test_engine.feed_command('pe',    ['matmul8   ofmem ifmem kmem 8 4 8'])
    test_engine.feed_command('ofmem', ['store16   pe    0x000 8 8'])

    # run test
    print 'simulation took {}ns'.format(test_engine.run())
