FROM python:3.6 
COPY example example 
WORKDIR example 
RUN pip install -r ./requirements.txt 
CMD ['python', 'api.py', '--port', '8080']~