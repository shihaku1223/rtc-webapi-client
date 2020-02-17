# coding:utf-8

from rtcclient.client import RTCClient
from rtcclient.workitem import WorkItem
import sys
import json
import collections


def printAttributeAllowedValueDict(project, defectType, title):
    print('{} allowedValue'.format(title))
    allowedValueDict = project.getAttributeAllowedValueDict(defectType, title)
    for title, resource in allowedValueDict.items():
        print(title, resource)

repository = "https://www.somed002.sony.co.jp/ccm"
username = "sibo.wang"
password = "sibo.wang"

client = RTCClient(repository, username, password)
client.login()

workItem = WorkItem.getWorkItemOSLCResource(client, 8888)
projectList = client.getProjectList()
for project in projectList:
    print(project._id)
    print(project.title)
 
project = client.getProjectAreaByName('OlySandBox')
print(project.title)
"""
properties = {
    'タイプ': '障害',
    '分類先': 'カテゴリー 1',
    '計画対象': 'リリース 1.0',
    '検出方法': '修正確認中',
    '検出工程': '[IPF-3]ソフトウェア結合試験',
    '発生トリガー': 'ソフトウェア構成',
    '障害カテゴリー': '1．正常系操作',
}

stringPropeties = {
    '発生日': '2020-02-12T03:00:00.000Z',
    '試験番号': '1'
}

project.createWorkItem('This is title.',
    'This is description.',
    'https://www.somed002.sony.co.jp/jts/users/sibo.wang',
    properties, stringPropeties)

"""

sys.exit(0)

print(client.getServiceProviderCatalogUrl())

workItems = WorkItem.retrieveWorkItems(client,
    filter="projectArea/name='OlySandBox'",
    properties=['id', 'summary', 'type/id'], size=10)

for workitem in workItems:
    print(workitem.getProperty('id'))

workItems = WorkItem.retrieveWorkItems(client,
    filter="id=8838",
    properties=['*/*'], size=10)

for workitem in workItems:
    print(workitem.getProperty('id'))
    print(workitem.getProperty('summary'))
    print(workitem.getProperty('type')['name'])

sys.exit(0)
"""
serviceList = projectList[0].workItemsServices()['rdf:RDF']['oslc:ServiceProvider']['oslc:service']

obj = project.retrieveWorkItems(page_size=1)['oslc_cm:Collection']['oslc_cm:ChangeRequest']
for i in obj:
    print(i, ' ',obj[i])
    if isinstance(obj[i], collections.OrderedDict):
        for j in obj[i]:
            print(j)
"""
print(project.getWorkItemTotalCount())
print('Project tile')
types = project.getTypes()
for item in types:
    print("type: {} {} {}".format(item.rdf_about, item.identifier, item.title))

defectType =  project.getTypeByName('障害')
print(defectType.title)

obj = project.getTypeAllowedValues(defectType)
"""
printAttributeAllowedValueDict(project, defectType, 'タイプ')
printAttributeAllowedValueDict(project, defectType, '分類先')
printAttributeAllowedValueDict(project, defectType, '計画対象')
printAttributeAllowedValueDict(project, defectType, '検出方法')
printAttributeAllowedValueDict(project, defectType, '検出工程')
printAttributeAllowedValueDict(project, defectType, '発生トリガー')
printAttributeAllowedValueDict(project, defectType, '障害カテゴリー')
"""


sys.exit(0)

