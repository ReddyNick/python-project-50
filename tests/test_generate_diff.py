from gendiff import generate_diff


def test_generate_diff_json_inputs():
    file_path1 = 'tests/fixtures/test_flat/file1.json'
    file_path2 = 'tests/fixtures/test_flat/file2.json'
    expected = open('tests/fixtures/test_flat/json_diff_expected.txt').read()
    assert generate_diff(file_path1, file_path2) == expected


def test_generate_diff_yaml_inputs():
    file_path1 = 'tests/fixtures/test_flat/file1.yml'
    file_path2 = 'tests/fixtures/test_flat/file2.yml'
    expected = open('tests/fixtures/test_flat/json_diff_expected.txt').read()
    assert generate_diff(file_path1, file_path2) == expected


def test_generate_diff_mixed_inputs():
    file_path1 = 'tests/fixtures/test_flat/file1.yml'
    file_path2 = 'tests/fixtures/test_flat/file2.json'
    expected = open('tests/fixtures/test_flat/json_diff_expected.txt').read()
    assert generate_diff(file_path1, file_path2) == expected
