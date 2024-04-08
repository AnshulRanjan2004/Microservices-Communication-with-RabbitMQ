FROM python:3.9
ENV PYTHONBUFFERED 1
WORKDIR /producerdock
COPY ./requirements.txt /producerdock/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /producerdock/requirements.txt

COPY ./producer.py /producerdock/

CMD ["uvicorn", "producer:app", "--host", "0.0.0.0", "--port", "8000"]
