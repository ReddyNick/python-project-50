import pytest

from pathlib import Path
from gendiff import generate_diff
from gendiff.formaters.stylish import stringify


def test_stringify():
    data = {
        "hello": None,
        "is": True,
        "nested": {
            "count": 5,
            "nested 2": {
                "name": "23",
                "list": [10, 23]
            }
        },
    }

    expected = """\
{
    hello: null
    is: true
    nested: {
        count: 5
        nested 2: {
            name: 23
            list: [10, 23]
        }
    }
}\
"""
    assert '\n'.join(stringify(data)) == expected


@pytest.fixture
def inputs_flat():
    file_path1 = 'tests/fixtures/test_flat/file1.json'
    file_path2 = 'tests/fixtures/test_flat/file2.json'
    expected = open('tests/fixtures/test_flat/json_diff_expected.txt').read()
    return (file_path1, file_path2, expected)


@pytest.fixture
def inputs_nested():
    file_path1 = 'tests/fixtures/test_nested/file1.json'
    file_path2 = 'tests/fixtures/test_nested/file2.json'
    return (file_path1, file_path2)


@pytest.fixture
def expected_nested():
    expected = open('tests/fixtures/test_nested/json_diff_expected.txt').read()
    return expected


@pytest.fixture
def expected_nested_plain():
    expected = open('tests/fixtures/test_nested/plain_diff_expected.txt').read()
    return expected


def test_generate_diff_json_inputs(inputs_flat):
    file_path1, file_path2, expected = inputs_flat
    assert generate_diff(file_path1, file_path2) == expected


def test_generate_diff_yaml_inputs(inputs_flat):
    file_path1, file_path2, expected = inputs_flat
    file_path1 = str(Path(file_path1).with_suffix('.yml'))
    file_path2 = str(Path(file_path2).with_suffix('.yml'))
    assert generate_diff(file_path1, file_path2) == expected


def test_generate_diff_mixed_inputs(inputs_flat):
    file_path1, file_path2, expected = inputs_flat
    file_path1 = str(Path(file_path1).with_suffix('.yml'))
    assert generate_diff(file_path1, file_path2) == expected


def test_generate_diff_nested_json_inputs(inputs_nested, expected_nested):
    file_path1, file_path2 = inputs_nested
    assert generate_diff(file_path1, file_path2) == expected_nested


def test_generate_diff_nested_plain(inputs_nested, expected_nested_plain):
    file_path1, file_path2 = inputs_nested
    output = generate_diff(file_path1, file_path2, 'plain')
    assert output == expected_nested_plain
