Docker Build
    
    docker build --no-cache -f docker/images/os/Dockerfile -t protyom/course_app:os .
    docker build -f docker/images/os/Dockerfile -t protyom/course_app:os .
    docker push protyom/course_app:os
    docker pull protyom/course_app:os
    
    
    docker build --no-cache -f docker/images/pip/Dockerfile -t protyom/course_app:pip .
    docker build -f docker/images/pip/Dockerfile -t protyom/course_app:pip .
    docker push protyom/course_app:pip

    docker build -f docker/images/pip_dev/Dockerfile -t protyom/course_app:pip .

    docker build --no-cache -f docker/images/app/Dockerfile -t protyom/course_app:app .
    docker build -f docker/images/app/Dockerfile -t protyom/course_app:app .
    docker push protyom/course_app:app

Docker on server side
    
    docker pull sportylife/sportylife:dev_658

    docker-compose up -d
    docker-compose up -d --no-deps web
    docker-compose up -d --force-recreate
    
    docker-compose down
    
    docker logs docker_app-uwsgi-server_1
    
- Execute in docker

        docker exec -it docker_app-uwsgi-server_1 python /bin/sh

Remove on Linux

- Containers

        docker rm $(docker ps -a -q)

- Images
        
        docker rmi $(docker images -q)
