import tensorflow as tf
from  tensorflow.io import gfile
LOG_DIR = 'logs'  # The path where you want to save tensorboard events

with tf.Session() as sess:
    model_filename = 'model.pb' # your model path
    with gfile.FastGFile(model_filename, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        g_in = tf.import_graph_def(graph_def)
train_writer = tf.summary.FileWriter(LOG_DIR)
train_writer.add_graph(sess.graph)