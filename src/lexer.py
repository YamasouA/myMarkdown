from models.myToken import Token
import re

TEXT = 'text'
STRONG = 'strong'

# .*?でなるべく少ない文字をマッチさせる
STRONG_ELM_REGXP = '\*\*(.*?)\*\*'

def genTextElement(id, text, parent):
    tk = Token()
    tk.id = id
    tk.elmType = TEXT
    tk.content = text
    tk.parent = parent
    return tk

def genStrongElement(id, text, parent):
    tk = Token()
    tk.id = id
    tk.elmType = STRONG
    tk.content = '',
    tk.parent = parent
    return tk

def matchWithStrongRegxp(text):
    result = re.search(STRONG_ELM_REGXP, text)
    index = text.find("**")
    return result, index

if __name__ == "__main__":
    print(matchWithStrongRegxp("**bo**bold**ld**|**bold**"))