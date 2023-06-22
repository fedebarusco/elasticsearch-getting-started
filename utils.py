import yaml
import json
import os
import requests

def read_config(filename):
    with open(filename, 'r') as file:
        config = yaml.safe_load(file)
    return config

def check_and_create_index(es, index_name):
    # Check if the index exists, otherwise create it
    if es.indices.exists(index=index_name):
        print(f"The index '{index_name}' already exists.")
    else:
        print(f"The index '{index_name}' does not exist.")
        es.indices.create(index=index_name)

def extract_data(xml):
    # Iterate over XML elements and store them in a dictionary
    data = {}
    for child in xml:
        if len(child) == 0:
            data[child.tag] = child.text
        else:
            data[child.tag] = extract_data(child)
    return data

def store_file(contents, file_path):
    # Create the "uploads" directory if it doesn't exist
    directory = os.path.dirname(file_path)
    os.makedirs(directory, exist_ok=True)
    # Store the file to a local path
    with open(file_path, "wb") as local_file:
        local_file.write(contents)

def launch_ingestion_pipeline(filename, data, es_index, es_pipeline, es_username, es_password, ca_cert):
    url = f"https://localhost:9200/{es_index}/_doc/1?pipeline={es_pipeline}"
    headers = {
        "Content-Type": "application/json",
    }
    auth = (es_username, es_password)
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data), auth=auth, verify=ca_cert)
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error occurred during the request: {e}")
        return None