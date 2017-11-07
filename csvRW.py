# -------------------------------------------------- #
#  Jeff Zhao
#  11/05/3017
#
#  show how to real and write CSV file, by using csv
#  library
# -------------------------------------------------- #

import csv

# ------------------------------------------------
# read a csv file
# content for the csv file
index = ['123','4','6']
name = ['NC','TN','MD']
value = ['23','22.5','27']

## write row by row --------------------------------
# open a file for writing
# use wb for binary
csv_out = open('mycsv.csv','wb')

# create a csv writer object
mywriter = csv.writer(csv_out)
# to change the delimiter to, e.g., tab, use mywriter = csv.writer(csv_out, delimiter ='\t')

# write row by row
for row in zip(index, name, value):
    mywriter.writerow(row)

csv_out.close()

## write a cluster of rows ------------------------
# open a file for writing
# use wb for binary
csv_out = open('mycsv.csv','wb')

# create a csv writer object
mywriter = csv.writer(csv_out)

# write a cluster of rows
rows = zip(index, name, value)
mywriter.writerows(rows)

# close the file otherwise it is empty
csv_out.close()

# ------------------------------------------------
# read a csv file

# lists to store the columns
index_rd = []
name_rd = []
value_rd = []

## read row by row --------------------------------
# create a csv reader object
csv_in = open('mycsv.csv','rb')

# create a csv reader object
myreader = csv.reader(csv_in)

# read row by row
# all variables are read as strings from csv. need to convert to corresponding type
for row in myreader:
    id_temp, name_temp, value_temp = row
    index_rd.append(id_temp)
    name_rd.append(name_temp)
    value_rd.append(float(value_temp))

# close csv file
csv_in.close()

## read all rows togeter --------------------------
# create a csv reader object
csv_in = open('mycsv.csv','rb')

# create a csv reader object
myreader = csv.reader(csv_in)

# read all rows together
# zip(*) transpose a list of rows into a list of coloumns
index_rd, name_rd, value_rd = zip(*myreader)


# map convert every item in the list into float
value_rd = map(float, value_rd)

# value_rd is converted to list by map, but index_rd and name_rd are still tuple since zip output tuple
# convert tuple into list
print 'Type of index_id is', type(index_rd)
print 'Convert to list...'
index_rd = list(index_rd)	
name_rd= list(name_rd)

print index_rd
print name_rd
print value_rd

print 'Type of index_id now is', type(index_rd)

# close csv file
csv_in.close()