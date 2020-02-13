# coding:utf-8

from rtcclient.client import RTCClient
from rtcclient.workitem import WorkItem
import sys

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

types = project.getTypes()
for item in types:
    print("type: {} {}".format(item.rdf_about, item.identifier))

obj = project.retrieveWorkItems(page_size=1)
print(project.getWorkItemTotalCount())

workItems = WorkItem.retrieveWorkItems(client,
    filter="projectArea/name='OlySandBox'",
    properties=['id', 'summary', 'type/id'], size=10)

for workitem in workItems:
    print(workitem.getProperty('id'))