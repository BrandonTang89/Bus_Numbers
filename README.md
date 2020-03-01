# Bus_Numbers
Helping the Visually Impaired Figure Out What Bus is Coming

Using a combination of Object Detection and Optical Character Recognition (OCR), this bus numbers project showcases the application of machine learning in helping the visually impaired "hear" what bus is coming when at the bus stop. 

Test out the API [Here](https://busapiwebpage.z21.web.core.windows.net/).

## About
This bus numbers project analyses an image and extracts the location of the bus number on a bus and then sends a cropped version of the image to an OCR API on Microsoft Azure to extract the bus number. This information is then encoded into an audio file which is played to the user (the visually impaired).

### Testing the Software
Head to [this website](https://busapiwebpage.z21.web.core.windows.net/) to test out the the project.

The website works in 5 main steps performed by Azure Functions.
1. Send image data to Azure Custom Vision API
2. Crop image according to bounding box given by Custom Vision API
3. Send image to Azure Recognize Text API
4. Identify bus number based on words in response (the last word that begins with a number)
5. Synthesize audio output

### Detailed Analysis
Open the "bus_project.ipynb" jupyter notebook to see how it works and test it out. 

The object detection is done by Microsoft Azure's Custom Vision Service while the OCR is done by Azure's Recognize Text API.

#### Example Execution
Input Image:<br>
<img src="https://raw.githubusercontent.com/BrandonTang89/Bus_Numbers/master/Documents/example_images/bus_high_res_1.jpg" height="400">

Cropped Bounding Box:<br>

![Cropped Bounding Box](https://raw.githubusercontent.com/BrandonTang89/Bus_Numbers/master/Documents/example_images/Bounding_Box.png "Image Cropped to Bounding Box")

Image Further Cropped for OCR:<br>
<img src="https://raw.githubusercontent.com/BrandonTang89/Bus_Numbers/master/Documents/example_images/Cropped.png" height="150">

Conclusion: **12**
## Subscription Keys
Due to the use of Microsoft Azure's Custom Vision Object Detection and Cognitive Services - Optical Character Recognition APIs, I have ommited my own subscriptions keys.

To get around the need for a custom vision API key, I have uploaded a docker container export of a valid model to use. There is no need to enable the use of the offline docker container, it is the default setting in the bus_project.ipynb notebook. 

However, an Azure Cognitive Services Key is still necessary for the OCR section of the code. It is preferable to get a [multiservice one](https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-apis-create-account?tabs=multiservice%2Cwindows). If not, get one for the [Recognize Text API](https://docs.microsoft.com/en-us/azure/cognitive-services/computer-vision/concept-recognizing-text#recognize-text-api). After acquiring one, put it into a ".env" file in the root directory of the repository as shown below.

<pre>
ocr_key="94382360c4eae43646bc9beec9a21d58b"
</pre>

## Dependencies
This runs with jupyter and Python 3.7+.

Install the required python 3 dependencies with
<pre>
pip3 install -r requirements.txt
</pre>
(for linux)

or
<pre>
pip install -r requirements.txt
</pre>
(for windows)

Learn about jupyter and how to install and use it [here](https://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/what_is_jupyter.html).

Also note that the paths in the jupyter files are written in unix style, thus take note to change the file paths if running on a windows machine.
