import unittest

from contextlib import redirect_stdout, redirect_stderr
with redirect_stdout(None), redirect_stderr(None):
    from exercises2a import Or, And, Not, Lit


class TestCountNots(unittest.TestCase):
    def countNots(self, expr, expected):
        from exercises2a import countNots
        got = countNots(expr)
        self.assertEqual(
            got, expected,
            f"countNots({repr(expr)}) = {repr(got)} (should be {repr(expected)})"
        )

    def test_size_0(self):
        self.countNots(Lit(True), 0)

    def test_size_1(self):
        self.countNots(Or(Lit(False), Lit(True)), 0)
        self.countNots(And(Lit(False), Lit(False)), 0)
        self.countNots(Not(Lit(False)), 1)

    def test_size_2(self):
        self.countNots(Or(Lit(True), Or(Lit(True), Lit(True))), 0)
        self.countNots(Or(Lit(True), And(Lit(True), Lit(True))), 0)
        self.countNots(Or(And(Lit(False), Lit(False)), Lit(False)), 0)
        self.countNots(Or(Not(Lit(True)), Lit(False)), 1)
        self.countNots(And(Lit(True), And(Lit(True), Lit(True))), 0)
        self.countNots(And(Lit(False), Not(Lit(True))), 1)
        self.countNots(And(And(Lit(False), Lit(False)), Lit(False)), 0)
        self.countNots(And(Not(Lit(True)), Lit(False)), 1)
        self.countNots(Not(Or(Lit(False), Lit(True))), 1)
        self.countNots(Not(Not(Lit(False))), 2)

    def test_size_3(self):
        self.countNots(Or(Lit(False), Or(Lit(True), And(Lit(True), Lit(True)))), 0)
        self.countNots(Not(Or(Lit(False), Not(Lit(True)))), 2)
        self.countNots(Or(Not(Or(Lit(False), Lit(False))), Lit(True)), 1)
        self.countNots(And(Not(And(Lit(True), Lit(True))), Lit(False)), 1)
        self.countNots(Not(And(And(Lit(False), Lit(True)), Lit(True))), 1)
        self.countNots(And(Lit(True), And(Lit(False), Or(Lit(False), Lit(False)))), 0)
        self.countNots(Or(Or(Lit(True), Lit(False)), Or(Lit(False), Lit(False))), 0)
        self.countNots(And(Lit(False), Or(Lit(True), Not(Lit(True)))), 1)
        self.countNots(And(Lit(False), Not(Not(Lit(True)))), 2)
        self.countNots(And(Not(Lit(False)), And(Lit(False), Lit(False))), 1)

    def test_size_4(self):
        self.countNots(And(Lit(True), Or(Or(Lit(True), Lit(True)), Or(Lit(False), Lit(False)))), 0)
        self.countNots(Or(And(Lit(True), Lit(False)), Or(Or(Lit(True), Lit(False)), Lit(True))), 0)
        self.countNots(Or(Not(Not(Lit(False))), Not(Lit(False))), 3)
        self.countNots(And(And(Or(Lit(False), Not(Lit(True))), Lit(True)), Lit(True)), 1)
        self.countNots(Not(Or(Or(Lit(True), Lit(False)), And(Lit(True), Lit(False)))), 1)
        self.countNots(And(And(Lit(True), Lit(False)), And(Or(Lit(True), Lit(True)), Lit(True))), 0)
        self.countNots(Not(Or(And(Not(Lit(True)), Lit(False)), Lit(False))), 2)
        self.countNots(And(Lit(True), Not(Not(Or(Lit(True), Lit(False))))), 2)
        self.countNots(Or(And(Lit(False), Or(Or(Lit(False), Lit(False)), Lit(True))), Lit(True)), 0)
        self.countNots(Not(And(Lit(False), And(And(Lit(False), Lit(True)), Lit(False)))), 1)


