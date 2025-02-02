from typing import Union

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from ai4water.backend import imputations

seed = 313
# use LGBM imputation method
# https://www.kaggle.com/robikscube/handling-with-missing-data-youtube-stream#Level-4:-LightGBM-Imputer!!
# plot imputation distribution

class Imputation(object):

    """
    Implements imputation of missing values using a range of methods.

    Imputation Methods
    -----------------

    - pandas:
        Pandas library provides two methods for filling input data.
        `interpolate`: filling by interpolation
          Example of imputer_args can be
              {'method': 'spline': 'order': 2}
          For detailed args to be passed see interpolate_

        `fillna`:
          example of imputer_args can be
             {'method': 'ffill'}
          For detailed args to be passed see fillna_

    - sklearn:
        scikit-learn library provides 3 different imputation methods.
        `SimplteImputer`:
          For details see SimpleImputer_
        `IterativeImputer`:
          imputer_args example: {'n_nearest_features': 2}
          For details see IterativeImputer_
        `KNNIMputer`:
          All the args accepted by KNNImputer of sklearn can be passed as in imputer_args.
          imputer_args example: {'n_neighbors': 3}.
          For details KNNImputer_
    - fancyimpute:
        knn:
        NuclearnNormMinimization
        SoftImpute
        Biscaler
    transdim:

    Methods
    --------
    - :py:meth:`ai4water.preprocessing.imputation.Imputation.plot` plots the imputed values.

    - :py:meth:`ai4water.preprocessing.imputation.Imputation.missing_indices` indices of missing data.


    Examples:
        >>> df = pd.DataFrame([1,3,np.nan,  np.nan, 9, np.nan, 11])
        >>> imputer = Imputation(df, method='fillna', imputer_args={'method': 'ffill'})
        >>> imputer()
        # change the imputation method
        >>> imputer.method = 'interpolate'
        >>> imputer(method='cubic')
        # Now try with KNN imputation
        >>> imputer.method = 'KNNImputer'
        >>> imputer(n_neighbors=3)

    .. _fillna:
        https://pandas.pydata.org/pandas-docs/version/0.22.0/generated/pandas.DataFrame.fillna.html
    .. _interpolate:
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.interpolate.html
    .. _SimpleImputer:
        https://scikit-learn.org/stable/modules/generated/sklearn.impute.SimpleImputer.html#sklearn.impute.SimpleImputer
    .. _IterativeImputer:
        https://scikit-learn.org/stable/modules/generated/sklearn.impute.IterativeImputer.html#sklearn.impute.IterativeImputer
    .. _KNNImputer:
        https://scikit-learn.org/stable/modules/generated/sklearn.impute.KNNImputer.html
    """
    def __init__(
            self,
            data: Union[pd.DataFrame, np.ndarray, list],
            method: str = 'KNNImputer',
            features=None,
            imputer_args: dict = None
    ):
        """
        Arguments:
            data:
                the data which contains missing values
            method:
                the method to apply for missing
            features:
                the features on which imputation is to be applied
            imputer_args:
                arguments for underlying imputer function
        """
        self.data = self.maybe_make_df(data)
        self.method = method
        self.features = features or self.data.columns
        self.imputer_args = {} if imputer_args is None else imputer_args
        self.new_data = None

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, x):
        self._method = x

    def call(self, *args, **kwargs):
        raise NotImplementedError(f"You must ovewrite the `call` method to implement {self.method} method")

    def __call__(self, *args, **kwargs):
        """
        If kwargs are provided they will overwrite self.imputer_args. This helps to use same instance of
        Imputantion class with different args.
        """
        if kwargs:
            kwargs = kwargs
        else:
            kwargs = self.imputer_args

        if self.method in ['fillna', 'interpolate']:  # it is a pandas based
            for col in self.data.columns:
                if col in self.features:
                    self.data[col] = getattr(self.data[col], self.method)(**kwargs)

        elif self.method in imputations:
            imputer = imputations[self.method](**kwargs)

            data = self.data.copy()  # making a copy so that non-imputed features remain intact
            _data = self.data[self.features].values
            data_ = imputer.fit_transform(_data)

            if isinstance(data_, np.ndarray):
                data_ = pd.DataFrame(data_, columns=self.features, index=self.data.index)

            data[self.features] = data_

            setattr(self, 'data', data)

        else:
            return self.call()

        if self._dtype == 'list':
            self.data = self.data.values.reshape(-1,).tolist()
        elif self._dtype == 'ndarray':
            self.data = self.data.values

        return self.data

    def plot(self, cols=None, st=0, en=None):
        """
        cols: columns to plot from data
        st: int
        en: int

        Example
        -------
            >>> imputer.plot(cols=['in1', 'in2'], st=0, en=25)
        """

        if cols is not None:
            if not isinstance(cols, list):
                assert isinstance(cols, str) and cols in self.data
                cols = [cols]
        else:
            cols = list(self.new_data.columns)

        if en is None:
            en = len(self.data)
        plt.close('all')
        _, axis = plt.subplots(len(cols), sharex='all')

        if not isinstance(axis, np.ndarray):
            axis = [axis]

        indices = self.missing_indices()
        for col, ax in zip(cols, axis):
            idx = indices[col]
            ax.plot(self.data[col][st:en], linestyle='-', color='k', marker='o', fillstyle='full', label="Original")
            ax.plot(self.new_data[col][idx][st:en], linestyle='--', marker='*', color='aqua', label="Imputed")

            ax.set_title(col)
            ax.legend()

        plt.show()

        return

    def missing_indices(self) -> dict:
        # https://github.com/scikit-learn/scikit-learn/blob/7cc3dbcbe/sklearn/impute/_base.py#L556
        indices = {}
        for col in self.data.columns:
            # https://stackoverflow.com/a/42795371/5982232
            indices[col] = np.isnan(self.data[col].values.astype(float))

        return indices

    def maybe_make_df(self, data):
        setattr(self, '_dtype', data.__class__.__name__)

        data = data.copy()

        if isinstance(data, pd.DataFrame):
            data = data
        else:
            data = np.array(data)
            if data.ndim == 1:
                data = data.reshape(-1, 1)
            assert isinstance(data, np.ndarray)
            data = pd.DataFrame(data, columns=['data'+str(i) for i in range(data.shape[1])])
        return data
