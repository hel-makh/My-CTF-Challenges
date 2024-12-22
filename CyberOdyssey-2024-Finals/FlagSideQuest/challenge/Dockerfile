FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py /app/

ENV FLAG="ODYSSEY{C0nfus1ng_S1d3_Qu357}"

# ENV DISCORD_TOKEN="MTMxNjAwODY3Mjc2NTI4MDI3OA.hhhhhh.hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"

CMD ["python", "bot.py"]
