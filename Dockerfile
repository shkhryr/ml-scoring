FROM python:3.9
WORKDIR /alif-test

RUN pip install --upgrade pip

COPY ./requirements.txt /alif-test/requirements.txt

RUN pip install -r /alif-test/requirements.txt

COPY ./ /alif-test

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]