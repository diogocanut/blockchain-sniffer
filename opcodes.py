OPCODES = {
    # push value
    "00": "OP_0",
    "OP_0": "OP_FALSE",
    "4c": "OP_PUSHDATA1",
    "4d": "OP_PUSHDATA2",
    "4e": "OP_PUSHDATA4",
    "4f": "OP_1NEGATE",
    "50": "OP_RESERVED",
    "51": "OP_1",
    "OP_1": "OP_TRUE",
    "52": "OP_2",
    "53": "OP_3",
    "54": "OP_4",
    "55": "OP_5",
    "56": "OP_6",
    "57": "OP_7",
    "58": "OP_8",
    "59": "OP_9",
    "5a": "OP_10",
    "5b": "OP_11",
    "5c": "OP_12",
    "5d": "OP_13",
    "5e": "OP_14",
    "5f": "OP_15",
    "60": "OP_16",

    # op control
    "61": "OP_NOP",
    "62": "OP_VER",
    "63": "OP_IF",
    "64": "OP_NOTIF",
    "65": "OP_VERIF",
    "66": "OP_VERNOTIF",
    "67": "OP_ELSE",
    "68": "OP_ENDIF",
    "69": "OP_VERIFY",
    "6a": "OP_RETURN",

    # stack ops
    "6b": "OP_TOALTSTACK",
    "6c": "OP_FROMALTSTACK",
    "6d": "OP_2DROP",
    "6e": "OP_2DUP",
    "6f": "OP_3DUP",
    "70": "OP_2OVER",
    "71": "OP_2ROT",
    "72": "OP_2SWAP",
    "73": "OP_IFDUP",
    "74": "OP_DEPTH",
    "75": "OP_DROP",
    "76": "OP_DUP",
    "77": "OP_NIP",
    "78": "OP_OVER",
    "79": "OP_PICK",
    "7a": "OP_ROLL",
    "7b": "OP_ROT",
    "7c": "OP_SWAP",
    "7d": "OP_TUCK",

    # splice ops
    "7e": "OP_CAT",
    "7f": "OP_SUBSTR",
    "80": "OP_LEFT",
    "81": "OP_RIGHT",
    "82": "OP_SIZE",

    # bit logic
    "83": "OP_INVERT",
    "84": "OP_AND",
    "85": "OP_OR",
    "86": "OP_XOR",
    "87": "OP_EQUAL",
    "88": "OP_EQUALVERIFY",
    "89": "OP_RESERVED1",
    "8a": "OP_RESERVED2",

    # numeric
    "8b": "OP_1ADD",
    "8c": "OP_1SUB",
    "8d": "OP_2MUL",
    "8e": "OP_2DIV",
    "8f": "OP_NEGATE",
    "90": "OP_ABS",
    "91": "OP_NOT",
    "92": "OP_0NOTEQUAL",
    "93": "OP_ADD",
    "94": "OP_SUB",
    "95": "OP_MUL",
    "96": "OP_DIV",
    "97": "OP_MOD",
    "98": "OP_LSHIFT",
    "99": "OP_RSHIFT",
    "9a": "OP_BOOLAND",
    "9b": "OP_BOOLOR",
    "9c": "OP_NUMEQUAL",
    "9d": "OP_NUMEQUALVERIFY",
    "9e": "OP_NUMNOTEQUAL",
    "9f": "OP_LESSTHAN",
    "a0": "OP_GREATERTHAN",
    "a1": "OP_LESSTHANOREQUAL",
    "a2": "OP_GREATERTHANOREQUAL",
    "a3": "OP_MIN",
    "a4": "OP_MAX",
    "a5": "OP_WITHIN",
    "a6": "OP_RIPEMD160",
    "a7": "OP_SHA1",
    "a8": "OP_SHA256",
    "a9": "OP_HASH160",
    "aa": "OP_HASH256",
    "ab": "OP_CODESEPARATOR",
    "ac": "OP_CHECKSIG",
    "ad": "OP_CHECKSIGVERIFY",
    "ae": "OP_CHECKMULTISIG",
    "af": "OP_CHECKMULTISIGVERIFY",
    "b0": "OP_NOP1",
    "b1": "OP_CHECKLOCKTIMEVERIFY",
    "b2": "OP_CHECKSEQUENCEVERIFY",
    "b3": "OP_NOP4",
    "b4": "OP_NOP5",
    "b5": "OP_NOP6",
    "b6": "OP_NOP7",
    "b7": "OP_NOP8",
    "b8": "OP_NOP9",
    "b9": "OP_NOP10",

    # template matching params
    "fa": "OP_SMALLINTEGER",
    "fb": "OP_PUBKEYS",
    "fc": "OP_PUBKEYHASH",
    "fe": "OP_PUBKEY",
    "ff": "OP_INVALIDOPCODE",
}

