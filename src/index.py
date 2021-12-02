import re
from parser import parse

def convertToHTMLString(markdown):
    mdArray = re.split(r'\r\n|\r|\n', markdown)
    asts = list(map(parse, mdArray))
    return asts

if __name__ == "__main__":
    ret = convertToHTMLString('aaas**bo**bold**ld**')
    print("=============test============")
    for token in ret:
        for text in token:
            print(text.id)
            print(text.content)
            print(text.elmType)
            print(text.parent)
