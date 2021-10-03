import unittest

from ai4water import Model
from ai4water.datasets import arg_beach
from ai4water.pre_processing.datahandler import DataHandler


dh = DataHandler(data=arg_beach(), verbosity=0)
x, y = dh.training_data()

def test_user_defined_data(_model):
    # using user defined x
    t,p = _model.predict(x=x)
    assert t is None
    assert len(p) == len(x)

    # using user defined x and y, post_processing must happen
    t,p = _model.predict(x=x, y=y)
    assert len(t) == len(p) == len(y)

    return


class TestPredictMethod(unittest.TestCase):

    def test_ml_inbuilt_data(self):
        model = Model(model="RandomForestRegressor",
                      data=arg_beach(),
                      verbosity=0)
        model.fit()

        test_user_defined_data(model)

        t,p = model.predict()
        assert len(t) == len(p)
        return

    def test_ml_userdefined_data(self):
        model = Model(model="RandomForestRegressor", verbosity=0)
        model.fit(x=x, y=y)

        test_user_defined_data(model)

        # using data generated by DataHnadler
        self.assertRaises(ValueError, model.predict)
        return

    def test_ml_userdefined_non_kw(self):
        # using non-keyword arguments to .predict
        model = Model(model="RandomForestRegressor", verbosity=0)
        model.fit(x=x, y=y)

        model.predict(x)
        return

    def test_hydro_metrics(self):

        model = Model(model="RandomForestRegressor", verbosity=0)
        model.fit(x=x, y=y)

        for metrics in ["minimal", "hydro_metrics", "all"]:
            model.predict(x=x, metrics=metrics)

        return

if __name__ == "__main__":

    unittest.main()