import unittest
from unittest import TestCase
import contextlib
with contextlib.redirect_stdout(None), contextlib.redirect_stderr(None):
    import exercises3
    from exercises3 import Expr, Add, Sub, Mul, Lit, Let, Ifnz, Dup


class Problem1(TestCase):
    def test_p1(self):
        self.assertEqual(str(exercises3.p1), "(2 * (if (0 + 0) != 0 then 2 else 3))")


class Problem2(TestCase):
    def try_run(self, e: Expr, expected: int) -> None:
        try:
            got = exercises3.exec(exercises3.scompile(e))
        except Exception as err:
            self.fail(f"exec(scompile({e})) threw an error (should be {expected})")
            raise err
        self.assertEqual(got, expected, f"exec(scompile({e})) = {got} (should be {expected})")

    def test_1(self):
        self.try_run(Sub(Lit(0), Lit(0)), 0)

    def test_2(self):
        self.try_run(Sub(Lit(1), Lit(0)), 1)

    def test_3(self):
        self.try_run(Sub(Lit(2), Lit(3)), -1)

    def test_4(self):
        self.try_run(Sub(Lit(5), Lit(4)), 1)

    def test_5(self):
        self.try_run(Sub(Lit(0), Lit(6)), -6)

    def test_6(self):
        self.try_run(Sub(Lit(7), Lit(-8)), 15)

    def test_7(self):
        self.try_run(Sub(Lit(-9), Lit(10)), -19)

    def test_8(self):
        self.try_run(Add(Lit(12), Sub(Lit(13), Lit(14))), 11)

    def test_9(self):
        self.try_run(Add(Sub(Lit(15), Lit(16)), Lit(17)), 16)

    def test_10(self):
        self.try_run(Sub(Add(Lit(18), Lit(19)), Sub(Lit(20), Lit(21))), 38)

    def test_11(self):
        self.try_run(Sub(Add(Lit(18), Lit(19)), Sub(Lit(20), Lit(21))), 38)

    def test_12(self):
        self.try_run(Ifnz(Sub(Mul(Lit(22), Lit(23)), Lit(24)), Sub(Lit(25), Lit(26)), Sub(Lit(27), Lit(-28))), -1)

    def test_13(self):
        self.try_run(Ifnz(Sub(Lit(29), Lit(29)), Sub(Mul(Lit(30), Lit(31)), Lit(32)), Sub(Mul(Lit(30), Lit(31)), Lit(32))), 898)
        

class Problem3(TestCase):
    def test_p3(self):
        self.assertIn(Dup(4), exercises3.compile(exercises3.p3))

    def test_p3_onelet(self):
        # Check for at most one `Let`.
        have_let = False
        def go(e: Expr) -> None:
            match e:
                case Add(left, right) | Sub(left, right) | Mul(left, right):
                    go(left)
                    go(right)
                case Let(_, defexpr, bodyexpr):
                    nonlocal have_let
                    self.assertFalse(have_let, f"{exercises3.p3} has more than one Let")
                    have_let = True
                    go(defexpr)
                    go(bodyexpr)
                case Ifnz(cond, thenexpr, elseexpr):
                    go(cond)
                    go(thenexpr)
                    go(elseexpr)
                case _:
                    pass
        go(exercises3.p3)

if __name__ == "__main__":
    unittest.main()
