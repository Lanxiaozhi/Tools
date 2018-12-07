FROM floydhub/pytorch:0.3.1-gpu.cuda9cudnn7-py3.37 
MAINTAINER xlearn 
ADD ./Xlearn-Service /app 
WORKDIR /app 
RUN pip install -r requirements.txt 
CMD ["python3", "main.py"]