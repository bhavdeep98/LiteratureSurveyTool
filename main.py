# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 21:23:45 2019

@author: Bhavdeep Singh
"""

import request_api
import xml.etree.ElementTree as ET
import networkx as nx
import json
from itertools import permutations
import matplotlib.pyplot as plt
import collections


def extract_data(root):
    extracted_title = []
    extracted_authorList = []
    for record in root.findall('{http://www.openarchives.org/OAI/2.0/}ListRecords')[0]:
        if len(record.findall('{http://www.openarchives.org/OAI/2.0/}metadata')) > 0:    
            for elements in record.findall('{http://www.openarchives.org/OAI/2.0/}metadata')[0]:
                for title in elements.findall('{http://arxiv.org/OAI/arXiv/}title'):
                    print(title.text)
                    extracted_title.append(title.text)
                for authorList in elements.findall('{http://arxiv.org/OAI/arXiv/}authors'):
                    temp_authorList = []
                    for author in authorList:
                        firstname = author.findall('{http://arxiv.org/OAI/arXiv/}keyname')[0].text
                        if len(author.findall('{http://arxiv.org/OAI/arXiv/}forenames')):
                            lastname = author.findall('{http://arxiv.org/OAI/arXiv/}forenames')[0].text
                        print(firstname+" "+lastname)
                        temp_authorList.append(firstname+" "+lastname)
                    extracted_authorList.append(temp_authorList)
    return extracted_title, extracted_authorList
                        
                    
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
    
    list_title, list_author = extract_data(root)
    
    ## dumping the data to a json
    with open('data.json','w') as outfile:
        json.dump([{"Title" : title,"Authors" : authors} for title, authors in zip(list_title,list_author)],outfile)
    
    #initialize the graph
    G =  nx.Graph()
    
    ##Adding nodes to the Graph
    ##Nodes are the author names
    for single_paper_author in list_author:
        for author in single_paper_author:
            G.add_node(author)
        # all the authors of a given paper are fully connected to each other
        possibleConnections = permutations(single_paper_author,2)
        G.add_edges_from(possibleConnections)
    
    nx.draw(G)
#    nx.degree_histogram(G)

    
