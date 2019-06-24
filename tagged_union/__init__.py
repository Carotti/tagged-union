Self = type("Self", (object,), {})

Unit = type("Unit", (object,), {})

_ = object()

def tagged_union(cls):
    assert issubclass(cls, object)

    class TaggedUnionMember(cls):
        def __init__(self, name, args):
            self.name = name
            self.args = args

        def __repr__(self):
            if '__repr__' in vars(cls):
                rep = cls.__repr__(self)
            else:
                rep = cls.__name__ + "." + self.name + repr(self.args)

            return rep

        def __eq__(self, other):
            return (self.name, self.args) == (other.name, other.args)

    class TaggedUnionMemberFactory:
        def __init__(self, name, types):
            for typ in types:
                assert isinstance(typ, type)

            self._name = name
            self._types = types

        def __call__(self, *args):
            gen_types = (t for t in self._types)

            for arg in args:
                assert isinstance(arg, next(gen_types))

            assert next(gen_types) == Unit

            return TaggedUnionMember(self._name, args)

        def __eq__(self, other):
            return other == self._name

        def __hash__(self):
            return hash(self._name)

        def __repr__(self):
            return "Union of " + repr(self._types)

    # Union members are either types or tuples
    members = (v for v in vars(cls) if isinstance(vars(cls)[v], (type, tuple)))

    for mem in members:
        types = vars(cls)[mem]

        if not isinstance(types, tuple):
            types = (types,)

        # Replace self references
        types = tuple(cls if t == Self else t for t in types)

        # Append a Unit to the end if not already present
        if not types[-1] == Unit:
            types = tuple(list(types) + [Unit])

        setattr(cls, mem, TaggedUnionMemberFactory(mem, types))

    return cls

def match(union, branches):
    key = union.name if hasattr(union, 'name') else union

    if key in branches:
        action = branches[key]
    else:
        action = branches[_]

    args = union.args if hasattr(union, 'args') else tuple()

    return action(*args)
