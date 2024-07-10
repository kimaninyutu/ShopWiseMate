import hashlib
password = 'pa$$w0rd'
h = hashlib.md5(password.encode())
print(h.hexdigest())
y = hashlib.md5(h.digest())
print(y.hexdigest())
