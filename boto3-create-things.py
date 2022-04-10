# Part 1 code for creating 50 things
################################################### Connecting to AWS
import boto3

import json
import string

import csv
import os

def createThing(i):
  global thingClient
  thingResponse = thingClient.create_thing(
      thingName = thingName
  )
  data = json.loads(json.dumps(thingResponse, sort_keys=False, indent=4))
  for element in data: 
    if element == 'thingArn':
        thingArn = data['thingArn']
    elif element == 'thingId':
        thingId = data['thingId']
        createCertificate(i)

def createCertificate(i):
    global thingClient
    certResponse = thingClient.create_keys_and_certificate(
        setAsActive = True
        )
    data = json.loads(json.dumps(certResponse, sort_keys=False, indent=4))
    for element in data:
        if element == 'certificateArn':
            certificateArn = data['certificateArn']
        elif element == 'keyPair':
            PublicKey = data['keyPair']['PublicKey']
            PrivateKey = data['keyPair']['PrivateKey']
        elif element == 'certificatePem':
            certificatePem = data['certificatePem']
        elif element == 'certificateId':
            certificateId = data['certificateId']

    directory = "vehicle{}/".format(i)
    parent_dir = "certs/"
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
    
    public_pem = path + "vehicle{}.public.pem".format(i)
    private_pem = path + "vehicle{}.private.pem".format(i)
    certificate_pem = path + "vehicle{}.certificate.pem".format(i)
    with open(public_pem, 'w') as outfile:
        outfile.write(PublicKey)
    with open(private_pem, 'w') as outfile:
        outfile.write(PrivateKey)
    with open(certificate_pem, 'w') as outfile:
        outfile.write(certificatePem)

    response = thingClient.attach_policy(
        policyName = defaultPolicyName,
        target = certificateArn
        )
    response = thingClient.attach_thing_principal(
        thingName = thingName,
        principal = certificateArn
        )

for i in range(50):
    ################################################### Parameters for Thing
    thingArn = ''
    thingId = ''
    thingName = "Vehicle_{}".format(i)
    defaultPolicyName = 'My_Iot_Policy'
    ###################################################
    thingClient = boto3.client('iot')
    createThing(i)
