import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from mecab import MeCab
from gluonnlp import Vocab
from typing import Tuple


class PreProcessor:
    """PreProcessor class"""
    def __init__(self, vocab: Vocab, tokenizer: MeCab, pad_idx: int = 0, pad_length: int = 70) -> None:
        """Instantiating PreProcessor class

        Args:
            vocab (gluonnlp.Vocab): the instance of gluonnlp.Vocab
            tokenizer (mecab.Mecab): the instance of mecab.Mecab
            pad_idx (int): the idx of padding token. Default: 0
            pad_length (int): padding length. Default: 70
        """
        self._vocab = vocab
        self._tokenizer = tokenizer
        self._pad_idx = pad_idx
        self._pad_length = pad_length

    def convert2idx(self, record: tf.Tensor) -> Tuple[tf.Tensor, tf.Tensor]:
        data, label = tf.io.decode_csv(record, record_defaults=[[''], [0]], field_delim='\t')
        data = [self._tokenizer.morphs(sen.numpy().decode('utf-8')) for sen in data]
        data = [[self._vocab.token_to_idx[token] for token in sen] for sen in data]
        data = pad_sequences(data, maxlen=self._pad_length, value=self._pad_idx,
                             padding='post', truncating='post')
        data = tf.convert_to_tensor(data, dtype=tf.int32)
        label = tf.reshape(label, (record.get_shape()[0], ))
        return data, label