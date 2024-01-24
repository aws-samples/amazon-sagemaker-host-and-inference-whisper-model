# Host the Whisper Model on Amazon SageMaker: exploring inference options

In this post, we embark on an exploration of SageMaker's capabilities, specifically focusing on hosting Whisper models. We'll dive deep into two methods for doing this: one utilizing the Whisper PyTorch model and the other using the Hugging Face implementation of the Whisper model. Additionally, we’ll conduct an in-depth examination of SageMaker's inference options, comparing them across parameters such as speed, cost, payload size, and scalability. This analysis empowers users to make informed decisions when integrating Whisper models into their specific use cases and systems.

<img src="images/solution_overview.png">


1. In order to host the model on Amazon SageMaker, the first step is to save the model artifacts. These artifacts refer to the essential components of a machine learning model needed for various applications, including deployment and retraining. They can include model parameters, configuration files, pre-processing components, as well as metadata, such as version details, authorship, and any notes related to its performance. It's important to note that Whisper models for PyTorch and Hugging Face implementations consist of different model artifacts. 

2. Next, we create custom inference scripts. Within these scripts, we define how the model should be loaded and specify the inference process. This is also where we can incorporate custom parameters as needed. Additionally, you can list the required Python packages in a *requirements.txt* file. During the model's deployment, these Python packages are automatically installed in the initialization phase. 

3. Then we select either the PyTorch or Hugging Face deep learning containers (DLC) provided and maintained by AWS. These containers are pre-built Docker images with deep learning frameworks and other necessary Python packages. For more information, you can check this [link](https://docs.aws.amazon.com/sagemaker/latest/dg/docker-containers-prebuilt.html).  

4. With the model artefacts, custom inference scripts and selected DLCs, we’ll create Amazon SageMaker models for PyTorch and Hugging Face respectively. 

5. Finally, the models can be deployed on SageMaker and used with the following options: real-time inference endpoints, batch transform jobs, and asynchronous inference endpoints. We’ll dive into these options in more detail later in this post.
 

This notebook is tested in SageMaker Studio. Below shows detailed setup.   
- SageMaker Studio: **ml.m5.large** instance with **Data Science 2.0** kernel.

## Tested Software Versions:

* sagemaker : 2.184.0
* transformers : 4.34.0
* openai-whisper : 20230918
* torchaudio : 2.1.0
* accelerate : 0.23.0
* datasets : 2.16.1
* librosa : 0.10.1
* soundfile : 0.12.1

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.