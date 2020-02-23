#!/usr/bin/env python
# coding: utf-8

# # Identification of Bus Numbers from Images
# 
# ### Steps
# 1. Find bounding box of bus numbers
# 2. Crop image to bounding box location
# 3. OCR on cropped image
# 4. Text to Speech to tell the visually impaired about the bus

# Libaries
import requests, json, numpy as np, time, sys, logging
from PIL import Image
from dotenv import load_dotenv
from os import getenv


# Import Keys
load_dotenv()

# Function Run if Unsuccessful
def if_fail():
    print("Unable to determine bus number")
    #sys.exit()

def check_bus_number(test_image, ocr_image_file = "/tmp/ocr.png"):
    logging.info("----- Check Bus Numbers Function Called -----")
    prediction_key = getenv("prediction_key")
    ocr_key = getenv("ocr_key")

    # ## Use Azure Custom Vision to Find Bounding Box of Image
    threshold = 0.2 #Threshold on what probability corresponds to a valid bounding box
    custom_vision_api = "https://southcentralus.api.cognitive.microsoft.com/customvision/v3.0/Prediction/b35dc00f-1a23-4f90-a2f1-c406952ff467/detect/iterations/Bus_Numbers_1/image"

    with open(test_image, 'rb') as image_file:
        custom_vision_response = requests.post(custom_vision_api, data=image_file, headers={"Prediction-Key": prediction_key, "Content-Type": "application/octet-stream"} )
    #print("Custom Vision Response:", custom_vision_response.text)

    json_response= json.loads(custom_vision_response.text)
    bounding_boxes = json_response['predictions']




    # Extract Best Bounding Box with Probability > 0.5
    max_probability = -1 
    for bounding_box in bounding_boxes:
        #print("Box:", bounding_box['probability'])
        max_probability = max(max_probability, bounding_box['probability'])

    if max_probability < threshold:
        print("No Valid Bounding Boxes Found")
        if_fail()
        return "-1"
    for i in bounding_boxes:
        if i['probability'] == max_probability:
            bounding_box = i 
            print(bounding_box)

    bounding_box = bounding_box['boundingBox']
    print("Bounding Box:", bounding_box)


    # ## Use Python Image Libary to Crop Image at Bounding Box
    # Import Test Image into Python
    raw_image = Image.open(test_image)
    width, height = raw_image.size

    # Set Points for Cropped Image to Bounding Box
    left = width*bounding_box['left']
    right = left + width*bounding_box['width']
    top = height*bounding_box['top']
    bottom = top + height*bounding_box['height']

    # Crop Image
    bus_num_image = raw_image.crop((left, top, right, bottom))


    ocr_crop_percentage = 0.5
    # Crop Away ocr_crop_percentage of Left Side for OCR Reasons
    width, height = bus_num_image.size
    left = width * ocr_crop_percentage
    right = width
    top = 0
    bottom = height

    ocr_image = bus_num_image.crop((left, top, right, bottom))

    # Resize Image with Interpolation if height too big (somehow OCR on Azure doesn't work too well with too sharp of bus numbers)
    width, height = ocr_image.size
    if height > 50:
        ocr_image = ocr_image.resize((int(width*50/height),50),Image.ANTIALIAS) # Ensure the aspect ratio doesn't change
    print("OCR Ready Image")

    # Save OCR Ready Image
    ocr_image.save(ocr_image_file)



    # Fits image into a square of at least 50x50 pixels by padding white space
    def Reformat_Image(ImageFilePath):

        from PIL import Image
        image = Image.open(ImageFilePath, 'r')
        image_size = image.size
        width = image_size[0]
        height = image_size[1]

        if(width != height or (width < 50 and height < 50)):
            bigside = width if width > height else height
            if bigside < 50:
                bigside = 50

            background = Image.new('RGBA', (bigside, bigside), (255, 255, 255, 255))
            offset = (int(round(((bigside - width) / 2), 0)), int(round(((bigside - height) / 2),0)))

            background.paste(image, offset)
            background.save(ocr_image_file)
            print("Image has been resized !")
            print(background.size)

        else:
            print("Image is already a square, it has not been resized !")
            
    Reformat_Image(ocr_image_file)


    # ## OCR with Azure Cognitive Services
    # 
    # Uses the Recognise Text API which operates asyncronously



    # Sending Image file to Recognise Text API
    #print("OCR KEY", ocr_key)
    ocr_api = "https://southcentralus.api.cognitive.microsoft.com/vision/v2.0/recognizeText"

    #ocr_image_file= "helloworld.png"
    params ={"mode": "Printed"}
    with open(ocr_image_file, 'rb') as image_file:
        print("Sending", ocr_image_file)
        ocr_response = requests.post(ocr_api, data=image_file, headers={"Ocp-Apim-Subscription-Key": ocr_key, "Content-Type": "application/octet-stream"}, params=params )
        print("Resource location", ocr_response.headers['Operation-Location'])
    ocr_response




    # Request for the Result
    request_result_api = ocr_response.headers['Operation-Location']
    counter = 0
    while True:
        ocr_status = requests.get(request_result_api, headers={"Ocp-Apim-Subscription-Key": ocr_key})
        print("Response Text:", ocr_status.text)
        json_response= json.loads(ocr_status.text)
        
        if json_response['status'] == "Succeeded":
            print("OCR Finished")
            break
        else:
            if (counter==5):
                print("OCR Requests Timed Out...")
                if_fail()
                return "-2"
            counter += 1
            time.sleep(0.5)




    # Extract Lines from Response
    lines = json_response["recognitionResult"]["lines"]
    if len(lines) == 0:
        print("No Text Identified...")

    # Finding first word that begins with a number
    predicted_number = ""
    for line in lines:
        for word in line["words"]:
            #print(word["text"][0])
            if word["text"][0].isdigit():

                predicted_number = word["text"]
                break
    if predicted_number == "":
        print("Failed to Get a Number...")
        if_fail()
        return "-2"
        
    else:
        print("Predicted Bus Number:", predicted_number)

    return (predicted_number)
    # ## Synthesise Speech to Output File



    #speech_key, service_region = ocr_key, "southcentralus"
    #speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    #audio_filename = "bus_number.wav"
    #audio_output = speechsdk.AudioOutputConfig(filename=audio_filename)

    #speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)

    #text = "Bus "+ predicted_number + " is coming now!"
    #result = speech_synthesizer.speak_text_async(text).get()

    #if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        #print("Speech synthesized to [{}] for text [{}]".format(audio_filename, text))
    #elif result.reason == speechsdk.ResultReason.Canceled:
        #cancellation_details = result.cancellation_details
        #print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        #if cancellation_details.reason == speechsdk.CancellationReason.Error:
            #if cancellation_details.error_details:
                #print("Error details: {}".format(cancellation_details.error_details))

#check_bus_number("bus_ext_1.jpeg")
