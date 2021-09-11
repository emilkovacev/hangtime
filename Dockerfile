FROM python:3.9

ENV HOME /root
WORKDIR /root

COPY . .

EXPOSE 8000

CMD python3 hello_world.py

