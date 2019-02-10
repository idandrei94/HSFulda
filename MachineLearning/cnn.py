"""
Machine learning demo in tensorflow, by Alex Gepperth.
!! In this version, this needs to executed with Python2 !!
** Has been tested on LinuxLab machines **
This program supports the following command line parameters:
linreg - simple lineaer regression demo in 2D
linclass - linear softmax MC on MNIST
linreg_mnist - linear regression on MNIST
deepclass - deep softmax MC on MNIST
cnn - deep convolutionla network on MNIST
cnnFilters - like cnn but visulizing the filters
cosmodel - eexperimental, ignore

The path/location of the MNIST data needs to be adapted here:
"""
mnistPath = "../../mnist.pkl.gz"

import matplotlib as mp ;
import gzip, pickle,numpy as np, matplotlib.pyplot as plt ;
import numpy.random as npr, tensorflow as tf, sys  ;
from matplotlib.widgets import Button ;
import math ;

# expects 1D array
def sm(arr):
  num = np.exp(arr) ;
  den = num.sum() ;
  return num/den ;



sess = tf.Session();

# ----------------------------------------------------------------
if sys.argv[1] == "cosmodel":

  deg = 60 ;
  N = 100 ;
  xdata = tf.Variable(tf.random_uniform([N,1],0,10),dtype=tf.float32) ;
  ydata = tf.Variable(1.5*xdata[:,0] + 1 + tf.random_uniform([N],-0.1,0.1),dtype=tf.float32) ;

  a = tf.Variable(np.zeros([1,deg]), dtype=tf.float32) ;
  b = tf.Variable(np.zeros([1,deg]), dtype=tf.float32) ;
  d= tf.Variable(0.0, dtype=tf.float32) ;
  sess.run(tf.global_variables_initializer()) ;



  # loss function MSE
  frq = tf.expand_dims(tf.range(0,deg,dtype=tf.float32)*2.*3.14159265, 0) ;
  print(frq);
  modelOutput = tf.reduce_sum(tf.cos(frq*xdata)*a+tf.sin(frq*xdata)*b,axis=1)+d ;
  print (modelOutput);
  mseLoss = tf.reduce_mean((modelOutput- ydata)**2) ;

  # tf optimization ops
  optimizer = tf.train.GradientDescentOptimizer(learning_rate = 0.1) ;
  update = optimizer.minimize(mseLoss, var_list = [a,d]) ;

  # gradeint descent

  iteration=0 ;

  def linreg_cb(self):
    global iteration, update ;
    _ = sess.run(update) ;
    lossVal,_a,_d = sess.run([mseLoss, a,d]) ;
    print ("epoch ", iteration, "loss=", lossVal, _a,_d) ;
    y_opt = sess.run(modelOutput)

    ax.cla();
    ax.scatter(sess.run(xdata), sess.run(ydata)) ;
    ax.scatter(sess.run(xdata),(y_opt)) ;
    f.canvas.draw();
    iteration += 1 ;

  # plot data
  f = plt.figure() ; ax = f.gca()
  _xdata = sess.run(xdata) ;
  print (_xdata.shape, ydata);
  ax.scatter(_xdata, sess.run(ydata)) ;
  f.canvas.mpl_connect('button_press_event', linreg_cb)
  f.show();
  plt.show() ;

# ----------------------------------------------------------------

if sys.argv[1] == "linreg":

  N = 100 ;
  xdata = tf.Variable(tf.random_uniform([N],0,1),dtype=tf.float32) ;
  ydata = tf.Variable(1.5*xdata + 1 + tf.random_uniform([N],-0.1,0.1),dtype=tf.float32) ;

  a = tf.Variable(0.0, dtype=tf.float32) ;
  d= tf.Variable(0.0, dtype=tf.float32) ;
  sess.run(tf.global_variables_initializer()) ;



  # loss function MSE
  mseLoss = tf.reduce_mean(((a*xdata + d)- ydata)**2) ;

  # tf optimization ops
  optimizer = tf.train.GradientDescentOptimizer(learning_rate = 0.1) ;
  update = optimizer.minimize(mseLoss, var_list = [a,d]) ;

  # gradeint descent

  iteration=0 ;

  def linreg_cb(self):
    global iteration, update ;
    _ = sess.run(update) ;
    lossVal,_a,_d = sess.run([mseLoss, a,d]) ;
    print ("epoch ", iteration, "loss=", lossVal, _a,_d) ;
    y_opt = xdata * a + d ;
    ax.cla();
    ax.scatter(sess.run(xdata), sess.run(ydata)) ;
    ax.scatter(sess.run(xdata),sess.run(y_opt)) ;
    f.canvas.draw();
    iteration += 1 ;

  # plot data
  f = plt.figure() ; ax = f.gca()
  ax.scatter(sess.run(xdata), sess.run(ydata)) ;
  f.canvas.mpl_connect('button_press_event', linreg_cb)
  f.show();
  plt.show() ;

