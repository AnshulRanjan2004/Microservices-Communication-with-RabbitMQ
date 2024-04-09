FROM python:3.9
ENV PYTHONBUFFERED 1
WORKDIR /producerdock
COPY ./requirements.txt /producerdock/requirements.txt
RUN pip install -r /producerdock/requirements.txt

COPY ./producer.py /producerdock/

CMD ["python","producer.py"]
