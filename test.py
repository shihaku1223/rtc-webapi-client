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
 
project = client.getProjectAreaByName('OlySandBox')
print(project.title)

serviceList = projectList[0].workItemsServices()['rdf:RDF']['oslc:ServiceProvider']['oslc:service']

types = project.getTypes()
for item in types:
    print("type: {} {}".format(item.rdf_about, item.identifier))
