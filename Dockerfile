FROM python:3.9.1-alpine

WORKDIR /git_repository_analyzer

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY git_repository_analyzer/ .

CMD [ "python3", "./analyzer/github_data_extracter.py" ]