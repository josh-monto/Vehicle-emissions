#visualize_notebook.py
# Part 3 Visualization code
import boto3
import pandas as pd
import matplotlib.pyplot as plt

# create IoT Analytics client
client = boto3.client('iotanalytics')

dataset = "dataset_2"
dataset_url = client.get_dataset_content(datasetName = dataset)['entries'][0]['dataURI']
data = pd.read_csv(dataset_url)
print(data)
plt.plot(data["hue"])
plt.title("Hue")
plt.show()
plt.plot(data["saturation"])
plt.title("Saturation")
plt.show()
plt.plot(data["value"])
plt.title("Value")
plt.show()
