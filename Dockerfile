FROM ubuntu:latest
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN apt update && apt -y install libmysqlclient-dev
RUN apt -y install python3-pip
RUN pip3 install -r requirements.txt
COPY . /app
ENTRYPOINT [ "python3" ]
CMD ["app.py"]
EXPOSE 8080