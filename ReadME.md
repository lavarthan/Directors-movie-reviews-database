# Tamil Director Database

This Repository includes the frontend,backend implementation for a search query.
After configuring the elasticsearch, the sample search engine is used to try the query searches.


Directory Structure
---
```
 ├── analyzers : Custom filters (Stemmers/stoppingwords,synonyms)
 ├── corpus : Modified data from the pre-processed data from actual (corpus) 
 ├── templates : The resultpage for UI (of Flask)
 ├── app.py : Flask backend to have transaction with ElasticSearch APIs
 ├── preprocesspy : Python file corpus data to elasticsearch input data format
 ├── query.py : ElasticSearch search queries inclusive of advanced queries, aggreagtions and textmining
 ├── data_scraper.py : Python file to scrape the data from the website
 ├── static: contain front-end files
```

Demo
---
* Install ElasticSearch
* Install packages `pip install -r requirements.txt`
* Add 'analyze' folder in config of Elasticsearch and add files from analyzers
* Run ElasticSearch
* Add index(uncomment indexing part if not manually added) and add data (`processed_review_bulk.json`)
* Go to http://localhost/5000/
* Enter keyword for search
* For advanced queries try the postman queries collection from postman or browser (Samples below)

Supported Queries
---
### Basic search
* Can search for lyrics if you just know movie/year/singer/lyricist/genre.
> E.g.- "நெல்சன்"
```
{
    "query": {
        "query_string": {
            "query":"நெல்சன்"
        }
    }
}
```
### Field based search
* Can search specifying the field when you just know _திரைப்படம்_, _இயக்குனர்_, _விமர்சனம்_, _தீர்ப்பு_, _மதிப்பீடு_, _வெளியிடப்பட்ட தேதி_.
> E.g.- "இயக்குனர் நெல்சன்"
```
{
     "query" : {
          "match" : {
             "இயக்குனர்" : "நெல்சன்"
         }
     }
 }
```

### Wildcard search
* Can search with WildCard when not so sure of spell
 > E.g.- "நெல்*" for "நெல்சன்"
 ```{
        "query": {
            "bool": {
                "must": [
                    {
                        "query_string": {
                            "query": "நெல்*",
                            "fields": ["திரைப்படம்", "இயக்குனர்", "விமர்சனம்", " தீர்ப்பு", "மதிப்பீடு",
                                       " வெளியிடப்பட்ட தேதி"]
                        }
                    }
                ]
            }
        }
 ```

### Multi match search
* Can search when you think one term might show up in multiple fields
 > E.g.- "செல்வராகவன்"
```
{
        "query": {
            "multi_match": {
                "query": "செல்வராகவன்",
                "fields": ["திரைப்படம்", "இயக்குனர்", "விமர்சனம்", " தீர்ப்பு", "மதிப்பீடு", " வெளியிடப்பட்ட தேதி"],
                "operator": operator,
                "type": "best_fields"
            }
        }
    }
```

### Best search 
* Can search for best director or best movie  where Top is marked on "மதிப்பீடு" (rating)
 > E.g. - மிகச்சிறந்த திரைப்படங்கள்
```{
        "sort": [
            {"மதிப்பீடு.keyword": {"order": "desc"}}
        ],
        "query": {
            "multi_match": {
                "query": "மிகச்சிறந்த திரைப்படங்கள்",
                "fields": ["திரைப்படம்", "இயக்குனர்", "விமர்சனம்", " தீர்ப்பு", "மதிப்பீடு", " வெளியிடப்பட்ட தேதி"],
                "operator": 'or',
                "type": "best_fields"
            }
        }
    }
```

*NOTE: These are the field supported currently by UI but using postman can do more advanced search*
