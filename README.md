# StegSuit
Used to do complete Steganography analysis of an image.

StegoSuit is a tool for extracting secret messages hidden in the images. It is has 5 basic functions which will help the the user to analyse the image.

This tool is developed in Python3.
You need to install these modules in python3 to get it running:
1. opencv-python
2. pillow
3. tkinter

Using this tool you can perform ELA (Error Level Analysis), String, Threshold, Edge and Metadata analysis of any image.


The First Module is the Error Level Analysis. This is done in digital data with lossy compression such as JPEG. In this module the image is compression and compared with the original image which is then multiplied with a scaling factor giving us the area with different noise ratio in the location where the image is edited. This can be very helpful in finding out fake images and detect the image that have been manipulated.

Second Module is the Threshold analysis of the image. This is very helpful in analysing the images with darker area or shades. This converts the image in binary image which basically is an image with tow colours black represented by 0 and white represented by 1. This converts the image into black and white format and displays only the portion of image with whose value is greater than the threshold value provided.

Third Module is Edge Detection is used to detect all the minute partials in the image which cannot be seen by naked eyes and helps in determining the basic structure of the image. It also highlights all the edges of the image, so the investigator can easily check for any irregularities in the image.

Fourth Module is the Metadata analysis which provide all the data of the image including the location and the device used to click the image and the time at which the image has been clicked. Fifth module is the String analysis which helps in finding any hidden text that is present in the image. This will display all the readable text that the tool will find in the image and display in the text box present.
