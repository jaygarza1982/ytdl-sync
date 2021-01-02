FROM ubuntu:20.04

WORKDIR /ytdl-sync
EXPOSE 80
EXPOSE 5000

# Copy main to here
COPY ./main .

# Do not prompt when installing or upgrading
ARG DEBIAN_FRONTEND=noninteractive

# Run install commands
RUN apt update && \
apt install wget python3 python3-pip python ffmpeg -y && \
pip3 install flask eyed3 youtube-dl requests && \
wget https://yt-dl.org/downloads/latest/youtube-dl -O /usr/local/bin/youtube-dl && \
chmod a+rx /usr/local/bin/youtube-dl