"""
# control
OP_NOP = CScriptOp(0x61)
OP_VER = CScriptOp(0x62)
OP_IF = CScriptOp(0x63)
OP_NOTIF = CScriptOp(0x64)
OP_VERIF = CScriptOp(0x65)
OP_VERNOTIF = CScriptOp(0x66)
OP_ELSE = CScriptOp(0x67)
OP_ENDIF = CScriptOp(0x68)
OP_VERIFY = CScriptOp(0x69)
OP_RETURN = CScriptOp(0x6a)

# stack ops
OP_TOALTSTACK = CScriptOp(0x6b)
OP_FROMALTSTACK = CScriptOp(0x6c)
OP_2DROP = CScriptOp(0x6d)
OP_2DUP = CScriptOp(0x6e)
OP_3DUP = CScriptOp(0x6f)
OP_2OVER = CScriptOp(0x70)
OP_2ROT = CScriptOp(0x71)
OP_2SWAP = CScriptOp(0x72)
OP_IFDUP = CScriptOp(0x73)
OP_DEPTH = CScriptOp(0x74)
OP_DROP = CScriptOp(0x75)
OP_DUP = CScriptOp(0x76)
OP_NIP = CScriptOp(0x77)
OP_OVER = CScriptOp(0x78)
OP_PICK = CScriptOp(0x79)
OP_ROLL = CScriptOp(0x7a)
OP_ROT = CScriptOp(0x7b)
OP_SWAP = CScriptOp(0x7c)
OP_TUCK = CScriptOp(0x7d)

# splice ops
OP_CAT = CScriptOp(0x7e)
OP_SUBSTR = CScriptOp(0x7f)
OP_LEFT = CScriptOp(0x80)
OP_RIGHT = CScriptOp(0x81)
OP_SIZE = CScriptOp(0x82)

# bit logic
OP_INVERT = CScriptOp(0x83)
OP_AND = CScriptOp(0x84)
OP_OR = CScriptOp(0x85)
OP_XOR = CScriptOp(0x86)
OP_EQUAL = CScriptOp(0x87)
OP_EQUALVERIFY = CScriptOp(0x88)
OP_RESERVED1 = CScriptOp(0x89)
OP_RESERVED2 = CScriptOp(0x8a)

# numeric
OP_1ADD = CScriptOp(0x8b)
OP_1SUB = CScriptOp(0x8c)
OP_2MUL = CScriptOp(0x8d)
OP_2DIV = CScriptOp(0x8e)
OP_NEGATE = CScriptOp(0x8f)
OP_ABS = CScriptOp(0x90)
OP_NOT = CScriptOp(0x91)
OP_0NOTEQUAL = CScriptOp(0x92)

OP_ADD = CScriptOp(0x93)
OP_SUB = CScriptOp(0x94)
OP_MUL = CScriptOp(0x95)
OP_DIV = CScriptOp(0x96)
OP_MOD = CScriptOp(0x97)
OP_LSHIFT = CScriptOp(0x98)
OP_RSHIFT = CScriptOp(0x99)

OP_BOOLAND = CScriptOp(0x9a)
OP_BOOLOR = CScriptOp(0x9b)
OP_NUMEQUAL = CScriptOp(0x9c)
OP_NUMEQUALVERIFY = CScriptOp(0x9d)
OP_NUMNOTEQUAL = CScriptOp(0x9e)
OP_LESSTHAN = CScriptOp(0x9f)
OP_GREATERTHAN = CScriptOp(0xa0)
OP_LESSTHANOREQUAL = CScriptOp(0xa1)
OP_GREATERTHANOREQUAL = CScriptOp(0xa2)
OP_MIN = CScriptOp(0xa3)
OP_MAX = CScriptOp(0xa4)

OP_WITHIN = CScriptOp(0xa5)

# crypto
OP_RIPEMD160 = CScriptOp(0xa6)
OP_SHA1 = CScriptOp(0xa7)
OP_SHA256 = CScriptOp(0xa8)
OP_HASH160 = CScriptOp(0xa9)
OP_HASH256 = CScriptOp(0xaa)
OP_CODESEPARATOR = CScriptOp(0xab)
OP_CHECKSIG = CScriptOp(0xac)
OP_CHECKSIGVERIFY = CScriptOp(0xad)
OP_CHECKMULTISIG = CScriptOp(0xae)
OP_CHECKMULTISIGVERIFY = CScriptOp(0xaf)

# expansion
OP_NOP1 = CScriptOp(0xb0)
OP_CHECKLOCKTIMEVERIFY = CScriptOp(0xb1)
OP_CHECKSEQUENCEVERIFY = CScriptOp(0xb2)
OP_NOP4 = CScriptOp(0xb3)
OP_NOP5 = CScriptOp(0xb4)
OP_NOP6 = CScriptOp(0xb5)
OP_NOP7 = CScriptOp(0xb6)
OP_NOP8 = CScriptOp(0xb7)
OP_NOP9 = CScriptOp(0xb8)
OP_NOP10 = CScriptOp(0xb9)

# template matching params
OP_SMALLINTEGER = CScriptOp(0xfa)
OP_PUBKEYS = CScriptOp(0xfb)
OP_PUBKEYHASH = CScriptOp(0xfd)
OP_PUBKEY = CScriptOp(0xfe)

OP_INVALIDOPCODE = CScriptOp(0xff)
"""
