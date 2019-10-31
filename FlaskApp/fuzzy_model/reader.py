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

    def readDirectory(self, directory):
        list_of_files = listdir(directory)
        for filename in list_of_files:
            if isfile(filename):
                self.readFile(join(directory,filename))

    def readFile(self, filename):
        _format = filename.split(".")[-1]
        if _format in self.readFunction.keys():
            self.readFunction[_format](filename)

    def readFiles(self,files):
        for file in files:
            self.readFile(file)

    def __readJson(self, filename):
        name = filename.split("/")[-1]
        data = ""
        with open(filename, encoding='utf-8') as js:
            data_dict = json.load(js)

        for _dict in data_dict:
            for k in _dict.keys():
                self.__save_data(_dict[k], k)

    def __readPdf(self, filename):
        name = filename.split("/")[-1]
        data = ""
        with open(filename, 'rb') as pdf:
            pdfFile = PyPDF2.PdfFileReader(pdf)
            for i_page in range(pdfFile.numPages):
                data += pdfFile.getPage(i_page).extractText()
        self.__save_data(data, name)

    def __readTxt(self, filename):
        name = filename.split("/")[-1]
        data = ""
        with open(filename, 'r') as txt:
            data = txt.read()
        self.__save_data(data, name)

    def __save_data(self, data, name):
        tokens = allPreprocess(data)

        doc = Document(name)
        for elem in tokens:
            doc[elem] = 1
            self.vocab.add(elem)
        self.documents.append(doc)

class Document(dict):
    def __init__(self, name):
        super(dict,self).__init__()
        self.name = name

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