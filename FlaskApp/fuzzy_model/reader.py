import PyPDF2
import json
from fuzzy_model.preprocess import allPreprocess
from os import listdir
from os.path import isfile, join
class Reader():
    def __init__(self):
        self.readFunction = {
            "txt" : self.__readTxt,
            "pdf" : self.__readPdf,
            "json" : self.__readJson
        }
        self.vocab = set()
        self.documents = []

    def readDirectory(self, directory,names=[]):
        list_of_files = listdir(directory)
        print(f'Se encuentran {list_of_files}')
        result = []
        for filename in list_of_files:
            path = join(directory,filename)
            if isfile(path):
                print(f'its a file {filename}')
                a = self.readFile(path)
                for name,content in a:
                    if name in names:
                        result.append(content)
        return result

    def readFile(self, filename):
        _format = filename.split(".")[-1]
        if _format in self.readFunction.keys():
            return self.readFunction[_format](filename)
        return []

    def readFiles(self,files):
        for file in files:
            self.readFile(file)

    def __readJson(self, filename):
        if "tesauro" in filename: return []
        name = filename.split("/")[-1]
        data = ""
        with open(filename, encoding='utf-8') as js:
            data_dict = json.load(js)
        result = []
        try:
            data_dict[0]["title"]
            for _dict in data_dict:                
                result.append(self.__save_data(_dict["narr"], _dict["title"], desc=_dict["desc"]))
        except:
            for _dict in data_dict:
                for k in _dict.keys():
                    result.append(self.__save_data(_dict[k], k))

        return result

    def __readPdf(self, filename):
        name = filename.split("/")[-1]
        data = ""
        with open(filename, 'rb') as pdf:
            pdfFile = PyPDF2.PdfFileReader(pdf)
            for i_page in range(pdfFile.numPages):
                data += pdfFile.getPage(i_page).extractText()
        return [self.__save_data(data, name)]
        
        
    def __readTxt(self, filename):
        print(f" Analizando el file {filename}")
        name = filename.split("/")[-1]
        data = ""
        with open(filename, 'r') as txt:
            data = txt.read()
        return [self.__save_data(data, name)]
         
    
    def __save_data(self, data, name,desc=""):
        tokens = allPreprocess(data)
        doc = Document(name,desc)
        for elem in tokens:
            doc[elem] = 1
            self.vocab.add(elem)
        self.documents.append(doc)
        return (name,doc)
        
class Document(dict):
    def __init__(self, name, description=""):
        super(dict,self).__init__()
        self.name = name
        self.description = description

    def __getitem__(self, i):
        try:
            return dict.__getitem__(self, i)
        except:
            return 0

    def __str__(self):
        return "{} => {}".format(self.name, dict.__str__(self))

#print(r.vocab)
#for doc in r.documents:
#    print(doc)