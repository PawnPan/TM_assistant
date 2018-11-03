FROM python:3.6-slim

ADD ./requirements.txt /tmp/requirements.txt
RUN set -xe && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone && \
    pip install --no-cache-dir -r /tmp/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

ADD app /code/app
ADD wsgi.py /code/wsgi.py
WORKDIR /code
EXPOSE 8848

CMD gunicorn wsgi:application -b :8848 -k gevent
