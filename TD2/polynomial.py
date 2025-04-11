class Polynomial:

    def __init__(self, coeffs):
        '''On stocke la liste des coefficients, par convention dans l'ordre croissant des puissances'''
        self.coeffs = coeffs

    def __str__(self):
        monomials = []
        for i in range(len(self.coeffs) - 1, -1, -1):#On affiche d'abord les plus grandes puissances
            val = self.coeffs[i]
            if val == 0:
                continue
            monomials.append(f"{val}*X^{i}")
        if len(monomials) == 0:
            return "0"
        joined = " + ".join(monomials)
        return joined.replace("+ -", "- ").replace("X^1", "X").replace("*X^0", "").replace("1*", "")
    
    def __add__(self, other):
        output = []
        for i in range(max(len(self.coeffs), len(other.coeffs))):
            vm = self.coeffs[i] if i < len(self.coeffs) else 0
            vn = other.coeffs[i] if i < len(other.coeffs) else 0
            output.append(vm + vn)
        return Polynomial(output)
    
class PolynomialModulo:

    def __init__(self, coeffs, q, n):
        assert len(coeffs) <= n#Supposition pour simplifier le problème: on a pas besoin de calculer le modulo des puissances, seulement pour les coefficients
        self.coeffs = [c % q for c in coeffs]
        self.q = q
        self.n = n

    def __str__(self):
        return str(Polynomial(self.coeffs))
    
    def __add__(self, other):
        assert self.q == other.q and self.n == other.n
        output = []
        for i in range(max(len(self.coeffs), len(other.coeffs))):
            vm = self.coeffs[i] if i < len(self.coeffs) else 0
            vn = other.coeffs[i] if i < len(other.coeffs) else 0
            output.append((vm + vn) % self.q)
        return PolynomialModulo(output, self.q, self.n)
    
    def scalar(self, c):
        return PolynomialModulo([(coeff * c) % self.q for coeff in self.coeffs], self.q, self.n)
    
    def rescale(self, r):
        return PolynomialModulo([coeff % r for coeff in self.coeffs], r, self.n)
    
    def __mul__(self, other):
        assert self.q == other.q and self.n == other.n
        coeffs = [0 for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                vm = self.coeffs[i] if i < len(self.coeffs) else 0
                vn = other.coeffs[j] if j < len(other.coeffs) else 0
                coeff = vm * vn % self.q
                power = i + j
                if power >= self.n:
                    power -= self.n
                    coeff *= -1
                coeffs[power] = (coeffs[power] + coeff) % self.q
        return PolynomialModulo(coeffs, self.q, self.n)