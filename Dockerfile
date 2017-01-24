FROM python:3.5.2

WORKDIR /opt/winzig

ADD ./requirements.txt /opt/winzig/requirements.txt

RUN pip install -U pip

RUN pip install -r /opt/winzig/requirements.txt
