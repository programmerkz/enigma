from itertools import permutations
from pytest import fixture, mark, raises
from src.enigma_v2.cypher import SubstitutionCypher
from src.enigma_v2.sequence import SubstitutionSequence


class TestCypher:
    @mark.parametrize('pin_id', [-7, -1, 4, 10**6])
    def test_invalid_pin(self, cypher_3210: SubstitutionCypher, pin_id):
        with raises(ValueError):
            cypher_3210.forward(pin_id)

    @mark.parametrize('pin_id', [7.1, '7', 'abc', '', 3.0])
    def test_invalid_pin_type(self, cypher_3210: SubstitutionCypher, pin_id):
        with raises(TypeError):
            cypher_3210.forward(pin_id)

    def test_forward_1(self, cypher_3210: SubstitutionCypher):
        input = [0, 0, 1, 1, 2, 2, 3, 3]
        target = [3, 3, 2, 2, 1, 1, 0, 0]

        assert [cypher_3210.forward(i) for i in input] == target

    def test_forward_2(self, cypher_3210: SubstitutionCypher):
        input = [1, 0, 2, 2, 2, 3, 1]
        target = [2, 3, 1, 1, 1, 0, 2]

        assert [cypher_3210.forward(i) for i in input] == target

    @mark.parametrize('cypher_seq_len', [1, 3, 7])
    def test_enc_dec(self, cypher_seq_len):
        for p in permutations(range(cypher_seq_len)):
            cypher = SubstitutionCypher(SubstitutionSequence(list(p)))
            for i in range(cypher_seq_len):
                enc = cypher.forward(i)
                dec = cypher.backward(enc)
                assert dec == i

    @fixture
    def cypher_3210(self):
        seq = [3, 2, 1, 0]
        sub_seq = SubstitutionSequence(seq)
        return SubstitutionCypher(sub_seq)
