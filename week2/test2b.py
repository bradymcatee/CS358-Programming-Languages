import unittest

from contextlib import redirect_stdout, redirect_stderr
with redirect_stdout(None), redirect_stderr(None):
    from exercises2b import Or, And, Not, Lit, Let, Name


class TestCountNameOccurrences(unittest.TestCase):
    def countNameOccurrences(self, expr, expected):
        from exercises2b import countNameOccurrences
        got = countNameOccurrences("x", expr)
        self.assertEqual(
            got, expected,
            f"countNameOccurrences({repr(expr)}) = {repr(got)} (should be {repr(expected)})"
        )

    def test_size_0(self):
        self.countNameOccurrences(Lit(True), 0)
        self.countNameOccurrences(Name('x'), 1)
        self.countNameOccurrences(Name('r'), 0)

    def test_size_1(self):
        self.countNameOccurrences(Let('z', Lit(False), Lit(True)), 0)
        self.countNameOccurrences(And(Name('x'), Lit(True)), 1)
        self.countNameOccurrences(Let('h', Name('x'), Name('x')), 2)
        self.countNameOccurrences(And(Name('x'), Name('u')), 1)
        self.countNameOccurrences(Let('o', Name('x'), Name('n')), 1)
        self.countNameOccurrences(And(Lit(False), Name('q')), 0)
        self.countNameOccurrences(Or(Lit(True), Name('x')), 1)
        self.countNameOccurrences(And(Lit(True), Lit(True)), 0)
        self.countNameOccurrences(Or(Name('x'), Lit(False)), 1)
        self.countNameOccurrences(Let('z', Lit(True), Name('p')), 0)

    def test_size_2(self):
        self.countNameOccurrences(And(Or(Lit(False), Name('z')), Lit(False)), 0)
        self.countNameOccurrences(And(Or(Lit(True), Name('x')), Name('y')), 1)
        self.countNameOccurrences(Let('z', Name('m'), Let('b', Name('j'), Lit(True))), 0)
        self.countNameOccurrences(Or(Let('u', Name('s'), Name('x')), Name('x')), 2)
        self.countNameOccurrences(Let('r', Or(Lit(True), Name('f')), Name('s')), 0)
        self.countNameOccurrences(Or(And(Name('u'), Lit(True)), Name('x')), 1)
        self.countNameOccurrences(Or(Name('a'), Not(Name('x'))), 1)
        self.countNameOccurrences(Or(Name('x'), And(Name('q'), Lit(False))), 1)
        self.countNameOccurrences(Or(And(Lit(True), Lit(False)), Name('y')), 0)
        self.countNameOccurrences(Let('w', Let('m', Lit(True), Lit(False)), Name('x')), 1)

    def test_size_3(self):
        self.countNameOccurrences(Let('r', Let('z', Name('x'), Name('x')), Let('w', Name('x'), Name('x'))), 4)
        self.countNameOccurrences(And(Name('x'), Let('y', Let('f', Lit(False), Name('m')), Name('s'))), 1)
        self.countNameOccurrences(Or(Name('x'), Or(And(Name('x'), Name('q')), Name('a'))), 2)
        self.countNameOccurrences(Let('w', And(Let('r', Name('n'), Lit(False)), Name('x')), Name('x')), 2)
        self.countNameOccurrences(Or(Name('n'), Or(Name('c'), And(Name('x'), Name('c')))), 1)
        self.countNameOccurrences(Or(Let('g', And(Name('x'), Lit(False)), Lit(True)), Name('s')), 1)
        self.countNameOccurrences(Let('i', Lit(False), Or(Name('m'), And(Lit(True), Name('x')))), 1)
        self.countNameOccurrences(And(And(Name('x'), Or(Lit(False), Lit(False))), Name('x')), 2)
        self.countNameOccurrences(And(Name('x'), Or(Lit(True), Let('y', Name('j'), Name('x')))), 2)
        self.countNameOccurrences(And(And(And(Name('x'), Lit(False)), Name('q')), Lit(False)), 1)


class TestUniquifyEnv(unittest.TestCase):
    def uniquifyEnv(self, env, expected):
        from exercises2b import uniquifyEnv
        got = uniquifyEnv(env)
        self.assertEqual(
            got, expected,
            f"uniquifyEnv({env}) = {got} (should be {expected})"
        )

    def test_length_0(self):
        self.uniquifyEnv((), ())

    def test_length_1(self):
        self.uniquifyEnv((("x", True),), (("x", True),))

    def test_length_2(self):
        self.uniquifyEnv((("x", True), ("y", True)), (("x", True), ("y", True)))
        self.uniquifyEnv((("x", True), ("x", True)), (("x", True),))
        self.uniquifyEnv((("x", True), ("x", False)), (("x", True),))

    def test_length_3(self):
        self.uniquifyEnv((("x", True), ("y", False), ("z", True)), (("x", True), ("y", False), ("z", True)))
        self.uniquifyEnv((("x", True), ("y", False), ("x", False)), (("x", True), ("y", False)))
        self.uniquifyEnv((("x", True), ("y", True), ("y", False)), (("x", True), ("y", True)))
        self.uniquifyEnv((("x", False), ("x", False), ("y", True)), (("x", False), ("y", True)))
        self.uniquifyEnv((("x", True), ("x", False), ("x", False)), (("x", True),))

    def test_length_4(self):
        self.uniquifyEnv((("w", False), ("x", False), ("y", True), ("z", True)), (("w", False), ("x", False), ("y", True), ("z", True)))
        self.uniquifyEnv((("w", False), ("x", True), ("y", True), ("w", False)), (("w", False), ("x", True), ("y", True)))
        self.uniquifyEnv((("x", True), ("y", True), ("y", False), ("x", False)), (("x", True), ("y", True)))
        self.uniquifyEnv((("w", False), ("x", False), ("y", True), ("z", True)), (("w", False), ("x", False), ("y", True), ("z", True)))
        self.uniquifyEnv((("x", True), ("x", False), ("x", False), ("x", True)), (("x", True),))


