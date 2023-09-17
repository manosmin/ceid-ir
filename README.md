
# Information Retrieval Project @CEID

This project aims to develop a powerful and intelligent search engine using ElasticSearch API and Python. This search engine will leverage natural language processing (NLP) and machine learning techniques to provide users with highly relevant search results and an enhanced user experience.


## Features

- Data Collection and Indexing
- Integration with ElasticSearch
- Query Expansion and Recommendations
- Evaluation and Testing
- Machine Learning Models
- Natural Language Processing (NLP)
## Tech Stack

**Front End:** Python

**Back End:** ElasticSearch, Python

**ML Libraries:** Gensim, Word2Vec, NLTK



## Deployment

To deploy this project run in the ElasticSearch folder

```bash
bin/elasticsearch.bat
```

Then, run in the Kibana folder

```bash
bin/kibana.bat
```

Finally, run the script to upload books data to ElasticSearch

```bash
python parser.py
```

## Screenshots
*Search Results*</br>
![Search Results](https://github.com/manosmin/ceid-ir/blob/master/screenshots/ss1.png)
</br>
*Query Expansion and Recommendations*</br>
![Query Expansion and Recommendations](https://github.com/manosmin/ceid-ir/blob/master/screenshots/ss2.png)
