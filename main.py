from src.rotor import (EnigmaMachine, EnigmaReflector, EnigmaRotor,
                       ScrambleCypher, ScrambleCypher26, SubstitutionCypher)
from src.settings import EnigmaRotors, EnigmaReflectors
from src.tools import shuffle_list


# example 1
scramble_sequence = [i for i in range(9, -1, -1)]
cyph = ScrambleCypher(scramble_sequence)

input = '74898400121004587693'
enc = ''.join(str(cyph.forward(int(ch))) for ch in input)
dec = ''.join(str(cyph.forward(int(ch), reverse=True)) for ch in enc)

assert dec == input, 'Decrypted string is not equal to input'
print(input, enc, dec, sep='\n', end='\n\n')


# example 2
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 !@#$%^&*()_+-=,.'
d: dict[str, int] = {ch: idx for idx, ch in enumerate(alphabet)}
d_rev: dict[int, str] = {idx: ch for idx, ch in enumerate(alphabet)}
scramble_sequence = shuffle_list([i for i in range(len(alphabet))])
cyph = ScrambleCypher(scramble_sequence)

input = alphabet
enc = ''.join(d_rev[cyph.forward(d[ch])] for ch in input)
dec = ''.join(d_rev[cyph.forward(d[ch], reverse=True)] for ch in enc)

assert dec == input, 'Decrypted string is not equal to input'
print(input, enc, dec, sep='\n', end='\n\n')


# example 3
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 !@#$%^&*()_+-=,.'
alphabet_encrypted = ''.join(shuffle_list(list(alphabet)))

cyph_2 = SubstitutionCypher(alphabet, alphabet_encrypted)

input = alphabet
enc = cyph_2.forward(input)
dec = cyph_2.forward(enc, reverse=True)

assert dec == input, 'Decrypted string is not equal to input'
print(input, enc, dec, sep='\n', end='\n\n')


# example 4
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
cyph_3 = ScrambleCypher26.get_enigma_rotor(EnigmaRotors.ROTOR_I)

input = alphabet
enc = ''.join(chr(ord('A') + cyph_3.forward(ord(ch) - ord('A'))) for ch in input)
dec = ''.join(chr(ord('A') + cyph_3.forward(ord(ch) - ord('A'), reverse=True)) for ch in enc)

assert dec == input, 'Decrypted string is not equal to input'
print(input, enc, dec, sep='\n', end='\n\n')


# example 5
rotors: list[EnigmaRotor] = []
rotors.append(EnigmaRotor.get_enigma_rotor(EnigmaRotors.ROTOR_I))
# rotors.append(EnigmaRotor.get_enigma_rotor(EnigmaRotors.ROTOR_II))
# rotors.append(EnigmaRotor.get_enigma_rotor(EnigmaRotors.ROTOR_III))
reflector = EnigmaReflector.get_enigma_reflector(EnigmaReflectors.REFLECTOR_B)

enigma = EnigmaMachine(rotors, reflector)
enigma.rotors[0].position = 1

input = 'C'#enigma.KEY_BOARD
enc = enigma.encrypt(input)
dec = enigma.encrypt(enc)

# assert dec == input, 'Decrypted string is not equal to input'
print(input, enc, dec, sep='\n', end='\n\n')
