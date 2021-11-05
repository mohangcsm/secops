FROM python:2.7

ENV app /app

RUN mkdir $app
WORKDIR $app
COPY requirements.txt $app

RUN apt-get update && apt-get install nano
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 80

ENTRYPOINT ["python", "./run.py"]