FROM python:3.11.7-alpine

ENV PYTHONDONTWRITEBYTECODE 1  # Do not write cache to pyc
ENV PYTHONUNBUFFERED 1 # Do not bufferize stdout and stdin

RUN pip install --upgrade pip && pip install poetry
RUN poetry config virtualenvs.create false

WORKDIR proj/backend/

COPY . /proj/backend/

RUN poetry install

CMD ["python", "-m", "src.presentation.api.main"]
