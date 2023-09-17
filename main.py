from elasticsearch import Elasticsearch
import warnings
warnings.filterwarnings("ignore", category=Warning)
#Connect to Elasticsearch
es = Elasticsearch(['http://localhost:9200'])
if es.ping():
    print('Connection established\n')
else:
    print('Connection failed\n')
#Request user input
user = int(input('User ID: '))
name = input('Keyword: ')

book_query_body= {
  "query": {
        "bool": {
          "must": [  {
              "match": {
                "book_title": name
                        }
                    }
                ]
            }
        }
  }

table=[]
#Generate my metric
res1 = es.search(index='books', body=book_query_body, size=1000)
for line1 in res1['hits']['hits']:
    res2 = es.search(index='ratings', body= {
        "query": {
            "bool": {
                "must":  [ {
                    "match": {
                        "isbn": line1['_source']['isbn'] }
                },
                    { "match": { "uid": user } } ]
                } } }, size=1000)
    if not (res2['hits']['hits']):
        userRating=0.00
    else:
        for line2 in res2['hits']['hits']:
            userRating = float(line2['_source']['rating'])
            #print(userRating)
    res3 = es.search(index='ratings', body={ 
        "query": {  
            "bool": {
              "must": {
                  "match": 
                    {   "isbn":  line1['_source']['isbn'] }  
                        }  
                    } } }, size=1000)
    s=0.0
    t=0
    for line3 in res3['hits']['hits']:
         t+=1
         k=float(line3['_source']['rating'])
         s+=k

    if(t): 
        s=s/t
    else: 
        s=0.0
    t=0
    my_Score = (float(line1['_score']) + s + userRating)/3
    line = (line1['_source']['book_title'], line1['_source']['isbn'], my_Score)

    table.append(line)

#Sort table
table = sorted(table, key=lambda x:x[2], reverse=True)
#Print results
for i in table:
    print('[ISBN]',i[1],'[Title]',i[0],'[Rating]',"%.2f" % float(i[2]))