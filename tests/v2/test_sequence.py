from pytest import mark, raises
from src.enigma_v2.sequence import SubstitutionSequence, SubstitutionSequenceBuilder


class TestSequence:
    def test_empty(self):
        with raises(ValueError):
            SubstitutionSequence([])

    @mark.parametrize(
            'sequence',
            [
                [1, 2, 3, 4],
                [0, 3, 5, 4, 2],
                [3, 2, 1],
                [2, 0],
                [i for i in range(10**3)] + [10**3 + 3],
            ])
    def test_gaps(self, sequence):
        with raises(ValueError):
            SubstitutionSequence(sequence)

    @mark.parametrize(
            'sequence',
            [
                [0, 1, 1, 3],
                [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9],
                [3, 2, 1, 0, 0],
                [1, 2, 0, 1],
                [i for i in range(10**3)] + [10**3 - 1],
            ])
    def test_dubs(self, sequence):
        with raises(ValueError):
            SubstitutionSequence(sequence)

    @mark.parametrize(
            'sequence,length',
            [
                ([0], 1),
                ([3, 1, 2, 0], 4),
                ([i for i in range(10**3)], 10**3),
            ])
    def test_length(self, sequence, length):
        ss = SubstitutionSequence(sequence)
        assert ss.length == length

    @mark.parametrize(
            'sequence',
            [
                [0, 1, 3, 2],
                [0, 2, 1, 3, 5, 4, 6, 9, 8, 7],
                [3, 2, 1, 0, 4],
                [1, 2, 0, 3],
                [i for i in range(10**3)],
            ])
    def test_substitute(self, sequence):
        ss = SubstitutionSequence(sequence)

        for i in range(ss.length):
            assert ss.substitute(i) == sequence[i]

    @mark.parametrize(
            'sequence,sequence_reversed',
            [
                ([1, 0, 3, 4, 2], [1, 0, 4, 2, 3]),
                ([1, 0, 3, 7, 8, 2, 6, 5, 4], [1, 0, 5, 2, 8, 7, 6, 3, 4]),
            ])
    def test_reverse(self, sequence, sequence_reversed):
        ss = SubstitutionSequence(sequence)
        ss_rev = ss.make_reverse_sequence()

        for i in range(ss.length):
            assert ss_rev.substitute(i) == sequence_reversed[i]

    @mark.parametrize(
            'sequence',
            [
                [0, 1, 3, 2],
                [0, 2, 1, 3, 5, 4, 6, 9, 8, 7],
                [3, 2, 1, 0, 4],
                [1, 2, 0, 3],
                [i for i in range(10**3)],
            ])
    def test_reverse_complex(self, sequence):
        ss = SubstitutionSequence(sequence)
        ss_rev = ss.make_reverse_sequence()

        input = [i for i in range(ss.length)]
        enc = [ss.substitute(i) for i in input]
        dec = [ss_rev.substitute(i) for i in enc]

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

        assert ss.length == seq_len

    def test_max_seq_len(self):
        seq_len = SubstitutionSequenceBuilder.MAX_SEQ_LEN
        ss = SubstitutionSequenceBuilder.make_random_sequence(seq_len)

        assert ss.length == seq_len

    @mark.parametrize(
            'alpha,scrambled',
            [
                ('abc', 'bac'),
                ('abc123', 'b2a1c3'),
                ('abc_123+@#$', 'b@2#a_1+c3$'),
            ])
    def test_make_by_alphabet(self, alpha, scrambled):
        d = {ch: i for i, ch in enumerate(alpha)}
        seq = [d[ch] for ch in scrambled]

        ss = SubstitutionSequenceBuilder.make_sequence_by_alphabet(alpha, scrambled)

        for i in range(ss.length):
            assert ss.substitute(i) == seq[i]

    @mark.parametrize(
            'alpha,scrambled',
            [
                ('abc', 'ba'),
                ('abc123', 'bb2a1c3'),
                ('abc_123+@#$', 'r@2#a_1+c3$'),
            ])
    def test_make_by_alphabet_with_errors(self, alpha, scrambled):
        with raises(ValueError):
            SubstitutionSequenceBuilder.make_sequence_by_alphabet(alpha, scrambled)

    def test_make_by_26_eng_cap_letters(self):
        scrambled = 'ZLCXPWOYDFKAHIUSNMBQTVGRJE'
        seq = [25, 11, 2, 23, 15, 22, 14, 24, 3, 5, 10, 0, 7, 8, 20, 18, 13, 12, 1, 16, 19, 21, 6, 17, 9, 4]

        ss = SubstitutionSequenceBuilder.make_sequence_by_26_eng_cap_letters(scrambled)

        for i in range(ss.length):
            assert ss.substitute(i) == seq[i]

    @mark.parametrize(
            'scrambled',
            [
                'ZLCXPWOYDFKAHIUSNMBQTV_RJE',
                'ZZCXPWOYDFKAHIUSNMBQTVGRJE',
                'ZLCXPWOYDFKAHIUSNMBQTVGRJEE',
                'ZLCXPWOYDFKAHIUSNMBQTVGRJ',
            ])
    def test_make_by_26_eng_cap_letters_with_errors(self, scrambled):
        with raises(ValueError):
            SubstitutionSequenceBuilder.make_sequence_by_26_eng_cap_letters(scrambled)
