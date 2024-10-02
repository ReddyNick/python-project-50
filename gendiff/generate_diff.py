import json


def read_file(file_path):
    return json.load(open(file_path))


def diff_json(first_file, second_file, keys_union):
    diff_lines = []
    for key in keys_union:
        first_has_key = key in first_file
        second_has_key = key in second_file
        if first_has_key and not second_has_key:
            diff_lines.append(f'- {key}: {first_file[key]}')
        elif not first_has_key and second_has_key:
            diff_lines.append(f'+ {key}: {second_file[key]}')
        elif first_has_key and second_has_key:
            first_value, second_value = first_file[key], second_file[key]
            if first_value == second_value:
                diff_lines.append(f'  {key}: {first_file[key]}')
            else:
                diff_lines.append(f'- {key}: {first_file[key]}')
                diff_lines.append(f'+ {key}: {second_file[key]}')

    diff_lines = '\n  '.join(diff_lines)
    diff_lines = '{\n  ' + diff_lines + '\n}'
    return diff_lines


def generate_diff(file_path1, file_path2):
    first_file = read_file(file_path1)
    second_file = read_file(file_path2)

    keys_union = set(first_file) | set(second_file)
    keys_union = sorted(keys_union)

    diff_function = diff_json
    diff_output_str = diff_function(first_file, second_file, keys_union)

    return diff_output_str