# ----------------------------------------------------------------

if sys.argv[1] == "linclass":


  with gzip.open(mnistPath, 'rb') as f:
    # python3
    ((traind,trainl),(vald,vall),(testd,testl))=pickle.load(f, encoding='bytes')
    # python2
    #((traind,trainl),(vald,vall),(testd,testl))=pickle.load(f) ;
    traind = traind.astype("float32").reshape(-1,28,28) ;
    trainl = trainl.astype("float32") ;
    testd = testd.astype("float32").reshape(-1,28,28) ;
    testl = testl.astype("float32") ;
  _traind = tf.placeholder(tf.float32,[None,28,28]) ;
  _trainl = tf.placeholder(tf.float32,[None,10]) ;

  fd = {_traind: traind, _trainl : trainl } ;
  #fd = {}


  W = tf.Variable(np.zeros([784,10]),dtype=tf.float32, name ="W") ;
  b = tf.Variable(np.zeros([1,10]),dtype=tf.float32, name ="W") ;


  sess.run(tf.global_variables_initializer()) ;
  logits = tf.matmul(tf.reshape(_traind, shape=(-1, 784)), W) + b;

  loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(logits=logits, labels=_trainl)) ;

  # classification accuracy
  nrCorrect = tf.reduce_mean(tf.cast(tf.equal (tf.argmax(logits,axis=1), tf.argmax(_trainl,axis=1)), tf.float32)) ;

  optimizer = tf.train.GradientDescentOptimizer(learning_rate = 0.1) ;
  update = optimizer.minimize(loss, var_list = [W,b]) ;

  iteration = 0 ;

  for iteration in range(0,30):

    sess.run(update, feed_dict = fd) ;
    correct, lossVal = sess.run([nrCorrect, loss], feed_dict = fd) ;
    print ("epoch ", iteration, "acc=", float(correct), "loss=", lossVal) ;


  testout = sess.run(logits, feed_dict = {_traind : testd}) ;

  testit = 0 ;

  def test_cb(self):
    global testit ;
    ax1.cla();
    ax2.cla();
    ax3.cla();
    ax1.imshow(testd[testit],cmap=plt.get_cmap("bone")) ;
    confs =sm(testout[testit]) ;
    ax2.bar(range(0,10),confs);
    ax2.set_ylim(0,1.)
    ce = -(confs*np.log(confs+0.00000001)).sum() ;
    ax3.text(0.5,0.5,str(ce),fontsize=20)
    testit = testit + 1;
    f.canvas.draw();
    print ("--------------------") ;
    print("logits", testout[testit], "probabilities", sm(testout[testit]), "decision", testout[testit].argmax(), "label", testl[testit].argmax()) ;

  f,(ax1,ax2,ax3) = plt.subplots(nrows=1,ncols=3) ;
  f.canvas.mpl_connect('button_press_event', test_cb)
  plt.show();
  #ax = f.gca() ;

