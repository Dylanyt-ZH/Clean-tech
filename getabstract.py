import json
import pandas as pd
import requests
import os
import xmltodict
from tqdm import tqdm
import multiprocessing



conf = open('config.json','r') 
config = json.load(conf)
api_key = config['API_key']
conf.close()
headers=  {'X-ELS-APIKey':api_key}

def getabstract(filename,filepath = 'data/'):
    keyword = filename.replace(".csv","")
    raw_data = pd.read_csv(filepath + filename,header=0)
    raw_data["abstract"] = None
    raw_data["topic"] = keyword
    print(keyword)
    for i in tqdm(range(0,len(raw_data))):
        doi = raw_data['doi'][i]
        aburl = 'https://api.elsevier.com/content/article/doi/'+doi
        # print(aburl)
        abstract = requests.get(aburl,headers = headers)
        try:
            d = xmltodict.parse(abstract.text)
            abstract_text = d["full-text-retrieval-response"]['coredata']['dc:description']
            raw_data.at[i,'abstract'] = abstract_text
            pass
        except:
            continue
    select_data = raw_data.dropna()
    select_data.to_csv(filepath + keyword + '-selected.csv', encoding='utf-8',index=False)





if __name__ == '__main__':
    filepath = 'data/'
    filelist = os.listdir(filepath)
    
    print(filelist)
    pool_obj = multiprocessing.Pool(4)
    pool_obj.map(getabstract,iter(filelist))


