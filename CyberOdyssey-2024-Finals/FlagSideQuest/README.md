# [**FlagSideQuest**](#)

## Description:
* 

## Difficulty:
* Hard

## Objective:
The objective of this challenge is to utilize the `CVE-2017-11424` vulnerability to obtain the server's public key and forge a JWT token to exploit the `Algorithm Confusion Attack` to retrieve the flag.

## Deployment:
```sh
docker build -t flag-side-quest .
docker run -e DISCORD_TOKEN=your_token_here flag-side-quest
```

## Solution:
See [solution](solution/).