class TestRemoveFalses(unittest.TestCase):
    def removeFalses(self, expr, expected):
        from exercises2a import removeFalses
        got = removeFalses(expr)
        self.assertEqual(
            got, expected,
            f"removeFalses({repr(expr)}) = {repr(got)} (should be {repr(expected)})"
        )

    def test_size_0(self):
        self.removeFalses(Lit(True), Lit(True))
        self.removeFalses(Lit(False), Not(Lit(True)))

    def test_size_1(self):
        self.removeFalses(Not(Lit(False)), Not(Not(Lit(True))))
        self.removeFalses(Or(Lit(False), Lit(True)), Or(Not(Lit(True)), Lit(True)))
        self.removeFalses(Or(Lit(False), Lit(False)), Or(Not(Lit(True)), Not(Lit(True))))
        self.removeFalses(And(Lit(False), Lit(True)), And(Not(Lit(True)), Lit(True)))
        self.removeFalses(And(Lit(True), Lit(False)), And(Lit(True), Not(Lit(True))))
        self.removeFalses(Not(Lit(True)), Not(Lit(True)))
        self.removeFalses(And(Lit(True), Lit(True)), And(Lit(True), Lit(True)))
        self.removeFalses(And(Lit(False), Lit(False)), And(Not(Lit(True)), Not(Lit(True))))
        self.removeFalses(Or(Lit(True), Lit(True)), Or(Lit(True), Lit(True)))
        self.removeFalses(Or(Lit(True), Lit(False)), Or(Lit(True), Not(Lit(True))))

    def test_size_2(self):
        self.removeFalses(And(Or(Lit(False), Lit(True)), Lit(True)), And(Or(Not(Lit(True)), Lit(True)), Lit(True)))
        self.removeFalses(And(Lit(True), Or(Lit(True), Lit(True))), And(Lit(True), Or(Lit(True), Lit(True))))
        self.removeFalses(Or(Or(Lit(False), Lit(False)), Lit(False)), Or(Or(Not(Lit(True)), Not(Lit(True))), Not(Lit(True))))
        self.removeFalses(Or(Or(Lit(False), Lit(True)), Lit(False)), Or(Or(Not(Lit(True)), Lit(True)), Not(Lit(True))))
        self.removeFalses(And(And(Lit(False), Lit(False)), Lit(True)), And(And(Not(Lit(True)), Not(Lit(True))), Lit(True)))
        self.removeFalses(And(And(Lit(True), Lit(True)), Lit(False)), And(And(Lit(True), Lit(True)), Not(Lit(True))))
        self.removeFalses(And(Or(Lit(True), Lit(False)), Lit(True)), And(Or(Lit(True), Not(Lit(True))), Lit(True)))
        self.removeFalses(Or(And(Lit(False), Lit(False)), Lit(True)), Or(And(Not(Lit(True)), Not(Lit(True))), Lit(True)))
        self.removeFalses(And(And(Lit(False), Lit(True)), Lit(False)), And(And(Not(Lit(True)), Lit(True)), Not(Lit(True))))
        self.removeFalses(And(Or(Lit(False), Lit(False)), Lit(True)), And(Or(Not(Lit(True)), Not(Lit(True))), Lit(True)))

    def test_size_3(self):
        self.removeFalses(And(Or(Lit(True), Lit(True)), Or(Lit(False), Lit(True))), And(Or(Lit(True), Lit(True)), Or(Not(Lit(True)), Lit(True))))
        self.removeFalses(Or(And(Or(Lit(True), Lit(False)), Lit(True)), Lit(False)), Or(And(Or(Lit(True), Not(Lit(True))), Lit(True)), Not(Lit(True))))
        self.removeFalses(Or(And(Or(Lit(True), Lit(False)), Lit(False)), Lit(True)), Or(And(Or(Lit(True), Not(Lit(True))), Not(Lit(True))), Lit(True)))
        self.removeFalses(And(Lit(False), Or(Lit(False), And(Lit(True), Lit(False)))), And(Not(Lit(True)), Or(Not(Lit(True)), And(Lit(True), Not(Lit(True))))))
        self.removeFalses(Or(Or(Lit(True), Or(Lit(True), Lit(True))), Lit(True)), Or(Or(Lit(True), Or(Lit(True), Lit(True))), Lit(True)))
        self.removeFalses(And(Lit(False), Or(Not(Lit(False)), Lit(True))), And(Not(Lit(True)), Or(Not(Not(Lit(True))), Lit(True))))
        self.removeFalses(And(Lit(True), And(Lit(True), And(Lit(True), Lit(True)))), And(Lit(True), And(Lit(True), And(Lit(True), Lit(True)))))
        self.removeFalses(Not(Or(Or(Lit(True), Lit(False)), Lit(True))), Not(Or(Or(Lit(True), Not(Lit(True))), Lit(True))))
        self.removeFalses(And(Or(Or(Lit(True), Lit(False)), Lit(True)), Lit(False)), And(Or(Or(Lit(True), Not(Lit(True))), Lit(True)), Not(Lit(True))))
        self.removeFalses(And(And(Lit(True), Or(Lit(False), Lit(True))), Lit(False)), And(And(Lit(True), Or(Not(Lit(True)), Lit(True))), Not(Lit(True))))

    def test_size_4(self):
        self.removeFalses(
            And(Not(Or(Lit(False), Lit(True))), Or(Lit(False), Lit(False))),
            And(Not(Or(Not(Lit(True)), Lit(True))), Or(Not(Lit(True)), Not(Lit(True))))
        )
        self.removeFalses(
            Or(Or(And(Or(Lit(False), Lit(False)), Lit(False)), Lit(False)), Lit(False)),
            Or(Or(And(Or(Not(Lit(True)), Not(Lit(True))), Not(Lit(True))), Not(Lit(True))), Not(Lit(True)))
        )
        self.removeFalses(
            And(Or(And(Lit(True), Lit(True)), Lit(False)), And(Lit(True), Lit(True))),
            And(Or(And(Lit(True), Lit(True)), Not(Lit(True))), And(Lit(True), Lit(True)))
        )
        self.removeFalses(
            Or(And(Lit(True), Lit(False)), And(Lit(False), Or(Lit(True), Lit(False)))),
            Or(And(Lit(True), Not(Lit(True))), And(Not(Lit(True)), Or(Lit(True), Not(Lit(True)))))
        )
        self.removeFalses(
            And(Or(Lit(False), Lit(False)), And(Lit(False), Or(Lit(True), Lit(True)))),
            And(Or(Not(Lit(True)), Not(Lit(True))), And(Not(Lit(True)), Or(Lit(True), Lit(True))))
        )
        self.removeFalses(
            And(And(Or(Lit(False), And(Lit(True), Lit(True))), Lit(True)), Lit(True)),
            And(And(Or(Not(Lit(True)), And(Lit(True), Lit(True))), Lit(True)), Lit(True))
        )
        self.removeFalses(
            Or(Or(Or(And(Lit(False), Lit(False)), Lit(False)), Lit(False)), Lit(False)),
            Or(Or(Or(And(Not(Lit(True)), Not(Lit(True))), Not(Lit(True))), Not(Lit(True))), Not(Lit(True)))
        )
        self.removeFalses(
            And(And(Or(Lit(False), Lit(True)), Lit(False)), Or(Lit(False), Lit(False))),
            And(And(Or(Not(Lit(True)), Lit(True)), Not(Lit(True))), Or(Not(Lit(True)), Not(Lit(True))))
        )
        self.removeFalses(
            And(Lit(True), Or(Lit(False), Or(Lit(True), And(Lit(False), Lit(True))))),
            And(Lit(True), Or(Not(Lit(True)), Or(Lit(True), And(Not(Lit(True)), Lit(True)))))
        )
        self.removeFalses(
            And(Or(Lit(False), Lit(False)), Not(Or(Lit(True), Lit(True)))),
            And(Or(Not(Lit(True)), Not(Lit(True))), Not(Or(Lit(True), Lit(True))))
        )


