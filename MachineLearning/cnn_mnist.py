import matplotlib as mp;
import gzip, pickle,numpy as np, matplotlib.pyplot as plt;
import numpy.random as npr, tensorflow as tf, sys;
from matplotlib.widgets import Button;
import math;

mnistPath = "../../mnist.pkl.gz"
sess = tf.Session()

# expects 1D array
def sm(arr):
  num = np.exp(arr) 
  den = num.sum() 
  return num/den 

with gzip.open(mnistPath, 'rb') as f:
    # python3
    #((traind,trainl),(vald,vall),(testd,testl))=pickle.load(f, encoding='bytes')
    # python2
    ((traind,trainl),(vald,vall),(testd,testl))=pickle.load(f, encoding="bytes") 
    traind = traind.astype("float32").reshape(-1,784) 
    trainl = trainl.astype("float32") 
    testd = testd.astype("float32").reshape(-1,784) 
    testl = testl.astype("float32") 
data_placeholder = tf.placeholder(tf.float32,[None,784]) 
label_placeholder = tf.placeholder(tf.float32,[None,10]) 

N = 10000
fd = {data_placeholder: traind[0:N], label_placeholder : trainl[0:N] }

## reshape data tensor into NHWC format
dataReshaped=tf.reshape(data_placeholder, (-1,28,28,1)) 
print (dataReshaped) 

## Hidden Layer 1
# Convolution Layer with 32 fiters and a kernel size of 5
conv1 = tf.nn.relu(tf.layers.conv2d(dataReshaped,32, 5,name="H1")) 
print (conv1) 
# Max Pooling (down-sampling) with strides of 2 and kernel size of 2
a1 = tf.layers.max_pooling2d(conv1, 2, 2) 
print (a1) 

## Hidden Layer 2
# Convolution Layer with 64 filters and a kernel size of 3
conv2 = tf.nn.relu(tf.layers.conv2d(a1, 64, 3,name="H2")) 
# Max Pooling (down-sampling) with strides of 2 and kernel size of 2
a2 = tf.layers.max_pooling2d(conv2, 2, 2) 
print (a2) 
a2flat = tf.reshape(a2, (-1,5*5*64)) 

## Hidden Layer 3
Z3 = 1000 
# allocate variables
W3 = tf.Variable(npr.uniform(-0.01,0.01, [5*5*64,Z3]),dtype=tf.float32, name ="W3") 
b3 = tf.Variable(npr.uniform(-0.01,0.01, [1,Z3]),dtype=tf.float32, name ="b3")
# compute activations
a3 = tf.nn.relu(tf.matmul(a2flat, W3) + b3) 
print (a3) 

## output layer
# alloc variables
W4 = tf.Variable(npr.uniform(-0.1,0.1, [Z3,10]),dtype=tf.float32, name ="W4") 
b4 = tf.Variable(npr.uniform(-0.01,0.01, [1,10]),dtype=tf.float32, name ="b4") 
# compute activations
logits = tf.matmul(a3, W4) + b4 
print (logits) 

## loss
lossBySample = tf.nn.softmax_cross_entropy_with_logits_v2(logits=logits, labels=label_placeholder) 
loss = tf.reduce_mean(lossBySample) 

## classification accuracy
nrCorrect = tf.reduce_mean(tf.cast(tf.equal (tf.argmax(logits,axis=1), tf.argmax(label_placeholder,axis=1)), tf.float32)) 

## create update op
optimizer = tf.train.GradientDescentOptimizer(learning_rate = 0.00001)  # 0.00001
update = optimizer.minimize(loss) 

## init all variables
sess.run(tf.global_variables_initializer()) 

## learn!!
iteration = 0 
tMax = 100
for iteration in range(0,tMax):
  # update parameters
  sess.run(update, feed_dict = fd)
  correct, lossVal= sess.run([nrCorrect, loss], feed_dict = fd)
  testacc = sess.run(nrCorrect, feed_dict = {data_placeholder: testd, label_placeholder: testl})
  print ("epoch ", iteration, "acc=", float(correct), "loss=", lossVal, "testacc=",testacc)



## visualize result on test data
testout = sess.run(logits, feed_dict = {data_placeholder : testd})

testit = 0

def test_cb(self):
  global testit 
  ax1.cla()
  ax2.cla()
  ax3.cla()
  ax1.imshow(testd[testit].reshape(28,28),cmap=plt.get_cmap("bone"))
  confs = sm(testout[testit])
  ax2.bar(range(0,10),confs)
  ax2.set_ylim(0,1.)
  ce = -(confs*np.log(confs+0.00000001)).sum()
  ax3.text(0.5,0.5,str(ce),fontsize=20)
  testit = testit + 1
  f.canvas.draw()
  print ("--------------------") 
  print("logits", testout[testit], "probabilities", sm(testout[testit]), "decision", testout[testit].argmax(), "label", testl[testit].argmax())

f,(ax1,ax2,ax3) = plt.subplots(nrows=1,ncols=3) 
f.canvas.mpl_connect('button_press_event', test_cb)
plt.show()
#ax = f.gca() ;