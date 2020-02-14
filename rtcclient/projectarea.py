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
        obj_dict = xmltodict.parse(response.text)['rdf:RDF']['rdf:Description']

        allowedValueDict = {}
        allowedValueDict['allowedValue'] = {}
        allowedValueDict['type'] = {}
        for desc in obj_dict:
            print("DESC")
            rdf_about = None
            if '@rdf:about' in desc:
                rdf_about = desc['@rdf:about']

                if rdf_about.split('/')[-1] == 'allowedValues':
                    allowedValueDict['allowedValue'][rdf_about] = []
                    allowedValueList = allowedValueDict['allowedValue'][rdf_about]
                    print(rdf_about)
                    if 'oslc:allowedValue' in desc:
                        for allowValue in desc['oslc:allowedValue']:
                            print(allowValue['@rdf:resource'])
                            allowedValueList.append(allowValue['@rdf:resource'])

            if 'oslc:name' in desc:
                typeName = desc['oslc:name']['#text']
                allowedValueDict['type'][typeName] = {}
                allowedValueDict['type'][typeName]['@rdf:about'] = rdf_about

                if 'dcterms:title' in desc:
                    print(desc['dcterms:title']['#text'])
                    allowedValueDict['type'][typeName]['title'] = desc['dcterms:title']['#text']

                if 'oslc:allowedValues' in desc:
                    allowedValueDict['type'][typeName]['allowedValues'] = desc['oslc:allowedValues']['@rdf:resource']
                    print(desc['oslc:allowedValues']['@rdf:resource'])

                if 'oslc:defaultValue' in desc:
                    if desc['oslc:defaultValue'] is not None:
                        if '@rdf:resource' in desc['oslc:defaultValue']:
                            allowedValueDict['type'][typeName]['defaultValue'] = desc['oslc:defaultValue']['@rdf:resource']
                            print(desc['oslc:defaultValue']['@rdf:resource'])
                        else:
                            allowedValueDict['type'][typeName]['defaultValue'] = desc['oslc:defaultValue']
        return allowedValueDict

    def getAttributeTitle(self, attributeUrl):
        _headers = {}
        _headers['Accept'] = 'application/rdf+xml'
        _headers['OSLC-Core-Version'] = '2.0'

        request = RequestBuilder('GET',
            attributeUrl,
            headers = _headers
            ).build()
        response = self.sendRequest(request)
        obj_dict = xmltodict.parse(response.text)['rdf:RDF']['rdf:Description']

        if 'dcterms:title' not in obj_dict:
            return None
        if '#text' not in obj_dict['dcterms:title']:
            return None

        return obj_dict['dcterms:title']['#text']

    def getAttributeAllowedValueDict(self, type, attributeTitle):
        allowedValueDict = self.getTypeAllowedValues(type)
        attributeTypes = allowedValueDict['type']
        allowedValues = allowedValueDict['allowedValue']

        attributeResourceDict = {}
        for typeName, attr in attributeTypes.items():
            #print('{}: {}'.format(attr['title'], typeName))
            if attr['title'] != attributeTitle:
                continue
            if 'allowedValues' in attr:
                print(attr['allowedValues'])
                for attribute in allowedValues[attr['allowedValues']]:
                    attributeResourceDict[self.getAttributeTitle(attribute)] = attribute
                    #print(attribute, self.getAttributeTitle(attribute))

        return attributeResourceDict

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
