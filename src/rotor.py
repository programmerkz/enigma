class Rotor:
    def __init__(self, substitution_cipher: list[int]):
        pass


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
