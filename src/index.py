import re
from parser import parse
from generator import generate

def convertToHTMLString(markdown):
    print("===============parse==================")
    mdArray = re.split(r'\r\n|\r|\n', markdown)
    print(mdArray)
    asts = list(map(parse, mdArray))
    for i in asts:
        for ast in i:
            print(ast)
            print(ast.id)
            print(ast.content)
            print(ast.elmType)
            print(ast.parent)
    print("===============generate==================")
    htmlString = generate(asts)
    return htmlString

if __name__ == "__main__":
    s = 'aaas**bo**bold**ld**\n- **hello**'
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