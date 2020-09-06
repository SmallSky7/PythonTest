import hashlib
import hmac

oldStr = input("请输入要加密的字符串：")

md5 = hashlib.md5()
md5.update(oldStr.encode('utf-8'))
print("MD5加密：", md5.hexdigest())

sha1 = hashlib.sha1()
sha1.update(oldStr.encode('utf-8'))
print("SHA1加密：", sha1.hexdigest())

sha256 = hashlib.sha256()
sha256.update(oldStr.encode('utf-8'))
print("SHA256加密：", sha256.hexdigest())

pwd = oldStr.encode('utf-8')
key = 'id'.encode('utf-8')
h = hmac.new(key, pwd, digestmod='MD5')
print("更安全的MD5加密：", h.hexdigest())