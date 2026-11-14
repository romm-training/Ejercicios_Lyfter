import hashlib

password = "mypassword123"
hashed_password = hashlib.md5(password.encode()).hexdigest()

print(hashed_password)