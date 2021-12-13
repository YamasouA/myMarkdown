import re
from parser import parse
from generator import generate
from lexer import analize

def convertToHTMLString(markdown):
    print("===============parse==================")
    # mdArray = re.split(r'\r\n|\r|\n', markdown)
    mdArray = analize(markdown)
    print('mdArray')
    print(mdArray)
    asts = list(map(parse, mdArray))
    print('===========asts============')
    for i in asts:
        print("===============loop=================")
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
    # s = '* list1\n* list2'
    # ret = convertToHTMLString(s)
    # print('input: ' + s)
    # print('output: ' + ret)
    s = '''
        1. sample
            * sample2
            * sample3
        2. sample4'''
    s = '''
# **H1**
## H2
### H3
#### H4
text**strong**text2
1. sample1 # 3
    1. **sample2**
    2. **sample3**
2. sample4
'''
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