FROM python:3.12

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

EXPOSE 34000

# CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "34000", "--reload"]
CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 34000 --reload --proxy-headers"]

# CMD ["uvicorn", "code/src/main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--proxy-headers"]