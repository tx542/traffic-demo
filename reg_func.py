# NOTE: be sure to run the import statements first, before anything else...
# import the relevant libraries
import pandas as pd
import numpy as np
import geopandas

# KNN
from sklearn.neighbors import KNeighborsRegressor as knn
# Random Forests
from sklearn.ensemble import RandomForestRegressor as rf
# Train-Test Split, Cross-Validation
from sklearn.model_selection import train_test_split, cross_val_score

# PCA - Dimension Reduction
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def predict_model(model_num, df, var_labels, y_label, min_param,
                 max_param, inc_param, regressor_obj, approach_name,
                 standardize_X = False,
                 num_cv = 5, is_PCA = False, PCA_param = 1.0):
    '''
    (c) Michael Xu (tx542)
    ARTS-UG 1647 Making Virtual Sense | Fall 2021 | NYU Gallatin

    -------------------------------------------------------------------------------------

    This function takes in the parameters:
    - model_num: the model number (ordinal),
    - df: a Pandas DataFrame (`df`),
    - var_labels: a list-like/iterable container object (`var_labels`) listing the
    column labels that shall be used as the explanatory variable,
    - y_label: a column label that is the explained variable (y variable/label),
    - a customizable range to find the optimal hyperparameter, where
        - min_param is the lower bound,
        - max_param is the upper bound (not inclusive),
        - inc_param is the increment
    - regressor_obj: the regressor object to use in this function (rf or knn, for Problem 1),
    - approach_name: name of the approach (regressor object),
    - standardize_X: whether the X variables should be standardized,
    - num_cv: a customizable number of cross-validation groups (default is 5),
    - is_PCA: boolean input to indicate whether PCA will be used,
    - PCA_param: parameter to pass into the PCA object, only needed if is_PCA is True

    It will then use the approach passed into the function through regressor_obj,
    with the optimal hyperparameter that has the maximum
    cross-validation score, to construct the optimal regressor object.

    It will then conduct a random train-test split, and
    print the test fit score.

    * Note that all random_state is 0, for the purpose of replicability.
    '''

    # some user input checks...

    # DataFrame data type
    if (type(df) != pd.core.frame.DataFrame) and \
    (type(df) != geopandas.geodataframe.GeoDataFrame):
        print('Dataset is not a Pandas DataFrame object!')
        return None

    # checks for the existence of x labels
    if [(item in df.columns) for item in var_labels].count(True)\
    < len(var_labels):
        print('Not all explanatory variables are in the given DataFrame!')
        return None

    # and also for the y label
    if (type(y_label) != str) or (y_label not in df.columns):
        print('Invalid y label!')
        return None

    # also for the num_cv optional input
    if (type(num_cv) != int):
        print('Invalid CV number! Function will proceed with the default value, 5.')
        num_cv = 5

    # only drop na for the col vars to be used to fit models
    # to preserve as many obs as necessary/possible
    all_drop_var = var_labels + [y_label]
    SUB_DF = df[all_drop_var].dropna()

    # ensure that not `too many` rows were dropped by reporting shape[0]
    print("The number of observations in the given DataFrame is: {:.0f}".\
         format(df.shape[0]))
    print("The valid number of observations left is: {:.0f}\n".\
         format(SUB_DF.shape[0]))


    # determine whether PCA will be used
    if is_PCA:

        # standardize the explanatory variables
        # (as indicated by the labels)

        X_vars_st = StandardScaler().fit_transform(SUB_DF[var_labels])

        # construct the PCA object and transform the X variables
        # according to the rule as specified in the PCA_param
        pca_obj = PCA(PCA_param).fit(X_vars_st)
        X_VARS = pca_obj.transform(X_vars_st)

        print("As instructed, PCA transformation is used on the given X labels.")
        print("{:.2f}% of all variations of the X labels is preserved.\n".\
             format(PCA_param * 100))

    elif standardize_X:
        # if PCA is not used:

        # only drop na for the col vars to be used to fit models
        # to preserve as many obs as necessary/possible

        # also, standard the X-variables for more equal weighing factors
        X_VARS = StandardScaler().fit_transform(SUB_DF[var_labels])

    else:
        # if no PCA and no standardizing X variables
        X_VARS = SUB_DF[var_labels]

        
    # --->>> use CV, experiment with the hyperparameter, within the given range <<<---
    score_array = [cross_val_score(regressor_obj(i),
                                   X = X_VARS,
                                   y = SUB_DF[y_label],
                                   cv = num_cv).mean() for i \
                   in range(min_param, max_param, inc_param)]

    # construct the df to record the score and corresponding hyperparameter (n_neighbors)
    cv_df = pd.DataFrame(score_array, columns = ['score'])
    cv_df['hyperparameter'] = list(range(min_param, max_param, inc_param))

    # let us find the entry with the maximum cv score
    # and the corresponding hyperparameter
    opt_obs = cv_df.loc[cv_df['score'] == cv_df['score'].max()]
    opt_param = int(opt_obs['hyperparameter'].iloc[0, ])
    # take the first optimal parameter, in case that there are multiple

    # report the optimal hyperparameter and CV score:
    print("Using the {} approach, the optimal hyperparameter is: {} (within the range of ({},{},{}).\n"\
          .format(approach_name, opt_param, min_param, max_param, inc_param))
    print("And the optimal CV score is: {:.4f}.\n".\
         format(float(opt_obs['score'].iloc[0, ])))

    # --->>> make the optimal prediction, using a train-test split <<<---

    # instantiate optimal predictor object
    opt_reg = regressor_obj(opt_param)

    # shuffle and split training and test sets
    X_train, X_test, Y_train, Y_test = train_test_split(X_VARS,
                                                        SUB_DF[y_label],
                                                        test_size = 0.2,
                                                        random_state = 0)

    # use the optimal hyperparameter, fit the train data,
    # obtain score using the test ("never-seen-before") data
    train_score = opt_reg.fit(X = X_train, y = Y_train)\
    .score(X = X_train, y = Y_train)
    test_score = opt_reg.fit(X = X_train, y = Y_train)\
    .score(X = X_test, y = Y_test)

    # --->>> report the train-train and train-test scores as derived above  <<<---

    print('''Using the {} approach, based on a random train-test split (using random_state = 0):\n'''\
         .format(approach_name))
    print("The score, fitted on the train data, of the train data is: {:4f};"\
         .format(train_score))
    print("The score, fitted on the train data, of the test data is: {:4f}.\n"\
         .format(test_score))

    # line of division (for aesthetics)
    print('-' * 90 + '\n')

    return {'model_num': model_num,
            'model_approach': approach_name,
            'opt_hyperparam': opt_param,
            'opt_cv_score': float(opt_obs['score'].iloc[0, ]),
            'train_train_score': train_score,
            'train_test_score': test_score,
            'opt_regressor_obj': opt_reg}
