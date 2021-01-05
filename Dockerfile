FROM python:3.9.1-alpine

WORKDIR /git_repository_analyzer

COPY requirements.txt .

RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip3 install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps
    
COPY git_repository_analyzer/ .

CMD [ "python3", "./main.py" ]