class Token():
    def __init__(self):
        self.id = None # その行を表すトークン列の中でユニークとなるid
        self.parent = None # 親トークン
        self.elmType = None # 湯その種別('bold''italic'など)
        self.content = None # トークンの中身

    def create_token(self, token, number, s1, s2):
        self.id = number # その行を表すトークン列の中でユニークとなるid
        self.parent = token # 親トークン
        self.elmType = s1 # 湯その種別('bold''italic'など)
        self.content = s2 # トークンの中身