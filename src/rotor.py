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
