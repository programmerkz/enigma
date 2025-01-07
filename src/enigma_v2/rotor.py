from src.enigma_v2.cypher import SubstitutionCypher


class Rotor:
    def __init__(self, cypher: SubstitutionCypher, ring_offset: int = 0, position: int = 0):
        if ring_offset < 0 or ring_offset >= cypher.length:
            err_msg = (f'Argument {ring_offset=} must be in range '
                       f'(0, {cypher.length - 1}) including both ends.')
            raise ValueError(err_msg)

        if position < 0 or position >= cypher.length:
            err_msg = (f'Argument {position=} must be in range '
                       f'(0, {cypher.length - 1}) including both ends.')
            raise ValueError(err_msg)

        self._cypher = cypher
        self._ring_offset = ring_offset
        self._position = position

    def forward(self, pin: int) -> int:
        pin = (pin + self._position + self._ring_offset) % self.number_of_pins
        pin = self._cypher.encrypt(pin)
        pin = (pin - self._position - self._ring_offset) % self.number_of_pins

        return pin

    def backward(self, pin: int) -> int:
        pin = (pin + self._position + self._ring_offset) % self.number_of_pins
        pin = self._cypher.decrypt(pin)
        pin = (pin - self._position - self._ring_offset) % self.number_of_pins

        return pin

    @property
    def number_of_pins(self) -> int:
        return self._cypher.length
