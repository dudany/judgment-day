import re
import pandas as pd
from elasticsearch import Elasticsearch
from ml_utils import get_embedding

es = Elasticsearch(["http://localhost:9200"])

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


def insert_into_enron_emails(m):
    header, body = re.split(r'\n\n', m, 1)
    fields = re.findall(r'^(.*?):\s*(.*?)$', header, re.MULTILINE)
    email_dict = dict(fields)
    email_dict['Message'] = body.strip()
    email_dict['Message_embedding'] = get_embedding(email_dict['Message'])
    es.index(index=index_name, document=email_dict)


file_path = '/Users/dani.dubinsky@openweb.com/Desktop/peskei_din/emails.csv'
chunk_iterator = pd.read_csv(file_path, chunksize=10000)
for chunk in chunk_iterator:
    chunk['message'].apply(insert_into_enron_emails)

