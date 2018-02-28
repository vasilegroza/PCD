FROM python:3.5

WORKDIR /usr/src/app


COPY ./server.py .
EXPOSE 8080
CMD ["/bin/sh", "-c", "python ./server.py -c=${CONN_TYPE} > ./server.log"]
