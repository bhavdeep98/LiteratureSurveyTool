# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 21:23:45 2019

@author: Bhavdeep Singh
"""

import request_api
import xml.etree.ElementTree as ET


if __name__=="__main__":
    url = 'http://export.arxiv.org'
    params = {
        'verb':'ListRecords',\
        'from':'2019-09-09',\
        'set':'cs',\
        'metadataPrefix':'arXiv'
    }
    data = request_api.RequestAPI(url, params) 
    
    data_string = data.get(url,params)
    root = ET.fromstring(data_string)
    
for record in root.findall('{http://www.openarchives.org/OAI/2.0/}ListRecords')[0]:
    if len(record.findall('{http://www.openarchives.org/OAI/2.0/}metadata')) > 0:    
        for elements in record.findall('{http://www.openarchives.org/OAI/2.0/}metadata')[0]:
            for title in elements.findall('{http://arxiv.org/OAI/arXiv/}title'):
                print(title.text)
            for authorList in elements.findall('{http://arxiv.org/OAI/arXiv/}authors'):
                for author in authorList:
                    firstname = author.findall('{http://arxiv.org/OAI/arXiv/}keyname')[0].text
                    if len(author.findall('{http://arxiv.org/OAI/arXiv/}forenames')):
                        lastname = author.findall('{http://arxiv.org/OAI/arXiv/}forenames')[0].text
                    print(firstname+" "+lastname)