class ResultObject:
    def __init__(self,name,url, description, value = 0):
        self.name = name
        self.url = url
        self.description = description
        self.value = value

class UploaddedFolderInfo:
    def __init__(self,folder_name,cnt_files,folder_temp_path):
        self.folder_name = folder_name
        self.cnt_files = cnt_files
        self.folder_temp_path = folder_temp_path

class GeneralResultInfo:
    def __init__(self, cnt_results, time):
        self.cnt_results = cnt_results
        self.time = time