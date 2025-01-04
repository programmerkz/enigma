from src.enigma_v2.sequence import SubstitutionSequence


class SubstitutionCypher:
    def __init__(self, seq: SubstitutionSequence):
        self.subtitution = seq
        self.subtitution_rev = seq.make_reverse_sequence()

    def forward(self, pin) -> int:
        return self.subtitution.seq[self._validate_pin(pin)]

    def backward(self, pin) -> int:
        return self.subtitution_rev.seq[self._validate_pin(pin)]

    def _validate_pin(self, pin: int) -> int:
        if not isinstance(pin, int):
            raise TypeError(f'Argument type {type(pin)=} must be int.')

        if pin < 0 or pin >= self.subtitution.seq_len:
            err_msg = (f'Argument {pin=} must be in range (0, {self.subtitution.seq_len - 1})'
                       'including both ends.')
            raise ValueError(err_msg)

        return pin