# ----------------------------------------------------------------

  
if sys.argv[1] == "linreg_mnist":


  with gzip.open(mnistPath, 'rb') as f:
    # python3
    #((traind,trainl),(vald,vall),(testd,testl))=pickle.load(f, encoding='bytes')
    # python2
    ((traind,trainl),(vald,vall),(testd,testl))=pickle.load(f) ;
    traind = traind.astype("float32").reshape(-1,28,28) ;
    trainl = trainl.astype("float32") ;
    testd = testd.astype("float32").reshape(-1,28,28) ;
    testl = testl.astype("float32") ;
  tf_traind = tf.placeholder(tf.float32,[None,28,28]) ;
  tf_trainl = tf.placeholder(tf.float32,[None,10]) ;

  fd = {tf_traind: traind, tf_trainl : trainl } ;
  #fd = {}


  W = tf.Variable(np.zeros([1,784]),dtype=tf.float32, name ="W") ;
  b = tf.Variable(np.zeros([1]),dtype=tf.float32, name ="b") ;
  sess.run(tf.global_variables_initializer()) ;
  logit = tf.reduce_sum(W*tf.reshape(tf_traind,(-1,784)),axis=1) + b;
  num_labels = tf.cast(tf.argmax(tf_trainl,axis=1),tf.float32);
  print (num_labels);
  print (logit);
  loss = tf.reduce_mean(   (logit-num_labels)**2   ) ;
  print (loss);

  print ("DEFINED") ;
  #print ("logits loss shape is ", sess.run([tf.shape(logits), tf.shape(loss)], feed_dict = fd)) ;

  # classification accuracy
  #nrCorrect = tf.reduce_mean(tf.cast(tf.equal (tf.argmax(logits,axis=1), tf.argmax(_trainl,axis=1)), tf.float32)) ;

  optimizer = tf.train.GradientDescentOptimizer(learning_rate = 0.01) ;
  update = optimizer.minimize(loss, var_list = [W,b]) ;

  iteration = 0 ;
  print ("START") ;

  for iteration in range(0,70):

    _ = sess.run(update, feed_dict = fd) ;
    lossVal = sess.run(loss, feed_dict = fd) ;
    print ("epoch ", iteration, "acc=", float(lossVal), "loss=", lossVal) ;


  testout = sess.run(logit, feed_dict = {tf_traind : testd}) ;

  testit = 0 ;

  def test_cb(self):
    global testit ;
    ax1.cla();
    ax2.cla();
    ax3.cla();
    ax1.imshow(testd[testit]) ;
    logit =testout[testit] ;
    ax2.text(0.5,0.5, str(logit),fontsize=20) ;
    ax2.set_ylim(0,1.)
    mse = math.sqrt((logit-testl[testit].argmax())**2) ;
    ax3.text(0.5,0.5,str(mse),fontsize=20)
    testit = testit + 1;
    f.canvas.draw();
    print ("--------------------") ;
    print("logits", testout[testit], "probabilities", sm(testout[testit]), "decision", testout[testit].argmax(), "label", testl[testit].argmax()) ;

  f,(ax1,ax2,ax3) = plt.subplots(nrows=1,ncols=3) ;
  f.canvas.mpl_connect('button_press_event', test_cb)
  plt.show();
  #ax = f.gca() ;

# ----------------------------------------------------------------
  
