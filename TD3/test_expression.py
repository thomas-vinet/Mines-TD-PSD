# -*- coding: utf-8 -*-

import unittest
from expression import Tree


class TestTree(unittest.TestCase):

    def test_create_tree1(self):
        a = Tree('a')
        a1 = Tree('a1', a)
        a2 = Tree('a1', a, a)
        self.assertIsNotNone(a)
        self.assertIsNot(a, a1)
        self.assertIsNot(a1, a2)

    def test_create_tree2(self):
        a = Tree('a')
        b = Tree('b')
        fab = Tree('f', a, b)
        ga = Tree('g', a)
        gb = Tree('g', b)

        self.assertEqual(a.label(), 'a')
        self.assertEqual(len(a.children()), 0)
        self.assertEqual(b.label(), 'b')
        self.assertEqual(len(b.children()), 0)

        self.assertEqual(fab.label(), 'f')
        self.assertEqual(fab.child(0), a)
        self.assertEqual(fab.child(1), b)

    def test_leaf(self):
        a = Tree('a')
        ga = Tree('g', a)

        self.assertTrue(a.is_leaf())
        self.assertFalse(ga.is_leaf())

    def test_depth(self):
        a = Tree('a')
        b = Tree('b')
        fab = Tree('f', a, b)
        ga = Tree('g', a)
        gb = Tree('g', b)
        fagb = Tree('f', a, gb)

        self.assertEqual(a.depth(), 0)
        self.assertEqual(fab.depth(), 1)
        self.assertEqual(ga.depth(), 1)
        self.assertEqual(gb.depth(), 1)
        self.assertEqual(fagb.depth(), 2)

    def test_eq_tree(self):
        a1 = Tree('a')
        a2 = Tree('a')
        fab1 = Tree('f', Tree('a'), Tree('b'))
        fab2 = Tree('f', Tree('a'), Tree('b'))

        self.assertEqual(a1, a2)
        self.assertEqual(fab1, fab2)
        
    def test_deriv_constant(self):
        X = Tree('X')
        a = Tree('a')
        zero = Tree('0')
        self.assertEqual(a.deriv('X'), zero)
        self.assertEqual(zero.deriv('X'), zero)

    def test_deriv_X(self):
        X = Tree('X')
        Y = Tree('Y')
        zero = Tree('0')
        un = Tree('1')

        self.assertEqual(X.deriv('X'), un)
        self.assertEqual(Y.deriv('X'), zero)

    def test_deriv_addition(self):
        X = Tree('X')
        zero = Tree('0')
        un = Tree('1')
        self.assertEqual(Tree('+', X, X).deriv('X'), Tree('+', un, un))
        self.assertEqual(Tree('+', X, un).deriv('X'), Tree('+', un, zero))

    def test_deriv_multiplication(self):
        P = Tree('+', Tree('*', Tree('3'), Tree('X'), Tree('X')), Tree('*', Tree('5'), Tree('X')), Tree('7'))
        print(str(P.deriv('X')))

if __name__ == '__main__':
    unittest.main()