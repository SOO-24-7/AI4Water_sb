
__all__ = ["MLRegressionExperiments"]

from ai4water.utils.utils import get_version_info, dateandtime_now
from ._main import Experiments
from .utils import regression_space


try:
    import catboost
except ModuleNotFoundError:
    catboost = None

try:
    import lightgbm
except ModuleNotFoundError:
    lightgbm = None

try:
    import xgboost
except ModuleNotFoundError:
    xgboost = None

import sklearn

VERSION_INFO = get_version_info(sklearn=sklearn)


class MLRegressionExperiments(Experiments):
    """
    Compares peformance of 40+ machine learning models for a regression problem.
    The experiment consists of `models` which are run using `fit()` method. A `model`
    is one experiment. 

    The user can define new `models` by subclassing this class. In fact any new
    method in the sub-class which starts with `model_` wll be considered
    as a new `model`. Otherwise the user has to overwite the attribute `models` to
    redefine, which methods (of class) are to be used as models and which should not. The
    method which is a `model` must only return key word arguments which will be
    streamed to the `Model` using `build_and_run` method. Inside this new method
    the user must define, which parameters to optimize, their param_space for optimization
    and the initial values to use for optimization.

    """

    def __init__(self,
                 param_space=None,
                 x0=None,
                 cases=None,
                 exp_name='MLRegressionExperiments',
                 num_samples=5,
                 verbosity=1,
                 **model_kwargs):
        """
        Initializes the class

        Arguments:
            param_space: dimensions of parameters which are to be optimized. These
                can be overwritten in `models`.
            x0 list: initial values of the parameters which are to be optimized.
                These can be overwritten in `models`
            exp_name str: name of experiment, all results will be saved within this folder
            model_kwargs dict: keyword arguments which are to be passed to `Model`
                and are not optimized.

        Examples:
            >>> from ai4water.datasets import busan_beach
            >>> from ai4water.experiments import MLRegressionExperiments
            >>> # first compare the performance of all available models without optimizing their parameters
            >>> data = busan_beach()  # read data file, in this case load the default data
            >>> inputs = list(data.columns)[0:-1]  # define input and output columns in data
            >>> outputs = list(data.columns)[-1]
            >>> comparisons = MLRegressionExperiments(
            ...       input_features=inputs, output_features=outputs,
            ...       nan_filler= {'method': 'KNNImputer', 'features': inputs} )
            >>> comparisons.fit(data=data,run_type="dry_run")
            >>> comparisons.compare_errors('r2')
            >>> # find out the models which resulted in r2> 0.5
            >>> best_models = comparisons.compare_errors('r2', cutoff_type='greater',
            ...                                                cutoff_val=0.3)
            >>> best_models = [m[1] for m in best_models.values()]
            >>> # now build a new experiment for best models and otpimize them
            >>> comparisons = MLRegressionExperiments(
            ...     inputs_features=inputs, output_features=outputs,
            ...     nan_filler= {'method': 'KNNImputer', 'features': inputs},
            ...     exp_name="BestMLModels")
            >>> comparisons.fit(data=data, run_type="optimize", include=best_models)
            >>> comparisons.compare_errors('r2')
            >>> comparisons.taylor_plot()  # see help(comparisons.taylor_plot()) to tweak the taylor plot

        """
        self.param_space = param_space
        self.x0 = x0
        self.model_kws = model_kwargs

        if exp_name == "MLRegressionExperiments":
            exp_name = f"{exp_name}_{dateandtime_now()}"

        super().__init__(cases=cases, exp_name=exp_name, num_samples=num_samples, verbosity=verbosity)

        self.spaces = regression_space(num_samples=num_samples)

        if catboost is None:
            self.models.remove('model_CatBoostRegressor')
        if lightgbm is None:
            self.models.remove('model_LGBMRegressor')
        if xgboost is None:
            self.models.remove('model_XGBRFRegressor')

        sk_maj_ver = int(sklearn.__version__.split('.')[0])
        sk_min_ver = int(sklearn.__version__.split('.')[1])
        if sk_maj_ver == 0 and sk_min_ver < 23:
            for m in ['model_PoissonRegressor', 'model_TweedieRegressor']:
                self.models.remove(m)

    @property
    def tpot_estimator(self):
        try:
            from tpot import TPOTRegressor
        except (ModuleNotFoundError, ImportError):
            TPOTRegressor = None
        return TPOTRegressor

    @property
    def mode(self):
        return "regression"

    def model_AdaBoostRegressor(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostRegressor.html

        self.path = "sklearn.ensemble.AdaBoostRegressor"
        self.param_space = self.spaces["AdaBoostRegressor"]["param_space"]
        self.x0 = self.spaces["AdaBoostRegressor"]["x0"]

        return {'model': {'AdaBoostRegressor': kwargs}}

    def model_ARDRegression(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ARDRegression.html

        self.path = "sklearn.linear_model.ARDRegression"
        self.param_space = self.spaces["ARDRegression"]["param_space"]
        self.x0 = self.spaces["ARDRegression"]["x0"]

        return {'model': {'ARDRegression': kwargs}}

    def model_BaggingRegressor(self, **kwargs):

        self.path = "sklearn.ensemble.BaggingRegressor"
        self.param_space = self.spaces["BaggingRegressor"]["param_space"]
        self.x0 = self.spaces["BaggingRegressor"]["x0"]

        return {'model': {'BaggingRegressor': kwargs}}

    def model_BayesianRidge(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.BayesianRidge.html

        self.path = "sklearn.linear_model.BayesianRidge"
        self.param_space = self.spaces["BayesianRidge"]["param_space"]
        self.x0 = self.spaces["BayesianRidge"]["x0"]

        return {'model': {'BayesianRidge': kwargs}}

    def model_CatBoostRegressor(self, **kwargs):
        # https://catboost.ai/docs/concepts/python-reference_parameters-list.html

        self.path = "catboost.CatBoostRegressor"
        self.param_space = self.spaces["CatBoostRegressor"]["param_space"]
        self.x0 = self.spaces["CatBoostRegressor"]["x0"]

        return {'model': {'CatBoostRegressor': kwargs}}

    def model_DecisionTreeRegressor(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html

        self.path = "sklearn.tree.DecisionTreeRegressor"
        # TODO not converging
        self.param_space = self.spaces["DecisionTreeRegressor"]["param_space"]
        self.x0 = self.spaces["DecisionTreeRegressor"]["x0"]

        return {'model': {'DecisionTreeRegressor': kwargs}}

    def model_DummyRegressor(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyRegressor.html

        self.path = "sklearn.dummy.DummyRegressor"
        self.param_space = self.spaces["DummyRegressor"]["param_space"]
        self.x0 = self.spaces["DummyRegressor"]["x0"]
        kwargs.update({'constant': 0.2,
                       'quantile': 0.2})

        return {'model': {'DummyRegressor': kwargs}}

    def model_ElasticNet(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNet.html

        self.path = "sklearn.linear_model.ElasticNet"
        self.param_space = self.spaces["ElasticNet"]["param_space"]
        self.x0 = self.spaces["ElasticNet"]["x0"]

        return {'model': {'ElasticNet': kwargs}}

    def model_ElasticNetCV(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNetCV.html

        self.path = "sklearn.linear_model.ElasticNetCV"
        self.param_space = self.spaces["ElasticNetCV"]["param_space"]
        self.x0 = self.spaces["ElasticNetCV"]["x0"]

        return {'model': {'ElasticNetCV': kwargs}}

    def model_ExtraTreeRegressor(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.tree.ExtraTreeRegressor.htm

        self.path = "sklearn.tree.ExtraTreeRegressor"
        self.param_space = self.spaces["ExtraTreeRegressor"]["param_space"]
        self.x0 = self.spaces["ExtraTreeRegressor"]["x0"]

        return {'model': {'ExtraTreeRegressor': kwargs}}

    def model_ExtraTreesRegressor(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesRegressor.html

        self.path = "sklearn.ensemble.ExtraTreesRegressor"
        self.param_space = self.spaces["ExtraTreesRegressor"]["param_space"]
        self.x0 = self.spaces["ExtraTreesRegressor"]["x0"]

        return {'model': {'ExtraTreesRegressor': kwargs}}

    # def model_GammaRegressor(self, **kwargs):
    # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.GammaRegressor.html?highlight=gammaregressor
    #     self.param_space = [
    #         Real(low=0.0, high=1.0, name='alpha', num_samples=self.num_samples),
    #         Integer(low=50, high=500, name='max_iter', num_samples=self.num_samples),
    #         Real(low= 1e-6, high= 1e-2, name='tol', num_samples=self.num_samples),
    #         Categorical(categories=[True, False], name='warm_start'),
    #         Categorical(categories=[True, False], name='fit_intercept')
    #     ]
    #     self.x0 = [0.5, 100,1e-6, True, True]
    #     return {'model': {'GammaRegressor': kwargs}}

    def model_GaussianProcessRegressor(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.gaussian_process.GaussianProcessRegressor.html

        self.path = "sklearn.gaussian_process.GaussianProcessRegressor"
        self.param_space = self.spaces["GaussianProcessRegressor"]["param_space"]
        self.x0 = self.spaces["GaussianProcessRegressor"]["x0"]

        return {'model': {'GaussianProcessRegressor': kwargs}}

    def model_GradientBoostingRegressor(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html

        self.path = "sklearn.ensemble.GradientBoostingRegressor"
        self.param_space = self.spaces["GradientBoostingRegressor"]["param_space"]
        self.x0 = self.spaces["GradientBoostingRegressor"]["x0"]

        return {'model': {'GradientBoostingRegressor': kwargs}}

    def model_HistGradientBoostingRegressor(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.HistGradientBoostingRegressor.html

        # TODO not hpo not converging
        self.path = "sklearn.ensemble.HistGradientBoostingRegressor"
        self.param_space = self.spaces["HistGradientBoostingRegressor"]["param_space"]
        self.x0 = self.spaces["HistGradientBoostingRegressor"]["x0"]

        return {'model': {'HistGradientBoostingRegressor':kwargs}}

    def model_HuberRegressor(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.HuberRegressor.html

        self.path = "sklearn.linear_model.HuberRegressor"
        self.param_space = self.spaces["HuberRegressor"]["param_space"]
        self.x0 = self.spaces["HuberRegressor"]["x0"]

        return {'model': {'HuberRegressor': kwargs}}

    def model_KernelRidge(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.kernel_ridge.KernelRidge.html

        self.path = "sklearn.kernel_ridge.KernelRidge"
        self.param_space = self.spaces["KernelRidge"]["param_space"]
        self.x0 = self.spaces["KernelRidge"]["x0"]

        return {'model': {'KernelRidge': kwargs}}

    def model_KNeighborsRegressor(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsRegressor.html

        self.path = "sklearn.neighbors.KNeighborsRegressor"
        self.param_space = self.spaces["KNeighborsRegressor"]["param_space"]
        self.x0 = self.spaces["KNeighborsRegressor"]["x0"]

        return {'model': {'KNeighborsRegressor': kwargs}}

    def model_LassoLars(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LassoLars.html

        self.path = "sklearn.linear_model.LassoLars"
        self.param_space = self.spaces["LassoLars"]["param_space"]
        self.x0 = self.spaces["LassoLars"]["x0"]

        return {'model': {'LassoLars': kwargs}}

    def model_Lars(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lars.html

        self.path = "sklearn.linear_model.Lars"
        self.param_space = self.spaces["Lars"]["param_space"]
        self.x0 = self.spaces["Lars"]["x0"]

        return {'model': {'Lars': kwargs}}

    def model_LarsCV(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LarsCV.html

        self.path = "sklearn.linear_model.LarsCV"
        self.param_space = self.spaces["LarsCV"]["param_space"]
        self.x0 = self.spaces["LarsCV"]["x0"]

        return {'model': {'LarsCV': kwargs}}

    def model_LinearSVR(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVR.html

        self.path = "sklearn.svm.LinearSVR"
        self.param_space = self.spaces["LinearSVR"]["param_space"]
        self.x0 = self.spaces["LinearSVR"]["x0"]

        return {'model': {'LinearSVR': kwargs}}

    def model_Lasso(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Lasso.html

        self.path = "sklearn.linear_model.Lasso"
        self.param_space = self.spaces["Lasso"]["param_space"]
        self.x0 = self.spaces["Lasso"]["x0"]

        return {'model': {'Lasso': kwargs}}

    def model_LassoCV(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LassoCV.html

        self.path = "sklearn.linear_model.LassoCV"
        self.param_space = self.spaces["LassoCV"]["param_space"]
        self.x0 = self.spaces["LassoCV"]["x0"]

        return {'model': {'LassoCV': kwargs}}

    def model_LassoLarsCV(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LassoLarsCV.html

        self.path = "sklearn.linear_model.LassoLarsCV"
        self.param_space = self.spaces["LassoLarsCV"]["param_space"]
        self.x0 = self.spaces["LassoLarsCV"]["x0"]

        return {'model': {'LassoLarsCV': kwargs}}

    def model_LassoLarsIC(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LassoLarsIC.html

        self.path = "sklearn.linear_model.LassoLarsIC"
        self.param_space = self.spaces["LassoLarsIC"]["param_space"]
        self.x0 = self.spaces["LassoLarsIC"]["x0"]

        return {'model': {'LassoLarsIC': kwargs}}

    def model_LGBMRegressor(self, **kwargs):
        # https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMRegressor.html

        self.path = "lightgbm.LGBMRegressor"
        self.param_space = self.spaces["LGBMRegressor"]["param_space"]
        self.x0 = self.spaces["LGBMRegressor"]["x0"]

        return {'model': {'LGBMRegressor': kwargs}}

    def model_LinearRegression(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html

        self.path = "sklearn.linear_model.LinearRegression"
        self.param_space = self.spaces["LinearRegression"]["param_space"]
        self.x0 = self.spaces["LinearRegression"]["x0"]

        return {'model': {'LinearRegression': kwargs}}

    def model_MLPRegressor(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html

        self.path = "sklearn.neural_network.MLPRegressor"
        self.param_space = self.spaces["MLPRegressor"]["param_space"]
        self.x0 = self.spaces["MLPRegressor"]["x0"]

        return {'model': {'MLPRegressor': kwargs}}

    def model_NuSVR(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.svm.NuSVR.html

        self.path = "sklearn.svm.NuSVR"
        self.param_space = self.spaces["NuSVR"]["param_space"]
        self.x0 = self.spaces["NuSVR"]["x0"]

        return {'model': {'NuSVR': kwargs}}

    def model_OrthogonalMatchingPursuit(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.OrthogonalMatchingPursuit.html

        self.path = "sklearn.linear_model.OrthogonalMatchingPursuit"
        self.param_space = self.spaces["OrthogonalMatchingPursuit"]["param_space"]
        self.x0 = self.spaces["OrthogonalMatchingPursuit"]["x0"]

        return {'model': {'OrthogonalMatchingPursuit': kwargs}}

    def model_OrthogonalMatchingPursuitCV(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.OrthogonalMatchingPursuitCV.html

        self.path = "sklearn.linear_model.OrthogonalMatchingPursuitCV"
        self.param_space = self.spaces["OrthogonalMatchingPursuitCV"]["param_space"]
        self.x0 = self.spaces["OrthogonalMatchingPursuitCV"]["x0"]

        return {'model': {'OrthogonalMatchingPursuitCV': kwargs}}

    def model_OneClassSVM(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.svm.OneClassSVM.html

        self.path = "sklearn.svm.OneClassSVM"
        self.param_space = self.spaces["OneClassSVM"]["param_space"]
        self.x0 = self.spaces["OneClassSVM"]["x0"]

        return {'model': {'OneClassSVM': kwargs}}

    def model_PoissonRegressor(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.PoissonRegressor.html

        self.path = "sklearn.linear_model.PoissonRegressor"
        self.param_space = self.spaces["PoissonRegressor"]["param_space"]
        self.x0 = self.spaces["PoissonRegressor"]["x0"]

        return {'model': {'PoissonRegressor': kwargs}}

    def model_Ridge(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html

        self.path = "sklearn.linear_model.Ridge"
        self.param_space = self.spaces["Ridge"]["param_space"]
        self.x0 = self.spaces["Ridge"]["x0"]

        return {'model': {'Ridge': kwargs}}

    def model_RidgeCV(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeCV.html

        self.path = "sklearn.linear_model.RidgeCV"
        self.param_space = self.spaces["RidgeCV"]["param_space"]
        self.x0 = self.spaces["RidgeCV"]["x0"]

        return {'model': {'RidgeCV': kwargs}}

    def model_RadiusNeighborsRegressor(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.RadiusNeighborsRegressor.html

        self.path = "sklearn.neighbors.RadiusNeighborsRegressor"
        self.param_space = self.spaces["RadiusNeighborsRegressor"]["param_space"]
        self.x0 = self.spaces["RadiusNeighborsRegressor"]["x0"]

        return {'model': {'RadiusNeighborsRegressor': kwargs}}

    def model_RANSACRegressor(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RANSACRegressor.html

        self.path = "sklearn.linear_model.RANSACRegressor"
        self.param_space = self.spaces["RANSACRegressor"]["param_space"]
        self.x0 = self.spaces["RANSACRegressor"]["x0"]

        return {'model': {'RANSACRegressor': kwargs}}

    def model_RandomForestRegressor(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html

        self.path = "sklearn.ensemble.RandomForestRegressor"
        self.param_space = self.spaces["RandomForestRegressor"]["param_space"]
        self.x0 = self.spaces["RandomForestRegressor"]["x0"]

        return {'model': {'RandomForestRegressor': kwargs}}

    def model_SVR(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html

        self.path = "sklearn.svm.SVR"
        self.param_space = self.spaces["SVR"]["param_space"]
        self.x0 = self.spaces["SVR"]["x0"]

        return {'model': {'SVR': kwargs}}

    def model_SGDRegressor(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDRegressor.html

        self.path = "sklearn.linear_model.SGDRegressor"
        self.param_space = self.spaces["SGDRegressor"]["param_space"]
        self.x0 = self.spaces["SGDRegressor"]["x0"]

        return {'model': {'SGDRegressor': kwargs}}

    # def model_TransformedTargetRegressor(self, **kwargs):
    #     ## https://scikit-learn.org/stable/modules/generated/sklearn.compose.TransformedTargetRegressor.html
    #     self.param_space = [
    #         Categorical(categories=[None], name='regressor'),
    #         Categorical(categories=[None], name='transformer'),
    #         Categorical(categories=[None], name='func')
    #     ]
    #     self.x0 = [None, None, None]
    #     return {'model': {'TransformedTargetRegressor': kwargs}}

    def model_TweedieRegressor(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.TweedieRegressor.html

        self.path = "sklearn.linear_model.TweedieRegressor"
        self.param_space = self.spaces["TweedieRegressor"]["param_space"]
        self.x0 = self.spaces["TweedieRegressor"]["x0"]

        return {'model': {'TweedieRegressor': kwargs}}

    def model_TheilsenRegressor(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.TheilSenRegressor.html

        self.path = "sklearn.linear_model.TheilSenRegressor"
        self.param_space = self.spaces["TheilSenRegressor"]["param_space"]
        self.x0 = self.spaces["TheilSenRegressor"]["x0"]

        return {'model': {'TheilSenRegressor': kwargs}}

    # TODO
    # def model_GAMMAREGRESSOR(self, **kwargs):
    #     # ValueError: Some value(s) of y are out of the valid range for family GammaDistribution
    #     return {'GAMMAREGRESSOR': {}}

    def model_XGBRFRegressor(self, **kwargs):
        # https://xgboost.readthedocs.io/en/latest/python/python_api.html#xgboost.XGBRFRegressor

        self.path = "xgboost.XGBRFRegressor"
        self.param_space = self.spaces["XGBRFRegressor"]["param_space"]
        self.x0 = self.spaces["XGBRFRegressor"]["x0"]

        return {'model': {'XGBRFRegressor': kwargs}}

    def model_XGBRegressor(self, **kwargs):
        # ##https://xgboost.readthedocs.io/en/latest/python/python_api.html#xgboost.XGBRegressor

        self.path = "xgboost.XGBRegressor"
        self.param_space = self.spaces["XGBRegressor"]["param_space"]
        self.x0 = self.spaces["XGBRegressor"]["x0"]

        return {'model': {'XGBRegressor': kwargs}}
