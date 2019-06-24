class Self(object):
    pass

class Unit(object):
    pass

class _(object):
    pass

def tagged_union(cls):
    assert(issubclass(cls, object))

    class TaggedUnionMember(cls):
        def __init__(self, name, args):
            self.name = name
            self.args = args

        def __repr__(self):
            if '__repr__' in vars(cls):
                return cls.__repr__(self)
            else:
                return cls.__name__ + "." + self.name + repr(self.args)

        def __eq__(self, other):
            return (self.name, self.args) == (other.name, other.args)

    class TaggedUnionMemberFactory(object):
        def __init__(self, name, types):
            for t in types:
                assert(isinstance(t, type))

            self._name = name
            self._types = types

        def __call__(self, *args):
            gen_types = (t for t in self._types)

            for arg in args:
                assert(isinstance(arg, next(gen_types)))

            assert(next(gen_types) == Unit)

            return TaggedUnionMember(self._name, args)

        def __eq__(self, other):
            return other == self._name

        def __hash__(self):
            return hash(self._name)

        def __repr__(self):
            return "Union of " + repr(self._types)

    # Union members are either types or tuples
    members = (v for v in vars(cls) if isinstance(vars(cls)[v], (type, tuple)))

    for m in members:
        types = vars(cls)[m]

        if not isinstance(types, tuple):
            types = (types,)

        # Replace self references
        types = tuple(cls if t == Self else t for t in types)

        # Append a Unit to the end if not already present
        if not types[-1] == Unit: 
            types = tuple(list(types) + [Unit])

        setattr(cls, m, TaggedUnionMemberFactory(m, types))

    return cls

def match(u, branches):
    key = u.name if hasattr(u, 'name') else u

    if key in branches:
        action = branches[key]
    else:
        action = branches[_]

    args = u.args if hasattr(u, 'args') else tuple()

    return action(*args)
