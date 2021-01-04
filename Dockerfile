FROM python:3.9.1-alpine

WORKDIR /git_repository_analyzer

COPY requirements.txt .

# RUN apk update
# RUN apk add postgresql-dev gcc python3-dev musl-dev

# RUN apk update
# RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    # apk update \
    # apk add postgresql-dev gcc python3-dev musl-dev \
    # pip3 install -r requirements.txt 
    pip3 install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps
    
# RUN apk --purge del .build-deps

COPY git_repository_analyzer/ .

CMD [ "python3", "./analyzer/github_data_extracter.py" ]