from models.myToken import Token
import re

TEXT = 'text'
STRONG = 'strong'

# .*?でなるべく少ない文字をマッチさせる
STRONG_ELM_REGXP = r'\*\*(.*?)\*\*'
LIST_REGXP = r'^( *)([-|\*|\+] (.+))$'
OL_REGEXP = r'^( *)((\d+)\. (.+))$'
BLOCKQUOTE_REGEXP = r'([>| ]+)(.+)'
PRE_REGEXP = r'^```'
TABLE_HEAD_BODY_REGEXP = r'\|(.+)\|'
TABLE_ALIGN_REGEXP = r'\|([- | :]+\|'

def analize(markdown):
    NEUTRAL_STATE = 'neutral_state'
    LIST_STATE = 'list_state'
    BLOCKQUOTE_STATE = 'blockquote_state'
    PRE_STATE = 'pre_state'
    TABLE_HEAD_STATE = 'table_head_state'
    TABLE_ALIGN_STATE = 'table_align_state'
    TABLE_BODY_STATE = 'table_body_state'
    state = NEUTRAL_STATE

    lists = ''
    blockquote = ''
    pre = ''
    table = ''

    rawMdArray = re.split(r'\r\n|\r|\n', markdown)
    print(rawMdArray)
    mdArray = []
    for index, md in enumerate(rawMdArray):
        listMatch = re.search(LIST_REGXP + '|' + OL_REGEXP, md)
        # neutral_stateで今見ている行がListの場合
        if state == NEUTRAL_STATE and listMatch:
            state = LIST_STATE
            lists += md + '\n'
        elif state == LIST_STATE and listMatch:
            lists += md + '\n'
        # list_stateで見ている行がlistではない
        elif state == LIST_STATE and listMatch == None:
            state = NEUTRAL_STATE
            mdArray.append({'mdType': 'list', 'content': lists})
            lists = ''
        # neutral_stateのとき
        if len(lists) > 0 and (state == NEUTRAL_STATE or index == len(rawMdArray) - 1):
            mdArray.append({'mdType': 'list', 'content': lists})

        preMatch = re.match(PRE_REGEXP, md)
        if state == NEUTRAL_STATE and preMatch:
            pre += md
            state = PRE_STATE
        elif state == PRE_STATE and preMatch:
            state = NEUTRAL_STATE
            mdArray.append({'mdType': 'pre', 'content': pre})
            pre = ''
        elif state ==PRE_STATE and preMatch == None:
            pre += md + '\n'
        if len(pre) > 0 and (state == NEUTRAL_STATE or index == len(rawMdArray) - 1):
            pre += '```'
            mdArray.append({'mdType': 'pre', 'content': pre})
            pre = ''

        tableHeadBodyMatch = re.search(TABLE_HEAD_BODY_REGEXP, md)
        tableAlignMatch = re.search(TABLE_ALIGN_REGEXP, md)
        if state == NEUTRAL_STATE and tableHeadBodyMatch:
            state = TABLE_HEAD_STATE
            table += md + '\n'
        elif state == TABLE_HEAD_STATE and tableAlignMatch:
            state = TABLE_ALIGN_STATE
            table += md + '\n'
        elif state == TABLE_HEAD_STATE and tableAlignMatch == None:
            state = NEUTRAL_STATE
        elif state == TABLE_ALIGN_STATE and tableHeadBodyMatch:
            state = TABLE_BODY_STATE
            table += md + '\n'
        elif state == TABLE_BODY_STATE and tableHeadBodyMatch == None:
            state = NEUTRAL_STATE
        if len(table) > 0 and (state == NEUTRAL_STATE or index == len(rawMdArray) - 1):
            mdArray.append({'mdType': 'table', 'content': table})
            table = ''

        blockquoteMatch = re.match(BLOCKQUOTE_REGEXP, md)
        if state == NEUTRAL_STATE and blockquoteMatch:
            state = BLOCKQUOTE_STATE
            blockquote += md  + '\n'
        elif state == BLOCKQUOTE_STATE and blockquoteMatch:
            blockquote += md + '\n'
        elif state == BLOCKQUOTE_STATE and blockquoteMatch == None:
            state = NEUTRAL_STATE
        if len(blockquote) > 0 and (state ==NEUTRAL_STATE or index == len(rawMdArray) - 1):
            # minuteでは'conte': blockquote.replace('\n$', '')になる
            mdArray.append({'mdType': 'blockquote', 'content': blockquote})
            blockquote = ''

        if len(lists) == 0 and \
            state != LIST_STATE and \
            len(md) != 0 and \
            len(blockquote) == 0 and \
            state != BLOCKQUOTE_STATE and \
            len(pre) == 0 and \
            state != PRE_STATE:
            mdArray.append({'mdType': 'text', 'content': md})
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