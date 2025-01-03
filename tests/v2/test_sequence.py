from pytest import raises
from src.enigma_v2.sequence import SubstitutionSequence


class TestSequence:
    def test_empty(self):
        with raises(ValueError):
            SubstitutionSequence([])

    def test_gaps_1(self):
        with raises(ValueError):
            SubstitutionSequence([1, 2])

    def test_gaps_2(self):
        with raises(ValueError):
            SubstitutionSequence([0, 3])

    def test_gaps_3(self):
        with raises(ValueError):
            seq = [i for i in range(10**3)]
            seq[-1] = 10**3 + 1
            SubstitutionSequence(seq)

    def test_dubs(self):
        with raises(ValueError):
            seq = [0, 1, 1, 3]
            SubstitutionSequence(seq)

    def test_dubs_2(self):
        with raises(ValueError):
            seq = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9]
            SubstitutionSequence(seq)

    def test_init(self):
        seq = [i for i in range(9, -1, -1)]
        ss = SubstitutionSequence(seq)
        assert ss.seq == seq

    def test_init_2(self):
        seq = [i for i in range(10**3, -1, -1)]
        ss = SubstitutionSequence(seq)
        assert ss.seq == seq

    def test_reverse(self):
        seq = [1, 0, 3, 4, 2]
        rev = [1, 0, 4, 2, 3]

        ss = SubstitutionSequence(seq)
        ss_rev = ss.make_reverse_sequence()

        assert ss_rev.seq == rev

    def test_reverse_complex(self):
        seq = [1, 0, 3, 4, 2, 6, 5]

        ss = SubstitutionSequence(seq)
        ss_rev = ss.make_reverse_sequence()

        input = [i for i in range(len(seq))]
        enc = [seq[i] for i in input]
        dec = [ss_rev.seq[i] for i in enc]

        assert input == dec
