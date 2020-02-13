# coding:utf-8

import requests
from rtcclient.request import RequestBuilder
from urllib.parse import urlencode
from rtcclient.workitem import WorkItem

import xmltodict

from rtcclient.type import Type

class ProjectArea:

    # initialize the object with the data retrieved from /oslc/projectareas
    def __init__(self, client, jsonDict):

        self._client = client
        self.resourceUrl = jsonDict['rdf:resource']
        self._id = self.resourceUrl.split('/')[-1]

        self.title = jsonDict['dc:title']
        self.description = jsonDict['dc:description']

    def retrieveWorkItems(self, page_size=100, start_index=0):
        url = self._client.repository + \
            '/oslc/contexts/{}/workitems' \
            '?oslc_cm.pageSize={}&_startIndex={}'
        url = url.format(self._id, page_size, start_index)

        _headers = {}
        _headers['Accept'] = 'application/xml'

        request = RequestBuilder('GET',
            url,
            headers = _headers
            ).build()
        response = self.sendRequest(request)

        obj_dict = xmltodict.parse(response.text)

        return obj_dict

    def sendRequest(self, request):
        return self._client.sendRequest(request)

    def workItemsServices(self):
        url = self._client.repository + \
            '/oslc/contexts/{}/workitems/services.xml'.format(self._id)
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

    def getWorkItemTotalCount(self):
        obj = self.retrieveWorkItems(page_size=1)

        return obj['oslc_cm:Collection']['@oslc_cm:totalCount']

    def getTypes(self):
        url = self._client.repository + \
            '/oslc/types/{}'.format(self._id)

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
