from __future__ import annotations
from src.settings import EnigmaRotors


class Rotor:
    def __init__(self, scramble_cypher: ScrambleCypher26):
        self.cypher = scramble_cypher
        self.position = 0

    def forward(self, pin_id: int, reverse: bool = False) -> int:
        if pin_id < 0 or pin_id > 25:
            raise ValueError(f'Argument {pin_id=} must be in range (0, 25) including both ends.')

        input = (pin_id + self.position) % 26
        return self.cypher.forward(input)

    def get_enigma_rotor(self, rotor_id: EnigmaRotors) -> Rotor:
        return Rotor(ScrambleCypher26.get_enigma_rotor(rotor_id))


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
