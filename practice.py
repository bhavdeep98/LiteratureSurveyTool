# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 18:52:17 2019

@author: Bhavdeep Singh
"""

#import arxiv
#import networkx as nx
#from itertools import permutations
#import matplotlib.pyplot as plt
#import collections
#import feedparser
import requests
import xml.etree.ElementTree as ET
#from urllib.parse import urlencode

# Keyword queries

#
#"""arxiv.query(query="",
#            id_list=[],
#            max_results=None,
#            start = 0,
#            sort_by="relevance",
#            sort_order="descending",
#            prune=True,
#            iterative=False,
#            max_chunk_results=1000)"""
#papers = arxiv.query(query="all:cs",\
#                     max_results=100)
#
##initialize the graph
#G =  nx.Graph()
#
#for paper in papers:
#    print(paper['title'])
#    print(paper['authors'])
#    for author in paper['authors']:
#        G.add_node(author)
#    possibleConnections = permutations(paper['authors'],2) 
#    G.add_edges_from(possibleConnections)
#
#
#nx.draw(G)
#
##calculate the Degree Sequence
#degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
#degreeCount = collections.Counter(degree_sequence)
#deg, cnt = zip(*degreeCount.items())
#
#fig, ax = plt.subplots()
#plt.bar(deg, cnt, width=0.80, color='b')
#
#plt.title("Degree Histogram")
#plt.ylabel("Count")
#plt.xlabel("Degree")
#ax.set_xticks([d + 0.4 for d in deg])
#ax.set_xticklabels(deg)
#
## draw graph in inset
#Gcc = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)[0]
#pos = nx.spring_layout(G)
#plt.axis('off')
#nx.draw_networkx_nodes(G, pos, node_size=20)
#nx.draw_networkx_edges(G, pos, alpha=0.4)
#
#
#
#plt.show()

url = 'http://export.arxiv.org/oai2'

#params = urlencode({
#    'verb':'ListRecords',\
#    'from':'2019-09-09',\
#    'set':'cs',\
#    'metadataPrefix':'arXiv'
#})
    
params = {
    'verb':'ListRecords',\
    'from':'2019-09-09',\
    'set':'cs',\
    'metadataPrefix':'arXiv'
}

#print(url+"?"+params)
#result = feedparser.parse(url+"?"+params)


resp = requests.get(url=url, params=params)
#resp_parsed = re.sub(r'^jsonp\d+\(|\)\s+$', '', resp.text)
#json.loads(resp.content.decode('utf-8'))
#resp.text
root = ET.fromstring(resp.text)
for record in root.findall('{http://www.openarchives.org/OAI/2.0/}ListRecords')[0]:
    for elements in record.findall('{http://www.openarchives.org/OAI/2.0/}metadata')[0]:
#        for title in elements.findall('{http://arxiv.org/OAI/arXiv/}title'):
#            print(title.text)
        for authorList in elements.findall('{http://arxiv.org/OAI/arXiv/}authors'):
            for author in authorList:
                firstname = author.findall('{http://arxiv.org/OAI/arXiv/}keyname')[0].text
                if len(author.findall('{http://arxiv.org/OAI/arXiv/}forenames')):
                    lastname = author.findall('{http://arxiv.org/OAI/arXiv/}forenames')[0].text
                print(firstname+" "+lastname)
                
            
            
