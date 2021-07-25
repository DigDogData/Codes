# linear regression model (includes polynomial regression without pipeline)
# len(features)=1 gives SLR, len(features)>1 gives MLR
def lrm(features, label):
    from sklearn.linear_model import LinearRegression
    lm = LinearRegression()         # create a LinearRegression object
    lm.fit(X=features, y=label)     # train model
    return lm

# polynomial regression model with pipeline
def prm(features, label, degree, bias=True, interaction=False):
    from sklearn.preprocessing import StandardScaler     #import StandardScalar
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.linear_model import LinearRegression
    from sklearn.pipeline import Pipeline                #import Pipeline
    # create pipeline input (list of tuples) with following steps:
    # normalize variables -> create polynomial features -> build model
    Input = [("scale", StandardScaler()),        # normalize variables
             ("polynomial", PolynomialFeatures(degree=degree,
                                               include_bias=bias,
                                               interaction_only=interaction)),
             ("model", LinearRegression())]
    pipe = Pipeline(Input)                      # create Pipeline object
    pipe.fit(X=features, y=label)       # train model
    return pipe

# cross validation
def cross(model, features, label, nfold, scoring=False):
    from sklearn.model_selection import cross_val_score
    from sklearn.model_selection import cross_val_predict
    if scoring:
        Rcross = -1 * cross_val_score(model,
                                      features,
                                      label,
                                      cv = nfold,
                                      scoring = scoring)
    else:
        Rcross = cross_val_score(model,
                                 features,
                                 label,
                                 cv = nfold)
    
    # prediction
    prediction = cross_val_predict(model,
                                   features,
                                   label,
                                   cv = nfold)
    return Rcross, prediction

# Ridge regression model
def rrm(features, label, alfa):
    from sklearn.linear_model import Ridge
    RigeModel = Ridge(alpha = alfa)        # create a Ridge regression object
    RigeModel.fit(features, label)
    return RigeModel

# grid search
def grid(features, label, params, nfold):
    from sklearn.linear_model import Ridge
    from sklearn.model_selection import GridSearchCV
    RR = Ridge()        # create Ridge regions object (uses default solver model 'auto')
    Grid1 = GridSearchCV(RR, params, cv = nfold) # create a ridge grid search object
    Grid1.fit(features, label)
    return Grid1.best_estimator_            # return model with best parameter

