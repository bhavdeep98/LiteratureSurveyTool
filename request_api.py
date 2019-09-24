# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 19:04:58 2019

@author: Bhavdeep Singh
"""

import logging
import requests
import json
#import os
"""
    Link for Request Documentaion: 
        https://2.python-requests.org/en/master/api/
    
"""
#initialize the logger
logger = logging.getLogger(__name__)

class RequestAPI:
    
    prune_keys = [
        'updated_parsed',
        'published_parsed',
        'arxiv_primary_category',
        'summary_detail',
        'author',
        'author_detail',
        'links',
        'guidislink',
        'title_detail',
        'tags',
        'id']
    
    def __init__(self, base_url = "http://export.arxiv.org", params = {
        'verb':'ListRecords',\
        'from':'2019-09-09',\
        'set':'cs',\
        'metadataPrefix':'arXiv'
    }):
        self.base_url = base_url
        self.params = params
    
    def __update_url(self, url, params):
        """
            Description: This function is to update the base URL. For the
            search query we are using a different API request here that is why
            this change is there.
            
            ToDo: the request for the query is yet to be updated.            
        """
        if 'query' in params.keys():
            url = url + "/api/query"
            
        else:
            url = url + "/oai2"
        
        self.base_url = url
        logger.info("The URL has been updated as {url}")
        return url
    
    def _prune_result(self, result):
        """
            Description: Deletes some of the keys from the downloaded result.
            This is necessary to increase the efficiency of the code so that
            we have to seach lesser number of nodes
            
            This function is copied from the arxiv library, 
                    https://pypi.org/project/arxiv/
        """

        for key in self.prune_keys:
            try:
                del result['key']
                logger.info("Deleted the Key : {key}")
            except KeyError:
                logger.error("Not able to find the Key :{key}")
        return result
    
    def __dump_json(self, json_data):
        with open('data.json','w') as outfile:
            json.dump(json_data, outfile)
        
    def get(self, url, params): 
        try:
            url = self.__update_url(url,params)
            print(url)
            response = requests.get(url=url, params=params)
            response.raise_for_status()
#            response_json  = requests.get(url=url, params=params).json()
        except requests.exceptions.HTTPError as http_err:
            """
                If you invoke .raise_for_status(), an HTTPError will be raised 
                for certain status codes. If the status code indicates a 
                successful request, the program will proceed without that 
                exception being raised.
            """
            logger.exception(f'HTTP error occurred: {http_err}')
            print(1)
            return ""
        except Exception as err:
            logger.exception(f'Other error occurred: {err}')
            print(2)
            return ""
        else:
            logger.info(f'Successful connection to {url} using {params}')
            print(3)
#            self.__dump_json(response_json)
            return response.text
    
    