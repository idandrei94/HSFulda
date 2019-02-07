import tensorflow as tf
import gzip
import pickle
import numpy as np
import matplotlib.pyplot as plt

with gzip.open ( '../../../mnist.pkl.gz', 'rb') as f:
    ((traind, trainl), (vald, vall), (testd, testl)) = pickle.load(f, encoding='bytes')
    trainl = trainl.astype('float32')
    testl = testl.astype('float32')   

def q_a():
    d_input = tf.placeholder(tf.float32)

    # a). reshape
    d_input_reshaped = tf.reshape(d_input, [-1, 28, 28])

    # b). mean across all pixels
    sum = tf.reduce_sum(d_input_reshaped, 0)
    mean_image = tf.math.divide(sum, d_input.length)




    