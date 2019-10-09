from opcodes import *

class Parser(object):
    def get_script(self, script):
        op_code = []
        x = 0
        print("SCRIPT: {0}".format(script))
        while(x < len(script) - 1):
            op = script[x:x+2]
            op_int = int(op, 16)
            if op_int == 0:
                x = x + 1
                print("OP ZERO")
                op_code.append(OPCODES['00'])
            elif op_int > 1 and op_int < 75:
                to_push_data = script[x:x + op_int]
                print("OP INT: {0}".format(op_int))
                print("TO PUSH DATA: {0}".format(to_push_data))
                op_code.append("DATA: {0}".format(to_push_data))
                x = x + op_int
            elif script[x:x+2] in OPCODES.keys():
                op_code.append(OPCODES[op])
                x = x + 2
            else:
                x = x + 2
                print("OP INT: {0}".format(op_int))
        print("Transaction opcodes: {0}".format(op_code))