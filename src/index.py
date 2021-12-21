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
text**strong**text2
~~strike~~
abcd
efgh
![img](https://avatars2.githubusercontent.com/u/11307908)
[asmsuechan.com](https://asmsuechan.com)
```
code test
```
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