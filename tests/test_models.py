import pandas as pd
import numpy as np

from dl4seq.utils import make_model
from dl4seq.models import Model, InputAttentionModel


def make_and_run(input_model, layers=None, lookback=12, epochs=4, batch_size=16, **kwargs):

    input_features = ['tide_cm', 'wat_temp_c', 'sal_psu', 'air_temp_c', 'pcp_mm', 'pcp3_mm', 'wind_speed_mps',
                      'rel_hum']
    # column in dataframe to bse used as output/target
    outputs = ['blaTEM_coppml']

    data_config, nn_config, total_intervals = make_model(batch_size=batch_size,
                                                         lookback=lookback,
                                                         lr=0.001,
                                                         inputs=input_features,
                                                         outputs = outputs,
                                                         epochs=epochs,
                                                         **kwargs)
    nn_config['layers'] = layers

    df = pd.read_csv('../data/all_data_30min.csv')

    _model = input_model(data_config=data_config,
                  nn_config=nn_config,
                  data=df,
                  intervals=total_intervals
                  )

    _model.build_nn()

    _ = _model.train_nn(indices='random')

    _,  pred_y = _model.predict(use_datetime_index=False)

    return pred_y


lyrs = {"Dense_0": {'config': {'units': 64, 'activation': 'relu'}},
          "Dropout_0": {'config': {'rate': 0.3}},
          "Dense_1": {'config': {'units': 32, 'activation': 'relu'}},
          "Dropout_1": {'config': {'rate': 0.3}},
          "Dense_2": {'config': {'units': 16, 'activation': 'relu'}},
          "Dense_3": {'config': {'units': 1}}
          }

prediction = model = make_and_run(Model, lookback=1, layers=lyrs)
np.testing.assert_almost_equal(float(prediction[0].sum()), 1312.9748, decimal=4)

##
# LSTM based model
lyrs = {"LSTM_0": {'config': {'units': 64, 'return_sequences': True}},
          "LSTM_1": {'config': {'units': 32}},
          "Dropout": {'config': {'rate': 0.3}},
          "Dense": {'config': {'units': 1, 'name': 'output'}}
          }
prediction = make_and_run(Model, lyrs)
np.testing.assert_almost_equal(float(prediction[0].sum()), 1452.8463, decimal=4)

##
# SeqSelfAttention
batch_size=16
lyrs = {
    "Input": {"config": {"batch_shape": (batch_size, 12, 8)}},
    "LSTM_0": {'config': {'units': 64, 'return_sequences': True}},
          "SeqSelfAttention": {"config": {"units": 32, "attention_width": 12, "attention_activation": "sigmoid"}},
          "LSTM_1": {'config': {'units': 32}},
          "Dropout": {'config': {'rate': 0.3}},
          "Dense": {'config': {'units': 1, 'name': 'output'}}
          }

prediction = make_and_run(Model, lyrs, batch_size=batch_size, batches_per_epoch=5)
np.testing.assert_almost_equal(float(prediction[0].sum()), 471.49829, decimal=4)

##
# SeqWeightedAttention
lyrs = {"LSTM_0": {'config': {'units': 64, 'return_sequences': True}},
          "SeqWeightedAttention": {"config": {}},
          "Dropout": {'config': {'rate': 0.3}},
          "Dense": {'config': {'units': 1, 'name': 'output'}}
          }
prediction = make_and_run(Model, lyrs)
np.testing.assert_almost_equal(float(prediction[0].sum()), 1457.831176, decimal=4)  #

##
# LSTM  + Raffel Attention
lyrs = {"LSTM_0": {'config': {'units': 64, 'return_sequences': True}},
          "LSTM_1": {'config': {'units': 32, 'return_sequences': True}},
          "AttentionRaffel": {'config': {'step_dim': 12}},
          "Dropout": {'config': {'rate': 0.3}},
          "Dense": {'config': {'units': 1, 'name': 'output'}}
          }
prediction = make_and_run(Model, lyrs)
np.testing.assert_almost_equal(float(prediction[0].sum()), 1378.492431, decimal=4)


##
# LSTM  + Snail Attention
lyrs = {"LSTM_0": {'config': {'units': 64, 'return_sequences': True}},
          "LSTM_1": {'config': {'units': 32, 'return_sequences': True}},
          "SnailAttention": {'config': {'dims': 32, 'k_size': 32, 'v_size': 32}},
          "Dropout": {'config': {'rate': 0.3}},
          "Dense_0": {'config': {'units': 1, 'name': 'output'}},
          "Flatten": {'config': {}},
          "Dense": {'config': {'units': 1}}
          }
prediction = make_and_run(Model, lyrs)
np.testing.assert_almost_equal(float(prediction[0].sum()), 1306.02380, decimal=4)

##
# LSTM + SelfAttention model
lyrs = {"LSTM_0": {'config': {'units': 64, 'return_sequences': True}},
          "SelfAttention": {'config': {}},
          "Dropout": {'config': {'rate': 0.3}},
          "Dense": {'config': {'units': 1, 'name': 'output'}}
          }
prediction = make_and_run(Model, lyrs)
np.testing.assert_almost_equal(float(prediction[0].sum()), 1527.28979, decimal=4)


