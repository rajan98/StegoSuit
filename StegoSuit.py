from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk, ExifTags
import cv2
import re
import string


def image_not_loaded():
    messagebox.showerror("Image Error", "No image selected. Please select an image")


def not_valid_image():
    messagebox.showerror("Wrong Image", "Selected image is not a Valide Image. Please select a valid image")


# Convert OpenCV image to ImageTk, resize it, bind it with label and display it on the screen
def display_image(displayImage, color):
    global imageLabel, imageFrame

    if displayImage is not None:

        if color != -1:
            displayImage = cv2.cvtColor(displayImage, cv2.COLOR_BGR2RGB)
            
        displayImage = Image.fromarray(displayImage)
        newHeight = 600
        newWidth = int(displayImage.width * (newHeight / displayImage.height))
        displayImage = ImageTk.PhotoImage(displayImage.resize((newWidth, newHeight)))

    if imageLabel is None:
        imageLabel = Label(imageFrame, image=displayImage)
        imageLabel.image = displayImage
        imageLabel.pack(side=LEFT, padx=10, pady=10)
    else:
        imageLabel.configure(image=displayImage)
        imageLabel.image = displayImage


# Create a Dialog Box to Import an image
def select_image():
    global image, pImage, path

    path = filedialog.askopenfilename()

    if len(path) > 0:
        try:
            pImage = Image.open(path)
            # Destroy widget from scaleFrame
            for widget in sliderFrame.winfo_children():
                widget.destroy()

            image = cv2.imread(path)
            display_image(image, 1)
        except:
            not_valid_image()

# ###########################Show Original Image#############################


def show_original_image():
    global image

    if image is None:
        image_not_loaded()
    else:
        # Destroy widget from scaleFrame
        for widget in sliderFrame.winfo_children():
            widget.destroy()

        l = Label(sliderFrame)
        l.pack()
        display_image(image, 1)

#############################################################################

# ########################Error Level Analysis###############################


def error_level_analysis():
    global quality, scale, sliderFrame, image

    # Destroy Older Widget to make room for new widget
    for widget in sliderFrame.winfo_children():
        widget.destroy()

    # Check if Image is loaded
    if image is None:
        image_not_loaded()
    else:
        quality = Scale(sliderFrame, from_=0, to=100, command=change, length=500)
        quality.set(80)
        quality.pack(side='right')

        scale = Scale(sliderFrame, from_=0, to=100, command=change, length=500)
        scale.set(20)
        scale.pack(side='right')

        ELA(quality.get(), scale.get())


