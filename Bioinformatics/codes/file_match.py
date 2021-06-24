import pandas as pd
import re
from operator import itemgetter
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

endonet = pd.read_csv('G:\\Dataset\\Endo_types\\final_resolve_3.csv')
coex_edges = pd.read_csv('G:\\Dataset\\Endo_types\\final_inter_edges_pan_mus.csv')
fp = open('G:\\Dataset\\Endo_types\\pancreas.txt')
pan_tissues = []
for line in fp.readlines():
	pan_tissues.append(line.split(','))
pan_tissues = pan_tissues[0]
fp.close()

fp = open('G:\\Dataset\\Endo_types\\sk_muscle.txt')
mus_tissues = []
for line in fp.readlines():
	mus_tissues.append(line.split(','))
mus_tissues = mus_tissues[0]
fp.close()
endonet_edges = []
'''
fp = open('G:\\Dataset\\Endo_types\\liver.txt')
liv_tissues = []
for line in fp.readlines():
	liv_tissues.append(line.split(','))
liv_tissues = liv_tissues[0]
fp.close()
#print(liv_tissues)
#print(endonet.head())

'''

'''
fp = open('G:\\Dataset\\Endo_types\\source.txt','r')
lst =[]
for line in fp:
  ls = line.split(", ")
  lst.append(ls)
lst = lst[0]
lst1 = [x.replace('"','').upper() for x in lst]
s = lst1.copy()
#s= s + [x + 'L' for x in s]
#print(s,len(s))
t1 = pd.DataFrame(s,columns = ['source'])
t1.to_csv('source.csv')
fp = open('G:\\Dataset\\Endo_types\\target.txt','r')
lst =[]
for line in fp:
  ls = line.split(", ")
  lst.append(ls)
lst = lst[0]
lst1 = [x.replace('"','').upper() for x in lst]
t = lst1.copy()
t1 = pd.DataFrame(t,columns = ['target'])
t1.to_csv('target.csv')

ins_endo_edges = []
for edge in endonet_edges:
	if edge[0] not in source_list:
		continue
	if edge[1] in target_list:
		ins_endo_edges.append(edge)

print(ins_endo_edges,len(ins_endo_edges))
'''
source = pd.read_csv('G:\\Dataset\\Endo_types\\source.csv')
target = pd.read_csv('G:\\Dataset\\Endo_types\\target.csv')
source_list = source['source'].tolist()
target_list = target['target'].tolist()
for ind in range(len(endonet)):
	if ind%1000 == 0:
		print(ind/len(endonet)*100)

	hor_cell_name = endonet.at[ind,'hor_cell_name']
	rec_cell_name = endonet.at[ind,'rec_cell_name']
	flag =0
	for st in pan_tissues:
		if re.search(hor_cell_name,st):
			flag = 1
			break
	if flag == 0:
		continue
	
	flag =0
	for st in mus_tissues:
		if re.search(rec_cell_name,st):
			flag = 1
			break

	if flag == 0:
		continue

	endonet_edges.append((endonet.at[ind,'hor_gene_name'],endonet.at[ind,'rec_gene_name']))

endonet_edges = list(set(endonet_edges))
e_temp = []
for item in endonet_edges:
	if item[0] == 'empty0' or item[1] == 'empty0':
		continue
	e_temp.append(item)

endonet_edges = e_temp
d_temp = pd.DataFrame(endonet_edges,columns = ['e1','e2'])
d_temp.to_csv("endonet_edges_pan_mus.csv")
t = []
temp = pd.DataFrame(t,columns = ['e1','e2'])
temp.to_csv("testing.csv")
co_ed_ls = []
for ind in range(len(coex_edges)):
	co_ed_ls.append((coex_edges.at[ind,'e1'], coex_edges.at[ind,'e2'][:-1] ))

print(endonet_edges,len(endonet_edges))
#print(co_ed_ls, len(co_ed_ls))
ex = intersection(co_ed_ls,endonet_edges)
ls_temp = []
for item in ex:
	ls_temp.append([item[0],item[1]])
'''
d1 = pd.DataFrame(ls_temp,columns = ['e1','e2'])
d1.to_csv("G:\\Dataset\\Endo_types\\end_common_edges.csv")
'''
ex = [list(x) for x in ex]
print(ex,len(ex))
common_inter_edges_coex_endo = pd.DataFrame(ex,columns=['e1','e2'])
common_inter_edges_coex_endo.to_csv("common_inter_edges_coex_endo.csv")
#print(list(set(endonet_test_s)),endonet_test_t)