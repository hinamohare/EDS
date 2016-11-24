Flask-MySQL
� Create a repository with the following structure:
     AssignmentExpenseManagement
	-\app
	    -\app.py
	-\docker-compose.yml
	-\Dockerfile
	-\requirements.txt
� To build the image and start the service run the following commands in docker quickstart terminal
	$ docker-compose build
	$ docker-compose up -d
� The application starts at the ip address of the docker machine which is obtained by
	$ docker-machine ip
	192.168.99.100
	Hence, the flask application runs at address 192.168.99.100:5000
� The docker images can be seen by
	$ docker images
� The docker running containers can be seen by
	$ docker ps
� All the running and stopped containers can be seen by
	$ docker ps -a
� The docker images are tagged by
	$ docker tag dockerhub_username/image_id: tagname
  or  docker tag imageId dockerhub_username/imageName:tag
� The docker image is pushed to the docker hub by
	$ docker login
� Provide the credential to log in to the system
	$ docker push tagged_image_name
  or docker push dockerhub_username/imageName
