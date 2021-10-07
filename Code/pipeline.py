import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from preprocessors import Pipeline
import config 
import h2o
from h2o.automl import H2OAutoML



pipeline = Pipeline(
                    target =  config.TARGET, features = config.FEATURES, rotation = config.ROTATION_Type , categorical_variables_to_inpute = config.categorical_variables_to_inpute 
                    , numerical_variables_to_inpute = config.numerical_variables_to_inpute,max_runtime_secs=config.max_runtime_secs
                    )
                   



if __name__ == '__main__':
    
# ======= Loading data Set + Standarization============

    data = pd.read_excel(config.PATH_TO_DATASET_EFA)
    pipeline.Standarize_Data(data)
# =======      EFA        ============
# ======= Adequacy Checks ============
    print('----------------------------')
    print(pipeline.check_validity())
# ======= Initial Number Of Factors ============
    print('----------------------------')
    print(pipeline.check_number_of_factors())
# =======   Final result   ============
    print('----------------------------')
    print(pipeline.final_factors_and_names())
# =======      CFA         ============
    print('----------------------------')
    print(pipeline.create_model_dict())
    print(pipeline.apply_CFA())
 # ======= AUTOML ============
    #h2o.init()
    data_autoMl = h2o.import_file(config.PATH_TO_DATASET_AutoML)
    pipeline.fit(data_autoMl,config.TARGET)
# ======= RUN Trainig ============
    print(pipeline.run_model())
# ======= IPerformance ============
    print(pipeline.model_performance_train_data())
# ======= Prediction============
    print(pipeline.predict())
# ======= Performance ============
    print(pipeline.model_performance_prediction())
