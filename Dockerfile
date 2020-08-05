FROM python:2.7

ENV app /app

RUN mkdir $app
WORKDIR $app
COPY . $app

RUN pip install -r requirements.txt

EXPOSE 80

ENTRYPOINT ["python", "./run.py"]