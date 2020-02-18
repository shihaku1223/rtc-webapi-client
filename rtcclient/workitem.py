# coding:utf-8

from rtcclient.request import RequestBuilder
import xmltodict
import collections
import json

class WorkItem(object):

    RAW_DATATYPE = {
        'DATATYPE_RPTXML': 1,
        'DATATYPE_OSLCJSON': 2
    }

    def __init__(self, raw_data, data_type):
        self._rawDataType = None

        if data_type not in self.RAW_DATATYPE:
            raise Exception('Not supported data type.')

        self._rawDataType = self.RAW_DATATYPE[data_type]

        if raw_data is not None:
            self._raw_data = raw_data

    def getBody(self):
        return self._raw_data

    def getId(self):
        if self._rawDataType == self.RAW_DATATYPE['DATATYPE_OSLCJSON']:
            return self._raw_data['dcterms:identifier']
        elif self._rawDataType == self.RAW_DATATYPE['DATATYPE_RPTXML']:
            return self._raw_data['id']

        raise Exception('Unknown data type')

    def getProperty(self, propertyName):
        return self._raw_data[propertyName]

    def updateWorkItem(self, client, eTag, action = None):

        url = client.repository + \
            '/resource/itemName/com.ibm.team.workitem.WorkItem/{}'
        url = url.format(self.getId())

        if action is not None:
            url = url + '?_action={}'.format(action)

        _headers = {}
        _headers['Accept'] = 'application/json'
        _headers['OSLC-Core-Version'] = '2.0'
        _headers['Content-Type'] = 'application/json'
        _headers['If-Match'] = eTag

        jsonStr = json.dumps(self.getBody())

        request = RequestBuilder('PUT',
            url,
            data = jsonStr,
            headers = _headers
            ).build()
        response = client.sendRequest(request)
        obj_dict =  json.loads(response.text)
        for k, v in obj_dict.items():
            print(k, v)

    @staticmethod
    def createWorkItemRPT(rptXML):
        return WorkItem(raw_data=rptXML, data_type='DATATYPE_RPTXML')

    @staticmethod
    def createWorkItemOSLCJSON(oslcJSON):
        return WorkItem(raw_data=oslcJSON, data_type='DATATYPE_OSLCJSON')

    @staticmethod
    def getWorkItemOSLCResource(client, workItemId):
        url = client.repository + \
            '/oslc/workitems/{}'
        url = url.format(workItemId)

        _headers = {}
        _headers['Accept'] = 'application/json'
        _headers['OSLC-Core-Version'] = '2.0'

        request = RequestBuilder('GET',
            url,
            headers = _headers
            ).build()
        response = client.sendRequest(request)
        obj_dict =  json.loads(response.text)

        return WorkItem.createWorkItemOSLCJSON(obj_dict), response.headers['ETag']

    # filter = "projectArea/name='Test' and owner/name='ABC'"
    @staticmethod
    def retrieveWorkItems(client, filter, properties=['id',], size=100, pos=0):

        elements = ''
        if properties is None:
            elements = '(*)'
        else:
            lis = iter(properties)
            first = next(lis)
            elements = '({}'.format(first)
            for elem in lis:
                elements += '|{}'.format(elem)

        elements +=')'

        url = client.repository + \
            '/rpt/repository/workitem?fields=workitem/workItem' \
            '[{}]/{}' \
            '&size={}&pos={}'
        url = url.format(filter, elements, size, pos)

        _headers = {}
        _headers['Accept'] = 'application/xml'

        request = RequestBuilder('GET',
            url,
            headers = _headers
            ).build()
        response = client.sendRequest(request)

        obj_dict = xmltodict.parse(response.text)

        workItems = obj_dict['workitem']['workItem']

        workItemList = []
        # only one workitem
        if isinstance(workItems, collections.OrderedDict):
            workItemList.append(WorkItem.createWorkItemRPT(workItems))
            return workItemList

        for workItem in workItems:
            workItemList.append(WorkItem.createWorkItemRPT(workItem))

        return workItemList

class AttributeTypeMap:

    def __init__(self, map_dict=None):
        self._map_dict = {
            'ID': 'dcterms:identifier',
            '要約': 'dcterms:title',
            '說明': 'dcterms:description',
            '所有者': 'dcterms:contributor',

            'タイプ': 'rtc_cm:type',
            '分類先': 'rtc_cm:filedAgainst',
            '計画対象': 'rtc_cm:plannedFor',

            '検出方法': 'rtc_ext:com.ibm.team.workitem.workItemType.defect.howto_detect',
            '検出工程': 'rtc_ext:com.ibm.team.workitem.workItemType.defect.detect_phase',
            '障害カテゴリー': 'rtc_ext:com.ibm.team.workitem.workItemType.defect.defect_category',
            '発生日': 'rtc_ext:com.ibm.team.workitem.workItemType.defect.detect_date',
            '試験番号': 'rtc_ext:com.ibm.team.workitem.workItemType.defect.exam_id',
            '発生トリガー': 'rtc_ext:com.ibm.team.workitem.workItemType.defect.trigger',
            '解決状況': 'rtc_ext:com.ibm.team.workitem.workItemType.defect.resolve_state',
        }

        if map_dict is not None:
            self._map_dict.update(map_dict)

    def getTypeByTitle(self, title):
        return self._map_dict[title]

    def getTitleByType(self, typeName):
        for k, v in self._map_dict:
            if typeName == v:
                return k
        return None
