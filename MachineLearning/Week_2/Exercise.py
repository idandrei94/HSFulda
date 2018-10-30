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

# there are 60000 samples, each sample has 28x28 numbers
print(traind.shape)
# the classes use one_hot encoding, one value for each class type, one is high, the others are low
print(trainl.shape)

# the class is 0
img = traind[1000]
print(img.shape)
imgplot = plt.imshow(img, cmap='gray')
plt.show()

# c
print("Max class is",  max(map(lambda x: x.argmax(), trainl)) )
print("Min class is",  min(map(lambda x: x.argmax(), trainl)) )
# d
print("Count of class 5 is",  sum(map(lambda x: 1 if x.argmax()==5 else 0, trainl)) )

#e
sample = traind[10]
print("10th sample max pixel", max(sample.reshape(-1)))
print("10th sample min pixel", min(sample.reshape(-1)))

#f
print("Every second collumn ", sample[..., 0::2])
print("Every second row ", sample[0::2, ...])
print("Inverted ", sample[::-1, ::-1])

print("10 top rows set to 0", list(map(lambda x: np.array([0,0,0]), sample[0:10, ...])))
print("10 top rows set to 0", list(map(lambda x: np.array([0,0,0]), sample[17:27:-1, ...])))
print("invert and every second", (sample[::-1, ::-1])[0::2, 0::2]  )