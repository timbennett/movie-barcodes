from __future__ import division
import subprocess as sp
import numpy
from PIL import Image, ImageDraw
import re
import time
import sys

# Timestamp so you can see how long it took
start_time = "Script started at " + time.strftime("%H:%M:%S")
print start_time

# optional starting time hh:mm:ss.ff; default value set to 00:00:00.0
hh = "%02d" % (0,)
mm = ":%02d" % (0,)
ss = ":%02d" % (0,)
ff = ".0"
print "Timestamp for first frame: "+hh+mm+ss+ff

# input file (first argument)
filename = str(sys.argv[1])
width = int(sys.argv[2])
height = int(sys.argv[3])
# output image file (same as input file, with non-alphanums stripped):
outfilename = re.sub(r'\W+', '', filename) + ".png"
print "Filename:", filename
print "Dimensions:",width,height

###
### This section: credit to http://zulko.github.io/blog/2013/09/27/read-and-write-video-frames-in-python-using-ffmpeg/

# Open the video file. In Windows you might need to use FFMPEG_BIN="ffmpeg.exe"; Linux/OSX should be OK.
FFMPEG_BIN = "ffmpeg"
command = [ FFMPEG_BIN,
            '-threads', '4',
            '-ss', hh+mm+ss,
            '-i', filename,
            '-f', 'image2pipe',
            '-pix_fmt', 'rgb24',
            '-vcodec', 'rawvideo', '-']
pipe = sp.Popen(command, stdout = sp.PIPE, bufsize=10**8)

# get the average rgb value of a frame
def draw_next_frame_rgb_avg(raw_frame):    
    frame =  numpy.fromstring(raw_frame, dtype='uint8')
    frame = frame.reshape((height,width,3))    
    rgb_avg = int(numpy.average(frame[:,:,0])),int(numpy.average(frame[:,:,1])),int(numpy.average(frame[:,:,2]))
    return rgb_avg


# Go through the pipe one frame at a time until it's empty; store each frame's RGB values in rgb_list 
rgb_list = []
x = 1 # optional; purely for displaying how many frames were processed
while pipe.stdout.read(width*height*3): # as long as there's data in the pipe, keep reading frames
    try:
        rgb_list.append(draw_next_frame_rgb_avg(pipe.stdout.read(width*height*3)))
        x = x + 1
    except:
        print "No more frames to process (or error occurred). Number of frames processed:", x

# create a new image width the same width as number of frames sampled,
# and draw one vertical line per frame at x=frame number
image_height = 720 # set image height to whatever you want; you could use int(len(rgb_list)*9/16) to make a 16:9 image for instance
new = Image.new('RGB',(len(rgb_list),image_height))
draw = ImageDraw.Draw(new)
# x = the location on the x axis of the next line to draw
x_pixel = 1
for rgb_tuple in rgb_list:
    draw.line((x_pixel,0,x_pixel,image_height), fill=rgb_tuple)
    x_pixel = x_pixel + 1
new.show() 
new.save(outfilename, "PNG")

print start_time
print "Script finished at " + time.strftime("%H:%M:%S")
