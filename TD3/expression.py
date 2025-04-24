from __future__ import annotations

class Tree:

    def __init__(self, label: str, *children: tuple[Tree]):
        self.__label = label
        self.__children = children

    def label(self) -> str:
        return self.__label
    
    def children(self) -> tuple[Tree]:
        return self.__children
    
    def nb_children(self) -> int:
        return len(self.__children)
    
    def child(self, i: int) -> Tree:
        assert 0 <= i < self.nb_children()
        return self.__children[i]
    
    def is_leaf(self) -> bool:
        return self.nb_children() == 0
    
    def depth(self) -> int:
        if self.is_leaf():
            return 0
        return max([c.depth() for c in self.__children]) + 1
    
    def __str__(self) -> str:
        s = self.label()
        if(self.is_leaf()):
            return s
        return f"{s}({",".join([str(c) for c in self.__children])})"
    
    def __eq__(self, other: Tree) -> bool:
        if self.label() != other.label():
            return False
        if self.nb_children() != other.nb_children():
            return False
        if self.is_leaf() and other.is_leaf():
            return True
        for i in range(self.nb_children()):
            if self.child(i) != other.child(i):
                return False
        return True
    
    def deriv(self, var: str) -> Tree:
        if self.is_leaf():
            #Si c'est une feuille, alors soit c'est la variable, soit un terme constant donc dérivé en 0
            if self.label() == var:
                return Tree("1")
            return Tree("0")
        if self.label() == "+":#Dérivation d'une somme : somme des dérivations
            return Tree("+", *[c.deriv(var) for c in self.children()])
        elif self.label() == "*":#Dérivation de f_1 f_2 ... f_n = \sum_{i=1}^n f_i' f_1 ... f_n
            childs = []
            for i in range(self.nb_children()):
                l = list(self.children()[::])
                l[i] = l[i].deriv(var)
                childs.append(Tree("*", *l))
            return Tree("+", *childs)
        return self
    
    def substitute(self, t1: Tree, t2: Tree) -> Tree:
        if self == t1:
            return t2
        if self.is_leaf():
            return self
        return Tree(self.label(), *[child.substitute(t1, t2) for child in self.children()])
    
    def simplify(self) -> Tree:
        if self.is_leaf():
            return self
        if self.label() == '+':#Somme
            numeric = 0
            childs = []
            for child in self.children():
                simp = child.simplify()
                if simp.is_leaf() and simp.label().isnumeric():
                    numeric += int(simp.label())
                elif simp.label() == "+":
                    childs.extend(list(simp.children()))
                else:
                    childs.append(simp)
            if numeric == 0:
                if len(childs) == 1:
                    return childs[0]
                return Tree("+", *childs)
            if len(childs) == 0:
                return Tree(str(numeric))
            return Tree("+", Tree(str(numeric)), *childs)
        if self.label() == "*":
            numeric = 1
            childs = []
            for child in self.children():
                simp = child.simplify()
                if simp.is_leaf() and simp.label().isnumeric():
                    v = int(simp.label())
                    if v == 0:
                        return Tree("0")
                    numeric *= v
                else:
                    childs.append(simp)
            if numeric == 1:
                if len(childs) == 1:
                    return childs[0]
                return Tree("*", *childs)
            if len(childs) == 0:
                return Tree(str(numeric))
            return Tree("*", Tree(str(numeric)), *childs)
        return self#Pas de somme ou multiplication on ne sait pas quoi faire
    
    def evaluate(self, value: int) -> int:
        return self.substitute(Tree("X"), Tree(str(value))).simplify()

    def pretty_print(self) -> str:
        label = self.label()
        if self.is_leaf():
            return label
        return label.join([c.pretty_print() for c in self.children()])