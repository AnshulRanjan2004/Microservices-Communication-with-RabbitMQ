FROM python:3.9
ENV PYTHONBUFFERED 1
WORKDIR /producer
COPY ./requirements.txt /producer/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /producer/requirements.txt

COPY . /producer/

CMD python producer.py
