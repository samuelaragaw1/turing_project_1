FROM python:3.11-slim

RUN pip install --no-cache-dir pytest==8.4.1 pytest-json-report==1.5.0 numpy==1.26.4 scipy==1.13.0

COPY . /tests
WORKDIR /tests

CMD ["/tests/test.sh"]
