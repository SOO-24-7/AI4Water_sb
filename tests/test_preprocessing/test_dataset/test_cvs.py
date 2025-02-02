
import unittest
import os
import site
cwd = os.path.dirname(os.path.abspath(__file__))
package_path = os.path.dirname(os.path.dirname(os.path.dirname(cwd)))
site.addsitedir(package_path)

from ai4water.datasets import busan_beach
from ai4water.preprocessing.dataset import DataSet


beach_data = busan_beach()


class TestCVs(unittest.TestCase):

    def make_cross_validator(self, **kwargs):

        ds = DataSet(
            data=beach_data,
            verbosity=0,
            **kwargs
        )

        return ds

    def test_kfold(self):
        ds = self.make_cross_validator()
        ds.KFold_splits(n_splits=5)
        ds.plot_KFold_splits(show=False)
        return

    def test_loocv(self):
        ds = self.make_cross_validator()
        ds.LeaveOneOut_splits()
        ds.plot_LeaveOneOut_splits(show=False)
        return

    def test_tscv(self):
        ds = self.make_cross_validator(train_fraction=0.4)
        ds.TimeSeriesSplit_splits(n_splits=5)
        ds.plot_TimeSeriesSplit_splits(show=False)
        return


if __name__ == '__main__':
    unittest.main()
