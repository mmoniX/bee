# test_import.py
from df_to_pg import DataSource
from project import BeeData

print(DataSource)
print(BeeData)
fe = BeeData()
df = fe.run()
print(df.dtypes)



