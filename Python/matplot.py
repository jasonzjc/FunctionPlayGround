# -------------------------------------------------- #
#  Jeff Zhao
#  11/10/3017
#
#  show how to use matplot to draw plots
# -------------------------------------------------- #

import csv
from matplotlib.pyplot import plot, title, show, grid, xlabel, ylabel

## read the csv fle
csv_in = open('mycsv.csv','rb')
myreader = csv.reader(csv_in)
index_rd, name_rd, value_rd = zip(*myreader)

index_rd = map(int, index_rd)
value_rd = map(float, value_rd)

plot(index_rd,value_rd,'r-')
title('try to plot')
xlabel('index')
ylabel('value')
grid()
show()
