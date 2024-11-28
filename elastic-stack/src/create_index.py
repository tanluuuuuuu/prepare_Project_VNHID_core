from elasticsearch import Elasticsearch

# Connect to Elasticsearch
client = Elasticsearch(
    "http://localhost:9200",  # Elasticsearch endpoint
    api_key="d1dUTGNKTUJBWGQ1Tlotc1ZrRUI6QlAydEtBY21Sd2ltc19aa05IMW56UQ==",
)

# Create an index
# client.indices.create(index="my_index")

# Index a document
client.index(
    index="my_index",
    id="my_document_id",
    document={
        "foo": "foo",
        "bar": "bar",
    }
)
