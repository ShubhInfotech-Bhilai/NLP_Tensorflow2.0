import tensorflow as tf
import keras
from keras import layers
from model.ops import MultiChannelEmbedding, ConvolutionLayer, MaxPooling
from gluonnlp import Vocab


class SenCNN(keras.Model):
    def __init__(self, num_classes: int, vocab: Vocab) -> None:
        super(SenCNN, self).__init__()
        self._embedding = MultiChannelEmbedding(vocab)
        self._convolution = ConvolutionLayer(300)
        self._pooling = MaxPooling()
        self._dropout = layers.Dropout(0.5)
        self._fc = layers.Dense(units=num_classes)

    def call(self, x: tf.Tensor) -> tf.Tensor:
        fmap = self._embedding(x)
        fmap = self._convolution(fmap)
        feature = self._pooling(fmap)
        score = self._fc(feature)
        return score