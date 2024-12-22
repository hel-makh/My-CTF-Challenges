FROM python:3.11-slim

RUN apt-get update \
    && apt-get install --no-install-recommends -y socat \
    && groupadd ctf \
    && useradd -r -g ctf ctf

WORKDIR /usr/src/app

COPY chall.py flag.txt /usr/src/app/

RUN chown ctf:root chall.py && \
    chmod 500 chall.py && \
    chown root:root flag.txt && \
    chmod 444 flag.txt

USER ctf

EXPOSE 4041

CMD socat \
    -T120 TCP-L:4041,fork,reuseaddr \
    EXEC:"python3 chall.py",pty,stderr,setsid,sane,raw,sigint,echo=0
