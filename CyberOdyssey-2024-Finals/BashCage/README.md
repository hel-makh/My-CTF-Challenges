# [**BashCage**](#)

## Description:
* 

## Difficulty:
* Medium

## Objective:
The goal of this challenge is to escape a restricted shell environment using only a limited set of allowed characters, which are: `(){}'\"$\\<#`

## Deployment:
```sh
docker build -t bash-cage .
docker run -p 4040:4040 bash-cage
```

## Solution:
See [solution](solution/).
