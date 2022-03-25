FROM ubuntu:20.04

RUN apt update -y && \
    apt install -y python3-pip && \
    apt install -y libpq-dev python3-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

ENV PORT=5143

EXPOSE 5143

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]
