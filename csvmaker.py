import pandas as pd

data = {
    'Empno': [2],
    'Empname': ['Ankit'],
    'Job': ['HR'],
    'Deptno': [2]
}

df = pd.DataFrame(data)
df.to_csv('employee_data.csv', index=False)
print("CSV file created: employee_data.csv")