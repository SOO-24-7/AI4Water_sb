"""
======================
permutation importance
======================
"""

from ai4water import Model
from ai4water.datasets import busan_beach
from ai4water.postprocessing.explain import PermutationImportance

data=busan_beach()

########################################################################

# build the  model

model = Model(model="XGBRegressor", verbosity=0)

# train the model

model.fit(data=data)

# get the data

x_val, y_val = model.validation_data()

pimp = PermutationImportance(
    model.predict,
    x_val,
    y_val.reshape(-1, ),
    feature_names=model.input_features
)

# plot permutatin importance of each feature  as box-plot
fig = pimp.plot_as_boxplot()
