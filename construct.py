from heapq import *

class Construct(object):
    """
        Construct Primitive
    """

    def __init__(self, name):
        self.cid = name
    
        self.input_list = {} # each input is a priority queue
        self.output_list = {} # output is just names of output constructs

        self.command = []

        self.crnt_time = 0.0

        # commands are not explicitly defined as a class, because definition 
        # of command needs to access some components of construct, which becomes
        # complex without concepts like "friend'
        self.quantum_time = {}
        self.function = {}
        self.inputs = {}
        self.outputs = {}
        self.arguments = {}

    def get_cid(self):
        return self.cid

    # entries of the input_list will be a heap
    def add_input(self, cid):
        self.input_list[cid] = []

    def add_output(self, construct):
        self.output_list[construct.get_cid()] = construct

    # to be used to implement functions for commands
    def pop_input(self, input_name):
        return heappop(self.input_list[input_name])[1]
    
    def push_output(self, output_name, value):
        heappush(self.output_list[output_name].input_list[self.get_cid()], 
                 (self.crnt_time, value))

    def get_input_list(self):
        return input_list.keys()

    def get_output_list(self):
        return output_list

    # inputs are when a command is dependent on other constructs
    # outputs are when result of the command will be sent to other constructs
    # arguments are when a command needs some values that are not from other inputs
    #   and this will be saved with the command
    # ex. load 'pe' 0x400 --> inputs will be False, 
    #                         outputs will be True,
    #                         arguments will be True
    #                     --> commands will be saved as it is and  will be parsed 
    #                         when quantum is run... (this I think will give more 
    #                         freedom to the compiler and whatever...)
    def set_command(self, op_name, quantum_time, function, inputs, outputs, arguments):
        self.quantum_time[op_name] = quantum_time
        self.function[op_name] = function
        self.inputs[op_name] = inputs
        self.outputs[op_name] = outputs
        self.arguments[op_name] = arguments

    # utility for parsing commands
    def parse_command(self, command):
        symbol_list = command.split()
        op = symbol_list[0]
        arg_list = symbol_list[1:]
        inputs = [arg_list[index] for index in self.inputs[op]]
        outputs = [arg_list[index] for index in self.outputs[op]]
        # NOTE assume arguments are all hexadecimal integers
        arguments = [int(arg_list[index], 0) for index in self.arguments[op]]

        return op, inputs, outputs, arguments

    # commands will be registered by the users
    # other means of detecting dependency or hazard for exact cycle 
    # measurements can be done by users
    def run_command(self, op, inputs, outputs, arguments):
        if len(inputs) != 0:
            # if there are inputs
            self.crnt_time = max([self.crnt_time] + 
                                 [self.input_list[input_name][0][0] 
                                  for input_name in inputs])
            self.crnt_time = self.crnt_time + self.quantum_time[op]
        else:
            # if there are no inputs
            self.crnt_time = self.crnt_time + self.quantum_time[op]
        self.function[op](inputs, outputs, arguments)
    
    # this could be dependent on the type of construct and the input value
    def get_quantum_time(self):
        return self.quantum_time[self.command.pop(0)]

    # this could be dependent on the type of construct and the input value
    # runs the first command
    def run_quantum(self):
        op, inputs, outputs, arguments = self.parse_command(self.command.pop(0))
        self.run_command(op, inputs, outputs, arguments)
