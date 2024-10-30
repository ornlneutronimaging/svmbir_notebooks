def retrieve_parameters(instance):
    list_all_variables = dict(instance)
    list_variables = [var for var in list_all_variables if not var.startswith('__')]
    my_dict = {_variable: getattr(instance, _variable) for _variable in list_variables}
    return my_dict
