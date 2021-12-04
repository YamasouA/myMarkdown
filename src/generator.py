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
    for c, i in enumerate(content.split()):
        if state == 1 & c == closeTagParentheses[state]:
            position = i
            break
        elif state == 0 & c == closeTagParentheses[state]:
            state += 1
    return position + 1

def createMergedContent(currentToken, parentToken):
    content = ''
    if parentToken.elmType == 'strong':
        content = '<strong>' + currentToken.content + '</strong>'
    elif parentToken.elmType == 'merged':
        position = getInsertPosition(parentToken.content)
        content = parentToken.content[0:position] + currentToken.content + parentToken.content[:position]
    return content

def generateHtmlString(tokens):
    s = []
    for token in tokens:
        if token.content == "":
            continue
        s.append(token.content)
    print(s)
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
    print("---------------mergeAsts------------------")
    while not isAllElmParentRoot(rearrangeAst):
        index = 0
        while index < len(rearrangeAst):
            if rearrangeAst[index].parent != None:
                if rearrangeAst[index].parent.elmType == 'root':
                    index += 1

                else:
                    currentToken = rearrangeAst[index]
                    rearrangeAst.pop(index)
                    parentIndex = findindex(rearrangeAst, currentToken)
                    print(parentIndex)
                    parentToken = rearrangeAst[parentIndex]
                    mergedToken = Token()
                    mergedToken.create_token(parentToken.parent, parentToken.id, 'merged', createMergedContent(currentToken, parentToken))
                    rearrangeAst[parentIndex] = mergedToken
                    # parentとマージする
                    # 子は削除、親は置き換え
                    # 1つ親と合成したら1つ要素を消す。ので、indexは変わらない
                    # マージしないときだけindex++
    return generateHtmlString(rearrangeAst)


def generate(asts):
    # tokens.reverse()はエラーになる
    htmlString = list(map(mergeAsts, asts))
    return ''.join(htmlString)

