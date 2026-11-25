##################### PDF loader ##########################

from langchain_community.document_loaders import PyPDFLoader

class DATA_LOADER:
    def __init__(self,pdf_path):
        self.pdf_path=pdf_path
    def pdf_load(self):
        loader = PyPDFLoader(self.pdf_path)
        documents = loader.load()
        return(documents)

if __name__=="__main__":
    obj= DATA_LOADER(r"/Users/deviprasadchebodula/Downloads/attention_is_all_you_need.pdf")
    docs=obj.pdf_load()