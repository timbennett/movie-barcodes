# Movie Barcode Generator
![github-bighero6](https://cloud.githubusercontent.com/assets/1192790/11238640/1f7ea5ac-8e3b-11e5-8c2b-e00758b1ec19.png)

Turn video files into 'barcodes' where vertical lines represent the average colour of individual frames. [Example album.](http://imgur.com/gallery/Pw6LD/) Uses code [published by zulko](http://zulko.github.io/blog/2013/09/27/read-and-write-video-frames-in-python-using-ffmpeg/).

**Requirements:**
* [ffmpeg](https://www.ffmpeg.org/)
* Python and [Python Imaging Library](http://www.pythonware.com/products/pil/)
 
**Usage:**  
    *python process_video.py inputfile width height*  
e.g.  
    *python process_video.py bigbuckbunny.mp4 320 180*

**Tips:**
* If it doesn't work on Windows, you might have to change FFMPEG_BIN from "ffmpeg" to "ffmpeg.exe"
* Use low resolution videos! They provide identical results but are processed exponentially faster than high definition videos (I've seen above 1300fps). You're smearing all the details anyway.
* By default, the resulting image will be as wide as the number of frames in the movie - probably several tens of thousands of pixels. However due to the nature of PNG files, it will only be a few hundred kilobytes! But you will need to use Photoshop or similar to format the images to your liking... or patch my code so the user can specify output size!
 
**Details:**

You may have seen sites like [moviebarcode](http://moviebarcode.tumblr.com/), [The Colors of Motion](http://thecolorsofmotion.com/) or the [Movie Barcode Generator](http://arcanesanctum.net/movie-barcode-generator/). In short, they compress a movie into a single image, with vertical lines representing the average colours of sequential frames. Ideally this gives a glanceable idea of the movie's colour palette.

While moviebarcode squashes each frame to a single pixel width (preserving some vertical gradients), this script uses a similar process to The Colors of Motion (a single colour per frame). First find the average RGB values of all pixels in a single frame:

![github-process-1](https://cloud.githubusercontent.com/assets/1192790/11238530/715e0d1e-8e3a-11e5-9736-68f2e67d21fc.png)

And then to repeat the process for all frames:

![github-process-2](https://cloud.githubusercontent.com/assets/1192790/11238535/7664e6ac-8e3a-11e5-8989-6be607fa395e.png)

This should work with any movie file ffmpeg can handle (though in practice I've only tested it with mp4 files). 

**Quibbles:**
* I'd love to autodetect the video resolution but this seems to require grepping some ffmpeg output.
* There ~~may be~~ is almost certainly a faster approach than the one I'm using. Perhaps I should only take every nth frame?
* Users should be able to specify an output size instead of having to manually edit the file.

(Video stills: [Big Buck Bunny](https://peach.blender.org/download/))
