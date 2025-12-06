import os

def read_file(filename):
    file_path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "prompts"), filename)
    with open(file_path, 'r') as file_contents:
        return file_contents.read()
    
def get_base_workdir():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "../")

def get_file_name(filename):
    return os.path.basename(filename).split(".py")[0]