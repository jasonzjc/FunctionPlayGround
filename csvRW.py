# -------------------------------------------------- #
#  Jeff Zhao
#  11/05/3017
#
#  show how to real and write CSV file, by using csv
#  library
# -------------------------------------------------- #

import csv

# open a file for writing
# use wb for binary
csv_out = open('mycsv.csv','wb')

# create csv writer object
mywriter = csv.writer(csv_out)

