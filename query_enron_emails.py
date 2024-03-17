from elasticsearch import Elasticsearch
from judgment_day.ml_utils import get_embedding


es = Elasticsearch(["http://localhost:9200"])

query_text = "Announcement: Here's what we predict."
query_embedding = get_embedding(query_text)

script_query = {
    "script_score": {
        "query": {"match_all": {}},
        "script": {
            "source": "cosineSimilarity(params.Message_embedding, 'Message_embedding') + 1.0",
            "params": {"Message_embedding": query_embedding}
        }
    }
}

response = es.search(index="enron_emails", body={"query": script_query})
print(response)