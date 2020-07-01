from Crypto.Hash import SHA256
import hashlib

obj = SHA256.new(hashlib.sha256('anshu'.encode()).hexdigest().encode())

print(obj.hexdigest())

obj.update('anshu'.encode())
print(obj.hexdigest())

obj.update('garima'.encode())
print(obj.hexdigest())