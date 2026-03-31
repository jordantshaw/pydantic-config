from pydantic_config.merge import deep_merge


def test_non_overlapping_keys():
    assert deep_merge({'a': 1}, {'b': 2}) == {'a': 1, 'b': 2}


def test_nested_dict_merge():
    base = {'app': {'name': 'foo', 'version': '1'}}
    nxt = {'app': {'version': '2', 'debug': True}}
    assert deep_merge(base, nxt) == {'app': {'name': 'foo', 'version': '2', 'debug': True}}


def test_scalar_override():
    assert deep_merge({'key': 'original'}, {'key': 'overridden'}) == {'key': 'overridden'}


def test_list_merge_unique():
    result = deep_merge({'items': [1, 2, 3]}, {'items': [3, 4, 5]}, unique=True)
    assert result == {'items': [1, 2, 3, 4, 5]}


def test_list_merge_non_unique():
    result = deep_merge({'items': [1, 2, 3]}, {'items': [3, 4, 5]}, unique=False)
    assert result == {'items': [1, 2, 3, 3, 4, 5]}


def test_does_not_mutate_base():
    base = {'app': {'name': 'foo'}}
    deep_merge(base, {'app': {'name': 'bar'}})
    assert base == {'app': {'name': 'foo'}}


def test_does_not_mutate_nxt():
    nxt = {'app': {'name': 'bar'}}
    deep_merge({'app': {'name': 'foo'}}, nxt)
    assert nxt == {'app': {'name': 'bar'}}