def ELA(quality, scale):
    global image
    cv2.imwrite('comp.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, quality])
    com = cv2.imread('comp.jpg', 1)
    output = cv2.subtract(image, com) * scale
    display_image(output, 1)


def change(var):
    global quality, scale
    ELA(quality.get(), scale.get())

###########################################################################


# #######################Threshold Analysis################################

def threshold_analysis():
    global sliderFrame, image, th

    # Destroy Older Widget to make room for new widget
    for widget in sliderFrame.winfo_children():
        widget.destroy()

    if image is None:
        image_not_loaded()
    else:
        th = Scale(sliderFrame, from_=3, to=701, command=calculate_threshold, length=500)
        th.set(115)
        th.pack(side='right')


def fix(thresh):
    if not thresh % 2:
        th.set(thresh+1)
        return thresh+1
    return thresh


def calculate_threshold(thresh):
    global image
    thresh = int(thresh)
    thresh = fix(thresh)
    output = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    output = cv2.adaptiveThreshold(output, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, thresh, 1)
    display_image(output, -1)


###########################################################################

# ##############################Edge Detection##############################

def edge_detection():
    global image, t1, t2

    if image is None:
        image_not_loaded()
    else:
        # Destroy Older Widget to make room for new widget
        for widget in sliderFrame.winfo_children():
            widget.destroy()

        t1 = Scale(sliderFrame, from_=0, to=500, command=edge_change, length=500)
        t1.set(50)
        t1.pack(side='right')

        t2 = Scale(sliderFrame, from_=0, to=500, command=edge_change, length=500)
        t2.set(100)
        t2.pack(side='right')

        calculate_edge(t1.get(), t2.get())


def calculate_edge(thr1, thr2):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edge = cv2.Canny(gray, thr1, thr2)
    display_image(edge, -1)


def edge_change(var):
    global t1, t2
    calculate_edge(t1.get(), t2.get())


############################################################################


# #########################Metadata of Image################################

def extract_metadata():
    global image, pImage

    if pImage is None:
        image_not_loaded()
    else:
        # Destroy Older Widget to make room for new widget
        for widget in sliderFrame.winfo_children():
            widget.destroy()

        mdata = "------------------------------Image Metadata--------------------------\n"

        # Arrange the item code with there tagId's
        try:
            exif = {
                ExifTags.TAGS[k]: v
                for k, v in pImage._getexif().items()
                if k in ExifTags.TAGS
            }
            # Converting Dictionary in String format
            for k in exif:
                mdata = mdata + "\n" + "{0}: {1}".format(k, exif[k])

        except:
            mdata = mdata + "\n\nNo Metadata Found for this Image"

        vs = Scrollbar(sliderFrame, orient="vertical")
        hs = Scrollbar(sliderFrame, orient="horizontal")
        text = Text(sliderFrame, spacing1=8)
        text.insert(END, mdata)

        # hook up the scrollbars to the text widget
        text.configure(yscrollcommand=vs.set, xscrollcommand=hs.set, wrap="none", height=27)
        vs.configure(command=text.yview)
        hs.configure(command=text.xview)

        text.grid(row=0, column=0, sticky='nesw')
        vs.grid(row=0,column=1,sticky="ns")
        hs.grid(row=1,column=0,sticky="news")

############################################################################


# #####################String Analysis######################################

def string_analysis():
    global path

    if pImage is None:
        image_not_loaded()
    else:
        # Destroy Older Widget to make room for new widget
        for widget in sliderFrame.winfo_children():
            widget.destroy()

        # Extracting Readable string from image
        nonPrintable = re.compile(b'[^%s]+' % re.escape(string.printable.encode('ascii')))
        s = ""
        
        with open(path, "rb") as f:
            for result in nonPrintable.split(f.read()):
                if result:
                    s = s + "\n" + result.decode('ASCII')

        # Displaying the Readable string in text widget
        vs = Scrollbar(sliderFrame, orient="vertical")
        hs = Scrollbar(sliderFrame, orient="horizontal")
        text = Text(sliderFrame)
        text.insert(END, s)

        # hook up the scrollbars to the text widget
        text.configure(yscrollcommand=vs.set, xscrollcommand=hs.set, wrap="none", height=40)
        vs.configure(command=text.yview)
        hs.configure(command=text.xview)

        text.grid(row=0, column=0, sticky='nesw')
        vs.grid(row=0, column=1, sticky="ns")
        hs.grid(row=1, column=0, sticky="news")

############################################################################

steg_root = Tk()
steg_root.title("StegoSuite")
steg_root.resizable(0,0)

image = None
t1 = None
t2 = None
pImage = None
# Top Option Buttons
topFrame = Frame(steg_root)
topFrame.grid(row=0, column=0)

showImageButton = Button(topFrame, text="Original Image", command=show_original_image, bg="DarkOliveGreen2")
elaButton = Button(topFrame, text="Error Level Analysis", command=error_level_analysis, bg="SeaGreen1")
thresholdButton = Button(topFrame, text="Threshold Analysis", command=threshold_analysis, bg="light sky blue")
edgeDetection = Button(topFrame, text="Edge Detection", command=edge_detection, bg="HotPink")
metadata = Button(topFrame, text="Metadata", command=extract_metadata, bg="DarkOrange1")
sanalysis = Button(topFrame, text='String Analysis', command=string_analysis, bg="goldenrod")

showImageButton.pack(side=LEFT)
elaButton.pack(side=LEFT)
thresholdButton.pack(side=LEFT)
edgeDetection.pack(side=LEFT)
metadata.pack(side=LEFT)
sanalysis.pack(side=LEFT)

# Image Container
imageFrame = Frame(steg_root, height=500, width=500)
imageFrame.grid(row=1, column=0)
imageLabel = None

# Frame to Store the Sliders
sliderFrame = Frame(steg_root)
sliderFrame.grid(row=1, column=1)
quality = None
scale = None

# Last Frame with Open Image Button
bottomFrame = Frame(steg_root)
bottomFrame.grid(row=2, column=0)
openImageButton = Button(bottomFrame, text="Open Image", command=select_image, font="Helvetica 14 bold", bg="PeachPuff2")
openImageButton.pack(side=LEFT)

# Footer

footerLabel = Label(steg_root,height="2",bg="grey1",width="100",fg="white",text="StegoSuite v0.1 BETA, Developed under Project OFTK\n Contributors: Rajan Kumar Shah")
footerLabel.grid(row=3, column=0)

steg_root.mainloop()