##
# LSTM + HierarchicalAttention model
lyrs = {"LSTM_0": {'config': {'units': 64, 'return_sequences': True}},
          "HierarchicalAttention": {'config': {}},
          "Dropout": {'config': {'rate': 0.3}},
          "Dense": {'config': {'units': 1, 'name': 'output'}}
          }
prediction = make_and_run(Model, lyrs)
np.testing.assert_almost_equal(float(prediction[0].sum()), 1374.090332, decimal=4)

##
# CNN based model
lyrs = {"Conv1D_9": {'config': {'filters': 64, 'kernel_size': 2}},
          "dropout": {'config': {'rate': 0.3}},
          "Conv1D_1": {'config': {'filters': 32, 'kernel_size': 2}},
          "maxpool1d": {'config': {'pool_size': 2}},
          'flatten': {'config': {}},
          'leakyrelu': {'config': {}},
          "Dense": {'config': {'units': 1}}
          }
prediction = make_and_run(Model, lyrs)
np.testing.assert_almost_equal(float(prediction[0].sum()), 1333.210693, decimal=4)

##
# LSTMCNNModel based model
lyrs = {"LSTM": {'config': {'units': 64, 'return_sequences': True}},
          "Conv1D_0": {'config': {'filters': 64, 'kernel_size': 2}},
          "dropout": {'config': {'rate': 0.3}},
          "Conv1D_1": {'config': {'filters': 32, 'kernel_size': 2}},
          "maxpool1d": {'config': {'pool_size': 2}},
          'flatten': {'config': {}},
          'leakyrelu': {'config': {}},
          "Dense": {'config': {'units': 1}}
          }
prediction = make_and_run(Model, lyrs)
np.testing.assert_almost_equal(float(prediction[0].sum()), 1398.09057, decimal=4)

##
# ConvLSTMModel based model
ins = 8
_lookback = 12
sub_seq = 3
sub_seq_lens = int(_lookback / sub_seq)
lyrs = {'Input' : {'config': {'shape':(sub_seq, 1, sub_seq_lens, ins)}},
          'convlstm2d': {'config': {'filters': 64, 'kernel_size': (1, 3), 'activation': 'relu'}},
          'flatten': {'config': {}},
          'repeatvector': {'config': {'n': 1}},
          'lstm':   {'config': {'units': 128,   'activation': 'relu', 'dropout': 0.3, 'recurrent_dropout': 0.4 }},
          'Dense': {'config': {'units': 1}}
          }
prediction = make_and_run(Model, lyrs, subsequences=sub_seq, lookback=_lookback)
np.testing.assert_almost_equal(float(prediction[0].sum()), 1413.6604, decimal=4)


##
# CNNLSTM based model
subsequences = 3
timesteps = _lookback // subsequences
lyrs = {'Input' : {'config': {'shape':(subsequences, timesteps, ins)}},
          "TimeDistributed_0": {'config': {}},
          "Conv1D_0": {'config': {'filters': 64, 'kernel_size': 2}},
          "leakyrelu": {'config': {}},
          "TimeDistributed_1": {'config': {}},
          "maxpool1d": {'config': {'pool_size': 2}},
          "TimeDistributed_2": {'config': {}},
          'flatten': {'config': {}},
          'lstm':   {'config': {'units': 64,   'activation': 'relu'}},
          'Dense': {'config': {'units': 1}}
               }
prediction = make_and_run(Model, lyrs, subsequences=subsequences)
np.testing.assert_almost_equal(float(prediction[0].sum()), 1523.9479, decimal=4)


##
# LSTM auto-encoder
lyrs = {
    'lstm_0': {'config': {'units': 100,  'recurrent_dropout': 0.4}},
    "leakyrelu_0": {'config': {}},
    'RepeatVector': {'config': {'n': 11}},
    'lstm_1': {'config': {'units': 100,  'dropout': 0.3}},
    "relu_1": {'config': {}},
    'Dense': {'config': {'units': 1}}
}
prediction = make_and_run(Model, lyrs, lookback=12)
np.testing.assert_almost_equal(float(prediction[0].sum()), 1514.47912, decimal=4)


##
# TCN based model auto-encoder
lyrs = {"tcn":  {'config': {'nb_filters': 64,
                  'kernel_size': 2,
                  'nb_stacks': 1,
                  'dilations': [1, 2, 4, 8, 16, 32],
                  'padding': 'causal',
                  'use_skip_connections': True,
                  'return_sequences': False,
                  'dropout_rate': 0.0}},
          'Dense':  {'config': {'units': 1}}
          }
prediction = make_and_run(Model, lyrs)
np.testing.assert_almost_equal(float(prediction[0].sum()), 935.47619, decimal=4)


##
# InputAttentionModel based model
import tensorflow as tf
tf.compat.v1.disable_eager_execution()

prediction = make_and_run(InputAttentionModel)
lyrs = {
    'Input_1': {'config': {'shape': (_lookback, ins), 'name': 'inputs'}},
    'Input_2': {'config': {'shape': (20,), 'name': 'input_s0'}},
    'Input_3': {'config': {'shape': (20,), 'name': 'input_h0'}},
    'EncAttention': {'config': {'n_s': 20, 'n_h': 20, 'm': 20, 'lookback': _lookback, 'ins': ins, 'outs': 1},
                       'inputs': ['inputs', 'input_s0', 'input_h0']},
    'Flatten': {'config': {}},
    'Dense': {'config': {'units': 1}}
    }
#make_and_run(Model, lyrs)
