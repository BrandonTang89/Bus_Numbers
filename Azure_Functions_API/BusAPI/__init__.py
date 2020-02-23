import logging
import azure.functions as func

print("Importing Bus Project Code")
from . import bus_project

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    print("Processing Request")
    temp_image = "/tmp/image.jpeg"
    image_data = req.get_body()
    f = open(temp_image, 'wb')
    f.write(image_data)
    print("Image Written to", temp_image)

    predicted_bus_number = bus_project.check_bus_number(temp_image)
    if predicted_bus_number != "-1" and predicted_bus_number != "-2":
        predict_string = "Bus " + predicted_bus_number + " is Coming Now!\n"
    elif predicted_bus_number == "-1":
        predict_string = "No Bus Detected in Image\n"
    else:
        predict_string = "Could Not Read Bus Number on Bus"


    return func.HttpResponse(
        predict_string,
        status_code=400
    )
