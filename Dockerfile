FROM python:3

RUN pip install pipenv

WORKDIR /tmp
COPY Pipfile* ./
RUN pipenv lock --requirements > ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

WORKDIR /usr/src/app
COPY . .

# unfortunately 
RUN sed -i "s/'server\.socket_host': '127\.0\.0\.1'/'server.socket_host': '0.0.0.0'/" server.py

RUN chown -R nobody:nogroup .

USER nobody

EXPOSE 8080
CMD [ "python", "./server.py" ]