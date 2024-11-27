# Import package
import pandas as pd
# install xlrd

# Assign url of file: url
url = 'https://assets.datacamp.com/course/importing_data_into_r/latitude.xls'

# Read in all sheets of Excel file: xls
df = pd.read_excel(url, sheet_name=None)

# Print the sheetnames to the shell
print(df.keys())

# Print the head of the first sheet (using its name, NOT its index)

print(df['1700'].head())