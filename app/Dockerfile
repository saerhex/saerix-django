FROM python:3.9-buster
WORKDIR /code
COPY requirements.txt /code
RUN pip install -r requirements.txt --no-cache-dir
ENTRYPOINT ["python3"]
CMD ["./manage.py", "runserver", "0.0.0.0:8000"]