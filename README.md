# Web Development Course Project
This repo contains all the code, artifacts and instructions required to run our project.

## Prerequisites for local environment
In order to build, test and run the code locally, Python 3.<fill here> needs to be installed.

### Build
```
pip3 install -r requirements.txt
```

### Test
```
python3 test_calculate_next_state.py
```

### Run
```
<insert commands here>
```

## Prerequisites for Docker Containers environment
First, both Docker Engine runtime and Docker Compose need to be installed (on a linux machine, as the images are linux based).

### Build
```
docker build -t currency-calculator:v1.0 .
```

### Run
```
docker run -d -p 5000:5000 currency-calculator:v1.0
```

### Docker Compose
```
docker-compose up
```
Then, you may surf to `http://localhost/`.

