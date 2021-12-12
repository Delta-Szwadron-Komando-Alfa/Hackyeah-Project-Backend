FROM openjdk:slim
COPY --from=python:3.9.9 / /

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

RUN adduser --disabled-password myuser
USER myuser

RUN python3 -m pip install --upgrade pip
COPY --chown=myuser:myuser requirements.txt ./
RUN pip install -r requirements.txt
COPY --chown=myuser:myuser . .

WORKDIR /usr/src/app/api

EXPOSE 8000
CMD ['python3', 'main.py']
