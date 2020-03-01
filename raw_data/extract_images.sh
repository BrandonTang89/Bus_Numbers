#!/bin/bash
echo "Bash version ${BASH_VERSION}..."
N=6 #Number of videos
for ((INDEX=1; INDEX<=$N; INDEX++)) 
do
	ffmpeg -i bus_$INDEX.mp4 bus_pics/bus_pic_${INDEX}_%04d.jpg -hide_banner -qscale:v 2
done
