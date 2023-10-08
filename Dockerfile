FROM python:3.10

COPY requirements.txt .

RUN pip install -r requirements.txt

ARG GOOGLE_API_KEY
ARG BOT_TOKEN
ENV BOT_TOKEN=$BOT_TOKEN
ENV GOOGLE_API_KEY=$GOOGLE_API_KEY

COPY . .

EXPOSE 80

CMD ["python3", "main.py"]
