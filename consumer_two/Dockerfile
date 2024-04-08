FROM python:3.9
ENV PYTHONBUFFERED 1
WORKDIR /createItem
COPY ./requirements.txt /createItem/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /createItem/requirements.txt

COPY ./create_item.py /createItem/

CMD python create_item.py