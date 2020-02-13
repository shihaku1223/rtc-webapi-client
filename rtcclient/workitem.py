# coding:utf-8

class WorkItem:

    def __init__(self):
        self._id = None

    @classmethod
    def retrieveWorkItems(client, properities, size=100, pos=0):
        url = client.repository + \
            '/rpt/repository/workitem?fields=workitem/workItem' \
            '[projectArea/name=\'{}\']/id' \
            '&size={}&pos={}'
        url = url.format('OlySandBox'. size, pos)

        _headers = {}
        _headers['Accept'] = 'application/xml'

        request = RequestBuilder('GET',
            url,
            headers = _headers
            ).build()
        response = client.sendRequest(request)
        return response

