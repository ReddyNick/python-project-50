import json


def generate_diff(file_path1, file_path2):
    first_file = read_file(file_path1)
    second_file = read_file(file_path2)

    keys_union = set(first_file) | set(second_file)
    keys_union = sorted(keys_union)

    diff_function = diff_function_json
    diff_post_processing = diff_post_processing_json

    diff_output_str = diff_engine(first_file, second_file, keys_union,
                                  diff_function, diff_post_processing)

    return diff_output_str


def read_file(file_path):
    return json.load(open(file_path))


def diff_engine(first_file, second_file, keys_union,
                diff_function, diff_post_processing):
    change_types = get_change_types(first_file, second_file, keys_union)

    diff_lines = []
    for key, change_type in change_types:
        diff_lines.extend(diff_function(first_file, second_file,
                                        key, change_type))

    diff_str = diff_post_processing(diff_lines)
    return diff_str


def get_change_types(first_file, second_file, keys_union):
    change_types = []
    for key in keys_union:
        first_has_key = key in first_file
        second_has_key = key in second_file
        if first_has_key and not second_has_key:
            change_types.append((key, 'remove'))
        elif not first_has_key and second_has_key:
            change_types.append((key, 'add'))
        elif first_has_key and second_has_key:
            first_value, second_value = first_file[key], second_file[key]
            if first_value == second_value:
                change_types.append((key, 'remain'))
            else:
                change_types.append((key, 'edit'))

    return change_types


def diff_function_json(first_file, second_file, key, type):
    diff_lines = []
    if type == 'remove':
        key_str, value_str = get_json_diff_key_value('-', key, first_file[key])
        diff_lines.append(f'{key_str}: {value_str}')
    elif type == 'add':
        key_str, value_str = get_json_diff_key_value('+', key, second_file[key])
        diff_lines.append(f'{key_str}: {value_str}')
    elif type == 'remain':
        key_str, value_str = get_json_diff_key_value(' ', key, first_file[key])
        diff_lines.append(f'{key_str}: {value_str}')
    elif type == 'edit':
        key_str_1, value_str_1 = get_json_diff_key_value('-', key,
                                                         first_file[key])
        key_str_2, value_str_2 = get_json_diff_key_value('+', key,
                                                         second_file[key])
        diff_lines.append(f'{key_str_1}: {value_str_1}')
        diff_lines.append(f'{key_str_2}: {value_str_2}')
    else:
        raise Exception(f'Uknown change type {type}!')

    return diff_lines


def diff_post_processing_json(diff_lines):
    diff_lines = '\n  '.join(diff_lines)
    diff_str = '{\n  ' + diff_lines + '\n}'
    return diff_str


def get_json_diff_key_value(prefix, key, value):
    key = f'{prefix} {key}'
    value = json.dumps(value).strip('"')
    return key, value
