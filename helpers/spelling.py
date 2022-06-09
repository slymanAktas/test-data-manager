import re


def camelCase_to_snake_case(variable_name):
    variable_name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', variable_name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', variable_name).lower()


def snake_case_to_camelCase(variable_name):
    variable_name = ''.join(word.title() for word in variable_name.split('_'))

    return variable_name[0].lower() + variable_name[1:]


def make_boolean_as_pythonic(param):
    return True if str(param).lower() == 'true' else False


def sql_semicolon_controller(sql_text):
    return sql_text[:-1] if str(sql_text[-1]).__eq__(";") else sql_text
