from src.rotor import ScrambleCypher


# example 1
scramble_sequence = [i for i in range(9, -1, -1)]
cyph = ScrambleCypher(scramble_sequence)

input = '74898400121004587693'
enc = ''.join(str(cyph.forward(int(ch))) for ch in input)
dec = ''.join(str(cyph.forward(int(ch), reverse=True)) for ch in enc)

assert dec == input, 'Decrypted string is not equal to input'
print(input, enc, dec, sep='\n', end='\n\n')
