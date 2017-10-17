'''
extractor.py

	extract an English word list from a csv database generated from http://elexicon.wustl.edu/default.asp
	set parameters "Word","I_Mean_RT","I_Mean_Accuracy" on website

'''

import csv
from math import log

def m(n):
	return 1/n

def score(reaction, accuracy):
	if accuracy == 0.00:
		accuracy = 0.005
	return (reaction*m(accuracy))

with open("wordz3.csv", "r") as r:
	csv_r = csv.reader(r, delimiter=',', quotechar='"')
	next(csv_r)
	sortedbydiff = sorted(csv_r, key=lambda row: score(float(row[1]),float(row[2])))
for row in sortedbydiff:
	if not ("'" in row[0] or any(c.isupper() for c in row[0])):
		#print("%s,%s" % (row[0],score(float(row[1]),float(row[2]))))
		print("%s,%s,%s,%s,%.2f" % (row[0],row[1],row[2],score(float(row[1]),float(row[2])), (m(float(row[2])))))