PATH_TO_DATASET_EFA = "data_f_most_frequent_encoded.xlsx"
PATH_TO_DATASET_AutoML = "cleaned_dff.csv"                    
TARGET = 'contract_suspect'
ROTATION_Type = "varimax"
# Not inculde correlated ones 
FEATURES = ['amount_national_currency', 'transaction_suspect', 'transaction_type',
       'contract_suspect', 'account_status', 'birth_place', 'citizenship',
       'nationality', 'profession', 'current_risk_rate', 'residence',
       'techniques_label', 'pays_emission_value', 'capacite_juridique',
       'id_delivery_place', 'categories_clientele_label', 'form_status',
       'is_pep']
categorical_variables_to_inpute = ['citizenship']
numerical_variables_to_inpute = ['current_risk_rate']
max_runtime_secs = 600
