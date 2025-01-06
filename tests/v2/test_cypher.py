from itertools import permutations
from pytest import fixture, mark, raises
from src.enigma_v2.cypher import SubstitutionCypher
from src.enigma_v2.sequence import SubstitutionSequence


class TestCypher:
    @mark.parametrize('pin_id', [-7, -1, 4, 10**6])
    def test_invalid_pin(self, cypher_3210: SubstitutionCypher, pin_id):
        with raises(ValueError):
            cypher_3210.encrypt(pin_id)

    @mark.parametrize('pin_id', [7.1, '7', 'abc', '', 3.0])
    def test_invalid_pin_type(self, cypher_3210: SubstitutionCypher, pin_id):
        with raises(TypeError):
            cypher_3210.encrypt(pin_id)

    @mark.parametrize(
            'input,target',
            [
                ([0, 0, 1, 1, 2, 2, 3, 3], [3, 3, 2, 2, 1, 1, 0, 0]),
                ([1, 0, 2, 2, 2, 3, 1], [2, 3, 1, 1, 1, 0, 2])
            ])
    def test_forward(self, input, target, cypher_3210: SubstitutionCypher):
        input = [0, 0, 1, 1, 2, 2, 3, 3]
        target = [3, 3, 2, 2, 1, 1, 0, 0]

        assert [cypher_3210.encrypt(i) for i in input] == target

    @mark.parametrize('cypher_length', [1, 3, 7])
    def test_encrypt_decrypt(self, cypher_length):
        for p in permutations(range(cypher_length)):
            cypher = SubstitutionCypher(SubstitutionSequence(list(p)))
            for i in range(cypher_length):
                enc = cypher.encrypt(i)
                dec = cypher.decrypt(enc)
                assert dec == i

    @fixture
    def cypher_3210(self):
        seq = [3, 2, 1, 0]
        sub_seq = SubstitutionSequence(seq)
        return SubstitutionCypher(sub_seq)
