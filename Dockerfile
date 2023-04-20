FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
#COPY ./html-template /code/html-template
COPY ./app /code/app
COPY ./sql_app /code/sql_app
COPY ./endpoint.py /code/endpoint.py


CMD ["uvicorn", "endpoint:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
