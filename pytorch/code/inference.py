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
import tempfile
import torchaudio
from botocore.exceptions import NoCredentialsError


DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def model_fn(model_dir):
    """
    Load and return the model
    """
    model = whisper.load_model(os.path.join(model_dir, 'base.pt'))
    model = model.to(DEVICE)
    print(f'whisper model has been loaded to this device: {model.device.type}')
    return model

def transform_fn(model, request_body, request_content_type, response_content_type="application/json"):
    """
    Transform the input data and generate a transcription result
    """
    logging.info("Check out the request_body type: %s", type(request_body))
    start_time = time.time()
    
    if sys.getsizeof(request_body) >= 1000:  # Assume binary data (video or audio)
        file = io.BytesIO(request_body)
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(file.read())
        
    else:  # JSON input with S3 location
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

    logging.info("Start generating the transcription ...")
    result = model.transcribe(tfile.name)
    logging.info("Transcription generation completed.")

    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info("Elapsed time: %s seconds", elapsed_time)

    return json.dumps(result), response_content_type