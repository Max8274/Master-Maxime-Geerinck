#!/usr/bin/env python3
from __future__ import absolute_import, division, print_function
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

import glob
#os.environ['CUDA_VISIBLE_DEVICES'] = '0'
import numpy as np
import fid
from imageio.v2 import imread
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()

##############################################################################################################################################
# [164.44917328647693, 134.59271128942876, 116.18560500937578, 127.46514762471266, 114.66565998755848, 109.55915669904897, 106.44690526433922]
# 130.17559950401025
##############################################################################################################################################

# Paths
image_path = '//composites/greenrace'  # set path to some generated images
stats_path = '//validation/TTUR/fid_stats.npz'  # training set statistics
inception_path = fid.check_or_download_inception(None) # download inception network

# loads all images into memory (this might require a lot of RAM!)
image_list = glob.glob(os.path.join(image_path, '*.png'))
images = np.array([imread(str(fn)).astype(np.float32) for fn in image_list])

# load precalculated training set statistics
f = np.load(stats_path)
mu_real, sigma_real = f['mu'][:], f['sigma'][:]
f.close()

fid.create_inception_graph(inception_path)  # load the graph into the current TF graph
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    mu_gen, sigma_gen = fid.calculate_activation_statistics(images, sess, batch_size=100)

fid_value = fid.calculate_frechet_distance(mu_gen, sigma_gen, mu_real, sigma_real)
print("FID: %s" % fid_value)
