from pytest import raises
from src.enigma_v2.sequence import SubstitutionSequence, SubstitutionSequenceBuilder


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


class TestSequenceBuilder:
    def test_empty(self):
        with raises(ValueError):
            SubstitutionSequenceBuilder.make_random_sequence(0)

    def test_seq_too_long(self):
        with raises(ValueError):
            seq_len = SubstitutionSequenceBuilder.MAX_SEQ_LEN + 1
            SubstitutionSequenceBuilder.make_random_sequence(seq_len)

    def test_min_seq_len(self):
        seq_len = 1
        ss = SubstitutionSequenceBuilder.make_random_sequence(seq_len)

        assert ss.seq_len == seq_len

    def test_max_seq_len(self):
        seq_len = SubstitutionSequenceBuilder.MAX_SEQ_LEN
        ss = SubstitutionSequenceBuilder.make_random_sequence(seq_len)

        assert ss.seq_len == seq_len

    def test_make_by_alphabet_abc(self):
        alpha = 'abc'
        scrambled = 'bac'

        ss = SubstitutionSequenceBuilder.make_sequence_by_alphabet(alpha, scrambled)

        assert ss.seq == [1, 0, 2]

    def test_make_by_alphabet_abc_123(self):
        alpha = 'abc123'
        scrambled = 'b1a2c3'

        ss = SubstitutionSequenceBuilder.make_sequence_by_alphabet(alpha, scrambled)

        assert ss.seq == [1, 3, 0, 4, 2, 5]

    def test_make_by_alphabet_diff_len(self):
        alpha = 'abc'
        scrambled = 'ba'

        with raises(ValueError):
            SubstitutionSequenceBuilder.make_sequence_by_alphabet(alpha, scrambled)

    def test_make_by_alphabet_diff_abc(self):
        alpha = 'abc'
        scrambled = 'cbe'

        with raises(ValueError):
            SubstitutionSequenceBuilder.make_sequence_by_alphabet(alpha, scrambled)

    def test_make_by_26_eng_cap_letters(self):
        scrambled = 'ZLCXPWOYDFKAHIUSNMBQTVGRJE'
        seq = [25, 11, 2, 23, 15, 22, 14, 24, 3, 5, 10, 0, 7, 8, 20, 18, 13, 12, 1, 16, 19, 21, 6, 17, 9, 4]

        ss = SubstitutionSequenceBuilder.make_sequence_by_26_eng_cap_letters(scrambled)

        assert ss.seq == seq

    def test_make_by_26_eng_cap_letters_gaps(self):
        scrambled = 'ZLCXPWOYDFKAHIUSNMBQTV_RJE'

        with raises(ValueError):
            SubstitutionSequenceBuilder.make_sequence_by_26_eng_cap_letters(scrambled)

    def test_make_by_26_eng_cap_letters_dubs(self):
        scrambled = 'ZZCXPWOYDFKAHIUSNMBQTVGRJE'

        with raises(ValueError):
            SubstitutionSequenceBuilder.make_sequence_by_26_eng_cap_letters(scrambled)
