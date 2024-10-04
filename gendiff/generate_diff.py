import json
from gendiff.parsing import read_file
from gendiff.formaters import stylish
from gendiff.formaters import plain_formater


def generate_diff(file_path1, file_path2, format_name='stylish'):
    first_file = read_file(file_path1)
    second_file = read_file(file_path2)

    diff_tree = create_diff_tree(first_file, second_file)

    if format_name == 'stylish':
        diff_str = stylish(diff_tree)
    elif format_name == 'plain':
        diff_str = plain_formater(diff_tree)
    elif format_name == 'json':
        print(json.dumps(diff_tree))
    else:
        raise Exception(f'Unknown format name {format_name}!')

    return diff_str


def create_diff_tree(first_file, second_file):
    keys_union = sorted(set(first_file) | set(second_file))

    diff_tree = {}
    for key in keys_union:
        first_has_key = key in first_file
        second_has_key = key in second_file
        children = None

        # remove
        if not second_has_key:
            change_type = 'remove'
            value = first_file[key]

        # add
        elif not first_has_key:
            change_type = 'add'
            value = second_file[key]

        else:
            first_value, second_value = first_file[key], second_file[key]

            # remain
            if first_value == second_value:
                change_type = 'remain'
                value = first_value

            # recursive step for nested dicts
            elif (isinstance(first_value, dict)
                  and isinstance(second_value, dict)):
                change_type = 'remain'
                value = None
                children = create_diff_tree(first_value, second_value)

            # update
            else:
                change_type = 'update'
                value = [first_file[key], second_file[key]]

        diff_tree[key] = {
            'change_type': change_type,
            'value': value,
            'children': children
        }

    return diff_tree
