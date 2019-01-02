from heapq import *
from construct import *

class SimulationEngine(object):
    """
        Simulation Engine
    """

    def __init__(self):
        self.crnt_time = 0.0

        self.constructs = {}
        self.pending = []
    
    def add_construct(self, construct):
        assert construct.get_cid() not in self.constructs.keys(), \
               'cid already in constructs'
        
        # TODO add list of commands supported by constructs maybe make a dict
        # so that later commands can be sorted to right constructs by the engine

        self.constructs[construct.get_cid()] = construct

    def get_construct_list(self):
        return self.constructs.keys()

    def add_connection(self, src_name, dst_name):
        assert src_name in constructs.keys(), 'src_name not in constructs'
        assert dst_name in constructs.keys(), 'dst_name not in constructs'

        src = constructs[src_name]
        dst = constructs[dst_name]

        src.add_output(dst)
        dst.add_input(src_name)

    def feed_commands(self, command_list):
        # TODO feed_command
        # (1) put constructs related to commands without dependency to pending
        # (2) put all into pertinent constructs
        pass

    # assumption is that (1) each construct is associated with an 
    # instruction queue (2) each quantum is associated with an instruction
    def run_set_time(self, set_time):
        assert len(pending_quantums) != 0, 'no pending quantums'

        while pending[0][0] < crnt_time + set_time:
            quantum = heappop(pending_quantums)
            inc_time = quantum[1].get_quantum_time()
            
            if value_aware:
                quantum[1].run_quantum()

        crnt_time = crnt_time + set_time

    def run(self):
        while len(pending_quantums) != 0:
            quantum = heappop(pending_quantums)
            crnt_time = quantum[0]
            inc_time = quantum[1].get_quantum_time()
            
            if value_aware:
                quantum[1].run_quantum()

            crnt_time = crnt_time + inc_time

if __name__ == '__main__':
    test_engine = SimulationEngine()
    test_construct = Construct('test_construct')
    test_engine.add_construct(test_construct)
    print test_engine.get_construct_list()
