import unittest
from polynomial import Polynomial, PolynomialModulo

class PolynomialTest(unittest.TestCase):

    def test_str(self):
        self.assertEqual(str(Polynomial([0, -1, 2])), "2*X^2 - X")
        self.assertEqual(str(Polynomial([0, 0, 0])), "0")
        self.assertEqual(str(Polynomial([1])), "1")
        self.assertEqual(str(Polynomial([-1])), "-1")
        self.assertEqual(str(Polynomial([0,1])), "X")
        self.assertEqual(str(Polynomial([0,-1])), "-X")
        self.assertEqual(str(Polynomial([0,2])), "2*X")
        self.assertEqual(str(Polynomial([1,0,1])), "X^2 + 1")
        self.assertEqual(str(Polynomial([1, 2, 3])), "3*X^2 + 2*X + 1")

    def setUp(self):
        # On définit ici les paramètres q et n communs à tous les tests.
        self.q = 5
        self.n = 3

    def test_polynome_nul(self):
        # Le polynôme nul devrait être affiché comme "0"
        p = PolynomialModulo([0,0,0], self.q, self.n)
        self.assertEqual(str(p), "0", "Le polynôme nul doit s'afficher comme '0'.")

    def test_polynome_constant(self):
        # Représente un polynôme constant non nul, par exemple 7.
        # Comme 7 mod 5 = 2, l'affichage attendu est "2"
        p = PolynomialModulo([7,0,0], self.q, self.n)
        self.assertEqual(str(p), "2", "Le polynôme constant doit être réduit modulo 5.")

    def test_polynome_lineaire(self):
        # Représente le polynôme 1 + 2*X + 0*X^2, attendu sous la forme "2*X + 1"
        p = PolynomialModulo([1, 2, 0], self.q, self.n)  # 1 + 2X
        self.assertEqual(str(p), "2*X + 1", "L'affichage doit être '2*X + 1'.")

    def test_polynome_quadratique(self):
        # Représente le polynôme 1 + 0*X + 3*X^2, attendu sous la forme "3*X^2 + 1"
        p = PolynomialModulo([1, 0, 3], self.q, self.n)  # 1 + 0*X + 3X^2
        self.assertEqual(str(p), "3*X^2 + 1", "Les termes à coefficient nul ne doivent pas apparaître.")

    def test_polynome_avec_coefficients_negatifs(self):
        # Représente le polynôme -1 + 2X - 3X^2.
        # Dans Z_5, -1 ≡ 4 et -3 ≡ 2, donc le polynôme canonique est 4 + 2*X + 2*X^2.
        # Attendu en ordre décroissant : "2*X^2 + 2*X + 4"
        p = PolynomialModulo([-1, 2, -3], self.q, self.n)
        self.assertEqual(str(p), "2*X^2 + 2*X + 4", "La réduction modulo 5 doit être correctement appliquée.")

    def test_add(self):
        # Test 1 : Addition simple
        p1 = PolynomialModulo([1, 2, 3], 5, 3)  # 3*X^2 + 2*X + 1
        p2 = PolynomialModulo([4, 0, 1], 5, 3)  #   X^2       + 4
        result = p1 + p2
        expected = PolynomialModulo([0, 2, 4], 5, 3)  # 4*X^2 + 2*X
        self.assertEqual(result.coeffs, expected.coeffs)

        # Test 2 : Addition avec dépassement de modulo
        p1 = PolynomialModulo([3, 4, 2], 5, 3)  # 2*X^2 + 4*X + 3
        p2 = PolynomialModulo([4, 3, 3], 5, 3)  # 3*X^2 + 3*X + 4
        result = p1 + p2
        expected = PolynomialModulo([2, 2, 0], 5, 3)  # 2*X + 2
        self.assertEqual(result.coeffs, expected.coeffs)

    def test_mul(self):
        # Test 1 : Multiplication simple
        p1 = PolynomialModulo([1, 2, 3], 5, 3)  # 3*X^2 + 2*X + 1
        p2 = PolynomialModulo([4, 0, 1], 5, 3)  # X^2 + 4
        result = p1 * p2
        expected = PolynomialModulo([2, 0, 3], 5, 3)  # 3*X^2 + 2
        self.assertEqual(result.coeffs, expected.coeffs)

        # Test 2 : Multiplication avec réduction modulo X^n + 1
        p1 = PolynomialModulo([1, 1, 1], 5, 3)  # X^2 + X + 1
        p2 = PolynomialModulo([1, 1, 1], 5, 3)  # X^2 + X + 1
        result = p1 * p2
        expected = PolynomialModulo([4, 1, 3], 5, 3)  # 3*X^2 + X + 4
        self.assertEqual(result.coeffs, expected.coeffs)

        # Test 3 : Multiplication avec coefficients nuls
        p1 = PolynomialModulo([0, 0, 0], 5, 3)  # 0
        p2 = PolynomialModulo([1, 2, 3], 5, 3)  # 3*X^2 + 2*X + 1
        result = p1 * p2
        expected = PolynomialModulo([0, 0, 0], 5, 3)  # 0
        self.assertEqual(result.coeffs, expected.coeffs)


if __name__ == "__main__":
    unittest.main(argv=['ignored', '-v'], exit=False)