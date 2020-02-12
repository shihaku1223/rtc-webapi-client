# coding:utf-8

class Type:

    def __init__(self, client, obj_dict):

        self.rdf_about = obj_dict['@rdf:about']
        self.projectArea = obj_dict['rtc_cm:projectArea']['@rdf:resource']
        self.category = obj_dict['rtc_cm:category']
        self.iconUrl = obj_dict['rtc_cm:iconUrl']
        self.title = obj_dict['dcterms:title']['#text']
        self.identifier = obj_dict['dcterms:identifier']['#text']
