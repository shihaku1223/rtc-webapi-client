# coding:utf-8

class Type:

    def __init__(self, obj_dict):

        rootDict = obj_dict['rtc_cm:Type']

        self.rdf_about = rootDict['@rdf:about']
        self.projectArea = rootDict['rtc_cm:projectArea']['@rdf:resource']
        self.category = rootDict['rtc_cm:category']
        self.iconUrl = rootDict['rtc_cm:iconUrl']
        self.title = rootDict['dcterms:title']['#text']
        self.identifier = rootDict['dcterms:identifier']['#text']
