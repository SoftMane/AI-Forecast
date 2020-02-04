
import tensorflow as tf
import numpy as np
# tf.enable_eager_execution()
# create TensorFlow variables
const = tf.Variable(2.0, name="const")
#b = tf.Variable(2.0, name='b')
b = tf.Variable(np.arange(0,10), name='b')
c = tf.Variable(1.0, name='c')
# now create some operations
#d = tf.add(b, c, name='d')
d = tf.cast(b, tf.float32) + c
e = tf.add(c, const, name='e')
a = tf.multiply(d, e, name='a')
print(f"Variable a is {a.numpy()}")