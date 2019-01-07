#  IoT Based Object Detection

#### *Key words:  Movidius, Raspberry Pi, Flask Backend*

### Introduction
Movidius NCS is Intel's framework to provide inference service on edge devices like Raspberry Pi, it works well with Intel's Neural Stick.
It takes Caffe and TensorFlow trained models and load it into embedded devices for machine learning inference tasks.

![alt text](https://cdn-images-1.medium.com/max/1600/1*sPZNuScv3C93RsCfONjWUg.jpeg)

In this project, I generall use Movidius NCS along with Raspberry Pi to  deploy a small AI backend server to provide service for user of local networks.

Based on machine learning models, I used both Caffe and TensorFlow pretrained models. I can get MobileNet model running at 6.5 FPS in raspberry pi, while yolo can only run at 2 fps. MobileNet is pretty good considering raspberry hardware.

Caffe ssd_mobilenet model is intended to do object detection task. It can recogninze 21 classes and support generating real time bounding boxes for classification. While TensorFlow  mobilenet model doesn't support generating bounding boxes but it support recognizing 1000 classes of objects as compensation. It's designed to do image classification task. 


##### About the model input and output
>For Caffe Models: ssd_mobilenet
compile:
mvNCCompile MobileNetSSD_deploy.prototxt -w MobileNetSSD_deploy.caffemodel  -s 12 -o graph
output:
output[0] :  num_valid_boxes
output[base_index + 1] : prediction class index
output[base_index + 2] : prediction confidence
output[base_index + 3] : object boxpoint x1 value (it needs to be scaled)
output[base_index + 4] : object boxpoint y1 value (it needs to be scaled)
output[base_index + 5] : object boxpoint x2 value (it needs to be scaled)
output[base_index + 6] : object boxpoint y2 value (it needs to be scaled)


>for TensorFlow Models: mobilenet
compile:
mvNCCompile -s 12 mobilenet_v1_1.0_224_frozen.pb  -in=input -on=MobilenetV1/Predictions/Reshape_1
output[i] : prediction confidence for class i



### General Steps 

1. compile the pre-trained TensorFlow models or Caffe models into a graph file for Neural Stick
2. write python scripts to run the model and do the prediction
3. set up a flask server to provide inference service by replying requests with JSON response
4. design a simple frontend page to make AJAX requests  


### Some Result about Inference:

>For Caffe ssd_mobilenet detection model (21 Classes):
ubuntu : 10.5 FPS
Raspberry pi: 6.5 FPS
I used ubuntu for development and raspberry for deployment

![alt text](https://github.com/liu578/MovidiusNCS/blob/master/caffe/results/Screenshot%20from%202018-12-05%2015-19-14.png?raw=true)
![alt text](https://github.com/liu578/MovidiusNCS/blob/master/caffe/results/Screenshot%20from%202018-12-05%2015-35-30.png?raw=true)
![alt text](https://github.com/liu578/MovidiusNCS/blob/master/caffe/results/Screenshot%20from%202018-12-05%2015-27-16.png?raw=true)
![alt text](https://github.com/liu578/MovidiusNCS/blob/master/caffe/results/Screenshot%20from%202018-12-06%2013-42-41.png?raw=true)

>For TensorFlow mobilenet classifying model (1000 Classes):
ubuntu : 20 FPS
Raspberry pi: 11.5 FPS

![alt text](https://github.com/liu578/MovidiusNCS/blob/master/tensorflow/results/Screenshot%20from%202018-12-06%2013-54-41.png?raw=true)
![alt text](https://github.com/liu578/MovidiusNCS/blob/master/tensorflow/results/Screenshot%20from%202018-12-06%2013-41-20.png?raw=true)

### Web Service

1.I tested both aiohttp and flask backend frameworks, flask backend is easier to use while aiohttp may be more powerful for combination of inference services and streaming service as concurrent in the future. Currently I mainly used flask for quick prototype

2.Frontend is a simple single-page app, each time the user click the snapshot button, an AJAX request is sended to the backend, while backend will 
take a snapshot immediately and do the inference to the image, and send back the result as a JSON response to the frontend. Each time a user click the snapshot button, a new photo took and a new inference result will be responsed.

3.Any devices can visit the flask server and make a request through the web browser. Users can set the camera with the raspberry pi any where because they are very low-power and portable.

![alt text](https://github.com/liu578/MovidiusNCS/blob/master/tensorflow/results/Screen%20Shot%202019-01-07%20at%203.19.23%20AM.png?raw=true)

### Future Plan
In the future I am gonna design a new web backend to do realtime streaming as well as realtime inference. I will use the Caffe ssd_mobilenet model for inference and set up a powerful backend to do concurrent tasks. Raspberry Pi is more powerful than I thought, I want to make the most of it and let it act as a local AI service center, providing AI services to local users.
