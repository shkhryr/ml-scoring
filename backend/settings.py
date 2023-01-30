PROJECT_NAME = 'scoring'

COLUMNS = [
    'client_id', 'gender', 'age', 'marital_status', 'job_position', 'credit_sum',
    'credit_month', 'tariff_id', 'score_shk', 'education', 'living_region',
    'monthly_income', 'credit_count', 'overdue_credit_count', 'open_account_flg'
]
CONTINUOUS_FEATURES = [
    'overdue_credit_count', 'credit_sum', 'credit_month', 'monthly_income', 'score_shk', 'open_account_flg'
]

CATEGORICAL_FEATURES = [
    'gender', 'marital_status', 'job_position', 'education', 'tariff_id', 'living_region'
]

PATH = "model/main/credit_train.csv"
