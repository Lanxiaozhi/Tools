FROM python:3.6 
MAINTAINER xlearn 
ENV SERVER_WORK 4 
ENV EXIT_TIME -1 
RUN git clone https://github.com/Lanxiaozhi/Example-api-server.git 
WORKDIR Example-api-server 
RUN pip install -r ./requirements.txt 
CMD ['python', 'api.py', '--port', '8080']~