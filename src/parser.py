import re
from models.myToken import Token

from lexer import genStrongElement, genTextElement, matchWithListRegxp, matchWithStrongRegxp

rootToken = Token()
rootToken.create_token(None, 0, 'root', '')

STRONG_ELM_REGXP = r'\*\*(.*?)\*\*'
LIST_REGXP = r'^( *)([-|\*|\+] (.+))$'
OL_REGEXP = r'( *)((\d+)\. (.+))$'
H1_REGEXP = r'^# (.+)$'
TEXT_ELM_REGEXPS = [
    {'elmType': 'h1', 'regexp': H1_REGEXP},
    {'elmType': 'h2', 'regexp': r'^## (.+)$'},
    {'elmType': 'h3', 'regexp': r'^### (.+)$'},
    {'elmType': 'h4', 'regexp': r'^#### (.+)$'},
    {'elmType': 'strong', 'regexp': r'\*\*(.*?)\*\*'},
    {'elmType': 'italic', 'regexp': r'__(.+)__'},
    ]

def tokenizeText(textElement, initialId = 0, initialRoot = rootToken):
    elements = []
    parent = initialRoot
    id = initialId
    
    def tokenize(originalText, p):
        print("tokenize!!!!!!!!!!")
        nonlocal id
        processingText = originalText
        parent = p
        # 行が空になるまで繰り返す
        while (len(processingText) != 0):
            print('Processing Text: ', processingText)
            # matchArray, index = matchWithStrongRegxp(processingText)
            # matchArray[0] -> **bold**
            # matchArray[1] -> bold
            matchArray = []
            for regexp in TEXT_ELM_REGEXPS:
                # print('processingText: ', processingText, ' regexp: ', regexp["regexp"])
                find = re.search(regexp["regexp"], processingText, flags=re.M)
                # print('find: ', find)
                # index = processingText.find(regexp["regexp"])
                index = find.start() if find else -1
                
                # print(index)
                matchArray.append({'elmType': regexp["elmType"], 'matchArray': find, 'index': index})
            # print(matchArray)
            matchArray = list(filter(lambda x: x["matchArray"] != None, matchArray))
            # print("matchArray")
            # print(matchArray)
            if len(matchArray) == 0:
                id += 1
                onlyText = genTextElement(id, processingText, parent)
                processingText = ''
                elements.append(onlyText)
            else:
                # 最も外側の状態をでマッチしたelementを保持する
                # **__itaric__**みたいに入れ子になっているのに対応する
                outerElement = ''
                prev = 10e8
                for match in matchArray:
                    if match["index"] < prev:
                        prev = match["index"]
                        outerElement = match
                # print("outerElement: ", outerElement["index"])
                if (outerElement["index"] > 0):
                    # aaa**bb**cc -> TEXT_TOKEN + **bb**cc　にする
                    text = processingText[:outerElement["index"]]
                    id += 1
                    textElm = genTextElement(id, text, parent)
                    elements.append(textElm)
                    processingText = processingText.replace(text, '', 1)
                id += 1
                elmType = outerElement["elmType"]
                content = outerElement["matchArray"][1]
                elm = Token()
                elm.create_token(id=id, elmType=elmType, content='', parent=parent)
                parent = elm
                elements.append(elm)
                print("processing Text bef: ", processingText)
                processingText = processingText.replace(outerElement["matchArray"][0], '')
                print("processing Text aft: ", processingText)
                tokenize(content, parent)
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
        print(parent.id)
        if currentIndentLevel < prevIndentLevel:
            print("case1")
            print("listType: ", listType)
            print("id: ", id)
            # change the parent
            for i in range(len(parents) - 1):
                # ネストする前の親要素を見つける
                if (len(parents[i].content) <= currentIndentLevel)  \
                    and (currentIndentLevel < len(parents[i+1].content)):
                    print("cahnge parent")
                    print("listType: ", listType)
                    print("id: ", id)
                    print("len: ", len(parents))
                    parent = parents[i].parent
                    print("parent.id: ", parent.id)
        elif currentIndentLevel > prevIndentLevel:
            print("case2")
            print("listType: ", listType)
            print("id: ", id)
            id += 1
            lastToken = tokens[-1]
            # text Tokenの親トークンを見る（strongとかならさらに親を見る）
            parentToken = lastToken.parent if match and lastToken.parent.elmType in ['code', 'italic', 'si', 'strong'] else lastToken
            newParent = Token()
            newParent.create_token(id=id, elmType=listType, content=currentIndent, parent=parentToken.parent)
            parents.append(newParent)
            tokens.append(newParent)
            parent = newParent
            print("parent.id: ", parent.id)
            print("currentIndent: ", currentIndentLevel)
        prevIndentLevel = currentIndentLevel

        id += 1
        print("out if")
        print("id: ", id)
        print("elmType: ", listType)
        print("parent.id: ", parent.id)
        listToken = Token()
        listToken.create_token(parent, id, LIST, currentIndent)
        parents.append(listToken)
        tokens.append(listToken)
        # contentはlistなら3番目OLなら4番目
        listContent = match[3] if listType==UL else match[4]
        print("listContent: ", listContent)
        listText = tokenizeText(listContent, id, listToken)
        id += len(listText)
        print("aft id: ", id)
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