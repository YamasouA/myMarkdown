import re
from models.myToken import Token

from lexer import genStrongElement, genTextElement, matchWithListRegxp, matchWithStrongRegxp

rootToken = Token()
rootToken.create_token(None, 0, 'root', '')

STRONG_ELM_REGXP = r'\*\*(.*?)\*\*'
LIST_REGXP = r'^( *)([-|\*|\+] (.+))$'
OL_REGEXP = r'( *)((\d+)\. (.+))$'

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
    OL = 'ol'

    listMatch = re.search(LIST_REGXP, listString)
    olMatch = re.search(OL_REGEXP, listString)

    rootType = (listMatch and UL) or (olMatch and OL)


    id = 1
    rootUlToken = Token()
    rootUlToken.create_token(rootToken, id, rootType, '')
    parents = [rootUlToken]
    parent = rootUlToken
    tokens = [rootUlToken]
    prevIndentLevel = 0

    sep = re.split(r'\r\n|\r|\n', listString)
    print('in tokenizeList')
    print(sep)
    for l in sep:
        if l == '':
            continue
        print('in loop')
        print(l)
        # match = matchWithListRegxp(l)
        listType = UL if re.match(LIST_REGXP, l) else OL
        match = re.match(LIST_REGXP, l) if listType == UL else re.match(OL_REGEXP, l)
        print(listType)
        currentIndentLevel = len(match[1])
        currentIndent = match[1]
        print(currentIndentLevel, prevIndentLevel)
        if currentIndentLevel < prevIndentLevel:
            # change the parent
            for i in range(len(parents) - 1):
                # ネストする前の親要素を見つける
                if (len(parents[i].content) <= currentIndentLevel)  \
                    and (currentIndentLevel < len(parents[i+1].content)):
                    parent = parents[i]
        elif currentIndentLevel > prevIndentLevel:
            id += 1
            lastToken = tokens[-1]
            parentToken = lastToken.parent if match and lastToken.parent.elmType in ['code', 'italic', 'si', 'strong'] else lastToken
            newParent = Token()
            newParent.create_token(id=id, elmType=listType, content=currentIndent, parent=parentToken.parent)
            parents.append(newParent)
            tokens.append(newParent)
            parent = newParent
        prevIndentLevel = currentIndentLevel

        id += 1
        listToken = Token()
        listToken.create_token(parent, id, LIST, '')
        parents.append(listToken)
        tokens.append(listToken)
        # contentはlistなら3番目OLなら4番目
        listContent = match[3] if listType==UL else match[4]
        listText = tokenizeText(listContent, id, listToken)
        id += len(listText)
        tokens.extend(listText)
    print(tokens)
    return sorted(tokens, key=lambda token: token.id)

def parse(markdownRow):
    # print('markdown')
    # if matchWithListRegxp(markdownRow):
    #     return tokenizeList(markdownRow)
    # return tokenizeText(markdownRow)

    if markdownRow["mdType"] == 'list':
        return tokenizeList(markdownRow["content"])
    return tokenizeText(markdownRow["content"])