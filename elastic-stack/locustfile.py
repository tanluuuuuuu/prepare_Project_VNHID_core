from locust import HttpUser, task
from elasticsearch import Elasticsearch
import json
import time

class TestElasticsearchLoad(HttpUser):
    es_client = Elasticsearch(
        "http://localhost:9200",  # Elasticsearch endpoint
        api_key="d1dUTGNKTUJBWGQ1Tlotc1ZrRUI6QlAydEtBY21Sd2ltc19aa05IMW56UQ==",
    )

    @task
    def test_get_index(self):
        start_time = time.time()
        try:
            res = self.es_client.get(index="my_index", id="my_document_id")
            response_time = (time.time() - start_time) * 1000 
            self.environment.events.request.fire(
                request_type="GET",
                name="get_document",
                response_time=response_time,
                response_length=len(json.dumps(res.body)),
                exception=None,
                context={}
            )
        except Exception as e:
            response_time = (time.time() - start_time) * 1000  
            self.environment.events.request.fire(
                request_type="GET",
                name="get_document",
                response_time=response_time,
                exception=e
            )
