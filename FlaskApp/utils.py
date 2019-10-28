class ResultObject:
    def __init__(self,name,url, description):
        self.name = name
        self.url = url
        self.description = description

class GeneralResultInfo:
    def __init__(self, cnt_results, time):
        self.cnt_results = cnt_results
        self.time = time