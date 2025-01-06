from src.enigma_v2.sequence import SubstitutionSequence


class SubstitutionCypher:
    def __init__(self, seq: SubstitutionSequence):
        self._subtitution = seq
        self._subtitution_rev = seq.make_reverse_sequence()

    def encrypt(self, pin) -> int:
        return self._subtitution.substitute(pin)

    def decrypt(self, pin) -> int:
        return self._subtitution_rev.substitute(pin)

    @property
    def length(self) -> int:
        return self._subtitution.length
