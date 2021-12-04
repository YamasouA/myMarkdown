from re import I
from models.myToken import Token

from lexer import genStrongElement, genTextElement, matchWithStrongRegxp

rootToken = Token()
rootToken.id = 0
rootToken.elmType = 'root'
rootToken.content = ''
rootToken.parent = None


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
            print("in while")
            print(processingText)
            matchArray, index = matchWithStrongRegxp(processingText)
            # matchArray[0] -> **bold**
            # matchArray[1] -> bold
            
            # ****にマッチしないとき、テキストトークンを作成する
            if matchArray is  None:
                print("case not match")
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

                print("case match")
                id += 1
                elm = genStrongElement(id, parent)
                print(elm.content)
                parent = elm
                elements.append(elm)

                processingText = processingText.replace(matchArray[0], '')

                tokenize(matchArray[1], parent)
                parent = p

                
        

    tokenize(textElement, parent)
    return elements

def parse(markdownRow):
    return tokenizeText(markdownRow)