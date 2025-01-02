from __future__ import annotations
from src.settings import EnigmaRotors, EnigmaReflectors


class EnigmaMachine:
    KEY_BOARD = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self, rotors: list[EnigmaRotor], reflector: EnigmaReflector):
        if len(rotors) < 1:
            raise ValueError('Argument rotors must contain at least one rotor.')

        self.rotors = rotors
        self.reflector = reflector
        self._key_board_set = set(self.KEY_BOARD)

    def forward(self, pin_id: int) -> int:
        print(f'enigma_forward({pin_id=})')

        for i in range(len(self.rotors)):
            pin_id = self.rotors[i].forward(pin_id)
            print(f'enigma_forward(...), rotor_{i}, {pin_id=}')

        pin_id = self.reflector.forward(pin_id)
        print(f'enigma_forward(...), reflector, {pin_id=}')

        for i in range(len(self.rotors) - 1, -1, -1):
            pin_id = self.rotors[i].forward(pin_id, reverse=True)
            print(f'enigma_forward(...), rotor_{i}, REV, {pin_id=}')

        return pin_id

    def encrypt(self, s: str) -> str:
        r: list[str] = []
        for ch in s:
            if ch not in self._key_board_set:
                raise ValueError(f'Simbol {ch=} is not on the Enigma keyboard.')

            pin_id = ord(ch) - ord('A')
            out_pin = self.forward(pin_id)
            out_letter = chr(out_pin + ord('A'))
            r.append(out_letter)

        return ''.join(r)


class Rotor:
    def __init__(self, scramble_cypher: ScrambleCypher):
        self.cypher = scramble_cypher
        self.position = 0
        self.number_of_pins = len(self.cypher.scramble_sequence)

    def forward(self, pin_id: int, reverse: bool = False) -> int:
        if pin_id < 0 or pin_id > self.number_of_pins - 1:
            err_msg = (f'Argument {pin_id=} must be in range '
                       f'(0, {self.number_of_pins - 1}) including both ends.')
            raise ValueError(err_msg)

        print(f'rotor_forward({pin_id=}, {reverse}), {self.position=}')

        if not reverse:
            pin_id = (pin_id + self.position) % self.number_of_pins
        else:
            pin_id = (pin_id - self.position) % self.number_of_pins

        print(f'{pin_id=}')

        if not reverse:
            return (self.cypher.forward(pin_id, reverse) - self.position) % self.number_of_pins
        else:
            return (self.cypher.forward(pin_id, reverse) + self.position) % self.number_of_pins


class EnigmaRotor(Rotor):
    def __init__(self, scramble_cypher: ScrambleCypher26):
        super().__init__(scramble_cypher)

    @classmethod
    def get_enigma_rotor(cls, rotor_id: EnigmaRotors) -> EnigmaRotor:
        return EnigmaRotor(ScrambleCypher26.get_enigma_rotor(rotor_id))


class EnigmaReflector(Rotor):
    def __init__(self, scramble_cypher: ScrambleCypher26):
        super().__init__(scramble_cypher)

    @classmethod
    def get_enigma_reflector(cls, reflector_id: EnigmaReflectors) -> EnigmaReflector:
        return EnigmaReflector(ScrambleCypher26.get_enigma_reflector(reflector_id))


class ScrambleCypher:
    def __init__(self, scramble_sequence: list[int]):
        if self._validate_scramble_sequence(scramble_sequence) is False:
            err_msg = ("Scramble sequence is not valid. "
                       "It must contain unique values from continuous range "
                       "with no gaps.")
            raise ValueError(err_msg)

        self.scramble_sequence = scramble_sequence
        self.reverse_sequence = self._reverse_sequence(scramble_sequence)
        self.upper_bound = len(scramble_sequence) - 1

    def forward(self, input: int, reverse=False) -> int:
        if input < 0 or input > self.upper_bound:
            err_msg = (f"Argument ({input=}) is out of range. "
                       f"Must be in (0, {self.upper_bound}) "
                       "including both ends.")
            raise KeyError(err_msg)

        if reverse is False:
            return self.scramble_sequence[input]
        else:
            return self.reverse_sequence[input]

    def _reverse_sequence(self, scramble_sequence: list[int]) -> list[int]:
        rev_seq = [-1] * len(scramble_sequence)

        for i, n in enumerate(scramble_sequence):
            rev_seq[n] = i

        assert -1 not in rev_seq, 'Reverse sequence is not correct.'

        return rev_seq

    def _validate_scramble_sequence(self, scramble_sequence: list[int]) -> bool:
        s = set(scramble_sequence)

        if len(s) != len(scramble_sequence):
            return False

        for n in scramble_sequence:
            s.remove(n)

        return len(s) == 0


class ScrambleCypher26(ScrambleCypher):
    ALPHABET_LEN = 26

    def __init__(self, scramble_sequence: list[int]):
        if err_len := len(scramble_sequence) != self.ALPHABET_LEN:
            err_msg = (f'The length of scramble_sequence argument ({err_len}) '
                       f'must be {self.ALPHABET_LEN}')
            raise ValueError(err_msg)

        super().__init__(scramble_sequence)

    @classmethod
    def get_enigma_rotor(cls, rotor_id: EnigmaRotors) -> ScrambleCypher26:
        seq = [ord(ch) - ord('A') for ch in rotor_id.value]

        return ScrambleCypher26(seq)

    @classmethod
    def get_enigma_reflector(cls, reflector_id: EnigmaReflectors) -> ScrambleCypher26:
        pairs = reflector_id.value.split()
        seq = [-1] * len(pairs * 2)

        for p in pairs:
            a, b = p[1], p[2]
            seq[ord(a) - ord('A')] = ord(b) - ord('A')
            seq[ord(b) - ord('A')] = ord(a) - ord('A')

        assert -1 not in seq, 'Sequence is not set properly'

        return ScrambleCypher26(seq)


class SubstitutionCypher:
    def __init__(self, alphabet: str, alphabet_encrypted: str):
        if self._validate_alphabet(alphabet, alphabet_encrypted) is False:
            err_msg = ('Alphabet and Encrypted alphabet strings must be the same length '
                       'and consist of same letter set.')
            raise ValueError(err_msg)

        self.encrypt_alphabet: dict[str, str] = dict()
        self.decrypt_alphabet: dict[str, str] = dict()

        for i in range(len(alphabet)):
            self.encrypt_alphabet[alphabet[i]] = alphabet_encrypted[i]
            self.decrypt_alphabet[alphabet_encrypted[i]] = alphabet[i]

    def forward(self, s: str, reverse: bool = False) -> str:
        if err_ch := self._validate_input(s) != '':
            raise ValueError(f'Input contains a char ({err_ch}) that is not in alpabet.')

        r = [' '] * len(s)
        for i, ch in enumerate(s):
            if reverse is False:
                r[i] = self.encrypt_alphabet[ch]
            else:
                r[i] = self.decrypt_alphabet[ch]

        return ''.join(r)

    def _validate_input(self, s: str) -> str:
        for ch in s:
            if ch not in self.encrypt_alphabet:
                return ch

        return ''

    def _validate_alphabet(self, alphabet: str, alphabet_encrypted: str) -> bool:
        return (len(alphabet) == len(alphabet_encrypted)
                and set(alphabet) == set(alphabet_encrypted))
