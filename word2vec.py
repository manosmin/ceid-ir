from elasticsearch import Elasticsearch
from gensim.models import Word2Vec
from gensim.models.keyedvectors import Vocab
import nltk
#nltk.download('punkt') ------------ IMPORTANT!!! ENABLE ONCE ------------
from nltk.corpus import stopwords
#nltk.download('stopwords') ------------ IMPORTANT!!! ENABLE ONCE ------------
from nltk.tokenize import word_tokenize, sent_tokenize
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

#Get ALL summaries of books the user has rated
res1 = es.search(index='books', body={
    "query": {
        "match_all": {
        }
    }
}, size=1000)
summaries=[]
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
    for line2 in res2['hits']['hits']:
        summaries.append(line1['_source']['summary'])

#Merge ALL the summaries in one sentence
s = ''.join(summaries)

#Tokenizer function
def tokenizeFunc(data): 
    stop_words = set(stopwords.words('English'))
    words = nltk.word_tokenize(data)
    words = [word.lower() for word in words if word.isalpha()]
    filtered_sentence = [w for w in words if not w in stop_words]
    filtered_sentence = []
    for w in words:
        if w not in stop_words:
            filtered_sentence.append(w)
    return filtered_sentence

#Calculate a float based on how similar the word given is to model
def mySimilarityFunc(model, randomWord):
    temp=0
    c=0
    for i in model.wv.most_similar(randomWord):
        #print(i[1])
        temp = temp +i[1]
        c=+1
    avg = temp / c
    return(avg)

#Tokenize the data
tokenizedData1 = tokenizeFunc(s)
#Create model based on the tokenized data
m1 = Word2Vec([tokenizedData1], min_count=1)

myFlag = 0
guessRating=0.00
userRating = 0.00
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
    #If the book is not rated by the specific user
    if not (res2['hits']['hits']):
        userRating=0
        #Tokenize the summary of the book
        tokenizedData2 = tokenizeFunc(line1['_source']['summary'])
        #If the tokenized summary has a word which is also included in the model we created for the specific user
        if tokenizedData2[0] in m1.wv.index_to_key:
            #Generate the float number
            guessRating = mySimilarityFunc(m1, tokenizedData2[0])
            tempRating = float(line2['_source']['rating'])
            #Calculate a rating based on this user's previous rating on similar book and the generated float number
            calculatedRating = tempRating + guessRating
            print('[ISBN]', line1['_source']['isbn'], '[Title]', line1['_source']['book_title'], '[Guessed User Rating]', "%.2f" % calculatedRating)
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
print('------')
#Sort table
table = sorted(table, key=lambda x:x[2], reverse=True)
#Print results
for i in table:
    print('[ISBN]',i[1],'[Title]',i[0],'[Rating]',"%.2f" % float(i[2]))

