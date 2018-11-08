import tensorflow as tf
import gzip
import pickle
import numpy as np
import matplotlib.pyplot as plt

with gzip.open ( '../../../mnist.pkl.gz', 'rb') as f:
    ((traind, trainl), (vald, vall), (testd, testl)) = pickle.load(f, encoding='bytes')
    traind = traind.astype('float32').reshape(-1, 28, 28)
    trainl = trainl.astype('float32')
    testd = testd.astype('float32').reshape(-1,28,28)
    testl = testl.astype('float32')   

def q_a():
    d_input = tf.placeholder(tf.float32, shape=[None, 28, 28])
    l_input = tf.placeholder(tf.float32, shape=[None, 10])
    data1k = d_input[999, :, :]
    label1k = l_input[999, :]
    min_val = tf.reduce_min(data1k)
    max_val = tf.reduce_max(data1k)
    with tf.Session() as sess:
        fdict = { d_input : traind, l_input : trainl }
        d1k, l1k, min_label, max_label = sess.run([data1k, label1k, min_val, max_val], feed_dict = fdict)
        print("Image label is ", l1k.argmax())
        imgplot = plt.imshow(d1k, cmap='gray')
        plt.show()
        print (min_label, max_label)

def q_b():
    l_input = tf.placeholder(tf.float32, shape=[None, 10])
    min_val = tf.reduce_min(tf.argmin(l_input, axis=1))
    max_val = tf.reduce_max(tf.argmax(l_input, axis=1))
    with tf.Session() as sess:
        fdict = {l_input : trainl}
        min_l, max_l = sess.run([min_val, max_val], feed_dict = fdict)
        print("Min label", min_l, "Max label", max_l)

def q_c():
    l_input = tf.placeholder(tf.float32, shape=[None, 10])
    count_nine = tf.reduce_sum(l_input, axis=0)[9]

    with tf.Session() as sess:
        fdict = {l_input : trainl}
        count = sess.run([count_nine], feed_dict = fdict)
        print("Lable 9 count", count)


def q_d():
    d_input = tf.placeholder(tf.float32, shape=[None, 28, 28])
    data = d_input[9, :, :]
    min_val = tf.reduce_min(data)
    max_val = tf.reduce_max(data)
    with tf.Session() as sess:
        fdict = { d_input : traind }
        min_v, max_v = sess.run([min_val, max_val], feed_dict = fdict)
        print (min_v, max_v)

def q_e():
    d_input = tf.placeholder(tf.float32, shape=[None, 28, 28])
    sample = d_input[9, :, :]
    every2ndC = sample[..., 0::2]
    every2ndR = sample[0::2, ...]
    inv =  sample[::-1, ::-1]
    invEvery2nd = (sample[::-1, ::-1])[0::2, 0::2]
    with tf.Session() as sess:
        fdict = { d_input : traind }
        a,b,c,d,e, = sess.run([sample, every2ndC, every2ndR, inv, invEvery2nd], feed_dict = fdict)
        print(a,b,c,d,e)

def q_f():
    d_input = tf.placeholder(tf.float32, shape=[None, 28, 28])
    l_input = tf.placeholder(tf.float32, shape=[None, 10])
    class_mask = tf.equal(tf.argmax(l_input, axis=1), 4)
    only_fours = tf.boolean_mask(d_input, class_mask)
    with tf.Session() as sess:
        fdict = { d_input : traind, l_input : trainl }
        o4 = sess.run(only_fours, feed_dict = fdict)
        print(o4.shape)

def q_g():
    d_input = tf.placeholder(tf.float32, shape=[None, 28, 28])
    l_input = tf.placeholder(tf.float32, shape=[None, 10])
    four_mask = tf.equal(tf.argmax(l_input, axis=1), 4)
    nine_mask = tf.equal(tf.argmax(l_input, axis=1), 9)
    class_mask = tf.logical_or(four_mask, nine_mask)
    foursnines = tf.boolean_mask(d_input, class_mask)
    foursnines_l = tf.boolean_mask(l_input, class_mask)
    with tf.Session() as sess:
        fdict = { d_input : traind, l_input : trainl }
        o49, o49_l = sess.run([foursnines, foursnines_l], feed_dict = fdict)
        print(o49.shape, o49_l.shape)
        imgplot = plt.imshow(o49[10], cmap='gray')
        plt.show()

def q_h():
    d_input = tf.placeholder(tf.float32, shape=[None, 28, 28])
    l_input = tf.placeholder(tf.float32, shape=[None, 10])
    first10k = d_input[0:1000, :, :]
    first10k_l = d_input[0:1000, :]
    with tf.Session() as sess:
        fdict = { d_input : traind, l_input : trainl }
        a,b = sess.run([first10k, first10k_l], feed_dict = fdict)

def q_i():
    d_input = tf.placeholder(tf.float32, shape=[None, 28, 28])
    random1k = tf.random.shuffle(d_input)[0:1000]
    with tf.Session() as sess:
        fdict = { d_input : traind }
        a = sess.run(random1k, feed_dict = fdict)
        imgplot = plt.imshow(a[0], cmap='gray')
        plt.show()


q_i();