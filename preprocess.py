import json
import codecs
import random
import pandas as pd

f = codecs.open('corpus/processed_review_bulk_api.json', 'w', encoding='utf-8')
df = pd.read_csv('corpus/behindwoods_data.csv')

for i in range(df.shape[0]):
    # try:
        print(i)
        dict_ = {}
        dict_["இயக்குனர்"] = df['director'][i]
        dict_["திரைப்படம்"] = df['movie'][i]
        dict_["விமர்சனம்"] = df['review'][i]
        dict_["வெளியிடப்பட்ட தேதி"] = df['date_published'][i]
        dict_["தீர்ப்பு"] = df['verdict'][i]
        dict_["மதிப்பீடு"] = df['p_rating'][i]

        f.write('{ "index" : { "_index" : "reviews_db", "_type" : "review", "_id" :' + str(i) + ' } }\n')
        json.dump(dict_, f, ensure_ascii=False)
        f.write('\n')
        i += 1