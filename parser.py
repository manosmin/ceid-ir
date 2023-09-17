from elasticsearch import Elasticsearch, helpers
import csv
import warnings
warnings.filterwarnings("ignore", category=Warning)
#Connect to Elasticsearch
es = Elasticsearch(['http://localhost:9200'])
if es.ping():print('Connection established')
else:print('Connection failed')
#Import csv to Elasticsearch
with open('./BX-Books.csv', encoding='utf-8') as f:
    r = csv.DictReader(f)
    helpers.bulk(es, r, index='books')
with open('./BX-Book-Ratings.csv', encoding='utf-8') as f:
    r = csv.DictReader(f)
    helpers.bulk(es, r, index='ratings')