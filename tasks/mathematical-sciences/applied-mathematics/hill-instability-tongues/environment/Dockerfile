FROM python:3.11-slim

RUN pip install --no-cache-dir numpy==1.26.4 scipy==1.13.0

RUN mkdir -p /root/data /root/result /root/solver
RUN chmod 777 /root/result

COPY data/public_case.json /root/data/input.json

WORKDIR /root
