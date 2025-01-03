from __future__ import annotations


class SubstitutionSequence:
    def __init__(self, seq: list[int]):
        if not self._is_valid_seq(seq):
            raise ValueError()

        self.seq = seq
        self.seq_len = len(seq)

    def make_reverse_sequence(self) -> SubstitutionSequence:
        rev = [-1] * self.seq_len

        for i, n in enumerate(self.seq):
            rev[n] = i

        return SubstitutionSequence(rev)

    def _is_valid_seq(self, seq: list[int]) -> bool:
        return len(seq) > 0 and max(seq) == len(seq) - 1 and len(seq) == len(set(seq))
