FROM python:3

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir ./testresults

RUN pytest > ./testresults/results.log

RUN cat ./testresults/results.log

EXPOSE 8000

CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "webserver:app"]
