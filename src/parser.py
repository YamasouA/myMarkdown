import re
from models.myToken import Token

from lexer import BLOCKQUOTE_REGEXP, genStrongElement, genTextElement, matchWithListRegxp, matchWithStrongRegxp

rootToken = Token()
rootToken.create_token(None, 0, 'root', '')

STRONG_ELM_REGXP = r'\*\*(.*?)\*\*'
LIST_REGXP = r'^( *)([-|\*|\+] (.+))$'
OL_REGEXP = r'( *)((\d+)\. (.+))$'
H1_REGEXP = r'^# (.+)$'
BLOCKQUOTE_REGEXP = r'([>| ]+)(.+)'
TEXT_ELM_REGEXPS = [
    {'elmType': 'h1', 'regexp': H1_REGEXP},
    {'elmType': 'h2', 'regexp': r'^## (.+)$'},
    {'elmType': 'h3', 'regexp': r'^### (.+)$'},
    {'elmType': 'h4', 'regexp': r'^#### (.+)$'},
    {'elmType': 'strong', 'regexp': r'\*\*(.*?)\*\*'},
    {'elmType': 'italic', 'regexp': r'__(.+)__'},
    {'elmType': 'si', 'regexp': r'~~(.+)~~'},
    {'elmType': 'img', 'regexp': r'\!\[(.*)\]\((.+)\)'},
    {'elmType': 'link', 'regexp': r'\[(.*)\]\((.*)\)'},
    {'elmType': 'code', 'regexp': r'```(.+)'},
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
                # print("outerElement: ", type(outerElement["elmType"]))
                print("outerElement: ", parent.elmType)
                if outerElement["elmType"] != 'h1' and \
                    outerElement["elmType"] != 'h2' and \
                    outerElement["elmType"] != 'h3' and \
                    outerElement["elmType"] != 'h4' and \
                    parent.elmType != 'h1' and \
                    parent.elmType != 'h2' and \
                    parent.elmType != 'h3' and \
                    parent.elmType != 'h4' and \
                    parent.elmType != 'ul' and \
                    parent.elmType != 'li' and \
                    parent.elmType != 'ol' and \
                    parent.elmType != 'code' and \
                    parent.elmType != 'link':
                    id += 1
                    pToken = Token()
                    pToken.create_token(id=id, elmType='paragraph', content='', parent=parent)
                    parent = pToken
                    elements.append(parent)

                if (outerElement["index"] > 0):
                    # aaa**bb**cc -> TEXT_TOKEN + **bb**cc　にする
                    text = processingText[:outerElement["index"]]
                    id += 1
                    textElm = genTextElement(id, text, parent)
                    elements.append(textElm)
                    processingText = processingText.replace(text, '', 1)
                attributes = []
                if parent.elmType == 'code':
                    id += 1
                    codeContent = genTextElement(id, outerElement["matchArray"][1], parent)
                    elements.append(codeContent)
                    processingText = processingText.replace(outerElement["matchArray"][0], '')
                else:
                    if outerElement["elmType"] == 'img':
                        attributes.append({'attrName': 'src', 'attrValue': outerElement["matchArray"][2]})
                    elif outerElement["elmType"] == 'link':
                        attributes.append({'attrName': 'href', 'attrValue': outerElement["matchArray"][2]})
                    id += 1
                    elmType = outerElement["elmType"]
                    content = outerElement["matchArray"][1]
                    elm = Token()
                    if len(attributes) == 0:
                        attributes.append('')
                    elm.create_token(id=id, elmType=elmType, content='', parent=parent, attributes=attributes)
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

def tokenizeBlockquote(blockquote):
    id = 1
    parent = Token()
    parent.create_token(id=id, elmType='blockquote', content='', parent=rootToken)
    tokens = [parent]
    parents = [{'level': 1, 'token': parent}]
    prevNestLevel = 0
    sep = re.split(r'\n', blockquote)
    for quote in sep:
        match = re.match(BLOCKQUOTE_REGEXP, quote)
        if match:
            # -2するのは、> nだと[>, n]になるのでnの分で1
            # >がネストレベル1と対応させるため
            nestLevel = len(re.split('>', match[1])) - 2
            if prevNestLevel < nestLevel:
                # >
                # >>>
                # この時に上のblockquoteに加えて2回分ネストする
                for _ in range(nestLevel - prevNestLevel):
                    id += 1
                    newBlockquote = Token()
                    newBlockquote.create_token(id=id, elmType='blockquote', content='', parent=parent)
                    parents.append({'level': nestLevel, 'token': newBlockquote})
                    textTokens = tokenizeText(match[2], id, newBlockquote)
                    id += len(textTokens)
                    tokens.append(newBlockquote)
                    tokens.extend(textTokens)
                    parent = newBlockquote
                prevNestLevel = nestLevel
            else:
                # ネストレベルが同じなら、同じparentにつければ良い
                textTokens = tokenizeText(match[2], id, parent)
                id += len(textTokens)
                tokens.extend(textTokens)
        else:
            textTokens = tokenizeText(quote, id, parent)
            id += len(textTokens)
            tokens.extend(textTokens)
    return tokens

def tokenizeTable(tableString):
    id = 0
    tableToken = Token()
    tableToken.create_token(id=id, elmType='table', content='', parent=rootToken)
    tokens = [tableToken]
    print("=======================")
    print(tableString)
    # tableLines = re.split('\n', tableString)
    tableLines = [t for t in re.split('\n', tableString) if not t == '']
    print('tableLines: ', tableLines)
    attributes = []
    if len(tableLines) >= 2:
        text = re.split('\|', tableLines[1])
        for tableAlign in text:
            if re.match('^:([-]+)$', tableAlign):
                attributes.append({'attrName': 'align', 'attrValue': 'left'})
            elif re.match('^([-]+):$', tableAlign):
                attributes.append({'attrName': 'align', 'attrValue': 'right'})
            elif re.match('^:([-]+):$', tableAlign):
                attributes.append({'attrName': 'align', 'attrValue': 'center'})
    print("=======================")
    print(attributes)
    for i, t in enumerate(tableLines):
        if i == 0:
            # Table Head
            id += 1
            theadToken = Token()
            theadToken.create_token(id=id, elmType='thead', content='', parent=tableToken)
            tokens.append(theadToken)
            id += 1
            tableRow = Token()
            tableRow.create_token(id=id, elmType='tr', content='', parent=theadToken)
            tokens.append(tableRow)
            t_split = [t for t in re.split('\|', t) if not t == '']
            print(t_split)
            for j, headItem in enumerate(t_split):
                print(headItem)
                print(j)
                alignAttributes = [attributes[j]] if len(attributes) > 0 else []
                id += 1
                tableHead = Token()
                tableHead.create_token(id=id, elmType='th', content='', parent=tableRow, attributes=alignAttributes)
                textTokens = tokenizeText(headItem, id, tableHead)
                id += len(textTokens)
                tokens.append(tableHead)
                tokens.extend(textTokens)
        elif i > 1:
            # Skip Alignment
            # Table Body
            id += 1
            tbodyToken = Token()
            tbodyToken.create_token(id=id, elmType='tbody', content='', parent=tableToken)
            tokens.append(tbodyToken)
            tableRow = Token()
            tableRow.create_token(id=id, elmType='tr', content='', parent=tbodyToken)
            tokens.append(tableRow)
            t_split = [t for t in re.split('\|', t) if not t == '']
            for j, bodyItem in enumerate(t_split):
                print(j)
                id += 1
                tableData = Token()
                tableData.create_token(id=id, elmType='td', content='', parent=tbodyToken, attributes=[attributes[j]])
                textTokens = tokenizeText(bodyItem, id, tableData)
                id += len(textTokens)
                tokens.append(tableData)
                tokens.extend(textTokens)
    return tokens

def parse(markdownRow):
    # print('markdown')
    # if matchWithListRegxp(markdownRow):
    #     return tokenizeList(markdownRow)
    # return tokenizeText(markdownRow)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(markdownRow["content"])
    print(markdownRow["mdType"])
    if markdownRow["mdType"] == 'list':
        return tokenizeList(markdownRow["content"])
    elif markdownRow["mdType"] == 'blockquote':
        return tokenizeBlockquote(markdownRow["content"])
    elif markdownRow["mdType"] == 'table':
        return tokenizeTable(markdownRow["content"])
    return tokenizeText(markdownRow["content"])