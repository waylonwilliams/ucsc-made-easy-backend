# usually would be an OS, in this case im just downloading a python image
FROM python:3.8-slim

# set the directory of your project and cd into it, creating a file system for the container
WORKDIR /app

# copy the contents of the current directory to this directory in the container
COPY . /app

# run command line
RUN pip install --no-cache-dir -r requirements.txt
CMD ["gunicorn"  , "-b", "0.0.0.0:8080", "app:app"]