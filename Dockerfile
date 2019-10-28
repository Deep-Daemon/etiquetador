#FROM python:3-onbuild
FROM python:3.7.3-slim-stretch
MAINTAINER Rodrigo Burciaga
## if not ssl certificates
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org  -r requirements.txt
EXPOSE 5000
CMD ["python","./app.py"]
