import re
from parser import parse
from generator import generate
from lexer import analize

def convertToHTMLString(markdown):
    mdArray = analize(markdown)
    # print('mdArray')
    # print(mdArray)
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
    s = '''
# h1
## h2
### h3
#### h4
text
**bold**
~~strike~~
__italic__
![img](https://avatars2.githubusercontent.com/u/11307908)
[asmsuechan.com](https://asmsuechan.com)
```
code
```
> blockquote1
>> blockquote2
>> blockquote2-2
>>> blockquote3



- list1
- list2
 1. nest_list1
 2. nest_list2
- list3

|table left|table center|table right|
|:---------|:----------:|----------:|
|left row1|center row1|right row1|
|left row2|center row2|right row2|
|left row3|center row3|right row3|
'''

    ret = convertToHTMLString(s)
    print('input: ' + s)
    print('output:' + ret)