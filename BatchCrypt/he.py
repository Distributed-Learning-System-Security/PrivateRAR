import time
import tensorflow as tf
from tensorflow import keras
import numpy as np
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import pysnooper
import argparse
from functools import reduce
import random
from encryption import paillier, encryption
from joblib import Parallel, delayed

def clip_gradients(grads, min_v, max_v):
    results = [tf.clip_by_value(t, min_v, max_v) for t in grads]
    return results
tf.enable_eager_execution(
    config=None,
    device_policy=None,
    execution_mode=None
)
clip = 0.5
num_clients = 2
q_width = 16

publickey, privatekey = paillier.PaillierKeypair.generate_keypair(n_length=2048)

len_x = 1605632
grads_0 = list(np.random.rand(1,len_x))
grads_1 = list(np.random.rand(1,len_x))
# print(grads_0)
# print(grads_1)
# party A
grads_0 = clip_gradients(grads_0, -1 * clip / num_clients, clip / num_clients)
# party B
grads_1 = clip_gradients(grads_1, -1 * clip / num_clients, clip / num_clients)

# grads_batch_clients = [clip_gradients(item, -1 * clip / num_clients, clip / num_clients) 
#                         for item in  grads_batch_clients]

# party A
enc_grads_0 = []
enc_grads_shape_0 = []
count = 0
print(grads_0)
for i in range(5):
    begin = time.time()
    #for component in grads_0:
    enc_g, enc_g_s = encryption.encrypt_matrix_batch(publickey, np.array(grads_0),
                                                    bit_width=q_width, r_max=clip)
    enc_grads_0.append(enc_g)
    enc_grads_shape_0.append(enc_g_s)
    end = time.time()
    print("time:",end-begin)
#loss_value_0 = encryption.encrypt(publickey, loss_value_0)
# party B
enc_grads_1 = []
enc_grads_shape_1 = []
for component in grads_1:
    enc_g, enc_g_s = encryption.encrypt_matrix_batch(publickey, component.numpy(),
                                                     bit_width=q_width, r_max=clip)
    enc_grads_1.append(enc_g)
    enc_grads_shape_1.append(enc_g_s)
#loss_value_1 = encryption.encrypt(publickey, loss_value_1)

def do_sum(x1, x2):
    results = []
    for i in range(len(x1)):
        results.append(x1[i] + x2[i])
    return results


def aggregate_gradients(gradient_list):
    results = reduce(do_sum, gradient_list)
    return results

#arbiter aggregate gradients
enc_grads = aggregate_gradients([enc_grads_0, enc_grads_1])
#loss_value = aggregate_losses([loss_value_0, loss_value_1])

# 密文梯度累加
#enc_grads = aggregate_gradients(enc_grads_batch_clients)
#client_weight = 1.0 / num_clients
# loss 值累加
#loss_value = aggregate_losses([item * client_weight for item in loss_batch_clients])

# on party A and B individually
#loss_value = encryption.decrypt(privatekey, loss_value)
grads = []
for i in range(len(enc_grads)):
    plain_g = encryption.decrypt_matrix_batch(privatekey, enc_grads_0[i], enc_grads_shape_0[i])
    #plain_g = encryption.decrypt_matrix_batch(privatekey, enc_grads[i], enc_grads_shape_batch_clients[0][i])
    grads.append(plain_g)


