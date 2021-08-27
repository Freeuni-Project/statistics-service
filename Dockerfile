# Dockerfile
FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /statapp
COPY requirements.txt /statapp/requirements.txt
RUN pip install -r requirements.txt
COPY . /statapp/
ENTRYPOINT ["python"]
CMD ["run.py"]