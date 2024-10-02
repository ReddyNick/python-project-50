from gendiff import generate_diff


def test_generate_diff():
    file_path1 = 'tests/test_files/file1.json'
    file_path2 = 'tests/test_files/file2.json'
    expected = open('tests/test_files/json_diff_expected.txt').read()
    assert generate_diff(file_path1, file_path2) == expected
