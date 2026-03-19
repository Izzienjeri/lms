FROM python:3.12-slim AS builder

RUN pip install pipenv

WORKDIR /server

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

FROM python:3.12-slim

WORKDIR /server

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .  

RUN useradd -m lmsuser
USER lmsuser

CMD ["python","app.py", "--host=0.0.0.0"]
