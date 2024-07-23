FROM python:3.11.5

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./.env /code/.env

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--port", "8080", "--host", "0.0.0.0"]