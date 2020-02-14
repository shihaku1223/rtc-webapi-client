# coding:utf-8

from rtcclient.client import RTCClient
from rtcclient.workitem import WorkItem
import sys

import collections

repository = "https://www.somed002.sony.co.jp/ccm"
username = "sibo.wang"
password = "sibo.wang"

client = RTCClient(repository, username, password)
client.login()
print(client.getServiceProviderCatalogUrl())
projectList = client.getProjectList()

for project in projectList:
    print(project._id)
    print(project.title)
 
project = client.getProjectAreaByName('OlySandBox')
print(project.title)

serviceList = projectList[0].workItemsServices()['rdf:RDF']['oslc:ServiceProvider']['oslc:service']

obj = project.retrieveWorkItems(page_size=1)['oslc_cm:Collection']['oslc_cm:ChangeRequest']
for i in obj:
    print(i, ' ',obj[i])
    if isinstance(obj[i], collections.OrderedDict):
        for j in obj[i]:
            print(j)
print(project.getWorkItemTotalCount())

types = project.getTypes()
for item in types:
    print("type: {} {}".format(item.rdf_about, item.identifier))

defectType =  types[-1]
obj = project.getTypeAllowedValues(defectType)['rdf:RDF']['rdf:Description']
for desc in obj:
    print("DESC")

    if 'dcterms:title' in desc:
        print(desc['dcterms:title']['#text'])

    if 'oslc:allowedValues' in desc:
        print(desc['oslc:allowedValues']['@rdf:resource'])

    if 'oslc:allowedValue' in desc:
        print(desc['oslc:allowedValue'][0]['@rdf:resource'])
    """
    for key, value in desc.items():
        print(key, value)
    """


print(project.title)
project.createWorkItemTest()
sys.exit(0)

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