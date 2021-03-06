from mvnc import mvncapi as mvnc
import numpy as np
import cv2
import time
GRAPH = 'graph_caffe'
IMAGE = 'images/000456.jpg'
CLASSES = ('background','aeroplane', 'bicycle', 'bird', 'boat',
           'bottle', 'bus', 'car', 'cat', 'chair',
           'cow', 'diningtable', 'dog', 'horse',
           'motorbike', 'person', 'pottedplant',
           'sheep', 'sofa', 'train', 'tvmonitor')



input_size = (300,300)
np.random.seed(3)
colors = 255 * np.random.rand(len(CLASSES),3)

#discover our device 
devices = mvnc.EnumerateDevices()
# print(len(devices),devices)
device = mvnc.Device(devices[0])
device.OpenDevice()


#load graph onto the device
with open(GRAPH,'rb')as f:
    graph_file = f.read()
graph = device.AllocateGraph(graph_file)


#image preprocessing
def preprocess(src):
    img = cv2.resize(src, input_size)
    img = img - 127.5
    img = img * 0.007843
    return img.astype(np.float16)

#graph => load the iamge to it,return a prediction
capture = cv2.VideoCapture(0)
_,image = capture.read()
width, height = int(capture.get(3)), int(capture.get(4))
# print(height,width)
# h_factor = height/input_size[0]
# w_factor = width/input_size[1]

while True:
    stime = time.time()
    _,image = capture.read()
    image_pro = preprocess(image)
    #print(image_pro.shape[:2])
    graph.LoadTensor(image_pro,None)
    output,_ = graph.GetResult()

    valid_boxes = int(output[0])
    # output
    for i in range(7,7*(1+valid_boxes),7):
        if not np.isfinite(sum(output[i+1:i+7])):
            continue
        clss = CLASSES[int(output[i+1])]
        conf = output[i+2]
        color = colors[int(output[i+1])]
        x1 = max(0,int(output[i+3] * width))
        y1 = max(0,int(output[i+4] * height))
        x2 = min(width,int(output[i+5] * width))
        y2 = min(height,int(output[i+6] * height))

        label = '{}:{:.0f}%'.format(clss,conf*100)
        image = cv2.rectangle(image,(x1,y1),(x2,y2),color,2)
        y = y1 - 5 if y1 - 15 > 15else y1 + 18
        image = cv2.putText(image,label,(x1-5,y),cv2.FONT_HERSHEY_SIMPLEX,0.8,color,2)
#         print(clss,conf)
    lebelfps = 'FPS: {:.1f}'.format(1/(time.time()- stime))
    image = cv2.putText(image,lebelfps,(0,470),cv2.FONT_HERSHEY_SIMPLEX,0.8,colors[-2],2)   
    cv2.imshow('frame',image)
    if cv2.waitKey(1)&0xff == ord('q'):
        break
capture.release()
cv2.destroyAllWindows()
device.CloseDevice()
    