class TestSubstituteAllNames(unittest.TestCase):
    def substituteAllNames(self, env, expr, expected):
        from exercises2b import substituteAllNames
        got = substituteAllNames(env, expr)
        self.assertEqual(
            got, expected,
            f"substituteAllNames({repr(env)}, {repr(expr)}) = {repr(got)} (should be {repr(expected)})"
        )

    def test_examples(self):
        env = (("x", True), ("y", False))
        self.substituteAllNames(
            env,
            Or(Name("x"), Lit(False)),
            Or(Lit(True), Lit(False))
        )
        self.substituteAllNames(
            env,
            Or(Name("x"), Name("y")),
            Or(Lit(True), Lit(False))
        )
        self.substituteAllNames(
            env,
            And(Not(Name("x")), Not(Or(Name("y"), Name("x")))),
            And(Not(Lit(True)), Not(Or(Lit(False), Lit(True))))
        )
        self.substituteAllNames(
            env,
            Let("x", Not(Name("y")), Name("y")),
            Let("x", Not(Lit(False)), Lit(False))
        )
        self.substituteAllNames(
            env,
            Let("x", Lit(False), Name("x")),
            Let("x", Lit(False), Lit(True))
        )

    def test_lit(self):
        self.substituteAllNames(
            (),
            Lit(True),
            Lit(True)
        )

    def test_nested_let(self):
        self.substituteAllNames(
            (("w", False), ("x", True), ("y", False), ("z", True)),
            Let("a", Let("b", And(Name("x"), Name("y")), Name("z")), Name("w")),
            Let("a", Let("b", And(Lit(True), Lit(False)), Lit(True)), Lit(False))
        )

    def test_lookup(self):
        self.substituteAllNames(
            (("x", True), ("x", False)),
            Name("x"),
            Lit(True)
        )

    def test_dup(self):
        self.substituteAllNames(
            (("x", True),),
            And(Name("x"), Name("x")),
            And(Lit(True), Lit(True))
        )

class TestSimplifyBindings(unittest.TestCase):
    def simplifyBindings(self, expr, expected):
        from exercises2b import simplifyBindings
        got = simplifyBindings(expr)
        self.assertEqual(
            got, expected,
            f"simplifyBindings({repr(expr)}) = {repr(got)} (should be {repr(expected)})"
        )

    def test_examples(self):
        self.simplifyBindings(
            Let("x", Lit(True), Let("y", Name("x"), Not(Name("y")))),
            Not(Lit(True))
        )
        self.simplifyBindings(
            Let("x", Lit(True), Let("x", Lit(False), Not(Name("x")))),
            Not(Lit(False))
        )
        self.simplifyBindings(
            And(Lit(False), Let("x", Lit(True), Name("x"))),
            And(Lit(False), Lit(True))
        )
        self.simplifyBindings(
            Let("x", Or(Lit(True), Lit(False)), And(Name("x"), Lit(True))),
            And(Or(Lit(True), Lit(False)), Lit(True))
        )

    def test_nested_let(self):
        self.simplifyBindings(
            Let("x", Let("y", And(Lit(True), Lit(False)), Name("y")), Not(Name("x"))),
            Not(And(Lit(True), Lit(False)))
        )

    def test_lit(self):
        self.simplifyBindings(Lit(True), Lit(True))

    def test_dup(self):
        self.simplifyBindings(
            Let("x", Lit(True), And(Name("x"), Name("x"))),
            And(Lit(True), Lit(True))
        )

    def test_ignored(self):
        self.simplifyBindings(
            Let("x", Lit(False), And(Lit(True), Lit(False))),
            And(Lit(True), Lit(False))
        )


class TestSimplifyToBool(unittest.TestCase):
    def simplifyToBool(self, expr, expected):
        from exercises2b import simplifyToBool1
        got = simplifyToBool(expr)
        self.assertEqual(
            got, expected,
            f"simplifyToBool({repr(expr)}) = {repr(got)} (should be {repr(expected)})"
        )

    def test_1(self):
        self.simplifyToBool(
            Let("x", Lit(True), Let("y", Name("x"), Not(Name("y")))),
            Lit(False)
        )

    def test_2(self):
        self.simplifyToBool(
            Let("x", Lit(True), Let("x", Lit(False), Not(Name("x")))),
            Lit(True)
        )

    def test_3(self):
        self.simplifyToBool(
            And(Lit(False), Let("x", Lit(True), Name("x"))),
            Lit(False)
        )

    def test_4(self):
        self.simplifyToBool(
            Let("x", Or(Lit(True), Lit(False)), And(Name("x"), Lit(True))),
            Lit(True)
        )

    def test_5(self):
        self.simplifyToBool(
            Let("x", Let("y", And(Lit(True), Lit(False)), Name("y")), Not(Name("x"))),
            Lit(True)
        )

    def test_6(self):
        self.simplifyToBool(
            Lit(True),
            Lit(True)
        )

    def test_7(self):
        self.simplifyToBool(
            Let("x", Lit(True), And(Name("x"), Name("x"))),
            Lit(True)
        )

    def test_8(self):
        self.simplifyToBool(
            Let("x", Lit(False), And(Lit(True), Lit(False))),
            Lit(False)
        )

if __name__ == "__main__":
    unittest.main()
