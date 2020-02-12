# coding:utf-8

import requests
from rtcclient.request import RequestBuilder
from urllib.parse import urlencode

import xmltodict

from rtcclient.type import Type

class ProjectArea:

    # initialize the object with the data retrieved from /oslc/projectareas
    def __init__(self, client, jsonDict):

        self._client = client
        self.resourceUrl = jsonDict['rdf:resource']
        self.uuid = self.resourceUrl.split('/')[-1]

        self.title = jsonDict['dc:title']
        self.description = jsonDict['dc:description']

    def retrieveWorkItems(self):
        pass

    def sendRequest(self, request):
        return self._client.sendRequest(request)

    def workItemsServices(self):
        url = self._client.repository + \
            '/oslc/contexts/{}/workitems/services.xml'.format(self.uuid)
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

    def getOSLCService(self):
        dict = self.workItemsServices()
        oslcService = dict['rdf:RDF']['oslc:ServiceProvider']['oslc:service']

        return oslcService

    def getTypes(self):
        url = self._client.repository + \
            '/oslc/types/{}'.format(self.uuid)

        _headers = {}
        _headers['Accept'] = 'application/xml'
        _headers['OSLC-Core-version'] = '2.0'

        request = RequestBuilder('GET',
            url,
            headers = _headers
            ).build()
        response = self.sendRequest(request)

        obj_dict = xmltodict.parse(response.text)
        types = obj_dict['rdf:RDF']['oslc:ResponseInfo']['rdfs:member']

        typeList = []
        for t in types:
            typeList.append(Type(t))

        return typeList
