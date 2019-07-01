from tagged_union import *

def test_match_int():
    result = match(5, {
        5: lambda: 1
    })

    assert result == 1

@tagged_union
class A(object):
    B = Self
    C = int

c = A.C(1)
b = A.B(c)

def test_tagged_union_subclass():
    assert isinstance(b, A)
    assert isinstance(c, A)

def test_repr_default():
    assert repr(c) == "A.C(1,)"
    assert repr(b) == "A.B(A.C(1,),)"

def test_eq_default():
    assert c == A.C(1)
    assert b == A.B(c)
    assert b == A.B(A.C(1))

@tagged_union
class ReprUnion(object):
    B = Self
    C = int

    def __repr__(self):
        return match(self, {
            A.B: lambda _: "BBB",
            A.C: lambda _: "CCC",
        })

cr = ReprUnion.C(1)
br = ReprUnion.B(cr)

def test_repr_override():
    assert repr(cr) == "CCC"
    assert repr(br) == "BBB"
