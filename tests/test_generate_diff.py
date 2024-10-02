from gendiff import generate_diff


def test_generate_diff():
    file_path1 = 'tests/fixtures/file1.json'
    file_path2 = 'tests/fixtures/file2.json'
    expected = open('tests/fixtures/json_diff_expected.txt').read()
    assert generate_diff(file_path1, file_path2) == expected
