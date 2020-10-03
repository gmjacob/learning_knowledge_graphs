import wikipedia
'''
    Extracts, stores and reads text data from a wikipedia page
'''
class TextExtractor:

    __pageTitle: str
    __pageId: str

    def __init__(self, pageTitle, pageId):
        self.__pageTitle = pageTitle
        self.__pageId = pageId

    def __getFilePath(self):
        return "./text/"+self.__pageTitle+".txt"

    def extract(self):
        page = wikipedia.page(
            title=self.__pageTitle,
            pageid= self.__pageId
            )
        print("File path")
        print(self.__getFilePath())
        f = open(self.__getFilePath(), "w")
        f.write(page.content)
        f.close()
    
    def getText(self):
        f = open(self.__getFilePath(), "r")
        return f.read()