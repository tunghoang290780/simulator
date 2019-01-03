from heapq import *
from construct import *

class SimulationEngine(object):
    """
        Simulation Engine
    """

    def __init__(self, value_aware):
        self.crnt_time = 0.0

        self.value_aware = value_aware

        self.constructs = {}
    
    def add_construct(self, construct):
        assert construct.get_cid() not in self.constructs.keys(), \
               'cid already in constructs'
        
        # TODO add list of commands supported by constructs maybe make a dict
        # so that later commands can be sorted to right constructs by the engine

        self.constructs[construct.get_cid()] = construct

    def get_construct(self, construct_name):
        return self.constructs[construct_name]
    
    def get_construct_list(self):
        return self.constructs.keys()

    def add_connection(self, src_name, dst_name):
        assert src_name in self.constructs.keys(), 'src_name not in constructs'
        assert dst_name in self.constructs.keys(), 'dst_name not in constructs'

        src = self.constructs[src_name]
        dst = self.constructs[dst_name]

        src.add_output(dst)
        dst.add_input(src_name)

    # TODO parser that makes binary or whatever form into command_list needs 
    # to be implemented
    def feed_command(self, construct_name, command_list):
        self.constructs[construct_name].feed_command(command_list)
    
    def all_command_empty(self):
        for construct_name, construct in self.constructs.items():
            if construct.command_empty() == False:
                return False
        return True

    def get_total_time(self):
        return max([c.get_crnt_time() for n, c in self.constructs.items()])

    # assumption is that (1) each construct is associated with an 
    # instruction queue (2) each quantum is associated with an instruction
    # TODO
    def run_set_time(self, set_time):
        return True

    def run(self):
        while self.all_command_empty() == False:
            for construct_name, construct in self.constructs.items():
                if not construct.command_empty() and construct.command_ready():
                    construct.run_quantum(self.value_aware)
        print self.get_total_time()
