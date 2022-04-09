#Lambda function for processing CO2 data
import json
import logging
import sys
import greengrasssdk

# Setup logging to stdout
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Creating a greengrass core sdk client
client = greengrasssdk.client("iot-data")


def function_handler(event, context):
    vehicle_no = list(event.keys())[0]
    CO2_dict = event[vehicle_no]
    CO2_values = CO2_dict.values()
    max_CO2_value = max(CO2_values)
    client.publish(
        topic="Data/{}".format(vehicle_no),
        queueFullPolicy="AllOrException",
        payload=json.dumps(max_CO2_value),
    )
