# coding:utf-8

import requests
from rtcclient.request import RequestBuilder
from urllib.parse import urlencode

class ProjectArea:

    # initialize the object with the data retrieved from /oslc/projectareas
    def __init__(self, jsonDict):

        self.resourceUrl = jsonDict['rdf:resource']
        self.uuid = self.resourceUrl.split('/')[-1]

        self.title = jsonDict['dc:title']
        self.description = jsonDict['dc:description']

    def retrieveWorkItems(self):
        pass

    def workItemsServices(self):
        url = self.repository + '/oslc/contexts/{}/workitems/services.xml'
        _headers = {}
        _headers['Accept'] = 'application/xml'
        _headers['OSLC-Core-version'] = '2.0'

        request = RequestBuilder('GET',
            url,
            headers = _headers
            ).build()
        response = self.sendRequest(request)

        dict = xmltodict.parse(response.text)
        return dict
