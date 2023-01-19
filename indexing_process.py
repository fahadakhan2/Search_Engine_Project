
class DocumentCollection:
    pass

class Index:
    pass


class Source:
    def read_documents(self):
        pass



def transform_documents(document_collection):
    pass


def create_index(transformed_documents):
    pass


def indexing_process(document_source: Source) -> (DocumentCollection, Index):
    document_collection = document_source.read_documents()
    transformed_documents = transform_documents(document_collection)
    index = create_index(transformed_documents)
    return (document_collection, index)