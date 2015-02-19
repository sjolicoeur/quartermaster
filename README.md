# Description

Docker app that polls docker to get a listing of  available containers that have an exposed port and then writes the information into an ETCD datastore.

it will annotate the key with the type of service it guesses from the docker container's name. For example a web facing container should have a name like so:  `<service>.<app name>` == `www.hello_world`

# BUILDING it: 

`docker build -t  quartermaster .` (`docker build -t sjolicoeur/quartermaster:lastest .`)

# Notes

## Service protocol dicovery is done by 

## Running it:


```docker run -e DOCKER_HOST=`echo $DOCKER_HOST` -e DOCKER_TLS_VERIFY=1 -e DOCKER_CERT_PATH=/docker_cert  -v `echo $DOCKER_CERT_PATH`:/docker_cert --add-host dockerhost:<docker host ip>  --name -t -i quartermaster:latest ```
