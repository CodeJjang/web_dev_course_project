FROM python:3.6-alpine
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD ["python3", "server.py"]