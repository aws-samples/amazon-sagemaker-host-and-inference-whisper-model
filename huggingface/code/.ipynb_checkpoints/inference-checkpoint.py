# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0


import os
import io
import sys
import time
import json
import logging

import whisper
import torch
import boto3
import ffmpeg
import torchaudio
import tempfile
from transformers import pipeline

device = "cuda:0" if torch.cuda.is_available() else "cpu"
chunk_length_s = int(os.environ.get('chunk_length_s'))

def model_fn(model_dir):
    model = pipeline(
        "automatic-speech-recognition",
        model=model_dir,
        chunk_length_s=chunk_length_s,
        device=device,
        )
    return model


def transform_fn(model, request_body, request_content_type, response_content_type="application/json"):
     
    logging.info("Check out the request_body type: %s", type(request_body))
    
    start_time = time.time()
    
    if sys.getsizeof(request_body) >= 1000: # video or audio loaded 
        file = io.BytesIO(request_body)
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(file.read())
        

    else: # json path loaded 
        input_data = json.loads(request_body)
        input_path = input_data['s3_location']
        logging.info("Check out the input_path: %s", input_path)

        input_bucket_name = input_path.split('/')[2]
        input_file_name = ('/').join(input_path.split('/')[3:])

        s3_client = boto3.client('s3')

        # Download the file
        logging.info("Download video file from S3 bucket: %s", input_bucket_name)

        # Create a temporary file. 
        # * File has to be saved as temp file. cannot write into the container
        tfile = tempfile.NamedTemporaryFile(delete=False)

        # Download the video file from S3
        s3_client.download_file(input_bucket_name, input_file_name, tfile.name)

        # Close the temporary file to ensure it is accessible for reading
        tfile.close()
    

    logging.info("Start to generate the transcription ...")
    result = model(tfile.name, batch_size=8)["text"]
    
    logging.info("Upload transcription results back to S3 bucket ...")
    
    # Calculate the elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info("The time for running this program is %s", elapsed_time)

    
    return json.dumps(result), response_content_type   
    
