import csv
import pandas as pd

filename = 'restaurants.csv'

districts = []

with open(filename, 'r') as csvfile:
  datareader = csv.reader(csvfile)
  for row in datareader:
    li = row[-1].strip('][').split(', ')
    for i in range(len(li)):
      li[i] = li[i].replace("'", "")
    for item in li:
      if districts.count(item) == 0 and item != 'Districts':
        districts.append(item)

df = pd.DataFrame({'Districts': districts}) 
df.to_csv('districts.csv', index=False, encoding='utf-8')