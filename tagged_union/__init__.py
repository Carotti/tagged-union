"""Tagged Unions

Python tagged unions (aka sum types, algebraic data types, etc.) are a common
tool in functional and functional style programming. This module provides a
class decorator to concisely specify tagged unions (including recursively) as
well as a match function for easily interacting with them.

To specify a class as a tagged union, decorate it with `tagged_union`. Note for
Python2, this class must also inherit from `object`. This is no longer
necessary in Python3. The possible members of the tagged union are specified as
class attributes, equal to a type or tuple of types representing how that union
member should be constructed. All tagged union members inherit from the orignal
tagged union class, allowing common implementations inside this class.

Example:
    The following example creates a tagged union which has two members, `Foo`
    and `Bar`. `Foo` accepts no arguments as its constructor and `Bar` accepts
    an instance of MyTaggedUnion (either another `Bar` or a `Foo`)::

        @tagged_union
        class MyU:
            Foo = Unit
            Bar = Self

        test = MyU.Bar(MyU.Bar(MyU.Bar(MyU.Foo())))

Attributes:
    Self (type): For defining recursive tagged unions. `Self` is replaced with
    the type of the tagged union class itself.

    Unit (type): Use as a type for tagged union members who accept no arguments
        in their constructors. Also used internally as a sentinel to check that
        the correct number of arguments were given to a tagged union member's
        constructor.

    _ (object): Used for wildcard matching. The corresponding dictionary value
        for the key of `_` is called if the object being matched doesn't match
        any of the other dictionary keys.

"""

Self = type("Self", (object,), {})

Unit = type("Unit", (object,), {})

_ = object()

def tagged_union(cls):
    """Tagged Union class decorator.

    Any members of the given class which are either types or tuples are
    converted into tagged union members, allowing members to be constructed
    from their identifiers.

    Args:
        cls (type): The class to be converted to a tagged union

    Returns:
        type: The updated class with updated relevant members.
    """
    assert issubclass(cls, object)

    class TaggedUnionMember(cls):
        """A tagged union member.

        Specified in and inherits from `cls`, is uniquely identified by its
        tag (`self.name`), and the arguments given to the constructor
        (`self.args). Has a default implementation of `__repr__` which prints
        out the canonical way of constructing an identical class, but can be
        overidden in `cls`. Also implements equality between different
        instances of the same tagged union members, provided their tag and
        constructor arguments are identical.

        """
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

        def __hash__(self):
            return hash((self.name, self.args))

    class TaggedUnionMemberFactory:
        """Helper class for creating tagged union members.

        The identifiers used in a tagged union class are replaced with
        `TaggedUnionMemberFactory`s for their relevant members. This
        checks the types on construction of a member and can also be used
        for matching these types using the `match` function.

        """
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
    """Match statement for tagged unions (and other purposes).

    Allows matching of instances of tagged union members against their type.
    Can also just be used as a switch-like statement if used with other objects
    such as `int`s. Uses the tagged union member's constructor arguments as the
    arguments to the matching branch's function.

    Args:
        union (object): The object to be matches
        branches (dict of object: function): A dict of which functions to call
            under the different matches. `_` can be used for wildcard matching.

    Returns:
        object: The result of calling the matches function with the arguments
            of the matched object.
    """

    key = union.name if hasattr(union, 'name') else union

    if key in branches:
        action = branches[key]
    else:
        action = branches[_]

    args = union.args if hasattr(union, 'args') else tuple()

    return action(*args)
