# Elasticsearch Getting Started

**Project Name**: *ElasticXML*

This repository is an example project that combines Elasticsearch and Python to build a metadata and full-text search system. The system will allow users to upload and store documents, as well as retrieve and search for them based on different criteria.

This is just a high-level overview of a project combining Elasticsearch and Python. It can be expanded on this foundation or customized it to fit the specific requirements.

## Table of Contents
- [Table of Contents](#table-of-contents)
- [General Information](#general-information)
- [Technologies Used](#technologies-used)
- [Features](#features)
- [Implementation Steps](#implementation-steps)
- [Elasticsearch](#elasticsearch)
  - [Elasticsearch Installation](#elasticsearch-installation)
  - [Running Elasticsearch](#running-elasticsearch)
  - [Elasticsearch as a Database](#elasticsearch-as-a-database)
  - [Basic Terms](#basic-terms)
- [Logstash](#logstash)
  - [Logstash Installation](#logstash-installation)
  - [Running Logstash](#running-logstash)
- [Kibana](#kibana)
  - [Kibana Installation](#kibana-installation)
  - [Running Kibana](#running-kibana)
- [Project Overview](#project-overview)
  - [Data Model](#data-model)
- [Usage](#usage)
  - [Microservices Approach](#microservices-approach)
    - [Endpoints](#endpoints)
    - [Tests](#tests)
  - [Ingest Processor Approach](#ingest-processor-approach)
  - [Logstash Pipeline Approach](#logstash-pipeline-approach)
- [ToDo](#todo)

## General Information

The repository is organized as follows:

    .
    ├── data                             # Sample input data to the microservice and the Elasticsearch pipeline
    │   ├── dummy-file.xml               # Sample input .xml to the microservice
    │   ├── lorem-ipsum.docx             # Sample input .docx to the microservice
    │   └── muspi-merol.pdf              # Sample input .pdf to the microservice 
    ├── ingest-attachment-pipelines      # Elasticsearch pipelines 
    │   ├── attachment_pipeline.json     # Pipeline to ingest attachment and store it in an ES index
    │   └── xml_pipeline.json            # Pipeline to ingest XML file and store it in an ES index
    ├── logstash-pipelines               # Logstash pipelines
    │   └── logstash_pipeline.conf       # Pipeline to ingest XML file and store it in an ES index
    ├── uploads                          # Stored files
    |   ├── docx                         # Stored docx files
    |   |   └── lorem-ipsum.docx         # Example of stored docx file
    |   ├── pdf                          # Stored pdf files
    |   |   └── muspi-merol.pdf          # Example of stored pdf file
    |   └── xml                          # Stored xml files
    |       └── dummy-file.xml           # Example of stored xml file 
    ├── .gitignore                       # Git ignored files
    ├── app.py                           # Main script
    ├── config.yaml                      # Configuration file
    ├── http_ca.crt                      # Elasticsearch ca certificate
    ├── postman_collection.json          # Postman collection
    ├── README.md                        # README
    ├── requirements.txt                 # Requirements for pip
    └── utils.py                         # Utils


## Technologies Used

* Elasticsearch - version 8.8.0 - Powerful and scalable search and analytics engine with lightning-fast data retrieval and advanced querying capabilities.
* Python - version 3.10.6 - Programming language used for the backend development and interaction with Elasticsearch.
* FastAPI - version 0.95.2 - High-performance web framework for building APIs with Python, known for its speed, simplicity, and type annotations-based approach.

## Features

* Add Document: Users can index new metadata documents to the inventory by providing an XML file containing the related details.
* Search Documents: Users can search for documents based on metadata attributes and retrieve a list of matching documents.
* Display Inventory: Users can view the complete inventory of documents, including all details.

## Implementation Steps

1. Set up Elasticsearch: Install Elasticsearch and start it.
2. Set up a Python virtual environment and install the necessary dependencies (FastAPI and Elasticsearch).
3. Create an application with routes to handle the different functionalities of the document management system (add, search, display).
4. Implement the necessary Python functions to interact with Elasticsearch. This includes connecting to the engine, performing operations, and handling search queries.
5. Test the application by running the server and interacting with the different functionalities.

## Elasticsearch 

### Elasticsearch Installation

This guide is based on Ubuntu 22.04.2 LTS ("Jammy") running through WSL2. To check the version of Ubuntu installed on your system you can use the ``lsb_release`` command: 
```console
lsb_release -a
```

In order to install Elasticsearch with Debian package, replicate the following steps: 
1. From a terminal, install ``apt-transport-https`` if it is not already installed:
    ```console
    sudo apt-get update
    sudo apt-get install apt-transport-https
    ```
    Then, import the Elasticsearch public PGP Key:
    ```console
    wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
   ```
2. Save the repository definition by creating the list file /etc/apt/sources.list.d/elastic-8.x.list: 
    ```console
    echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
    ```
3. Reload the local package database: 
    ```console
    sudo apt-get update
    ```
4. Install Elasticsearch: 
    ```console
    sudo apt-get install elasticsearch
    ```
    **Note:** remember that ``apt-get`` will upgrade the packages when a newer version becomes available. 

For more information about the installation process: [Install Elasticsearch with Debian Package](https://www.elastic.co/guide/en/elasticsearch/reference/8.8/deb.html)

### Running Elasticsearch

To check which init system (``systemd`` or ``service``) your platform uses in order to run elasticsearch, run the following command:
```console
ps --no-headers -o comm 1
```

Run the ``elasticsearch`` process by using the operating system's built-in init system (e.g. ``systemd``):
1. Start the elasticsearch process by running the following command: 
    ```console
    sudo systemctl start elasticsearch.service
    ```
2. Verify that Elasticserach has started successfully (it may take some time): 
    ```console
    curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic https://localhost:9200
    ```
3. When prompted, specify the ``elastic`` user's password that was generated during installation, which should return a response like this:: 
    ```json
    {
    "name" : "Cp8oag6",
    "cluster_name" : "elasticsearch",
    "cluster_uuid" : "AT69_T_DTp-1qgIJlatQqA",
    "version" : {
        "number" : "8.8.0",
        "build_flavor" : "default",
        "build_type" : "deb",
        "build_hash" : "c01029875a091076ed42cdb3a41c10b1a9a5a20f",
        "build_flavor" : "default",
        "build_date" : "2023-05-23T17:16:07.179039820Z",
        "build_snapshot" : false,
        "lucene_version" : "9.6.0",
        "minimum_wire_compatibility_version" : "7.17.0",
        "minimum_index_compatibility_version" : "7.0.0"
    },
    "tagline" : "You Know, for Search"
    }
    ```

### Elasticsearch as a Database

Even if its primary focus is on search and analytics rather than traditional database features like transactional consistency or ACID (Atomicity, Consistency, Isolation, Durability) properties, Elasticsearch is often categorized as a NoSQL database because it does not rely on the traditional relational model. It is designed to handle large volumes of unstructured or semi-structured data and provide fast, scalable search capabilities. 

While Elasticsearch stores and indexes data, allowing you to retrieve and analyze it, it has some differences compared to traditional databases. For example:
1. Schema flexibility: Elasticsearch does not enforce a strict schema for documents. You can dynamically add or modify fields without having to define a rigid schema beforehand.
2. Full-text search: Elasticsearch provides powerful full-text search capabilities, allowing you to perform complex searches and relevance scoring based on textual content.
3. Distributed architecture: Elasticsearch is designed to scale horizontally across multiple nodes, allowing you to distribute data and operations for high availability and performance. It uses sharding and replication techniques to achieve scalability.
4. Real-time data: Elasticsearch is optimized for near real-time data ingestion and retrieval. It excels at handling constantly changing data and providing fast search results.
5. Limited transactional support: While Elasticsearch supports basic CRUD operations (Create, Read, Update, Delete), it lacks full transactional consistency and does not provide features like joins or referential integrity constraints.

So, while Elasticsearch can serve as a data store and provide querying capabilities like a database, it is best suited for use cases that prioritize search, analytics, and scalability rather than traditional transactional requirements.

### Basic Terms

Here are some basic terms related to Elasticsearch along with their definitions:
- **Index**: A collection of documents with similar characteristics that are stored and organized together in Elasticsearch. It is the highest level of abstraction in Elasticsearch.
- **Document**: A basic unit of information that can be indexed and searched in Elasticsearch. It is represented as a JSON object and contains key-value pairs of fields and their corresponding values.
- **Type** (deprecated in Elasticsearch 7.x): A way to categorize documents within an index. In Elasticsearch 7.x and later versions, a single index can contain multiple document types.
- **Mapping**: A schema definition that describes the structure and properties of the fields within a document type or index. It defines the data types, analyzers, and other characteristics of the fields.
- **Field**: A named data element within a document that holds a single value or an array of values. Fields can be of various data types such as strings, numbers, booleans, dates, etc.
- **Analyzer**: A component responsible for converting text into terms during indexing and searching. It applies tokenization, normalization, and other text processing techniques to enable efficient and accurate searching.
- **Query**: A request to Elasticsearch to retrieve specific documents that match certain criteria. Queries can be simple or complex, and Elasticsearch provides a wide range of query types and capabilities.
- **Query** DSL: Query Domain-Specific Language is a JSON-based language used to construct queries in Elasticsearch. It provides a flexible and expressive way to define search criteria and perform advanced queries.
- **Aggregation**: A feature in Elasticsearch used to perform complex calculations and analytics on the data. Aggregations allow you to summarize and group data, calculate metrics, and generate statistical results.
- **Cluster**: A collection of one or more nodes (servers) that work together to store and process data in Elasticsearch. Clustering provides scalability, fault tolerance, and high availability.
- **Node**: A single server or instance within an Elasticsearch cluster. Each node stores data, performs indexing and searching operations, and participates in cluster management.
- **Shard**: Elasticsearch divides an index into multiple shards to distribute data and operations across different nodes in a cluster. Sharding allows horizontal scalability and parallel processing of data.
- **Replica**: Elasticsearch allows creating replicas of each shard to provide redundancy and improve performance. Replicas are exact copies of primary shards and serve read requests to increase search throughput.
- **Query**-time relevance scoring: Elasticsearch employs relevance scoring algorithms, such as the TF-IDF (Term Frequency-Inverse Document Frequency) and BM25 (Best Match 25), to determine the relevance of documents based on search queries.
These are some fundamental terms in Elasticsearch that should provide a good starting point.

## Logstash 

Logstash is an open-source data processing tool that is part of the Elastic Stack, which also includes Elasticsearch and Kibana. It is designed to collect, transform, and enrich data from various sources and then send it to different destinations, typically Elasticsearch for indexing and searching. So, the main purpose of Logstash is to facilitate the ingestion of data from diverse inputs such as log files, system metrics, databases, message queues, and more, allowing to parse, filter, and modify the incoming data before sending it to the desired output systems or storage repositories.

Logstash uses a pipeline-based architecture, where data flows through a sequence of stages. Each stage represents an input, filter, or output plugin, and you can configure multiple stages to handle complex data processing workflows:
- A wide range of input plugins is provided in order to support numerous data sources, including files, network protocols, APIs, and message brokers. 
- Logstash also offers various filter plugins to process and transform the data, enabling tasks like parsing structured logs, performing data enrichment, and applying conditional logic.
- Once the data is processed, Logstash can send it to various output plugins, such as Elasticsearch, Amazon S3, databases, message queues, and many others.

### Logstash Installation

This guide is based on Ubuntu 22.04.2 LTS ("Jammy") running through WSL2. To check the version of Ubuntu installed on your system you can use the ``lsb_release`` command: 
```console
lsb_release -a
```

In order to install Logstash with Debian package, supposing that you have already followed the installation process of Elasticsearch, replicate the following steps: 
1. From a terminal, reload the local package database: 
    ```console
    sudo apt-get update
    ```
4. Install Logstash: 
    ```console
    sudo apt-get install logstash
    ```
    **Note:** remember that ``apt-get`` will upgrade the packages when a newer version becomes available. 

For more information about the installation process: [Installing from Package Repositories](https://www.elastic.co/guide/en/logstash/current/installing-logstash.html)

### Running Logstash

To check which init system (``systemd`` or ``service``) your platform uses in order to run logstash, run the following command:
```console
ps --no-headers -o comm 1
```

Run the ``logstash`` process by using the operating system's built-in init system (e.g. ``systemd``).
1. Start the logstash process by running the following command: 
    ```console
    sudo systemctl start logstash.service
    ```
2. From terminal, launch the example pipeline provided to index the XML file: 
    ```console
    sudo /usr/share/logstash/bin/logstash -f /path/to/elasticsearch-getting-started/logstash-pipelines/logstash_pipeline.conf --debug
    ```
3. Kill the pipeline with Ctrl + C


## Kibana 

Kibana is an open-source data visualization and exploration tool designed to work with Elasticsearch. It provides a user-friendly interface to interact with data stored in Elasticsearch and helps in analyzing and visualizing large volumes of data. 

Here's a concise list of Kibana's features:
- Data Visualization: Kibana allows users to create interactive visualizations such as charts, graphs, maps, and histograms to represent data in a meaningful way.
- Dashboard Creation: It enables the creation of customized dashboards by combining multiple visualizations into a single view, providing a comprehensive overview of data.
- Search and Filtering: Kibana offers powerful search capabilities to explore and filter data based on specific criteria or patterns.
- Real-time Monitoring: It supports real-time data streaming and allows users to monitor live data and receive instant insights or alerts.
- Time-Series Analysis: Kibana provides tools for analyzing time-based data, enabling users to identify trends, patterns, and anomalies over a specific time period.
- Geospatial Analysis: It offers geospatial capabilities, allowing users to visualize and analyze data on maps, and perform location-based queries.
- Machine Learning Integration: Kibana integrates with Elasticsearch's machine learning features to perform anomaly detection, forecasting, and other advanced analytics tasks.

Overall, Kibana serves as a powerful tool for data visualization, exploration, and monitoring, helping users gain insights and make informed decisions based on their data.

### Kibana Installation

This guide is based on Ubuntu 22.04.2 LTS ("Jammy") running through WSL2. To check the version of Ubuntu installed on your system you can use the ``lsb_release`` command: 
```console
lsb_release -a
```

In order to install Kibana with Debian package, supposing that you have already followed the installation process of Elasticsearch, replicate the following steps: 
1. From a terminal, reload the local package database: 
    ```console
    sudo apt-get update
    ```
4. Install Kibana: 
    ```console
    sudo apt-get install kibana
    ```
    **Note:** remember that ``apt-get`` will upgrade the packages when a newer version becomes available. 
5. Generate an enrollment token for Kibana:
    ```console
    sudo /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
    ```

For more information about the installation process: [Install Kibana with Debian package](https://www.elastic.co/guide/en/kibana/current/deb.html)

### Running Kibana

To check which init system (``systemd`` or ``service``) your platform uses in order to run Kibana, run the following command:
```console
ps --no-headers -o comm 1
```

Run the ``kibana`` process by using the operating system's built-in init system (e.g. ``systemd``).
1. Start the elasticsearch process by running the following command: 
    ```console
    sudo systemctl start kibana.service
    ```
2. Verify that Kibana has started successfully (it may take some time) by navigating to [Kibana](http://localhost:5601).
3. When prompted, specify the ``elastic`` user and password that was generated during installation and the token previously generated. 

## Project Overview

### Data Model

In a search system, you could have several indexes within Elasticsearch to organize and store the data effectively. Here are the indexes for this specific sample:
- **xml-index**: This index keeps track of the xml documents sent to the microservice, storing the specific properties of each file
- **docx-attachment-pipeline-index**: This index stores information about each .docx attachment in the inventory, such as title, author, content, and any other relevant details.
- **pdf-attachment-pipeline-index**: This index stores information about each .pdf attachment in the inventory, such as title, author, content, and any other relevant details.

These are just a few examples of indexes that could be included in a search system. The specific collections you choose would depend on the system's requirements and the level of detail to track.

## Usage

### Microservices Approach
1. Clone/Download the repository.
2. Move to the cloned/downloaded directory, create a virtual environment (e.g. ``python3 -m venv venv``) and activate it (e.g. ``. venv/bin/activate``)
3. Install packages from requirements (e.g. ``pip3 install -r requirements.txt``)
4. Connect to Kibana and execute the following command from the integrated *Dev Tools* interface to define the pipeline to ingest docx attachments:
     ```console
    PUT _ingest/pipeline/docx_attachment_pipeline
    {
        "description" : "Pipeline to ingest docx attachments and store them in an index",
        "processors" : [
            {
            "attachment" : {
                "field" : "data"
            },
            "remove":{
                "field":"data"
            }
            }
        ]
    }
    ```
5. From the same interface define the pipeline to ingest pdf attachments:
     ```console
    PUT _ingest/pipeline/pdf_attachment_pipeline
    {
        "description" : "Pipeline to ingest pdf attachments and store them in an index",
        "processors" : [
            {
            "attachment" : {
                "field" : "data"
            },
            "remove":{
                "field":"data"
            }
            }
        ]
    }
    ```
4. Run the application using the following command:
    ```console
    uvicorn app:app --reload
    ```
5. Import the [postman_collection.json](/postman_collection.json) available in the repository and send the requests
6. As an alternative to the collection provided, once the XML documents have been uploaded, to retrieve them by using Kibana, you can connect and execute the following command from the integrated Dev Tools interface:
     ```console
    POST /microservice-index/_search
    {
        "query": {
            "match_all": {}
        }
    }
    ```
    Or the following one to retrieve, for instance, all the documents with ``DocumentaryUnitType`` equal to ``ATTI DEL DIRIGENTE``: 
     ```console
    POST /microservice-index/_search
    {
        "query": {
            "match": {
               "Header.DocumentaryUnitType.keyword": "ATTI DEL DIRIGENTE"
            }
        }
    }
    ```

#### Endpoints

- POST /upload: It parses the loaded XML file and indexes its content, also indexes the attached documents (.docx and .pdf) and stores the three files in their respective file system paths.
- GET /xml-index: Retrieves all documents from the *xml-index* index.
- GET /xml-index/{search_term}: Retrieves the documents from the *xml-index* index by a search term.
- GET /docx-attachments: Retrieves all documents from the *docx-attachments* index.
- GET /docx-attachments/{search_term}: Retrieves the documents from the *docx-attachments* index by a search term.
- GET /pdf-attachments: Retrieves all documents from the *pdf-attachments* index.
- GET /pdf-attachments/{search_term}: Retrieves the documents from the *pdf-attachments* index by a search term.

#### Tests

*TBD*

<!-- To check that the functions output the expected value, the following unit tests were implemented: 
- ``test_get_all_documents``: Tests the route to retrieve all documents from the index... -->

### Ingest Attachment Plugin Approach
To test only the attachment ingestion plugin, proceed as described in the steps 4 and 5 of the previous section and simply run the pipeline using the following command to ingest a pdf file: 

    ```console
    (echo -n '{"filename":"muspi-merol.pdf", "data": "'; base64 /path/to/elasticsearch-getting-started/data/muspi-merol.pdf; echo '"}') | sudo curl -H "Content-Type: application/json" -d @- --cacert http_ca.crt -u elastic https://localhost:9200/pdf-attachment-pipeline-index/_doc/1?pipeline=pdf_attachment_pipeline
    ```

Or the following one to ingest a docx file: 

    ```console
    (echo -n '{"filename":"lorem-ipsum.docx", "data": "'; base64 /path/to/elasticsearch-getting-started/data/lorem-ipsum.docx; echo '"}') | sudo curl -H "Content-Type: application/json" -d @- --cacert http_ca.crt -u elastic https://localhost:9200/docx-attachment-pipeline-index/_doc/1?pipeline=docx_attachment_pipeline
    ```

Then, to retrieve them by using the Dev Tools interface within Kibana, execute, for instance, the following query: 

    ```console
    POST /pdf-attachment-pipeline-index/_search
    {
        "query": {
            "query_string": {
            "default_field": "attachment.content", 
            "query": "ymunon"
            }
        }
    }
    ```

### Logstash Pipeline Approach

*TBD*

1. Connect and execute the following command from the integrated Dev Tools interface of Kibana to define the index:
     ```console
    PUT /logstash-pipeline-index
    ```
2. Simply run the pipeline using the following command
    ```console
    sudo /usr/share/logstash/bin/logstash -f /path/to/elasticsearch-getting-started/logstash-pipelines/logstash_pipeline.conf --debug
    ```

## ToDo

This section lists the tasks and improvements planned for the project. It serves as a roadmap for future development and can be used to track progress and keep everyone informed about upcoming changes:
- [x] Add 'Content' key to the metadata document to support full-text search on metadata.
- [ ] Refactor code for better readability and maintainability.
- [ ] Write unit tests to ensure proper functionality.
- [ ] Update documentation to reflect recent changes.
- [ ] Optimize performance for better efficiency.
- [ ] Improve error handling and logging.
- [ ] Explore integration with object storage services APIs.
- [ ] Consider adding automated deployment and continuous integration.