class TestRemoveNots(unittest.TestCase):
    def removeNots(self, expr, expected):
        from exercises2a import removeNots
        got = removeNots(expr)
        self.assertEqual(
            got, expected,
            f"removeNots({repr(expr)}) = {repr(got)} (should be {repr(expected)})"
        )

    def test_size_0(self):
        self.removeNots(Lit(True), Lit(True))

    def test_size_1(self):
        self.removeNots(Or(Lit(True), Lit(True)), Or(Lit(True), Lit(True)))
        self.removeNots(And(Lit(False), Lit(False)), And(Lit(False), Lit(False)))
        self.removeNots(Not(Lit(False)), Lit(True))

    def test_size_2(self):
        self.removeNots(And(Or(Lit(True), Lit(True)), Lit(False)), And(Or(Lit(True), Lit(True)), Lit(False)))
        self.removeNots(Not(Or(Lit(False), Lit(True))), And(Lit(True), Lit(False)))
        self.removeNots(And(And(Lit(False), Lit(False)), Lit(True)), And(And(Lit(False), Lit(False)), Lit(True)))
        self.removeNots(Or(Or(Lit(True), Lit(False)), Lit(False)), Or(Or(Lit(True), Lit(False)), Lit(False)))
        self.removeNots(And(Lit(False), And(Lit(True), Lit(True))), And(Lit(False), And(Lit(True), Lit(True))))
        self.removeNots(And(Lit(False), Or(Lit(True), Lit(False))), And(Lit(False), Or(Lit(True), Lit(False))))
        self.removeNots(Or(Not(Lit(True)), Lit(True)), Or(Lit(False), Lit(True)))
        self.removeNots(Or(Lit(False), Or(Lit(False), Lit(True))), Or(Lit(False), Or(Lit(False), Lit(True))))
        self.removeNots(Not(Not(Lit(True))), Lit(True))
        self.removeNots(Not(And(Lit(False), Lit(False))), Or(Lit(True), Lit(True)))

    def test_size_3(self):
        self.removeNots(And(Or(Or(Lit(True), Lit(True)), Lit(True)), Lit(False)), And(Or(Or(Lit(True), Lit(True)), Lit(True)), Lit(False)))
        self.removeNots(Not(Or(Lit(True), And(Lit(True), Lit(True)))), And(Lit(False), Or(Lit(False), Lit(False))))
        self.removeNots(Or(Not(Lit(True)), Not(Lit(False))), Or(Lit(False), Lit(True)))
        self.removeNots(And(Not(Or(Lit(False), Lit(False))), Lit(False)), And(And(Lit(True), Lit(True)), Lit(False)))
        self.removeNots(And(Lit(True), Or(Lit(True), And(Lit(True), Lit(True)))), And(Lit(True), Or(Lit(True), And(Lit(True), Lit(True)))))
        self.removeNots(Not(Or(Not(Lit(True)), Lit(False))), And(Lit(True), Lit(True)))
        self.removeNots(And(And(Not(Lit(False)), Lit(True)), Lit(True)), And(And(Lit(True), Lit(True)), Lit(True)))
        self.removeNots(Or(And(Or(Lit(True), Lit(False)), Lit(True)), Lit(False)), Or(And(Or(Lit(True), Lit(False)), Lit(True)), Lit(False)))
        self.removeNots(And(Lit(False), Or(Lit(False), Not(Lit(False)))), And(Lit(False), Or(Lit(False), Lit(True))))
        self.removeNots(Or(Not(Lit(True)), And(Lit(True), Lit(False))), Or(Lit(False), And(Lit(True), Lit(False))))

    def test_size_4(self):
        self.removeNots(And(Or(Or(Lit(True), Lit(True)), Lit(True)), Lit(False)), And(Or(Or(Lit(True), Lit(True)), Lit(True)), Lit(False)))
        self.removeNots(Not(Or(Lit(True), And(Lit(True), Lit(True)))), And(Lit(False), Or(Lit(False), Lit(False))))
        self.removeNots(Or(Not(Lit(True)), Not(Lit(False))), Or(Lit(False), Lit(True)))
        self.removeNots(And(Not(Or(Lit(False), Lit(False))), Lit(False)), And(And(Lit(True), Lit(True)), Lit(False)))
        self.removeNots(And(Lit(True), Or(Lit(True), And(Lit(True), Lit(True)))), And(Lit(True), Or(Lit(True), And(Lit(True), Lit(True)))))
        self.removeNots(Not(Or(Not(Lit(True)), Lit(False))), And(Lit(True), Lit(True)))
        self.removeNots(And(And(Not(Lit(False)), Lit(True)), Lit(True)), And(And(Lit(True), Lit(True)), Lit(True)))
        self.removeNots(Or(And(Or(Lit(True), Lit(False)), Lit(True)), Lit(False)), Or(And(Or(Lit(True), Lit(False)), Lit(True)), Lit(False)))
        self.removeNots(And(Lit(False), Or(Lit(False), Not(Lit(False)))), And(Lit(False), Or(Lit(False), Lit(True))))
        self.removeNots(Or(Not(Lit(True)), And(Lit(True), Lit(False))), Or(Lit(False), And(Lit(True), Lit(False))))

if __name__ == "__main__":
    unittest.main()
