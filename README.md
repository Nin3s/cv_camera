# cv_camera
Camera program written using Python and OpenCV  
The purpose of this program is to be used with a Raspberry Pi in order to take photos during the NASA Student Launch competition.  

Do take a look at the [current issues](https://github.com/Nin3s/cv_camera/issues) to see what needs to be done (feel free to add more if needed as well)  

NOTE: When using the gif overlay, there is a lag in video output. I do not know if that will affect the camera output on the raspberry pi since we don't actually need video output, but it's something to keep in mind.

## How to run it:
1. Install python on your system
2. Install opencv-python with the command `pip install opencv-python`
3. To run it, type in `python cam.py` into the terminal

## Button Inputs for Testing Purposes:
`space`: takes a photo  
`1`: toggle grayscale effect  
`2`: toggle 180 flip effect  
`3`: overlay a gif image of the bad news gif  
`4`: static overlay (not needed but just in case gif overlay ends up falling through)  
`5`: clears all effects  
`q`: quits and closes the program  

## Color Channels
Images read in opencv using RGB or BGR are read using 3 color channels (red, green, blue). Our opencv program reads images using BGR, which just means the color blue is read in first.  

Converting the image into grayscale turns that 3 channel image into a 2 channel one. That's why if you want to overlay another image, you have to either convert that overlay into a 2 channel, or convert the captured grayscale frame into a 3 channel.  

You can see the different sizes of the images with the `print([image].shape)` that's inserted into the code.  

## Requirements for NSL:
1. Add timestamp to photo
2. Change image to and from grayscale
3. Special effects filter
4. Pan camera at different angles
5. Be able to receive commands from radio signals
