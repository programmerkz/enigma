from enum import Enum


ROTOR_I = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'
ROTOR_II = 'AJDKSIRUXBLHWTMCQGZNPYFVOE'
ROTOR_III = 'BDFHJLCPRTXVZNYEIWGAKMUSQO'
ROTOR_IV = 'ESOVPZJAYQUIRHXLNFTGKDCMWB'
ROTOR_V = 'VZBRGITYUPSDNHLXAWMJQOFECK'
ROTOR_VI = 'JPGVOUMFYQBENHZRDKASXLICTW'
ROTOR_VII = 'NZJHGRCXMYSWBOUFAIVLPEKQDT'
ROTOR_VIII = 'FKQHTLXOCBJSPDZRAMEWNIUYGV'
ROTOR_BETTA = 'LEYJVCNIXWPBQMDRTAKZGFUHOS'
ROTOR_GAMMA = 'FSOKANUERHMBTIYCWLQPZXVGJD'

REFLECTOR_B = '(AY) (BR) (CU) (DH) (EQ) (FS) (GL) (IP) (JX) (KN) (MO) (TZ) (VW)'
REFLECTOR_C = '(AF) (BV) (CP) (DJ) (EI) (GO) (HY) (KR) (LZ) (MX) (NW) (TQ) (SU)'
REFLECTOR_B_DUNN = '(AE) (BN) (CK) (DQ) (FU) (GY) (HW) (IJ) (LO) (MP) (RX) (SZ) (TV)'
REFLECTOR_C_DUNN = '(AR) (BD) (CO) (EJ) (FN) (GT) (HK) (IV) (LM) (PW) (QZ) (SX) (UY)'


class EnigmaRotors(Enum):
    ROTOR_I = ROTOR_I
    ROTOR_II = ROTOR_II
    ROTOR_III = ROTOR_III
    ROTOR_IV = ROTOR_IV
    ROTOR_V = ROTOR_V
    ROTOR_VI = ROTOR_VI
    ROTOR_VII = ROTOR_VII
    ROTOR_VIII = ROTOR_VIII
    ROTOR_BETTA = ROTOR_BETTA
    ROTOR_GAMMA = ROTOR_GAMMA


class EnigmaReflectors(Enum):
    REFLECTOR_B = REFLECTOR_B
    REFLECTOR_C = REFLECTOR_C
    REFLECTOR_B_DUNN = REFLECTOR_B_DUNN
    REFLECTOR_C_DUNN = REFLECTOR_C_DUNN
