from config.chat import ChatGPT
from config import config
import os

def read_prompt(filename):
    file_path = os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "prompts"), filename)
    with open(file_path, 'r') as file_contents:
        return file_contents.read()
    
def get_function_name(filename):
    return os.path.basename(filename).split(".py")[0]

def create_vector_store(vector_store_name):
    vector_store = ChatGPT().client.vector_stores.create( 
        name=vector_store_name,
    )
    return vector_store.id

def upload_file_to_vector_store(vector_store_id, filename):
    ChatGPT().client.vector_stores.files.upload_and_poll(
        vector_store_id=vector_store_id,
        file=open(filename, "rb")
    )

def search_vector_store(vector_store_id, search_query):
    results = ChatGPT().client.vector_stores.search(
        vector_store_id=vector_store_id,
        query=search_query,
    )
    # Concatenate all the returned information to pass it to the new prompt
    context_info = ""
    for data in results.data:
        for content in data.content:
            context_info += f"{content.text}\n"
    context_info