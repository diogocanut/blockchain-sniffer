from opcodes import *

class Parser(object):
    def get_script(self, script):
        op_code = []
        for x in range(0,len(script)-1):
            if script[x:x+2] in OPCODES.keys():
                op_code.append(OPCODES[script[x:x+2]])
        # TODO: move to db
        print("Transaction opcodes: {0}".format(op_code))