from tagged_union import Unit, Self, tagged_union, match

@tagged_union
class BTree(object):
    branch = (Self, Self, object)
    leaf = Unit

    def add(self, data):
        return match(self, {
            BTree.leaf: lambda: BTree.branch(BTree.leaf(), BTree.leaf(), data),
            BTree.branch: lambda l, r, d:
                BTree.branch(l.add(data), r, d) if data <= d \
                    else BTree.branch(l, r.add(data), d)
        })

    def __repr__(self):
        return match(self, {
            BTree.leaf: lambda: "",
            BTree.branch: lambda l, r, d:
                repr(l) + "/" + repr(d) + "\\" + repr(r),
        })

empty_btree = BTree.leaf()

print(empty_btree == BTree.leaf())

a = empty_btree.add(5)

print(a)

b = a.add(6)

print(b)

c = b.add(4)

print(c)
