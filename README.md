# IoT Based Object Detection 
### *Key words:  Movidius, Raspberry Pi, Flask Backend*
Movidius NCS is Intel's framework to provide inference service on edge devices like Raspberry Pi, it works well with Intel's Neural Stick.
It takes Caffe and TensorFlow trained models and load it into embedded devices for machine learning inference tasks.

In this project, I generall use Movidius NCS along with Raspberry Pi to  deploy a small AI backend server to provide service for user of local networks.

Based on machine learning models, I used both Caffe and TensorFlow pretrained models. I can get MobileNet model running at 6.5 FPS in raspberry pi, while yolo can only run at 2 fps. MobileNet is pretty good considering raspberry hardware.

The general idea has four steps.

1. compile the pre-trained TensorFlow models or Caffe models into a graph file for Neural Stick
2. write python scripts to test the model and do the prediction
3. set up a flask server to provide inference service by replying requests with JSON response
4. design a simple frontend page to make AJAX requests  

Based on the different models I choose, Caffe ssd_mobilenet model is intended to do object detection task. It can recogninze 21 classes and support generating real time bounding boxes for classification. While TensorFlow  mobilenet model doesn't support generating bounding boxes but it support recognizing 1000 classes of objects as compensation. It's designed to do image classification task. 

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


## Some Result:

>For Caffe ssd_mobilenet detection model (21 Classes):
ubuntu : 10.5 FPS
Raspberry pi: 6.5 FPS



>For TensorFlow mobilenet classifying model (1000 Classes):
ubuntu : 20 FPS
Raspberry pi: 11.5 FPS

