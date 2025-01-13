from typing import Sequence
import unittest
from unittest import TestCase

import exercises1
from exercises1 import Tree, Branch, Leaf, LTree


class Problem1(TestCase):
    def is_palindrome(self, s: str) -> None:
        self.assertTrue(exercises1.ispal1(s), f"ispal1 thinks that \"{s}\" is not a palindrome")
        self.assertTrue(exercises1.ispal2(s), f"ispal2 thinks that \"{s}\" is not a palindrome")

    def not_palindrome(self, s: str) -> None:
        self.assertFalse(exercises1.ispal1(s), f"ispal1 thinks that \"{s}\" is a palindrome")
        self.assertFalse(exercises1.ispal2(s), f"ispal2 thinks that \"{s}\" is a palindrome")

    def test_empty(self) -> None:
        self.is_palindrome("")

    def test_one(self) -> None:
        self.is_palindrome("a")

    def test_two(self) -> None:
        self.is_palindrome("kk")
        self.not_palindrome("ok")

    def test_three(self) -> None:
        self.is_palindrome("aaa")
        self.is_palindrome("ana")
        self.not_palindrome("cat")
        self.not_palindrome("add")
        self.not_palindrome("oom")

    def test_long(self) -> None:
        self.is_palindrome("racecar")
        self.is_palindrome("tattarrattat")
        self.is_palindrome("saippuakivikauppias")
        self.is_palindrome("able was i ere i saw elba")

        self.not_palindrome("ricercar")
        self.not_palindrome("Able was i ere i saw elba")


class Problem2(TestCase):
    def fac_equal(self, x: int, y: int | None) -> None:
        z = exercises1.fac1(x)
        self.assertEqual(exercises1.fac1(x), y, f"fac1({x}) is {z} (should be {y})")
        z = exercises1.fac2(x)
        self.assertEqual(exercises1.fac2(x), y, f"fac2({x}) is {z} (should be {y})")

    def test_negative(self) -> None:
        self.fac_equal(-1, None)

    def test_0(self) -> None:
        self.fac_equal(0, 1)

    def test_1(self) -> None:
        self.fac_equal(1, 1)

    def test_2(self) -> None:
        self.fac_equal(2, 2)

    def test_3(self) -> None:
        self.fac_equal(3, 6)

    def test_4(self) -> None:
        self.fac_equal(4, 24)

    def test_5(self) -> None:
        self.fac_equal(5, 120)

    def test_10(self) -> None:
        self.fac_equal(10, 3628800)



class Problem3(TestCase):
    def dupz_equal(self, x: Sequence[int], y: list[int]) -> None:
        z = exercises1.dupz1(x)
        self.assertEqual(exercises1.dupz1(x), y, f"dupz1({x}) is {z} (should be {y})")
        z = exercises1.dupz2(x)
        self.assertEqual(exercises1.dupz2(x), y, f"dupz2({x}) is {z} (should be {y})")

    def list_and_tuple_equal(self, x: Sequence[int], y: list[int]) -> None:
        self.dupz_equal(list(x), y)
        self.dupz_equal(tuple(x), y)

    def range_equal(self, start: int, end: int, y: list[int]) -> None:
        r = range(start, end)
        self.list_and_tuple_equal(r, y)
        self.dupz_equal(r, y)

    def test_empty(self) -> None:
        self.range_equal(0, 0, [])

    def test_one_zero(self) -> None:
        self.range_equal(0, 1, [0, 0])

    def test_two_zeros(self) -> None:
        self.list_and_tuple_equal([0, 0], [0, 0, 0, 0])

    def test_zero_start(self) -> None:
        self.range_equal(0, 3, [0, 0, 1, 2])

    def test_zero_end(self) -> None:
        self.range_equal(-2, 1, [-2, -1, 0, 0])

    def test_zero_middle(self) -> None:
        self.range_equal(-2, 3, [-2, -1, 0, 0, 1, 2])

    def test_no_zeros(self) -> None:
        self.range_equal(1, 6, [1, 2, 3, 4, 5])

    def test_misc(self) -> None:
        self.list_and_tuple_equal([0, 1, 0, -1, 0, 3, 0], [0, 0, 1, 0, 0, -1, 0, 0, 3, 0, 0])


def t2l(t: Tree) -> LTree:
    match t:
       case Branch(l, r): return ['B', t2l(l), t2l(r)]
       case Leaf(v): return ['L', v]


class Depth(TestCase):
    def depth_equal(self, t: Tree, d: int) -> None:
        self.assertEqual(t.depth(), d)
        self.assertEqual(exercises1.depthlt(t2l(t)), d)

    def test_leaf(self) -> None:
        self.depth_equal(Leaf(100), 0)

    def test_list(self) -> None:
        self.depth_equal(
            Branch(Leaf(0), Branch(Leaf(1), Branch(Leaf(2), Branch(Leaf(3), Leaf(4))))),
            4
        )

    def test_llist(self) -> None:
        self.depth_equal(
            Branch(Branch(Branch(Branch(Leaf(0), Leaf(1)), Leaf(2)), Leaf(3)), Leaf(4)),
            4
        )

    def test_balanced(self) -> None:
        self.depth_equal(
            Branch(
                Branch(
                    Branch(
                        Leaf(1),
                        Leaf(2)
                    ),
                    Branch(
                        Leaf(3),
                        Leaf(4)
                    )
                ),
                Branch(
                    Branch(
                        Leaf(5),
                        Leaf(6)
                    ),
                    Branch(
                        Leaf(7),
                        Leaf(8)
                    )
                )
            ),
            3
        )


class Swap(TestCase):
    def swap_equal(self, t1: Tree, t2: Tree) -> None:
        self.assertEqual(exercises1.swap(t1), t2)
        self.assertEqual(exercises1.swaplt(t2l(t1)), t2l(t2))
    
    def test_leaf(self) -> None:
        self.swap_equal(Leaf(100), Leaf(100))

    def test_list(self) -> None:
        self.swap_equal(
            Branch(Leaf(0), Branch(Leaf(10), Branch(Leaf(20), Branch(Leaf(30), Leaf(40))))),
            Branch(Branch(Branch(Branch(Leaf(40), Leaf(30)), Leaf(20)), Leaf(10)), Leaf(0))
        )

    def test_llist(self) -> None:
        self.swap_equal(
            Branch(Branch(Branch(Branch(Leaf(-1), Leaf(-2)), Leaf(-3)), Leaf(-4)), Leaf(-5)),
            Branch(Leaf(-5), Branch(Leaf(-4), Branch(Leaf(-3), Branch(Leaf(-2), Leaf(-1)))))
        )

    def test_balanced(self) -> None:
        self.swap_equal(
            Branch(
                Branch(
                    Branch(
                        Leaf(0),
                        Leaf(1)
                    ),
                    Branch(
                        Leaf(1),
                        Leaf(2)
                    )
                ),
                Branch(
                    Branch(
                        Leaf(3),
                        Leaf(5)
                    ),
                    Branch(
                        Leaf(8),
                        Leaf(13)
                    )
                )
            ),
            Branch(
                Branch(
                    Branch(
                        Leaf(13),
                        Leaf(8)
                    ),
                    Branch(
                        Leaf(5),
                        Leaf(3)
                    )
                ),
                Branch(
                    Branch(
                        Leaf(2),
                        Leaf(1)
                    ),
                    Branch(
                        Leaf(1),
                        Leaf(0)
                    )
                )
            )
        )


if __name__ == "__main__":
    unittest.main()
