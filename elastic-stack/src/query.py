from elasticsearch import Elasticsearch

# Connect to Elasticsearch
client = Elasticsearch(
    "http://localhost:9200",  # Elasticsearch endpoint
    api_key="Y2kwcFlwTUJJMkVSSU9EVlhYSy06SVBCaWxNWjhSQXlzd0ZTVDdvZ2dhdw==",
)

# Getting documents
res = client.get(index="my_index", id="my_document_id")
print(res)

# Searching documents
res_search = client.search(index="my_index", query={
    "match": {
        "foo": "foo"
    }
})
print(res_search)

# Updating documents
client.update(index="my_index", id="my_document_id", doc={
    "foo": "bar",
    "new_field": "new value",
})

# Deleting documents
client.delete(index="my_index", id="my_document_id")

# Deleting an index
client.indices.delete(index="my_index")