#!/usr/bin/env python
# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
from docx import Document
import os

# Connect to Elasticsearch
es = Elasticsearch(["http://localhost:9200"])

# Elasticsearch index name
index_name = "verdicts"


# Function to read .docx file content
def read_docx(file_path):
    try:
        doc = Document(file_path)
        fullText = []
        for para in doc.paragraphs:
            fullText.append(para.text)
        return '\n'.join(fullText)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


# Function to index document in Elasticsearch
def index_document(doc_id, content, file_path):
    try:
        res = es.index(index=index_name, id=doc_id, body={"content": content, "file_path": file_path})
        print(f"Document {doc_id} indexed: {res['result']}")
    except Exception as e:
        print(f"Error indexing document {doc_id}: {e}")


# Directory containing your .docx files
directory_path = "/Users/dani.dubinsky@openweb.com/Desktop/peskei_din/training"

# Loop through all .docx files in the directory and index them
for filename in os.listdir(directory_path):
    if filename.endswith(".docx"):
        file_path = os.path.join(directory_path, filename)
        content = read_docx(file_path)
        if content:
            index_document(filename, content, file_path)

# Construct the search query
query = {
    "query": {
        "match": {
            "content": 'הנאשם הורשע על פי הודאתו במסגרת הסדר טיעון, בביצוען של עבירות שעניינן איומים; תקיפה סתם – בן זוג והפרעה לשוטר במילוי תפקידו. הצדדים הציגו הסדר דיוני במסגרתו תוקן כתב האישום, הנאשם הודה והורשע בעבירות המיוחסות לו בכתב האישום המתוקן, וצירף תיק נוסף. '
        }
    },
    "size": 5
}

query_2 = {"query": {"bool": {"must": [{
    "match": {
        "content": 'הנאשם הורשע על פי הודאתו במסגרת הסדר טיעון, בביצוען של עבירות שעניינן איומים; תקיפה סתם – בן זוג והפרעה לשוטר במילוי תפקידו. הצדדים הציגו הסדר דיוני במסגרתו תוקן כתב האישום, הנאשם הודה והורשע בעבירות המיוחסות לו בכתב האישום המתוקן, וצירף תיק נוסף. '
    }
}],
    "filter": [{"match_all": {}}],
    "should": [],
    "must_not": []
}
}
}

# Execute the search query
response = es.search(index=index_name, body=query_2)

# Extract and print the top 5 documents
top_docs = response['hits']['hits']
for doc in top_docs:
    print(f"ID: {doc['_id']}, Score: {doc['_score']}, Source: {doc['_source']}")
