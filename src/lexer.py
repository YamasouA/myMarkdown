from models.myToken import Token
import re

TEXT = 'text'
STRONG = 'strong'

# .*?でなるべく少ない文字をマッチさせる
STRONG_ELM_REGXP = r'\*\*(.*?)\*\*'
LIST_REGXP = r'^( *)([-|\*|\+] (.+))$'

def analize(markdown):
    NEUTRAL_STATE = 'neutral_state'
    LIST_STATE = 'list_state'
    state = NEUTRAL_STATE

    lists = ''

    rawMdArray = re.split(r'\r\n|\r|\n', markdown)
    print(rawMdArray)
    mdArray = []
    for index, md in enumerate(rawMdArray):
        listMatch = re.search(LIST_REGXP, md)
        # neutral_stateで今見ている行がListの場合
        if state == NEUTRAL_STATE and listMatch:
            state = LIST_STATE
            lists += md + '\n'
            if index == len(rawMdArray) - 1:
                mdArray.append(lists)
            print('lists')
            print(lists)
        elif state == LIST_STATE and listMatch:
            # 最後の行の時
            if index == len(rawMdArray) - 1:
                lists += md
                mdArray.append(lists)
            # 2つ目以降のlistの場合
            else:
                lists += md + '\n'
        # list_stateで見ている行がlistではない
        elif state == LIST_STATE and listMatch == None:
            state = NEUTRAL_STATE
            mdArray.append(lists)
            lists = ''
        # neutral_stateのとき
        if len(lists) == 0:
            mdArray.append(md)
    print(mdArray)
    return mdArray
    

def genTextElement(id, text, parent):
    tk = Token()
    tk.id = id
    tk.elmType = TEXT
    tk.content = text
    tk.parent = parent
    return tk

def genStrongElement(id, parent, text=""):
    tk = Token()
    tk.id = id
    tk.elmType = STRONG
    tk.content = text
    tk.parent = parent
    return tk

def matchWithStrongRegxp(text):
    result = re.search(STRONG_ELM_REGXP, text)
    index = text.find("**")
    return result, index

def matchWithListRegxp(text):
    result = re.search(LIST_REGXP, text, flags=re.M)
    return result

if __name__ == "__main__":
    print(matchWithStrongRegxp("**bo**bold**ld**|**bold**"))