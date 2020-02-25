# Bus_Numbers
Helping the Visually Impaired Figure Out What Bus is Coming

Using a combination of Object Detection and Optical Character Recognition (OCR), this bus numbers project showcases the application of machine learning in helping the visually impaired "hear" what bus is coming when at the bus stop. 

Test out the API [Here](https://busapiwebpage.z21.web.core.windows.net/).

## Subscription Keys
Due to the use of Microsoft Azure's Custom Vision Object Detection and Cognitive Services - Optical Character Recognition APIs, I have ommited my own subscriptions keys.

To get around the need for a custom vision API key, I have uploaded a docker container export of a valid model to use. There is no need to enable the use of the offline docker container, it is the default setting in the bus_project.ipynb notebook. 

However, an Azure Cognitive Services Key is still necessary for the OCR section of the code. It is preferable to get a [multiservice one](https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-apis-create-account?tabs=multiservice%2Cwindows). After acquiring one, put it into a ".env" file in the root directory of the repository as shown below.

<pre>
ocr_key="94382360c4eae43646bc9beec9a21d58b"
</pre>

## Dependencies
This runs with jupyter and Python 3.7+.

Install the required python dependencies with
<pre>
pip3 install -r requirements.txt
</pre>

## About the Software
This bus number identification framework works in 5 main steps performed as a Azure Function

1. Send image data to Azure Custom Vision API
2. Crop image according to bounding box given by Custom Vision API
3. Send image to Azure Recognize Text API
4. Identify bus number based on words in response (the last word that begins with a number)
5. Synthesize audio output

