import json


def plain_formater(diff_tree, parent=''):
    output = []
    for key, node in diff_tree.items():
        change_type = node['change_type']
        if change_type == 'remove':
            output.append(remove_diff_str(key, parent))
        if change_type == 'add':
            output.append(add_diff_str(key, node['value'], parent))
        if change_type == 'update':
            output.append(update_diff_str(key, node['value'], parent))
        if change_type == 'remain' and node['children'] is not None:
            nested_diff = plain_formater(node['children'], parent + key + '.')
            output.append(nested_diff)

    return '\n'.join(output)


def plain_json_stringify(value):
    if isinstance(value, dict):
        return '[complex value]'
    if isinstance(value, str):
        return f"'{value}'"
    return json.dumps(value).strip('"')


def remove_diff_str(key, parent):
    return f"Property '{parent + key}' was removed"


def add_diff_str(key, value, parent):
    value = plain_json_stringify(value)
    return f"Property '{parent + key}' was added with value: {value}"


def update_diff_str(key, values, parent):
    value1, value2 = [plain_json_stringify(v) for v in values]
    return f"Property '{parent + key}' was updated. From {value1} to {value2}"
