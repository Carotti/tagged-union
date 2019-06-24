from tagged_union import Unit, Self, tagged_union, match

@tagged_union
class Nat(object):
    O = Unit
    S = Self

    def __add__(self, other):
        return match(self, {
            Nat.O: lambda: other,
            Nat.S: lambda n: n + Nat.S(other)
        })

    def __sub__(self, other):
        return match(self, {
            Nat.O: lambda: self,
            Nat.S: lambda ns:
                match(other, {
                    Nat.O: lambda: self,
                    Nat.S: lambda no: ns - no,
                }),
        })

    def __mul__(self, other):
        return match(self, {
            Nat.O: lambda: Nat.O(),
            Nat.S: lambda ns: other + (other * ns), # x * y = y + (x - 1) * y
        })

    def __pow__(self, other):
        return match(other, {
            Nat.O: lambda: Nat.S(Nat.O()), # forall x, x ** 0 = 1
            Nat.S: lambda no: self * (self ** no), # x ** y = x * x ** (y - 1)
        })

    def __lt__(self, other):
        return match(other, {
            Nat.O: lambda: False,
            Nat.S: lambda no:
                match(self, {
                    Nat.O: lambda: True,
                    Nat.S: lambda ns: ns < no,
                }),
        })

    def __ge__(self, other):
        return not self < other
    
    def to_int(self):
        return match(self, {
            Nat.O: lambda: 0,
            Nat.S: lambda n: 1 + n.to_int()
        })

    def __repr__(self):
        return repr(self.to_int())

zero = Nat.O()

two = Nat.S(Nat.S(Nat.O()))
three = Nat.S(two)
four = Nat.S

a27 = three ** three
print(a27)

print(two * two * two * two * two * two * three)

print(two == Nat.S(Nat.S(Nat.O())))
print(two == a27)