class Token():
    def __init__(self):
        self.id = None # その行を表すトークン列の中でユニークとなるid
        self.parent = None # 親トークン
        self.elmType = None # 湯その種別('bold''italic'など)
        self.content = None # トークンの中身

    def create_token(self, parent, id, elmType, content):
        self.id = id # その行を表すトークン列の中でユニークとなるid
        self.parent = parent # 親トークン
        self.elmType = elmType # 湯その種別('bold''italic'など)
        self.content = content # トークンの中身