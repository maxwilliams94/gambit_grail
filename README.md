# Building
## pip
```bash
pip install /path/to/dir/containing/pyproject.toml
```

## Docker
### Locally
```bash
docker build -t gambit:0.1 -f Dockerfile.develop
```
### From git
```bash
docker build https://github.com/maxwilliams94/gambit_grail.git
```
# Running
## From Source
```bash
cd src/gambit/gambit
uvicorn main:app
```
## Using Docker
```bash
# Get debug logging and also have logs written to /tmp/gambit.log
LOG_LEVEL=DEBUG docker run -p 127.0.0.1:80:80 -v /tmp:/tmp gambit_grail:0.1
```


# Logging
- "gambit" - NullHandler() by default. Add handler of your choice