if sys.argv[1] == "deepclass":


  with gzip.open(mnistPath, 'rb') as f:
    # python3
    ((traind,trainl),(vald,vall),(testd,testl))=pickle.load(f, encoding='bytes')
    # python2
    #((traind,trainl),(vald,vall),(testd,testl))=pickle.load(f) ;
    traind = traind.astype("float32") ;
    trainl = trainl.astype("float32") ;
    testd = testd.astype("float32") ;
    testl = testl.astype("float32") ;
  data_placeholder = tf.placeholder(tf.float32,[None,784]) ;
  label_placeholder = tf.placeholder(tf.float32,[None,10]) ;

  fd = {data_placeholder: traind, label_placeholder : trainl } ;
  #fd = {}


  Wh1 = tf.Variable(npr.uniform(-0.01,0.01, [784,100]),dtype=tf.float32, name ="Wh1") ;
  bh1 = tf.Variable(npr.uniform(-0.01,0.01, [1,100]),dtype=tf.float32, name ="bh1") ;
  Wh2 = tf.Variable(npr.uniform(-0.1,0.1, [100,100]),dtype=tf.float32, name ="Wh2") ;
  bh2 = tf.Variable(npr.uniform(-0.01,0.01, [1,100]),dtype=tf.float32, name ="bh2") ;
  W = tf.Variable(npr.uniform(-0.01,0.01, [100,10]),dtype=tf.float32, name ="W") ;
  b = tf.Variable(npr.uniform(-0.01,0.01, [1,10]),dtype=tf.float32, name ="b") ;


  sess.run(tf.global_variables_initializer()) ;
  l1 = tf.nn.relu(tf.matmul(data_placeholder, Wh1) + bh1) ;
  print(l1)
  l2 = tf.nn.relu(tf.matmul(l1, Wh2) + bh2) ;
  print(l2)
  logits = tf.matmul(l2, W)+b;
  print (logits)
  lossBySample = tf.nn.softmax_cross_entropy_with_logits_v2(logits=logits, labels=label_placeholder) ;
  print (lossBySample) ;

  loss = tf.reduce_mean(lossBySample) ;

  # classification accuracy
  nrCorrect = tf.reduce_mean(tf.cast(tf.equal (tf.argmax(logits,axis=1), tf.argmax(label_placeholder,axis=1)), tf.float32)) ;

  optimizer = tf.train.GradientDescentOptimizer(learning_rate = 0.2) ;  # 0.00001
  update = optimizer.minimize(loss) ;

  iteration = 0 ;

  for iteration in range(0,300):

    sess.run(update, feed_dict = fd) ;
    correct, lossVal,_W = sess.run([nrCorrect, loss,W], feed_dict = fd) ;
    print ("epoch ", iteration, "acc=", float(correct), "loss=", lossVal, "wmM=", _W.min(), _W.max()) ;


  testout = sess.run(logits, feed_dict = {data_placeholder : testd}) ;

  testit = 0 ;

  def test_cb(self):
    global testit ;
    ax1.cla();
    ax2.cla();
    ax3.cla();
    ax1.imshow(testd[testit].reshape(28,28)) ;
    confs =sm(testout[testit]) ;
    ax2.bar(range(0,10),confs);
    ax2.set_ylim(0,1.)
    ce = -(confs*np.log(confs+0.00000001)).sum() ;
    ax3.text(0.5,0.5,str(ce),fontsize=20)
    testit = testit + 1;
    f.canvas.draw();
    print ("--------------------") ;
    print("logits", testout[testit], "probabilities", sm(testout[testit]), "decision", testout[testit].argmax(), "label", testl[testit].argmax()) ;

  f,(ax1,ax2,ax3) = plt.subplots(nrows=1,ncols=3) ;
  f.canvas.mpl_connect('button_press_event', test_cb)
  plt.show();
  #ax = f.gca() ;

# ----------------------------------------------------------------

