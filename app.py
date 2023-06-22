import json
import base64
import xml.etree.ElementTree as ET

from fastapi import FastAPI, UploadFile, File
from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from utils import read_config, check_and_create_index, extract_data, store_file, launch_ingestion_pipeline

app = FastAPI()

# Read the configuration file
config = read_config('config.yaml')

# Access the configuration values
es_host = config['elasticsearch']['host']
es_port = config['elasticsearch']['port']
es_xml_index = config['elasticsearch']['xml_index']
es_docx_index = config['elasticsearch']['docx_index']
es_pdf_index = config['elasticsearch']['pdf_index']
es_ca_cert = config['elasticsearch']['ca_cert']
es_username = config['elasticsearch']['username']
es_password = config['elasticsearch']['password']

# Elasticsearch client
es = Elasticsearch([{'host': es_host, 'port': es_port, 'scheme': 'https'}],
    http_auth=(es_username, es_password),
    ca_certs=es_ca_cert
)

@app.post("/upload")
async def upload_file(xml_file: UploadFile = File(...), docx_file: UploadFile = File(None), pdf_file: UploadFile = File(None)):

    index_names = [es_xml_index, es_docx_index, es_pdf_index]
    for index_name in index_names:
        check_and_create_index(es, index_name)
    
    if xml_file:
        xml_contents = await xml_file.read()

        # Process the XML file here        
        root = ET.fromstring(xml_contents)

        # Create a document for each XML
        data = extract_data(root)
        data['Content'] = json.dumps(data)

        # Index the document in Elasticsearch
        es.index(index=es_xml_index, body=data)

        # Refresh the index to make the documents searchable
        es.indices.refresh(index=es_xml_index)

        # Store the XML file to a local path
        xml_file_path = f"uploads/xml/{xml_file.filename}"
        store_file(xml_contents, xml_file_path)

    if docx_file:
        docx_contents = await docx_file.read()
        
        # Store the .docx attachment to a local path
        docx_file_path = f"uploads/docx/{docx_file.filename}"
        store_file(docx_contents, docx_file_path)
        
        # Encode the docx contents as Base64
        docx_base64 = base64.b64encode(docx_contents).decode("utf-8")
        
        # Launch the Elasticsearch docx ingestion pipeline
        status_code = launch_ingestion_pipeline(docx_file.filename, {"filename": docx_file.filename, "data": docx_base64}, es_docx_index, "docx_attachment_pipeline", es_username, es_password, "http_ca.crt")

        # Check the response status
        if status_code == 200:
            print("Elasticsearch docx ingestion pipeline executed successfully.")
        else:
            print(f"Elasticsearch docx ingestion pipeline execution failed. Status code: {status_code}")

    if pdf_file:
        pdf_contents = await pdf_file.read()

        # Store the .pdf attachment to a local path
        pdf_file_path = f"uploads/pdf/{pdf_file.filename}"
        store_file(pdf_contents, pdf_file_path)

        # Encode the pdf contents as Base64
        pdf_base64 = base64.b64encode(pdf_contents).decode("utf-8")
        
        # Launch the Elasticsearch pdf ingestion pipeline
        status_code = launch_ingestion_pipeline(docx_file.filename, {"filename": pdf_file.filename, "data": pdf_base64}, es_pdf_index, "pdf_attachment_pipeline", es_username, es_password, "http_ca.crt")

        # Check the response status
        if status_code == 200:
            print("Elasticsearch pdf ingestion pipeline executed successfully.")
        else:
            print(f"Elasticsearch pdf ingestion pipeline execution failed. Status code: {status_code}")

    return {"message": "Files processed and stored successfully."}

@app.get("/xml-index")
async def get_items():
    items = []

    # Use the scan API to retrieve all items in the index
    scanner = scan(client=es, index=es_xml_index, query={"query": {"match_all": {}}})

    # Iterate over the scan results
    for result in scanner:
        items.append(result['_source'])

    return items

@app.get("/xml-index/{search_term}")
async def get_items(search_term: str):

    # Define the query using Elasticsearch DSL
    query = {
        "query": {
            "match": {
                "Header.DocumentaryUnitType.keyword": search_term
            }
        }
    }

    # Execute the query
    response = es.search(
        index=es_xml_index,
        body=query
    )

    return response['hits']['hits']

@app.get("/docx-attachments")
async def get_docx_attachments():
    items = []

    # Use the scan API to retrieve all items in the index
    scanner = scan(client=es, index=es_docx_index, query={"query": {"match_all": {}}})

    # Iterate over the scan results
    for result in scanner:
        items.append(result['_source'])

    return items

@app.get("/docx-attachments/{search_term}")
async def get_docx_attachments(search_term: str):
    
    # Define the query using Elasticsearch DSL
    query = {
        "query": {
            "query_string": {
                "default_field": "attachment.content", 
                "query": search_term
        }
    }
    }

    # Execute the query
    response = es.search(
        index=es_docx_index,
        body=query
    )

    return response['hits']['hits']

@app.get("/pdf-attachments")
async def get_pdf_attachments():
    items = []

    # Use the scan API to retrieve all items in the index
    scanner = scan(client=es, index=es_pdf_index, query={"query": {"match_all": {}}})

    # Iterate over the scan results
    for result in scanner:
        items.append(result['_source'])

    return items

@app.get("/pdf-attachments/{search_term}")
async def get_pdf_attachments(search_term: str):
    
    # Define the query using Elasticsearch DSL
    query = {
        "query": {
            "query_string": {
                "default_field": "attachment.content", 
                "query": search_term
        }
    }
    }

    # Execute the query
    response = es.search(
        index=es_pdf_index,
        body=query
    )

    return response['hits']['hits']

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)