import asyncio
import re

import aiohttp as aiohttp
import pandas as pd
from elasticsearch import Elasticsearch, helpers
from ml_utils import get_embedding

es_url = "http://localhost:9200"
es = Elasticsearch([es_url])
file_path = '/Users/dani.dubinsky@openweb.com/Desktop/peskei_din/emails.csv'
index_name = "enron_emails"
mapping = {
    "mappings": {
        "properties": {
            "Message-ID": {"type": "keyword"},
            "Date": {"type": "date", "format": "EEE, d MMM yyyy HH:mm:ss Z"},
            "From": {"type": "keyword"},
            "To": {"type": "keyword"},
            "Subject": {"type": "text"},
            "Mime-Version": {"type": "keyword"},
            "Content-Type": {"type": "text"},
            "Content-Transfer-Encoding": {"type": "keyword"},
            "X-From": {"type": "text"},
            "X-To": {"type": "text"},
            "X-cc": {"type": "text"},
            "X-bcc": {"type": "text"},
            "X-Folder": {"type": "text"},
            "X-Origin": {"type": "keyword"},
            "X-FileName": {"type": "text"},
            "Message": {"type": "text"},
            "Message_embedding": {
                "type": "dense_vector"
            }
        }
    }
}



def generate_documents(df):
    for _, row in df.iterrows():
        message = row['message']
        header, body = re.split(r'\n\n', message, 1)
        fields = re.findall(r'^(.*?):\s*(.*?)$', header, re.MULTILINE)
        email_dict = {k: v for k, v in dict(fields).items() if k in mapping["mappings"]["properties"]}
        email_dict['Message'] = body.strip()
        email_dict['Message_embedding'] = get_embedding(email_dict['Message'])

        yield {
            "_index": index_name,
            "_source": email_dict,
        }


def bulk_insert(df):
    documents = generate_documents(df)
    helpers.bulk(es, documents)


chunk_iterator = pd.read_csv(file_path, chunksize=10000)
for chunk in chunk_iterator:
    bulk_insert(chunk)
