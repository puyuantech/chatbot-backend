FROM python:3.7.5

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt -i https://pypi.douban.com/simple

CMD ["gunicorn", "-w", "1", "-k", "gevent", "-b", "0.0.0.0:8003", "manager:app"]
