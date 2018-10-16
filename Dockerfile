# Set initial image to ubuntu
FROM tensorflow/tensorflow:latest-py3
# Author
LABEL maintainer="Smuggler - EGH455-Group3"
RUN adduser --quiet --disabled-password qtuser
# Updating
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    binutils \
    build-essential \
    curl \
    dialog \
    git \
    mc \
    mesa-utils \    
    tar \    
    libpulse-dev \
    mesa-utils \
    libgl1-mesa-glx \
    gstreamer1.0-libav \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-base-apps \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-ugly \
    alsa-base \
    alsa-utils \
    vim \
    wget \
    ffmpeg libav-tools x264 x265

RUN pip install --upgrade pip
RUN pip install --upgrade pyqt5==5.8
RUN pip install --upgrade opencv-python
RUN pip install --upgrade moviepy
RUN pip install --upgrade requests
RUN apt-get install -y libqt5gstreamer-dev libqt5multimedia5-plugins

# copy the app
ADD /Video_Processing /app

# Set Up Nvidia drivers
ADD NVIDIA-DRIVER.run /tmp/NVIDIA-DRIVER.run
# ADD ffmpeg-linux64-v3.3.1 /home/qtuser/.imageio/ffmpeg/ffmpeg-linux64-v3.3.1
# RUN chmod 777 /home/qtuser/.imageio/ffmpeg/ffmpeg-linux64-v3.3.1
RUN sh /tmp/NVIDIA-DRIVER.run -a -N --ui=none --no-kernel-module
RUN rm /tmp/NVIDIA-DRIVER.run

# Default directory
WORKDIR /app