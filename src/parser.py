import re
from models.myToken import Token

from lexer import genStrongElement, genTextElement, matchWithListRegxp, matchWithStrongRegxp

rootToken = Token()
rootToken.create_token(None, 0, 'root', '')


def tokenizeText(textElement, initialId = 0, initialRoot = rootToken):
    elements = []
    parent = initialRoot
    id = initialId
    
    def tokenize(originalText, p):
        nonlocal id
        processingText = originalText
        parent = p
        # 行が空になるまで繰り返す
        while (len(processingText) != 0):
            matchArray, index = matchWithStrongRegxp(processingText)
            # matchArray[0] -> **bold**
            # matchArray[1] -> bold
            
            # ****にマッチしないとき、テキストトークンを作成する
            if matchArray is  None:
                id += 1
                onlyText = genTextElement(id, processingText, parent)
                processingText = ''
                elements.append(onlyText)
            else:
                if (index > 0):
                    # aaa**bb**cc -> TEXT_TOKEN + **bb**cc　にする
                    text = processingText[:index]
                    id += 1
                    textElm = genTextElement(id, text, parent)
                    elements.append(textElm)
                    processingText = processingText.replace(text, '')
                id += 1
                elm = genStrongElement(id, parent)
                parent = elm
                elements.append(elm)

                processingText = processingText.replace(matchArray[0], '')

                tokenize(matchArray[1], parent)
                parent = p
    tokenize(textElement, parent)
    return elements

def tokenizeList(listString):
    UL = 'ul'
    LIST = 'li'

    id = 1
    rootUlToken = Token()
    rootUlToken.create_token(rootToken, id, UL, '')
    parents = [rootUlToken]
    parent = rootUlToken
    tokens = [rootUlToken]
    sep = re.split(r'\r\n|\r|\n', listString)
    print('in tokenizeList')
    print(sep)
    for l in sep:
        if l == '':
            continue
        print('in loop')
        print(l)
        match = matchWithListRegxp(l)
        id += 1
        listToken = Token()
        listToken.create_token(parent, id, LIST, '')
        parents.append(listToken)
        tokens.append(listToken)
        listText = tokenizeText(match[3], id, listToken)
        id += len(listText)
        tokens.extend(listText)
    return tokens

def parse(markdownRow):
    print('markdown')
    if matchWithListRegxp(markdownRow):
        return tokenizeList(markdownRow)
    return tokenizeText(markdownRow)