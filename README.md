# Project was created based on EGH455 assignment QUT

This Assignment contain semester project assignment for QUT University EGH455-2018sem2. Submission date and presentation set on *Friday, October 19 2018*. Task was completed in gropu.

This solution performed in a docker container using tensorflow with CPU-only usage build on Python3. In addition, it includes support of NVIDEA player with jupyter notebook to run test codes.
## Variables
export PYTHONPATH=$(pwd)/detection:$(pwd)/detection/slim
or
set PYTHONPATH=$(pwd)/detection:$(pwd)/detection/slim


## Prerequisites
This project may be run independantly or using docker container. Below you will be able to crete you own container. For instructions how to train model and instalation refer to ****

### Installing on Linux 
```
sudo apt install docker.io
```
### Installing on Mac
Download from following websites and go through Getting Started.
```
https://store.docker.com/editions/community/docker-ce-desktop-mac
https://docs.docker.com/docker-for-mac/
```
## Deployment
With DocvkerFile in folder run following command to build image.
```
docker build -t egh455-detection .
```
Next, run docker in order to acess it. It will run one time container.
```
docker run -it -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v $(pwd)/Video_Processing:/app \
    -e DISPLAY=$DISPLAY \
    --env-file ./env.list \
    -u qtuser \
    --group-add audio \
    --device /dev/dri \
    --privileged \
    egh455-detection python3 application.py
```
If you require copying files to the docker container, use following command. You can use purne to delete all container which you were running.
```
Copy files:~$ docker cp Video_Processing/ egh455-detection:/app
delete containers:~$ docker container prune
```

If there are difficulties with accesing Display for player run following unseccury code. If it concerns you, run second to disable.
```
xhost +local:root # for the lazy and reckless
xhost -local:root # Disable access
```

# Explore you container if necessary and make changes.
```
docker run -it \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --privileged \
    -v $(pwd)/test:/app \
    -e DISPLAY=$DISPLAY \
    -e QT_X11_NO_MITSHM=1 \   
    -u qtuser \
    --group-add audio \
    --device /dev/snd \
    egh455-project bash
```
## Install Support of Nvidea.
Download driver matches yours
Rename it
Uncoment files in DockerFile
Build it.

## Jyputer notebook
Link appeared on console will be link to jupyter. replace link with localhost, but keep port the same.
```
docker run -it --env-file ./env.list \
    -u qtuser \
    -p 8888:8888 \
    egh455-detection jupyter notebook --ip 0.0.0.0
```

If for some reason, this not work. Use full example below:
```
docker run -it -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v $(pwd)/Video_Processing:/app \
    -e DISPLAY=$DISPLAY \
    --env-file ./env.list \
    -u qtuser \
    --group-add audio \
    --device /dev/dri \
    --privileged \
    -p 8888:8888 \
    egh455-detection jupyter notebook --ip 0.0.0.0
```

## Removing
Container after start
```
docker stop Assignment1
docker rm Assignment1
```
Image after stopping everything
```
docker rmi weekends-pl
```
## Upload your container to DockerHub:
Following command will upload image to DockerHub
```
docker tag weekends-pl smugglersmr/egh455-detection:latest
docker push smugglersmr/egh455-detection
```

## Built With

* [DockerHub](https://hub.docker.com/) - Official Docker Hub
* [GitHub](https://github.com/SmugglerSMR/CAB432-assgn1) - Storage Location for repository
* [Tensorflow:latest-py3](https://www.latex-project.org/get/) - Report written using Latex
* [NVIDIA drivers] - 
* models/research
* Faster-RCNN tutorial
* Model prepared - Inception

## Contributing

Please read [CONTRIBUTING.md](https://github.com/) too see how many my OS's girls participated in writing.

## Authors

* **Matt Sadykov** - *Developer* - [Email](marat.sadykov@connect.qut.edu.au)

## License

This project is licensed under the Eclipse License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
Link which were used to build container, fix issue and produce sollution:

https://github.com/gklingler/docker3d
https://blog.csdn.net/sunshinezhihuo/article/details/80921053
http://gernotklingler.com/blog/howto-get-hardware-accelerated-opengl-support-docker/
https://www.howtoinstall.co/en/ubuntu/xenial/libqt5gstreamer-dev
https://unix.stackexchange.com/questions/450507/pyqt5-qmediaplayer-defaultserviceproviderrequestservice-no-service-found-fo
https://github.com/jessfraz/dockerfiles/issues/253
https://github.com/fadawar/docker-pyqt5-qml-qtmultimedia
https://www.tensorflow.org/install/docker
