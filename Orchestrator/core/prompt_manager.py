import os

def read_prompt(filename):
    file_path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "prompts"), filename)
    with open(file_path, 'r') as file_contents:
        return file_contents.read()