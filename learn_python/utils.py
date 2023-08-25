import importlib


def import_string(str_to_import):
    module_name, attr_name = str_to_import.rsplit('.', 1)
    module = importlib.import_module(module_name)
    return getattr(module, attr_name)
