# coding:utf-8

from rtcclient.client import RTCClient

repository = "https://www.somed002.sony.co.jp/ccm"
username = "sibo.wang"
password = "sibo.wang"

client = RTCClient(repository, username, password)
client.login()
print(client.getServiceProviderCatalogUrl())
projectList = client.getProjectList()

for project in projectList:
    print(project.uuid)
    print(project.title)

serviceList = projectList[0].workItemsServices()['rdf:RDF']['oslc:ServiceProvider']['oslc:service']

count = projectList[1].getTypes()['rdf:RDF']['oslc:ResponseInfo']['oslc:totalCount']
print(count)
types = projectList[1].getTypes()['rdf:RDF']['oslc:ResponseInfo']['rdfs:member']
for item in types:
    print("Type")
    print(item)
