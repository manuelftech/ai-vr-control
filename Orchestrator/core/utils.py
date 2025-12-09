import os

def read_file(filename):
    file_path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "prompts"), filename)
    with open(file_path, 'r') as file_contents:
        return file_contents.read()
    
def get_base_workdir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")

def get_file_name(filename):
    return os.path.basename(filename).split(".py")[0]

def update_nested_key(data, path, value):
    current_value = data
    keys = path.split('.')
    for index, key in enumerate(keys):
        previous_value = current_value
        try:
            current_value = current_value[key]
            if index == len(keys):
                previous_value[key] = value
        except (KeyError, TypeError):
            pass