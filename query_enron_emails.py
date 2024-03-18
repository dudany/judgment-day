from elasticsearch import Elasticsearch
from ml_utils import get_embedding

es = Elasticsearch(["http://localhost:9200"])

query_text = "Announcement: Here's what we predict."
query_text_2 = "Over the last three years, the WineCommune platform has evolved from a simple forum for wine enthusiasts to trade bottles into a global marketplace, now boasting more than 10,000 users."
query_text_3 = "WineCommune"
query_text_4 = "Off-balance sheet"
query_embedding = get_embedding(query_text_4)

script_query = {
    "script_score": {
        "query": {"match_all": {}},
        "script": {
            "source": "cosineSimilarity(params.Message_embedding, 'Message_embedding') + 1.0",
            "params": {"Message_embedding": query_embedding}
        },

    }
}

response = es.search(index="enron_emails", body={"query": script_query}, )
for it in response['hits']['hits']:
    print(f"score: {it['_score']}, Message: {it['_source']['Message']}")

