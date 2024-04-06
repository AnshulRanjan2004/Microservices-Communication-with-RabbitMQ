FROM python:3.11
ENV PYTHONUNBUFFERED=1
WORKDIR /stockmanager
COPY requirements.txt /stockmanager/requirements.txt
RUN pip install -r requirements.txt
COPY . /stockmanager

CMD 'uvicorn stock_managment:app --host 0.0.0.0 --port 8000'