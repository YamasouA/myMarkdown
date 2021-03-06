from re import I
import re
from models.myToken import Token

def isAllElmParentRoot(tokens):
    for token in tokens:
        if token.parent != None:
            if token.parent.elmType == 'root':
                continue
            else:
                return False
    return True

def getInsertPosition(content):
    state = 0
    closeTagParentheses = ['<', '>']
    position = 0
    # print('content')
    # print(content)
    for i, c in enumerate(list(content)):
        # print(c, i)
        if (state == 1) and (c == closeTagParentheses[state]):
            position = i
            break
        elif (state == 0) and (c == closeTagParentheses[state]):
            state += 1
    # print(position)
    # print(position)
    return position + 1

def createMergedContent(currentToken, parentToken):
    # print('=================createMergedContent====================')
    # print(currentToken.content)
    # print(parentToken.content)
    # print(parentToken.elmType)
    content = ''
    if parentToken.elmType == 'paragraph':
        content = '<p>' + currentToken.content + '</p>'
    elif parentToken.elmType == 'strong':
        # print("strong")
        content = '<strong>' + currentToken.content + '</strong>'
    elif parentToken.elmType == 'italic':
        content = '<i>' + currentToken.content + '</i>'
    elif parentToken.elmType == 'si':
        content = '<strike>' + currentToken.content + '</strike>'
    elif parentToken.elmType == 'merged':
        # print("merged")
        position = getInsertPosition(parentToken.content)
        content = parentToken.content[0:position] + currentToken.content + parentToken.content[position:]
    elif parentToken.elmType == 'li':
        # print('li')
        content = '<li>' + currentToken.content + '</li>'
    elif parentToken.elmType == 'ul':
        # print('ul')
        content = '<ul>' + currentToken.content + '</ul>'
    # print(content)
    elif parentToken.elmType == 'ol':
        content = '<ol>' + currentToken.content + '</ol>'
    elif parentToken.elmType == 'img':
        src = parentToken.attributes[0]['attrValue']
        # print(src)
        content = '<img src="' + src + '" alt="' + currentToken.content + '" />'
    elif parentToken.elmType == 'link':
        href = parentToken.attributes[0]['attrValue']
        content = '<a href="' + href + '">' + currentToken.content + '</a>'
    elif parentToken.elmType == 'code':
        content = '<code>' + currentToken.content + '</code>'
    elif parentToken.elmType == 'h1':
        content = '<h1>' + currentToken.content + '</h1>'
    elif parentToken.elmType == 'h2':
        content = '<h2>' + currentToken.content + '</h2>'
    elif parentToken.elmType == 'h3':
        content = '<h3>' + currentToken.content + '</h3>'
    elif parentToken.elmType == 'h4':
        content = '<h4>' + currentToken.content + '</h4>'
    elif parentToken.elmType == 'blockquote':
        content = '<blockquote>' + currentToken.content + '</blockquote>'
    elif parentToken.elmType == 'table':
        content = '<table>' + currentToken.content + '</table>'
    elif parentToken.elmType == 'tbody':
        content = '<tbody>' + currentToken.content + '</tbody>'
    elif parentToken.elmType == 'thead':
        content = '<thead>' + currentToken.content + '</thead>'
    elif parentToken.elmType == 'tr':
        content = '<tr>' + currentToken.content + '</tr>'
    elif parentToken.elmType == 'th':
        thAttributes = parentToken.attributes[0]['attrName'] + '=' + parentToken.attributes[0]['attrValue']
        content = '<th ' + thAttributes + '>' + currentToken.content + '</th>'
    elif parentToken.elmType == 'td':
        tdAttributes = parentToken.attributes[0]['attrName'] + '=' + parentToken.attributes[0]['attrValue']
        content = '<td ' + tdAttributes + '>' + currentToken.content + '</td>'
    # print(content)
    return content

def generateHtmlString(tokens):
    # print('generateHtmlString')
    s = []
    for token in tokens:
        if token.content == "":
            continue
        if token.elmType == 'break':
            s.append('<br>')
        s.append(token.content)
        # print(s)
    return ''.join(s[::-1])

def findindex(rearrangeAst, currentToken):
    idx = 0
    for ast in rearrangeAst:
        if ast.id == currentToken.parent.id:
            return idx
        idx += 1
    return -1

def mergeAsts(rearrangeAst):
    rearrangeAst = rearrangeAst[::-1]
    while not isAllElmParentRoot(rearrangeAst):
        index = 0
        while index < len(rearrangeAst):
            # print(rearrangeAst[index].content)
            if rearrangeAst[index].parent != None:
                if rearrangeAst[index].parent.elmType == 'root':
                    # print('root')
                    index += 1

                else:
                    currentToken = rearrangeAst[index]
                    rearrangeAst.pop(index)
                    parentIndex = findindex(rearrangeAst, currentToken)
                    parentToken = rearrangeAst[parentIndex]
                    mergedToken = Token()
                    mergedToken.create_token(parentToken.parent, parentToken.id, 'merged', createMergedContent(currentToken, parentToken))
                    rearrangeAst[parentIndex] = mergedToken
                    # parent??????????????????
                    # ?????????????????????????????????
                    # 1????????????????????????1??????????????????????????????index??????????????????
                    # ??????????????????????????????index++
    return generateHtmlString(rearrangeAst)


def generate(asts):
    # tokens.reverse()?????????????????????
    htmlString = list(map(mergeAsts, asts))
    return ''.join(htmlString)

