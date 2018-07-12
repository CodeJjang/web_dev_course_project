# Web Development Course Project
This repo contains all the code, artifacts and instructions required to run our project.

## Prerequisites for local environment
In order to build, test and run the code locally, Python 3.6 needs to be installed.

### Build
```
pip3 install -r requirements.txt
```

### Unit Tests
```
python3 test_calculate_next_state.py
```

### Integration Tests
```
python3 test_server.py
```

### Run
```
python3 server.py
```
Server will then listen on localhost:5000.

## Prerequisites for Docker Containers environment
First, both Docker Engine runtime and Docker Compose need to be installed (on a linux machine, as the images are linux based).

### Build
```
sudo docker build -t currency-calculator:v1.0 .
```

### Run
```
sudo docker run -d -p 5000:5000 currency-calculator:v1.0
```

### Docker Compose
```
sudo docker-compose build
sudo docker-compose up
```
Then, you may surf to `http://localhost/`.

