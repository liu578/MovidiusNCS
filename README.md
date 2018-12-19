# MovidiusNCS
Movidius NCS deployment with Caffe and TensorFlow models

The MobileNet model is specially designed for mobile devices like smart phones and embedded systems
I can get MobileNet running at 6.5 FPS in raspberry pi, while yolo can only run at 2 fps. MobileNet is pretty good considering raspberry hardware.

The general idea has two steps.
1. compile the pre-trained TensorFlow models or Caffe models into a graph file for Neural Stick
2. write a python script to run the model and do the prediction
3. set up a local server to reply HTTP request with JSON as inference result

The input and output of the graph file is same as the original model

For Caffe Models: ssd_mobilenet
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


TensorFlow Models: mobilenet
compile:
mvNCCompile -s 12 mobilenet_v1_1.0_224_frozen.pb  -in=input -on=MobilenetV1/Predictions/Reshape_1

output[i] : prediction confidence for class i


Result:

For Caffe ssd_mobilenet detection model (20 Classes):
ubuntu : 10.5 FPS
pi: 6.5 FPS

For TensorFlow mobilenet classifying model (20 Classes):
ubuntu : 20 FPS
pi: 11.5 FPS

