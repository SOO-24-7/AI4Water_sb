
__all__ = ["MLClassificationExperiments"]

from ._main import Experiments
from .utils import classification_space
from ai4water.utils.utils import dateandtime_now


class MLClassificationExperiments(Experiments):
    """Runs classification models for comparison, with or without
    optimization of hyperparameters. It compares around 30 classification
    algorithms from sklearn, xgboost, catboost and lightgbm.

    Examples
    --------
    >>> from ai4water.datasets import MtropicsLaos
    >>> from ai4water.experiments import MLClassificationExperiments
    >>> data = MtropicsLaos().make_classification(lookback_steps=2)
    >>> inputs = data.columns.tolist()[0:-1]
    >>> outputs = data.columns.tolist()[-1:]
    >>> exp = MLClassificationExperiments(input_features=inputs,
    >>>                                       output_features=outputs)
    >>> exp.fit(data=data, include=["CatBoostClassifier", "LGBMClassifier",
    >>>             'RandomForestClassifier', 'XGBClassifier'])
    >>> exp.compare_errors('accuracy', show=False)
    """

    def __init__(self,
                 param_space=None,
                 x0=None,
                 cases=None,
                 exp_name='MLClassificationExperiments',
                 num_samples=5,
                 **model_kwargs):
        """

        Parameters
        ----------
            param_space : list, optional
            x0 : list, optional
            cases : dict, optional
            exp_name : str, optional
                name of experiment
            num_samples : int, optional
            **model_kwargs :
                keyword arguments for :py:class:`ai4water.Model` class
        """
        self.param_space = param_space
        self.x0 = x0
        self.model_kws = model_kwargs

        self.spaces = classification_space(num_samples=num_samples)

        if exp_name == "MLClassificationExperiments":
            exp_name = f"{exp_name}_{dateandtime_now()}"
        super().__init__(cases=cases, exp_name=exp_name, num_samples=num_samples)

    @property
    def tpot_estimator(self):
        try:
            from tpot import TPOTClassifier
        except (ModuleNotFoundError, ImportError):
            TPOTClassifier = None
        return TPOTClassifier

    @property
    def mode(self):
        return "classification"

    def model_AdaBoostClassifier(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html

        self.path = "sklearn.ensemble.AdaBoostClassifier"
        self.param_space = self.spaces["AdaBoostClassifier"]["param_space"]
        self.x0 = self.spaces["AdaBoostClassifier"]["x0"]

        return {'model': {'AdaBoostClassifier': kwargs}}

    def model_BaggingClassifier(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.BaggingClassifier.html

        self.path = "sklearn.ensemble.BaggingClassifier"
        self.param_space = self.spaces["BaggingClassifier"]["param_space"]
        self.x0 = self.spaces["BaggingClassifier"]["x0"]

        return {'model': {'BaggingClassifier': kwargs}}

    def model_BernoulliNB(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.BernoulliNB.html

        self.path = "sklearn.naive_bayes.BernoulliNB"
        self.param_space = self.spaces["BernoulliNB"]["param_space"]
        self.x0 = self.spaces["BernoulliNB"]["x0"]

        return {'model': {'BernoulliNB': kwargs}}

    def model_CalibratedClassifierCV(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.calibration.CalibratedClassifierCV.html

        self.path = "sklearn.calibration.CalibratedClassifierCV"
        self.param_space = self.spaces["CalibratedClassifierCV"]["param_space"]
        self.x0 = self.spaces["CalibratedClassifierCV"]["x0"]

        return {'model': {'CalibratedClassifierCV': kwargs}}

    # def model_CheckingClassifier(self, **kwargs):
    #     return

    def model_DecisionTreeClassifier(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html

        self.path = "sklearn.tree.DecisionTreeClassifier"
        self.param_space = self.spaces["DecisionTreeClassifier"]["param_space"]
        self.x0 = self.spaces["DecisionTreeClassifier"]["x0"]

        return {'model': {'DecisionTreeClassifier': kwargs}}

    def model_DummyClassifier(self, **kwargs):
        #  https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html

        self.path = "sklearn.dummy.DummyClassifier"
        self.param_space = self.spaces["DummyClassifier"]["param_space"]
        self.x0 = self.spaces["DummyClassifier"]["x0"]

        return {'model': {'DummyClassifier': kwargs}}

    def model_ExtraTreeClassifier(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.tree.ExtraTreeClassifier.html

        self.path = "sklearn.tree.ExtraTreeClassifier"
        self.param_space = self.spaces["ExtraTreeClassifier"]["param_space"]
        self.x0 = self.spaces["ExtraTreeClassifier"]["x0"]

        return {'model': {'ExtraTreeClassifier': kwargs}}

    def model_ExtraTreesClassifier(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html

        self.path = "sklearn.ensemble.ExtraTreesClassifier"
        self.param_space = self.spaces["ExtraTreesClassifier"]["param_space"]
        self.x0 = self.spaces["ExtraTreesClassifier"]["x0"]

        return {'model': {'ExtraTreesClassifier': kwargs}}

    def model_GaussianProcessClassifier(self, **kwargs):
        #  https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html

        self.path = "sklearn.gaussian_process.GaussianProcessClassifier"
        self.param_space = self.spaces["GaussianProcessClassifier"]["param_space"]
        self.x0 = self.spaces["GaussianProcessClassifier"]["x0"]

        return {'model': {'GaussianProcessClassifier': kwargs}}

    def model_GradientBoostingClassifier(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.tree.ExtraTreeClassifier.html

        self.path = "sklearn.ensemble.GradientBoostingClassifier"
        self.param_space = self.spaces["GradientBoostingClassifier"]["param_space"]
        self.x0 = self.spaces["GradientBoostingClassifier"]["x0"]

        return {'model': {'GradientBoostingClassifier': kwargs}}

    def model_HistGradientBoostingClassifier(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html

        self.path = "sklearn.ensemble.HistGradientBoostingClassifier"
        self.param_space = self.spaces["HistGradientBoostingClassifier"]["param_space"]
        self.x0 = self.spaces["HistGradientBoostingClassifier"]["x0"]

        return {'model': {'HistGradientBoostingClassifier': kwargs}}

    def model_KNeighborsClassifier(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html

        self.path = "sklearn.neighbors.KNeighborsClassifier"
        self.param_space = self.spaces["KNeighborsClassifier"]["param_space"]
        self.x0 = self.spaces["KNeighborsClassifier"]["x0"]

        return {'model': {'KNeighborsClassifier': kwargs}}

    def model_LabelPropagation(self, **kwargs):
        ## https://scikit-learn.org/stable/modules/generated/sklearn.semi_supervised.LabelPropagation.html

        self.path = "sklearn.semi_supervised.LabelPropagation"
        self.param_space = self.spaces["LabelPropagation"]["param_space"]
        self.x0 = self.spaces["LabelPropagation"]["x0"]

        return {'model': {'LabelPropagation': kwargs}}

    def model_LabelSpreading(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.semi_supervised.LabelSpreading.html

        self.path = "sklearn.semi_supervised.LabelSpreading"
        self.param_space = self.spaces["LabelSpreading"]["param_space"]
        self.x0 = self.spaces["LabelSpreading"]["x0"]

        return {'model': {'LabelSpreading': kwargs}}

    def model_LGBMClassifier(self, **kwargs):
        # https://lightgbm.readthedocs.io/en/latest/pythonapi/lightgbm.LGBMClassifier.html

        self.path = "lightgbm.LGBMClassifier"
        self.param_space = self.spaces["LGBMClassifier"]["param_space"]
        self.x0 = self.spaces["LGBMClassifier"]["x0"]

        return {'model': {'LGBMClassifier': kwargs}}

    def model_LinearDiscriminantAnalysis(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.discriminant_analysis.LinearDiscriminantAnalysis.html

        self.path = "sklearn.discriminant_analysis.LinearDiscriminantAnalysis"
        self.param_space = self.spaces["LinearDiscriminantAnalysis"]["param_space"]
        self.x0 = self.spaces["LinearDiscriminantAnalysis"]["x0"]

        return {'model': {'LinearDiscriminantAnalysis': kwargs}}

    def model_LinearSVC(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html

        self.path = "sklearn.svm.LinearSVC"
        self.param_space = self.spaces["LinearSVC"]["param_space"]
        self.x0 = self.spaces["LinearSVC"]["x0"]

        return {'model': {'LinearSVC': kwargs}}

    def model_LogisticRegression(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html

        self.path = "sklearn.linear_model.LogisticRegression"
        self.param_space = self.spaces["LogisticRegression"]["param_space"]
        self.x0 = self.spaces["LogisticRegression"]["x0"]

        return {'model': {'LogisticRegression': kwargs}}

    def model_MLPClassifier(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html

        self.path = "sklearn.neural_network.MLPClassifier"
        self.param_space = self.spaces["MLPClassifier"]["param_space"]
        self.x0 = self.spaces["MLPClassifier"]["x0"]

        return {'model': {'MLPClassifier': kwargs}}

    def model_NearestCentroid(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestCentroid.html

        self.path = "sklearn.neighbors.NearestCentroid"
        self.param_space = self.spaces["NearestCentroid"]["param_space"]
        self.x0 = self.spaces["NearestCentroid"]["x0"]

        return {'model': {'NearestCentroid': kwargs}}

    def model_NuSVC(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.svm.NuSVC.html

        self.path = "sklearn.svm.NuSVC"
        self.param_space = self.spaces["NuSVC"]["param_space"]
        self.x0 = self.spaces["NuSVC"]["x0"]

        return {'model': {'NuSVC': kwargs}}

    def model_PassiveAggressiveClassifier(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.PassiveAggressiveClassifier.html

        self.path = "sklearn.linear_model.PassiveAggressiveClassifier"
        self.param_space = self.spaces["PassiveAggressiveClassifier"]["param_space"]
        self.x0 = self.spaces["PassiveAggressiveClassifier"]["x0"]

        return {'model': {'PassiveAggressiveClassifier': kwargs}}

    def model_Perceptron(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Perceptron.html

        self.path = "sklearn.linear_model.Perceptron"
        self.param_space = self.spaces["Perceptron"]["param_space"]
        self.x0 = self.spaces["Perceptron"]["x0"]

        return {'model': {'Perceptron': kwargs}}

    def model_QuadraticDiscriminantAnalysis(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.discriminant_analysis.QuadraticDiscriminantAnalysis.html

        self.path = "sklearn.discriminant_analysis.QuadraticDiscriminantAnalysis"
        self.param_space = self.spaces["QuadraticDiscriminantAnalysis"]["param_space"]
        self.x0 = self.spaces["QuadraticDiscriminantAnalysis"]["x0"]

        return {'model': {'QuadraticDiscriminantAnalysis': kwargs}}

    # def model_RadiusNeighborsClassifier(self, **kwargs):
    #     # https://scikit-learn.org/stable/modules/generated/sklearn.discriminant_analysis.QuadraticDiscriminantAnalysis.html
    #
    #     self.path = "sklearn.neighbors.RadiusNeighborsClassifier"
    #     self.param_space = self.spaces["RadiusNeighborsClassifier"]["param_space"]
    #     self.x0 = self.spaces["RadiusNeighborsClassifier"]["x0"]
    #
    #     return {'model': {'RadiusNeighborsClassifier': kwargs}}

    def model_RandomForestClassifier(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html

        self.path = "sklearn.ensemble.RandomForestClassifier"
        self.param_space = self.spaces["RandomForestClassifier"]["param_space"]
        self.x0 = self.spaces["RandomForestClassifier"]["x0"]

        return {'model': {'RandomForestClassifier': kwargs}}

    def model_RidgeClassifier(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeClassifier.html

        self.path = "sklearn.linear_model.RidgeClassifier"
        self.param_space = self.spaces["RidgeClassifierCV"]["param_space"]
        self.x0 = self.spaces["RidgeClassifierCV"]["x0"]

        return {'model': {'RidgeClassifier': kwargs}}

    def model_RidgeClassifierCV(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.RidgeClassifierCV.html

        self.path = "sklearn.linear_model.RidgeClassifierCV"
        self.param_space = self.spaces["RidgeClassifierCV"]["param_space"]
        self.x0 = self.spaces["RidgeClassifierCV"]["x0"]

        return {'model': {'RidgeClassifierCV': kwargs}}

    def model_SGDClassifier(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html

        self.path = "sklearn.linear_model.SGDClassifier"
        self.param_space = self.spaces["SGDClassifier"]["param_space"]
        self.x0 = self.spaces["SGDClassifier"]["x0"]

        return {'model': {'SGDClassifier': kwargs}}

    def model_SVC(self, **kwargs):
        # https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html

        self.path = "sklearn.svm.SVC"
        self.param_space = self.spaces["SVC"]["param_space"]
        self.x0 = self.spaces["SVC"]["x0"]

        return {'model': {'SVC': kwargs}}

    def model_XGBClassifier(self, **kwargs):
        # https://xgboost.readthedocs.io/en/latest/python/python_api.html

        self.path = "xgboost.XGBClassifier"
        self.param_space = self.spaces["XGBClassifier"]["param_space"]
        self.x0 = self.spaces["XGBClassifier"]["x0"]

        return {'model': {'XGBClassifier': kwargs}}

    def model_XGBRFClassifier(self, **kwargs):
        # https://xgboost.readthedocs.io/en/latest/python/python_api.html#xgboost.XGBRFClassifier

        self.path = "xgboost.XGBRFClassifier"
        self.param_space = self.spaces["XGBRFClassifier"]["param_space"]
        self.x0 = self.spaces["XGBRFClassifier"]["x0"]

        return {'model': {'XGBRFClassifier': kwargs}}

    def model_CatBoostClassifier(self, **suggestions):
        # https://catboost.ai/en/docs/concepts/python-reference_catboostclassifier

        self.path = "catboost.CatBoostClassifier"
        self.param_space = self.spaces["CatBoostClassifier"]["param_space"]
        self.x0 = self.spaces["CatBoostClassifier"]["x0"]

        return {'model': {'CatBoostClassifier': suggestions}}
