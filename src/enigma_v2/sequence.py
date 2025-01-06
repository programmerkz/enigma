from __future__ import annotations
from random import randint, seed


class SubstitutionSequence:
    def __init__(self, sequence: list[int]):
        if not self._is_valid_seq(sequence):
            raise ValueError()

        self._sequence = sequence
        self._lenght = len(sequence)

    def substitute(self, i: int) -> int:
        if not isinstance(i, int):
            raise TypeError(f'Argument type {type(i)=} must be int.')

        if i < 0 or i >= self.length:
            err_msg = (f'Argument {i=} must be in range '
                       f'(0, {self.length - 1}) including both ends.')
            raise ValueError(err_msg)

        return self._sequence[i]

    def make_reverse_sequence(self) -> SubstitutionSequence:
        rev = [-1] * self.length

        for i, n in enumerate(self._sequence):
            rev[n] = i

        return SubstitutionSequence(rev)

    @property
    def length(self) -> int:
        return self._lenght

    def _is_valid_seq(self, seq: list[int]) -> bool:
        return len(seq) > 0 and max(seq) == len(seq) - 1 and len(seq) == len(set(seq))


class SubstitutionSequenceBuilder:
    MAX_SEQ_LEN = 10**3
    ENG_26_CAP_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    @classmethod
    def make_random_sequence(cls, seq_len: int) -> SubstitutionSequence:
        if seq_len < 1 or seq_len > cls.MAX_SEQ_LEN:
            raise ValueError(f'Argument {seq_len=} must be in range(1, {cls.MAX_SEQ_LEN})')

        seq = [i for i in range(seq_len)]
        cls._shuffle(seq)

        return SubstitutionSequence(seq)

    @classmethod
    def make_sequence_by_alphabet(cls, alphabet: str, scrambled: str) -> SubstitutionSequence:
        if len(alphabet) != len(scrambled) or set(alphabet) != set(scrambled):
            raise ValueError('Argument scrambled must be a permutation of the alphabet argument.')

        d = {ch: i for i, ch in enumerate(alphabet)}
        seq = [d[ch] for ch in scrambled]

        return SubstitutionSequence(seq)

    @classmethod
    def make_sequence_by_26_eng_cap_letters(cls, scrambled: str) -> SubstitutionSequence:
        if len(scrambled) != 26 or set(scrambled) != set(cls.ENG_26_CAP_LETTERS):
            raise ValueError('Argument scrambled must be a permutation of 26 english capital letters.')

        return cls.make_sequence_by_alphabet(cls.ENG_26_CAP_LETTERS, scrambled)

    @classmethod
    def _shuffle(cls, seq: list[int], times: int | None = None, seed_id: int | None = None) -> None:
        n = len(seq)

        if seed_id is not None:
            seed(seed_id)

        if times is None:
            times = n * 7

        for _ in range(times):
            i = randint(0, n - 1)
            j = randint(0, n - 1)
            seq[i], seq[j] = seq[j], seq[i]
