# coding:utf-8

import requests
from rtcclient.request import RequestBuilder
from urllib.parse import urlencode
from rtcclient.workitem import WorkItem

import xmltodict
import json

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
        _headers['OSLC-Core-Version'] = '2.0'

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
        _headers['OSLC-Core-Version'] = '2.0'

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

    def getTypeAllowedValues(self, type):
        url = self._client.repository + \
            '/oslc/context/{}/shapes/workitems/{}'.format(self._id, type.identifier)

        _headers = {}
        _headers['Accept'] = 'application/rdf+xml'
        _headers['OSLC-Core-Version'] = '2.0'

        request = RequestBuilder('GET',
            url,
            headers = _headers
            ).build()
        response = self.sendRequest(request)
        obj_dict = xmltodict.parse(response.text)
        return obj_dict

    def createWorkItemTest(self, type = None):
        url = self._client.repository + \
            '/oslc/contexts/{}/workitems'.format(self._id)
        _headers = {}
        _headers['Accept'] = 'text/json'
        _headers['Content-Type'] = 'application/x-oslc-cm-change-request+json'

        body = {}
        body['dc:title'] = 'This is title.'
        body['dc:description'] = 'This is description.'

        body['dc:type'] = {}
        body['dc:type']['rdf:resource'] = 'https://www.somed002.sony.co.jp/ccm/oslc/types/_cC2EQNNsEei2Go0VaWWcug/defect'

        body['rtc_cm:filedAgainst'] = {}
        body['rtc_cm:filedAgainst']['rdf:resource'] = 'https://www.somed002.sony.co.jp/ccm/resource/itemOid/com.ibm.team.workitem.Category/_c6Ue0NNsEei2Go0VaWWcug'

        body['rtc_cm:com.ibm.team.workitem.workItemType.defect.defect_category'] = {}
        body['rtc_cm:com.ibm.team.workitem.workItemType.defect.defect_category']['rdf:resource'] = 'https://www.somed002.sony.co.jp/ccm/oslc/enumerations/_cC2EQNNsEei2Go0VaWWcug/defect_categories/defect_categories.literal.l4'

        # 計画対象
        body['rtc_cm:plannedFor'] = {}
        body['rtc_cm:plannedFor']['rdf:resource'] = "https://www.somed002.sony.co.jp/ccm/oslc/iterations/_cQPAAdNsEei2Go0VaWWcug"

        # 所有者
        body['rtc_cm:ownedBy'] = {}
        body['rtc_cm:ownedBy']['rdf:resource'] = "https://www.somed002.sony.co.jp/jts/users/sibo.wang"

        # 検出方法
        body['rtc_cm:com.ibm.team.workitem.workItemType.defect.howto_detect'] = {}
        body['rtc_cm:com.ibm.team.workitem.workItemType.defect.howto_detect']['rdf:resource'] = 'https://www.somed002.sony.co.jp/ccm/oslc/enumerations/_cC2EQNNsEei2Go0VaWWcug/howto_detect/howto_detect.literal.l4'

        # 検出工程
        body['rtc_cm:com.ibm.team.workitem.workItemType.defect.detect_phase'] = {}
        body['rtc_cm:com.ibm.team.workitem.workItemType.defect.detect_phase']['rdf:resource'] = 'https://www.somed002.sony.co.jp/ccm/oslc/enumerations/_cC2EQNNsEei2Go0VaWWcug/detect_phase/detect_phase.literal.l84'

        # 発生日
        body['rtc_cm:com.ibm.team.workitem.workItemType.defect.detect_date'] = '2020-02-12T03:00:00.000Z'

        # 試験番号
        body['rtc_cm:com.ibm.team.workitem.workItemType.defect.exam_id'] = '1'

        # 発生トリガー
        body['rtc_cm:com.ibm.team.workitem.workItemType.defect.trigger'] = {}
        body['rtc_cm:com.ibm.team.workitem.workItemType.defect.trigger']['rdf:resource'] = 'https://www.somed002.sony.co.jp/ccm/oslc/enumerations/_cC2EQNNsEei2Go0VaWWcug/defect_trigger/defect_trigger.literal.l57'
        jsonStr = json.dumps(body)

        request = RequestBuilder('POST',
            url,
            headers = _headers,
            data = jsonStr
            ).build()
        response = self.sendRequest(request)

        obj = json.loads(response.text)
        for k, v in obj.items():
            print('{}: {}'.format(k, v))
