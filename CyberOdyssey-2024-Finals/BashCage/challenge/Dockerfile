FROM alpine:3.19

RUN apk add --no-cache socat bash && \
    adduser -D -s /bin/bash ctf

WORKDIR /home/ctf

COPY chall.sh flag.txt /home/ctf/

RUN chmod +x chall.sh && \
    chown root:root chall.sh && \
    chmod 555 chall.sh && \
    chown root:root flag.txt && \
    chmod 444 flag.txt

USER ctf

EXPOSE 4040

CMD socat \
    -T120 TCP-L:4040,fork,reuseaddr \
    EXEC:"/home/ctf/chall.sh",pty,stderr,setsid,sane,raw,sigint,echo=0
