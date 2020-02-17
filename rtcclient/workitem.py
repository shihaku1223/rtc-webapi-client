# coding:utf-8

from rtcclient.request import RequestBuilder
import xmltodict
import collections

class WorkItem(object):

    def __init__(self, raw_dict):
        self._raw_dict =  raw_dict

        """
        for identifier in raw_dict:
            #print(identifier, raw_dict[identifier])
            if identifier == 'id':
                self._id = raw_dict[identifier]
        """

    def getProperty(self, propertyName):
        return self._raw_dict[propertyName]

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
        print(url)
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
            workItemList.append(WorkItem(workItems))
            return workItemList

        for workItem in workItems:
            workItemList.append(WorkItem(workItem))

        return workItemList

class AttributeTypeMap:

    def __init__(self, map_dict=None):
        self._map_dict = {
            'ID': 'dc:identifier',
            '要約': 'dc:title',
            '說明': 'dc:description',
            'タイプ': 'dc:type',

            '分類先': 'rtc_cm:filedAgainst',
            '計画対象': 'rtc_cm:plannedFor',
            '所有者': 'rtc_cm:ownedBy',

            '検出方法': 'rtc_cm:com.ibm.team.workitem.workItemType.defect.howto_detect',

            '検出工程': 'rtc_cm:com.ibm.team.workitem.workItemType.defect.detect_phase',

            '障害カテゴリー': 'rtc_cm:com.ibm.team.workitem.workItemType.defect.defect_category',

            '発生日': 'rtc_cm:com.ibm.team.workitem.workItemType.defect.detect_date',

            '試験番号': 'rtc_cm:com.ibm.team.workitem.workItemType.defect.exam_id',

            '発生トリガー': 'rtc_cm:com.ibm.team.workitem.workItemType.defect.trigger'
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
