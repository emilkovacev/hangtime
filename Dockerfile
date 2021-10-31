FROM python:3.9
WORKDIR /app
COPY . .

RUN pip install pymongo

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

CMD /wait && python server.py