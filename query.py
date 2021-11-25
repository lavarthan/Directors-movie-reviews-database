from elasticsearch import Elasticsearch, helpers
import json, re
import codecs
import unicodedata
import json

client = Elasticsearch(HOST="http://localhost", PORT=9200)
INDEX = 'reviews_db'
# top_words = ['சிறந்த',
#              'மிக சிறந்த',
#              'மிகச்சிறந்த',
#              'மிகசிறந்த',
#              'மிகவும்சிறப்பான',
#              'சிறப்பான',
#              'தலைசிறந்த']


def standard_analyzer(query):
    q = {
        "analyzer": "standard",
        "text": query
    }
    return q


def basic_search(query):
    q = {
        "query": {
            "query_string": {
                "query": query
            }
        }
    }
    return q


def search_with_field(query, field):
    q = {
        "query": {
            "match": {
                field: query
            }
        }
    }
    return q


def multi_match(query, operator='or'):
    q = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["திரைப்படம்", "இயக்குனர்", "விமர்சனம்", " தீர்ப்பு", "மதிப்பீடு", " வெளியிடப்பட்ட தேதி"],
                "operator": operator,
                "type": "best_fields"
            }
        }
    }
    return q


def wild_card_search(query):
    q = {
    "query": {
        "wildcard" : {
                       "இயக்குனர்" : query
        }
    },
    "_source": ["திரைப்படம்", "இயக்குனர்", "விமர்சனம்", " தீர்ப்பு", "மதிப்பீடு", " வெளியிடப்பட்ட தேதி"],
    "highlight": {
        "fields" : {
                  "இயக்குனர்" : {}
        }
    }
}
    return q


def best_search(query):
    q = {
        "sort": [
            {"மதிப்பீடு.keyword": {"order": "desc"}}
        ],
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["திரைப்படம்", "இயக்குனர்", "விமர்சனம்", " தீர்ப்பு", "மதிப்பீடு", " வெளியிடப்பட்ட தேதி"],
                "operator": "OR",
                "type": "best_fields"
            }
        }
    }
    return q


def exact_search(query):
    q = {
        "query": {
            "multi_match": {
                "query": query,
                "type": "phrase"
            }
        }
    }
    return q


def process_query(query):
    if any(word in query for word in top_words):
        query_body = best_search(query)
    if '''"''' in query:
        query_body = exact_search(query)
    elif '*' in query:
        query_body = wild_card_search(query)
    else:
        query_body = basic_search(query)
    return query_body


def search(query):
    query_body = process_query(query)
    print('Searching...')
    resp = client.search(index=INDEX, body=query_body)
    return resp
