import typing


def tokenize(document_text: str) -> typing.List[str]:
    return document_text.replace('.', ' . ').replace(',', ' , ').lower().split()
