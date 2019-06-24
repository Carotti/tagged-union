from tagged_union import *

def test_match_int():
    result = match(5, {
        5: lambda: 1
    })

    assert result == 1

def test_tagged_union_subclass():
    @tagged_union
    class A:
        B = Self
        C = int

    c = A.C(1)
    b = A.B(c)

    assert isinstance(b, A)
    assert isinstance(c, A)
