import unittest

import numpy as np
import pandas as pd

from ai4water import Model
from ai4water.datasets import busan_beach, MtropicsLaos
from ai4water.models import MLP, LSTM, CNN, CNNLSTM, LSTMAutoEncoder
from sklearn.datasets import make_classification


data = busan_beach()
input_features = data.columns.tolist()[0:-1]
output_features = data.columns.tolist()[-1:]

laos = MtropicsLaos()
cls_data = laos.make_classification(lookback_steps=1)
input_features_cls = cls_data.columns.tolist()[0:-1]
output_features_cls = cls_data.columns.tolist()[-1:]

multi_cls_inp = [f'data_{i}' for i in range(10)]
multi_cls_out = ['outputs']
X, y = make_classification(n_classes=4,
                           n_features=len(multi_cls_inp),
                           n_informative=len(multi_cls_inp),
                           n_redundant=0,
                           n_repeated=0)
y = y.reshape(-1, 1)

multi_cls_data = pd.DataFrame(np.concatenate([X, y], axis=1), columns=multi_cls_inp + multi_cls_out)

class TestModels(unittest.TestCase):

    def test_mlp(self):
        model = Model(model=MLP(32),
                      input_features=input_features,
                      output_features=output_features,
                      epochs=1,
                      verbosity=0
                      )
        assert model.category == "DL"
        return

    def test_lstm(self):
        model = Model(model=LSTM(32),
                      input_features=input_features,
                      output_features=output_features,
                      ts_args={'lookback': 5},
                      verbosity=0)
        assert model.category == "DL"
        return

    def test_cnn(self):
        model = Model(model=CNN(32, 2),
                      input_features=input_features,
                      output_features=output_features,
                      ts_args={'lookback': 5},
                      verbosity=0)
        assert model.category == "DL"
        return

    def test_cnnlstm(self):
        model = Model(model=CNNLSTM(input_shape=(9, 13), sub_sequences=3),
                      input_features=input_features,
                      output_features=output_features,
                      ts_args={'lookback': 9},
                      verbosity=0)
        assert model.category == "DL"
        return

    def test_mlp_for_cls_binary(self):
        model = Model(model=MLP(32,
                                mode="classification",
                                output_features=2),
                      input_features=input_features_cls,
                      output_features=output_features_cls,
                      epochs=2,
                      loss="binary_crossentropy",
                      verbosity=0
                      )
        model.fit(data=cls_data)
        return

    def test_mlp_for_cls_binary_softmax(self):
        model = Model(model=MLP(32,
                                mode="classification",
                                output_features=2,
                                output_activation="softmax",
                                ),
                      input_features=input_features_cls,
                      output_features=output_features_cls,
                      epochs=2,
                      loss="binary_crossentropy",
                      verbosity=0
                      )

        model.fit(data=cls_data)
        return

    def test_mlp_for_cls_multicls(self):
        model = Model(model=MLP(32, mode="classification",
                                output_features=4),
                      input_features=multi_cls_inp,
                      output_features=multi_cls_out,
                      epochs=2,
                      loss="categorical_crossentropy",
                      verbosity=0,
                      )
        model.fit(data=multi_cls_data)
        return

if __name__ == "__main__":
    unittest.main()
