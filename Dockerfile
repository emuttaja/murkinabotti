FROM python:3.10-alpine

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

CMD python3 ./murkina.py