
from numpy.core.arrayprint import dtype_short_repr
from numpy.linalg.linalg import det
import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn import preprocessing
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
from factor_analyzer.factor_analyzer import calculate_kmo
import pandas as pd
import numpy as np
from factor_analyzer import (ConfirmatoryFactorAnalyzer,
                             ModelSpecificationParser)
import ast
import h2o
from h2o.automl import H2OAutoML


class Pipeline:
    
    ''' When we call the FeaturePreprocessor for the first time
    we initialise it with the data set we use to train the model,
    plus the different groups of variables to which we wish to apply
    the different engineering procedures'''
    
    
    def __init__(self, target,features,rotation,categorical_variables_to_inpute,numerical_variables_to_inpute,max_runtime_secs):
        ''' , categorical_to_impute, year_variable,
                 numerical_to_impute, numerical_log, categorical_encode,
                 features, test_size = 0.1, random_state = 0,
                 percentage = 0.01, ref_variable = 'YrSold' '''
       
        
        
        
        # engineering parameters (to be learnt from data)
        self.EFA_Result = {}
        self.factors_names = []
        self.model_dict = {}
        self.initial_number_of_factors = None

        self.x = []
        self.y = []
        

        # groups of variables to engineer
        self.Test = False
        self.max_runtime_secs = max_runtime_secs
        self.features = features
        self.rotation = rotation
        self.categorical_variables_to_inpute = categorical_variables_to_inpute
        self.numerical_variables_to_inpute = numerical_variables_to_inpute     

        # models
        h2o.init()
        self.scaler = StandardScaler()
        self.aml = H2OAutoML(max_models=20, seed=1, max_runtime_secs = max_runtime_secs)



        # data sets
        self.data_standarized = None
        self.train = None
        self.test = None
        self.valid = None

  # ======= Starting BY applying EFA ============

    #standarizing Data

    def Standarize_Data(self,data):
      # scale variables
      data = data[self.features]
      self.scaler.fit(data)
      data = self.scaler.transform(data[self.features]) 
      self.data_standarized = pd.DataFrame(data, columns=self.features)  
      return self.data_standarized 
   
    #validity check

    def check_validity(self):
      # train scaler
      Bartlett_test = ''
      Kmo_test = ''
      References = 'For reference, Kaiser put the following values on the results: \n 0.00 to 0.49 unacceptable. \n 0.50 to 0.59 miserable. \n 0.60 to 0.69 mediocre. \n 0.70 to 0.79 middling. \n 0.80 to 0.89 meritorious. \n 0.90 to 1.00 marvelous. '    
      chi_square_value,p_value=calculate_bartlett_sphericity(self.data_standarized)
      kmo_all,kmo_model=calculate_kmo(self.data_standarized)
      ###Bartlett_test 
      if p_value == 0 or p_value < 0.05 : 
        Bartlett_test = 'Bartlett Sphericity Test: Check of intercorrelation between manifest variables \n Value :  {} '.format(p_value) + ' \n Status: Valid '
      else : 
        Bartlett_test = 'Bartlett Sphericity Test: Test whether it is appropriate to use the manifest variables for factor analysis \n Value :  {}'.format(p_value)  + ' \n Status: Not Valid \n Hint: check correlation between variables or  One of the variables is categorical '
      ###KMO_test
      if 0.5 < kmo_model < 1 :
        Kmo_test = 'KMO test: Test whether it is appropriate to use the manifest variables for factor analysis \n Value :  {} '.format(kmo_model) + ' \n Status: Valid '
      else : 
        Kmo_test = 'KMO test: Test whether it is appropriate to use the manifest variables for factor analysis \n Value :  {} '.format(kmo_model) + ' \n Status: Not Valid '

      #print(Bartlett_test) 
      #print(Kmo_test)
      #print(References)
      return Bartlett_test,Kmo_test,References
      
    #Determining Initial number of Factors
      
    def check_number_of_factors(self): 

      fa = FactorAnalyzer(rotation=None, n_factors=len(self.features))
      fa.fit(self.data_standarized)
      # Check Eigenvalues
      ev, v = fa.get_eigenvalues()
      ev = pd.DataFrame(ev)
      self.initial_number_of_factors = ev[(ev[0] > 1)].size
      return self.initial_number_of_factors
    
    #Applying EFA on initial factors numbers + returning final result
    def final_factors_and_names(self):
      
      while self.Test == False:

        fa = FactorAnalyzer(rotation=self.rotation, n_factors=self.initial_number_of_factors)
        fa.fit(self.data_standarized)

            # Check loadings
        loadings = pd.DataFrame(fa.loadings_)
        loadings.index = self.features
            # Select columns which contains all values under 0.4
        filter = (abs(loadings)  < 0.4  ).all()
        factors_to_delete = len((loadings.loc[: , filter].columns))
        self.initial_number_of_factors = self.initial_number_of_factors - factors_to_delete
        if factors_to_delete == 0 :
          self.Test = True      

        if self.Test == True:
          break
      #factors_name = []
      for i in loadings.columns: 
        self.factors_names.append(" ".join(loadings[loadings[i]>=0.4].index.tolist()))
          # Check variance
      factorVariance = pd.DataFrame(fa.get_factor_variance())
      cum_variance = (factorVariance[2].values[2])*100
      #return factors_name
      self.EFA_Result = {"all_columns": loadings.index.tolist() , "factors_names": self.factors_names, "cum_variance": cum_variance }
      return self.EFA_Result

  # ======= Validation of EFA with CFA ============

    #creating model_dict to be included in CFA 
    def create_model_dict(self):
      list=[]
      #fact_names = a['factors_names']
      for i in range(len(self.factors_names)):
        s = "'" + str(i) +  "'" + ":" + str( [self.factors_names[i]] ) +","
        list.append(s)
        final ="".join(list)
        f = "{" + final[:-1] + "}"
        self.model_dict = ast.literal_eval(f) 
      return self.model_dict 
    #Applyin CFA + Final REsult 

    def apply_CFA(self):
      Interpretation_CFA = ' '
      Test_lenght = False
      data_CFA = self.data_standarized[self.factors_names]
    
      model_spec = ModelSpecificationParser.parse_model_specification_from_dict(data_CFA, self.model_dict )
      cfa = ConfirmatoryFactorAnalyzer(model_spec, disp=False)
      cfa.fit(data_CFA)
      loadings_CFA = pd.DataFrame(cfa.loadings_)
      loadings_CFA.rename(columns = lambda x: 'Factor-' + str(x + 1), inplace=True)
      loadings_CFA.index = data_CFA.columns
      covar = pd.DataFrame(cfa.factor_varcovs_)
      covar.index = data_CFA.columns
      covar.columns = data_CFA.columns
      filter = (abs(loadings_CFA.values)  > 0  )
      factors_CFA = len((loadings_CFA.loc[: , filter].columns))
      if factors_CFA == len(self.factors_names):
        Test_lenght = True

      filter_covar = (abs(covar.values)  > 0.5  )
      correlation_covar = len((covar.loc[: , filter_covar].columns))
      correlation_covar = correlation_covar -   factors_CFA   
      if Test_lenght == True and correlation_covar == 0 :
        Interpretation_CFA = 'Conformatory Factor Analysis Result: Confirmed '
      else : 
        Interpretation_CFA = 'Conformatory Factor Analysis Result: Not Confirmed '

      
      return Interpretation_CFA , covar , loadings_CFA 

    # ======= Applying H2O =================

      # ======= functions to transform data =================

    def inpute_numercial_variables(self,data):
      
      for variable in self.numerical_variables_to_inpute: 
        mean_impute = data.impute(variable, method = "mean")   
      return data
    def inpute_categorical_variables(self,data,target): 
      
      for variable in self.categorical_variables_to_inpute: 
        mode_impute = data.impute(variable,method="mode",by=[target])
      return data


    def fit(self,data,target):
      data = data[:, self.factors_names]
      self.train = h2o.H2OFrame(self.train)
      self.test = h2o.H2OFrame(self.test)
      data = self.inpute_categorical_variables(data,target)
      data = self.inpute_numercial_variables(data)
      self.train, self.test = data.split_frame(ratios=[.75])
      # Identify predictors and response
      self.x = self.factors_names
      self.y = target
      self.x.remove(self.y)
      #print(data.anyfactor())
      # For binary classification, response should be a factor
      self.train[self.y] = self.train[self.y].asfactor()
      self.test[self.y] = self.test[self.y].asfactor()
     
      return self  
 
   #Starting TRaining 
   #   
    def run_model(self):
      # Run AutoML for 20 base models (limited to 1 hour max runtime by default)
      
      
      self.aml.train(x=self.x, y=self.y, training_frame=self.train)
      # View the AutoML Leaderboard
      lb = self.aml.leaderboard
      lb_view = lb.head(rows=lb.nrows)
      #lb_view = h2o.as_list(lb_view, header=True)
      return lb_view  # Print all rows instead of default (10 rows)

    #model performance in training set

    def model_performance_train_data(self):
      
      model_ids = list(self.aml.leaderboard['model_id'].as_data_frame().iloc[:,0])
      first_model = model_ids[0]
      #first_model = model_ids[0].split("_", 1)
      #model_leader = first_model[0]
      details = h2o.get_model(first_model)
      
      return details 
  #Predicitions 

    def predict(self):
      preds = self.aml.predict(self.test)
      #preds = h2o.as_list(preds, header=True)
      return preds

    #model performance in predictions 
    def model_performance_prediction(self):
      model_performance = self.aml.leader.model_performance(self.test) 
      
      return model_performance
