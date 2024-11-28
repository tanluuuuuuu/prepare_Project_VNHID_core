from elasticsearch import Elasticsearch

# Connect to Elasticsearch
client = Elasticsearch(
    "http://localhost:9200",  # Elasticsearch endpoint
    api_key="Y2kwcFlwTUJJMkVSSU9EVlhYSy06SVBCaWxNWjhSQXlzd0ZTVDdvZ2dhdw==",
)

# Create an index
client.indices.create(index="my_index")

# Index a document
client.index(
    index="my_index",
    id="my_document_id",
    document={
        "foo": "foo",
        "bar": "bar",
    }
)
