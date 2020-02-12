# coding:utf-8

import requests
from rtcclient.request import RequestBuilder
from urllib.parse import urlencode

import xmltodict
import json

from rtcclient.projectarea import ProjectArea

class RTCClient:

    OSLC_HEADER_ACCEPT = "application/rdf+xml"

    def __init__(self, repository, username, password):

        self.repository = repository
        self.username = username
        self.password = password

        self._session = requests.Session()

    def sendRequest(self, request, sslVerify = False):
        self._session.prepare_request(request)
        prepped = self._session.prepare_request(request)

        response = self._session.send(prepped,
            verify = sslVerify,
            allow_redirects = False)

        #print(response.url)
        #print(response.headers)
        #print(response.cookies)
        #print(response.status_code)
        #print(response.text)
        return response

    def login(self):
        url = self.repository + '/auth/j_security_check'

        _headers = {}
        _headers['Content-Type'] = 'application/x-www-form-urlencoded'

        credentials = urlencode({
            "j_username": self.username,
            "j_password": self.password
        })
        request = RequestBuilder('POST',
            url,
            data = credentials,
            headers = _headers
            ).build()
        response = self.sendRequest(request)

    def logout(self):
        pass

    def rootServices(self):
        url = self.repository + '/rootservices'
        _headers = {}
        _headers['Accept'] = self.OSLC_HEADER_ACCEPT

        request = RequestBuilder('GET',
            url,
            headers = _headers
            ).build()
        response = self.sendRequest(request)

        dict = xmltodict.parse(response.text)
        return dict

    def getServiceProviderCatalogUrl(self):
        oslcCatalogsList = self.rootServices()["rdf:Description"]["jd:oslcCatalogs"]

        return oslcCatalogsList[0]["oslc:ServiceProviderCatalog"]["@rdf:about"]

    def getProjectList(self):
        url = self.repository + '/oslc/projectareas'
        _headers = {}
        _headers['Accept'] = 'application/json'

        request = RequestBuilder('GET',
            url,
            headers = _headers
            ).build()

        response = self.sendRequest(request)
        jsonObj = json.loads(response.text)

        projectList = []

        for projectJson in jsonObj['oslc_cm:results']:
            project = ProjectArea(projectJson)
            projectList.append(project)

        return projectList

    def test(self):
        url = self.repository + '/oslc/workitems/8162'
        _headers = {}
        _headers['Accept'] = 'application/json'

        request = RequestBuilder('GET',
            url,
            headers = _headers
            ).build()
        response = self.sendRequest(request)