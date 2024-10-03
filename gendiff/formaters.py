import json


def stylish(diff_tree):
    return '\n'.join(stylish_lines(diff_tree))


def stylish_lines(diff_tree, padding=4):
    output = []
    for key, node in diff_tree.items():
        change_type = node['change_type']
        if change_type == 'edit':
            value1, value2 = node['value']

            value1_lines = stringify(value1)
            diff_lines = construct_key_diff(key, value1_lines,
                                            prefix='-', padding=padding)
            output.extend(diff_lines)

            value2_lines = stringify(value2)
            diff_lines = construct_key_diff(key, value2_lines,
                                            prefix='+', padding=padding)
            output.extend(diff_lines)
        else:
            if node['children'] is None:
                value_diff_lines = stringify(node['value'])
            else:
                value_diff_lines = stylish_lines(node['children'])

            if change_type == 'remove':
                prefix = '-'
            elif change_type == 'add':
                prefix = '+'
            elif change_type == 'remain':
                prefix = ' '
            diff_lines = construct_key_diff(key, value_diff_lines,
                                            prefix, padding)
            output.extend(diff_lines)

    # output = map(lambda s: '  ' + s, output)
    output = ['{', *output, '}']
    return output


def construct_key_diff(key, lines, prefix, padding):
    lines[0] = f'{prefix} {key}: {lines[0]}'
    lines[0] = pad(lines[0], padding - len(prefix) - 1)
    for i in range(1, len(lines)):
        lines[i] = pad(lines[i], padding)
    return lines


def pad(str, padding, character=' '):
    return character * padding + str


def stringify(data, replacer=' ', spacesCount=4):
    if not isinstance(data, dict):
        return [json.dumps(data).strip('"')]

    lines = []
    for key, value in data.items():
        if not isinstance(value, dict):
            value_str = json.dumps(value).strip('"')
            lines.append(f'{key}: {value_str}')
        else:
            nested_lines = stringify(value, replacer, spacesCount)
            nested_lines[0] = f'{key}: {nested_lines[0]}'
            lines.extend(nested_lines)

    lines = map(lambda s: replacer * spacesCount + s, lines)
    lines = ['{', *lines, '}']

    return lines
