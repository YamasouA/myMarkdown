import re
from parser import parse
from generator import generate

def convertToHTMLString(markdown):
    print("===============parse==================")
    mdArray = re.split(r'\r\n|\r|\n', markdown)
    asts = list(map(parse, mdArray))
    # s = ''
    # for i in asts:
    #     for ast in i:
    #         print(ast.id)
    #         print(ast.content)
    #         print(ast.elmType)
    #         print(ast.parent)
    #         s += ast.content
    #     print(s)
    print("===============generate==================")
    htmlString = generate(asts)
    return htmlString

if __name__ == "__main__":
    s = 'aaas**bo**bold**ld**'
    ret = convertToHTMLString(s)
    print('input: ' + s)
    print('output:' + ret)
    # print("=============start parse test============")
    # for token in ret:
    #     for text in token:
    #         print(text.id)
    #         print(text.content)
    #         print(text.elmType)
    #         print(text.parent)
    # print("=============end parse test=============")
    # print("")
    # print("==================start generate test=================")
    # print(convertToHTMLString('normal'))