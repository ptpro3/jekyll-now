FROM ubuntu:latest

RUN apt-get -y update
RUN apt-get install -y python-pip python-dev build-essential

COPY . /hw
ENV HOME=/hw
WORKDIR /hw

RUN pip install flask
ENTRYPOINT ["python"]
CMD ["hello.py"]