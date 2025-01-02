from src.rotor import ScrambleCypher
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
