
import time
import unittest

import tensorflow as tf

if 230 <= int(''.join(tf.__version__.split('.')[0:2]).ljust(3, '0')) < 250:
    from ai4water.functional import Model
    print(f"Switching to functional API due to tensorflow version {tf.__version__}")
else:
    from ai4water import Model

from ai4water.datasets import arg_beach, MtropicsLaos

from ai4water.functional import Model as FModel
from ai4water.preprocessing.datahandler import DataHandler


data = arg_beach()
dh = DataHandler(data=data, verbosity=0)
x_reg, y_reg = dh.training_data()

laos = MtropicsLaos()
data_cls = laos.make_classification(lookback_steps=2)
dh_cls = DataHandler(data=data_cls, verbosity=0)
x_cls, y_cls = dh_cls.training_data()


def test_user_defined_data(_model, x, y):
    # using user defined x
    t, p = _model.predict(x=x, return_true=True)
    assert t is None
    assert len(p) == len(x)

    # using user defined x and y, post_processing must happen
    t, p = _model.predict(x=x, y=y, return_true=True)
    assert len(t) == len(p) == len(y)

    return


def _test_ml_inbuilt_data_reg(_model):
    model = _model(model="RandomForestRegressor",
                   data=arg_beach(),
                   verbosity=0)
    model.fit()

    test_user_defined_data(model, x_reg, y_reg)

    t, p = model.predict(return_true=True)
    assert len(t) == len(p)
    return


def _test_ml_inbuilt_data_cls(_model):
    model = _model(model="RandomForestClassifier",
                   data=data_cls,
                   verbosity=0)
    model.fit()

    test_user_defined_data(model, x_cls, y_cls)

    t, p = model.predict(return_true=True)
    assert len(t) == len(p)
    return


def _test_ml_userdefined_data(_model, model_name, x, y):
    model = _model(model=model_name, verbosity=0)
    model.fit(x=x, y=y)

    test_user_defined_data(model, x, y)

    return model


def _test_fit(_model, model_name, x, y):
    model = _model(model=model_name, verbosity=0)
    model.fit(x, y)

    model.fit(x, y=y)

    model.fit(x=x, y=y)
    return


def _test_ml_userdefined_non_kw(_model, model_name, x, y):
    # using non-keyword arguments to .predict
    model = _model(model=model_name, verbosity=0)
    model.fit(x=x, y=y)

    model.predict(x)
    return


def _test_hydro_metrics(_model, model_name, x, y):
    model = _model(model=model_name, verbosity=0)
    model.fit(x=x, y=y)

    for metrics in ["minimal", "hydro_metrics", "all"]:
        model.predict(x=x, metrics=metrics)
    return


class TestPredictMethod(unittest.TestCase):
    """Tests the `predict` method of Model class"""

    def test_ml_inbuilt_data(self):
        _test_ml_inbuilt_data_reg(Model)
        _test_ml_inbuilt_data_cls(Model)
        return

    def test_ml_inbuilt_data_fn(self):
        #_test_ml_inbuilt_data_reg(FModel)
        _test_ml_inbuilt_data_cls(FModel)
        return

    def test_ml_userdefined_data(self):
        model = _test_ml_userdefined_data(Model, "RandomForestRegressor", x_reg, y_reg)
        # using data generated by DataHnadler
        self.assertRaises(ValueError, model.predict)

        model = _test_ml_userdefined_data(Model, "RandomForestClassifier", x_cls, y_cls)
        self.assertRaises(ValueError, model.predict)
        return

    def test_ml_userdefined_data_fn(self):
        model = _test_ml_userdefined_data(FModel, "RandomForestRegressor", x_reg, y_reg)
        # using data generated by DataHnadler
        self.assertRaises(ValueError, model.predict)

        model = _test_ml_userdefined_data(FModel, "RandomForestClassifier", x_cls, y_cls)
        # using data generated by DataHnadler
        self.assertRaises(ValueError, model.predict)
        return

    def test_ml_userdefined_non_kw(self):
        _test_ml_userdefined_non_kw(Model, "RandomForestRegressor", x_reg, y_reg)
        _test_ml_userdefined_non_kw(Model, "RandomForestClassifier", x_cls, y_cls)
        return

    def test_ml_userdefined_non_kw_fn(self):
        _test_ml_userdefined_non_kw(FModel, "RandomForestRegressor", x_reg, y_reg)
        _test_ml_userdefined_non_kw(FModel, "RandomForestClassifier", x_cls, y_cls)
        return

    def test_hydro_metrics(self):
        _test_hydro_metrics(Model, "RandomForestRegressor", x_reg, y_reg)
        _test_hydro_metrics(Model, "RandomForestClassifier", x_cls, y_cls)
        return

    def test_hydro_metrics_functional(self):
        _test_hydro_metrics(FModel, "RandomForestRegressor", x_reg, y_reg)
        _test_hydro_metrics(FModel, "RandomForestClassifier", x_cls, y_cls)
        return


class TestFit(unittest.TestCase):

    def test_fit(self):
        _test_fit(Model, "RandomForestRegressor", x_reg, y_reg)
        _test_fit(Model, "RandomForestClassifier", x_cls, y_cls)
        return

    def test_fit_functional(self):
        _test_fit(FModel, "RandomForestRegressor", x_reg, y_reg)
        _test_fit(FModel, "RandomForestClassifier", x_cls, y_cls)
        return

    def test_fit_as_native(self):
        time.sleep(1)
        model = FModel(
            model={"layers": {"Dense": 1}},
            lookback=1,
            data=arg_beach(),
            verbosity=0,
        )

        model.fit(batch_size=30, callbacks=[tf.keras.callbacks.EarlyStopping(patience=5)] )
        assert model.config['batch_size'] == 30

        return


class TestPermImp(unittest.TestCase):

    def test_basic0(self):
        model = Model(model="XGBRegressor",
                      verbosity=0,
                      data=arg_beach())
        model.fit()
        imp = model.permutation_importance(data="validation")
        assert imp.shape == (13, 5)
        return


if __name__ == "__main__":

    unittest.main()
