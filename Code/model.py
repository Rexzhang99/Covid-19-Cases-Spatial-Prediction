import geoplot
import geopandas
import numpy as np
from pykrige.rk import Krige
from sklearn.model_selection import GridSearchCV
import pandas as pd
import geopandas
import matplotlib.pyplot as plt

param_dict = {
    "method": ["ordinary", "universal"],
    "variogram_model": ["linear", "power", "gaussian", "spherical"],
    # "nlags": [4, 6, 8],
    # "weight": [True, False]
}

estimator = GridSearchCV(
    Krige(), param_dict, verbose=True, return_train_score=True, cv=5)

# ['covid_hospital_admissions_per_100k','covid_cases_per_100k','lon','lat']
dt = pd.read_csv('Code/Data/cleaned_data.csv')

X = dt[['lon', 'lat']].to_numpy()
y = dt['covid_cases_per_100k'].to_numpy()

estimator.fit(X=X, y=y)

if hasattr(estimator, "best_score_"):
    print("best_score R² = {:.3f}".format(estimator.best_score_))
    print("best_params = ", estimator.best_params_)

print("\nCV results::")
if hasattr(estimator, "cv_results_"):
    for key in [
        "mean_test_score",
        "mean_train_score",
        "param_method",
        "param_variogram_model",
    ]:
        print(" - {} : {}".format(key, estimator.cv_results_[key]))

# estimator.cv_results_
estimator.predict(X)-y


lat, lon, case = X['lat'], X['lon'], y

gdf = geopandas.GeoDataFrame(
    dt, geometry=geopandas.points_from_xy(dt.lon, dt.lat))
gdf.explore("covid_cases_per_100k", legend=False)