if sys.argv[1] in ["cnnFilters","cnn"] :


  with gzip.open(mnistPath, 'rb') as f:
    # python3
    #((traind,trainl),(vald,vall),(testd,testl))=pickle.load(f, encoding='bytes')
    # python2
    ((traind,trainl),(vald,vall),(testd,testl))=pickle.load(f, encoding="bytes") ;
    traind = traind.astype("float32").reshape(-1,784) ;
    trainl = trainl.astype("float32") ;
    testd = testd.astype("float32").reshape(-1,784) ;
    testl = testl.astype("float32") ;
  data_placeholder = tf.placeholder(tf.float32,[None,784]) ;
  label_placeholder = tf.placeholder(tf.float32,[None,10]) ;

  N = 10000 ;
  fd = {data_placeholder: traind[0:N], label_placeholder : trainl[0:N] } ;

  ## reshape data tensor into NHWC format
  dataReshaped=tf.reshape(data_placeholder, (-1,28,28,1)) ;
  print (dataReshaped) ;

  ## Hidden Layer 1
  # Convolution Layer with 32 fiters and a kernel size of 5
  conv1 = tf.nn.relu(tf.layers.conv2d(dataReshaped,32, 5,name="H1")) ;
  print (conv1) ;
  # Max Pooling (down-sampling) with strides of 2 and kernel size of 2
  a1 = tf.layers.max_pooling2d(conv1, 2, 2) ;
  print (a1) ;

  ## Hidden Layer 2
  # Convolution Layer with 64 filters and a kernel size of 3
  conv2 = tf.nn.relu(tf.layers.conv2d(a1, 64, 3,name="H2")) ;
  # Max Pooling (down-sampling) with strides of 2 and kernel size of 2
  a2 = tf.layers.max_pooling2d(conv2, 2, 2) ;
  print (a2) ;
  a2flat = tf.reshape(a2, (-1,5*5*64)) ;

  ## Hidden Layer 3
  Z3 = 1000 ;
  # allocate variables
  W3 = tf.Variable(npr.uniform(-0.01,0.01, [5*5*64,Z3]),dtype=tf.float32, name ="W3") ;
  b3 = tf.Variable(npr.uniform(-0.01,0.01, [1,Z3]),dtype=tf.float32, name ="b3") ;
  # compute activations
  a3 = tf.nn.relu(tf.matmul(a2flat, W3) + b3) ;
  print (a3) ;

  ## output layer
  # alloc variables
  W4 = tf.Variable(npr.uniform(-0.1,0.1, [Z3,10]),dtype=tf.float32, name ="W4") ;
  b4 = tf.Variable(npr.uniform(-0.01,0.01, [1,10]),dtype=tf.float32, name ="b4") ;
  # compute activations
  logits = tf.matmul(a3, W4) + b4 ;
  print (logits) ;

  ## loss
  lossBySample = tf.nn.softmax_cross_entropy_with_logits_v2(logits=logits, labels=label_placeholder) ;
  loss = tf.reduce_mean(lossBySample) ;

  ## classification accuracy
  nrCorrect = tf.reduce_mean(tf.cast(tf.equal (tf.argmax(logits,axis=1), tf.argmax(label_placeholder,axis=1)), tf.float32)) ;

  ## create update op
  optimizer = tf.train.GradientDescentOptimizer(learning_rate = 0.1) ;  # 0.00001
  update = optimizer.minimize(loss) ;

  ## init all variables
  sess.run(tf.global_variables_initializer()) ;

  ## learn!!
  iteration = 0 ;
  tMax = 10000;
  for iteration in range(0,tMax):
    # update parameters
    sess.run(update, feed_dict = fd) ;
    correct, lossVal= sess.run([nrCorrect, loss], feed_dict = fd) ;
    testacc = sess.run(nrCorrect, feed_dict = {data_placeholder: testd, label_placeholder: testl})
    print ("epoch ", iteration, "acc=", float(correct), "loss=", lossVal, "testacc=",testacc) ;

  if sys.argv[1] == "cnnFilters":
    ## download layer 1 weights
    globVars =  tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)  ;
    filtersH1 = [v for v in globVars if v.name=="H1/kernel:0"] [0] ;
    filtersH1np = sess.run(filtersH1) ;
    print (filtersH1np.min(), filtersH1np.max());

    f,axesplt = plt.subplots(nrows=4,ncols=8) ;
    i = 0 ;
    for ax in axesplt.ravel():
      ax.imshow(filtersH1np[:,:,0,i],cmap=plt.get_cmap("bone"));
      i+=1 ;
    plt.show()


  ## visualize result on test data
  testout = sess.run(logits, feed_dict = {data_placeholder : testd}) ;

  testit = 0 ;

  def test_cb(self):
    global testit ;
    ax1.cla();
    ax2.cla();
    ax3.cla();
    ax1.imshow(testd[testit].reshape(28,28),cmap=plt.get_cmap("bone")) ;
    confs =sm(testout[testit]) ;
    ax2.bar(range(0,10),confs);
    ax2.set_ylim(0,1.)
    ce = -(confs*np.log(confs+0.00000001)).sum() ;
    ax3.text(0.5,0.5,str(ce),fontsize=20)
    testit = testit + 1;
    f.canvas.draw();
    print ("--------------------") ;
    print("logits", testout[testit], "probabilities", sm(testout[testit]), "decision", testout[testit].argmax(), "label", testl[testit].argmax()) ;

  f,(ax1,ax2,ax3) = plt.subplots(nrows=1,ncols=3) ;
  f.canvas.mpl_connect('button_press_event', test_cb)
  plt.show();
  #ax = f.gca() ;