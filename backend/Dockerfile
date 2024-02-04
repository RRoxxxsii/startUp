FROM python:3.11.7-alpine as build_app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && pip install poetry
RUN poetry config virtualenvs.create false

WORKDIR proj/backend/

COPY . /proj/backend/


FROM build_app as prod

ENV PROD 1

RUN poetry install --without dev

CMD ["python", "-m", "src.presentation.api.main"]


FROM build_app as dev

ENV DEV 1

RUN poetry install --with dev

CMD ["python", "-m", "src.presentation.api.main"]
