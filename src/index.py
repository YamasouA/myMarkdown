import re
from parser import parse
from generator import generate
from lexer import analize

def convertToHTMLString(markdown):
    print("===============parse==================")
    # mdArray = re.split(r'\r\n|\r|\n', markdown)
    mdArray = analize(markdown)
    print(mdArray)
    asts = list(map(parse, mdArray))
    # for i in asts:
    #     for ast in i:
    #         print(ast)
    #         print(ast.id)
    #         print(ast.content)
    #         print(ast.elmType)
    #         print(ast.parent)
    print("===============generate==================")
    htmlString = generate(asts)
    return htmlString

if __name__ == "__main__":
    # s = '* list1\n* list2'
    # ret = convertToHTMLString(s)
    # print('input: ' + s)
    # print('output: ' + ret)
    s = 'normal text\n \n * **boldlist1**\n * list2'
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