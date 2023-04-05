#base image
FROM python:3-onbuild

#set dir for app
WORKDIR /usr/src/app

#copy all files to container
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install flask requests
RUN pip install flask_sqlalchemy
RUN pip install sqlalchemy_utils
RUN pip install pymysql

#port number for container
EXPOSE 5000

#run the app
CMD ["python", "./app.py"]
