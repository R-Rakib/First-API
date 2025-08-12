#Base Image

FROM python:3.13.6

#Work Directory
WORKDIR /app

#Copy
COPY . /app

#run 
RUN pip install -r requirements.txt

#Port
EXPOSE 5000


#Command
CMD ["python","./app.py"]






