# coding:utf-8

from rtcclient.request import RequestBuilder
import xmltodict

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
    @classmethod
    def retrieveWorkItems(self, client, filter, properties=['id',], size=100, pos=0):

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

        for workItem in workItems:
            workItemList.append(WorkItem(workItem))

        return workItemList