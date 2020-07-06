# -*- coding:utf-8 -*-

import bcrypt

class PasswordApi:
    def __init__(self):
        self.key = bcrypt.gensalt()

    def hashed(self,pwd):
        if not isinstance(pwd,bytes):
            if not isinstance(pwd,str):
                pwd = str(pwd).encode("utf8")
            else:
                pwd = pwd.encode("utf8")
        return bcrypt.hashpw(pwd, self.key).decode('utf8')

    def checkpw(self,pwd,hash):
        if not isinstance(pwd,bytes):
            if not isinstance(pwd,str):
                pwd = str(pwd).encode("utf8")
            else:
                pwd = pwd.encode("utf8")
        if not isinstance(hash,bytes):
            if not isinstance(hash,str):
                hash = str(hash).encode("utf8")
            else:
                hash = hash.encode("utf8")

        return bcrypt.checkpw(pwd,hash)


if __name__=="__main__":
    pd = PasswordApi()
    import hashlib
    hexpwd = hashlib.sha256("111111".encode('utf8')).hexdigest()
    print(hexpwd)
    print(pd.hashed(hexpwd))