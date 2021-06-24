import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
#driver = webdriver.Firefox(firefox_binary=binary, executable_path=r'C:\\geckodriver.exe')

def resolve(ls1):
	final_ls = []
	for element in ls1:
		if element == '[]':
			continue
		templist = [re.sub('[^A-Za-z0-9]+', '', x) for x in element.split(', ') ]
		final_ls = final_ls + templist
	return final_ls

def res1(element):
	return [re.sub('[^A-Za-z0-9-]+', '', x) for x in element.split(', ') ]

def uni_for(end_id):
	driver.get('https://www.uniprot.org/')
	element = driver.find_element_by_id("query")
	element.send_keys(end_id)
	element.send_keys(Keys.ENTER)
	timeout = 5

	try:
		element_present = EC.presence_of_element_located((By.ID, 'element_id'))
		WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
		print ("Timed out")
	driver.switch_to_window(driver.window_handles[0])
	
	name = 'empty0'
	comps = driver.find_elements_by_id('content-gene')
	if len(comps)>0:
		elems = comps[0].find_elements_by_tag_name('h2')
		name = elems[0].text
	
	return name

def uni_name():
	r = pd.read_csv('G:\\Dataset\\Endo_types\\final_resolve_2.csv')
	uniprots = list(set(resolve(r['hor_uniprot'].tolist()) + resolve(r['hor_uniprot'].tolist())))

	fp = open('test1.txt','a')
	for item in uniprots:
		if item == 'empty0':
			continue

		fp.write(item+'\n')

	fp.close()

def check_mapping():
	r = pd.read_csv('G:\\Dataset\\Endo_types\\final_resolve_2.csv')
	fp = open('G:\\Dataset\\Endo_types\\resolve.txt','r')
	dir1 = {}
	for item in fp.readlines():
		ls = item.strip().split("\t")
		if ls[0] == 'From':
			continue
		dir1[ls[0]] = ls[1]
	check_gene = []
	for item in r['hor_uniprot'].tolist():
		if item == 'empty0':
			continue

		if item[0] == '[':
			for i1 in res1(item):
				if i1 not in dir1:
					check_gene.append(i1)
			continue
		if item not in dir1:
			check_gene.append(item)

	for item in r['rec_uniprot'].tolist():
		if item == 'empty0':
			continue

		if item[0] == '[':
			for i1 in res1(item):
				if i1 not in dir1:
					check_gene.append(i1)
			continue
		if item not in dir1:
			check_gene.append(item)

	return list(set(check_gene)) 

def add_name():
	r = pd.read_csv('G:\\Dataset\\Endo_types\\final_resolve_2.csv')
	fp = open('G:\\Dataset\\Endo_types\\resolve.txt','r')
	dir1 = {}
	for item in fp.readlines():
		ls = item.strip().split("\t")
		if ls[0] == 'From':
			continue
		dir1[ls[0]] = ls[1]
	hor_gene_name = []
	for item in r['hor_uniprot'].tolist():
		if item == 'empty0':
			hor_gene_name.append('empty0')
			continue

		if item[0] == '[':
			hor_gene_name.append([dir1[x] for x in res1(item)])
			continue
		hor_gene_name.append(dir1[item])
	r['new1'] = hor_gene_name
	r.to_csv('G:\\Dataset\\Endo_types\\ex1.csv')

def final_resolve():
	r = pd.read_csv('G:\\Dataset\\Endo_types\\resolve_left_2.csv')
	for ind in range(len(r)):
		if r.at[ind,'to'] == 'empty0':
			r.at[ind,'to'] = uni_for(r.at[ind,'from'])
			r.to_csv('G:\\Dataset\\Endo_types\\resolve_left_2.csv')	


def res_empty():
	ls = check_mapping()
	ls.sort()
	i =0
	ans = []
	for uni in ls:
		i = i+1
		driver.delete_all_cookies()
		if i%4 == 0:
			print(i/len(ls)*100)
		name = uni_for(uni)
		ans.append([uni,name])
		d1 = pd.DataFrame(ans,columns = ['from','to'])
		d1.to_csv('G:\\Dataset\\Endo_types\\resolve_left_2.csv')

def add_column():
	d1 = pd.read_csv('G:\\Dataset\\Endo_types\\final_resolve_2.csv')
	d1 = d1.drop(columns= ['Unnamed: 0'])
	d2 = pd.read_csv('G:\\Dataset\\Endo_types\\resolve_left_2.csv')
	d2 = d2.drop(columns= ['Unnamed: 0'])
	fp = open('G:\\Dataset\\Endo_types\\resolve.txt','r')
	dir1 = {}
	for item in fp.readlines():
		ls = item.strip().split("\t")
		if ls[0] == 'From':
			continue
		dir1[ls[0]] = ls[1]

	for ind in range(len(d2)):
		dir1[d2.at[ind,'from']] = d2.at[ind,'to']

	hor_gene_name = []
	for item in d1['hor_uniprot'].tolist():
		if item == 'empty0':
			hor_gene_name.append('empty0')
			continue

		if item[0] == '[':
			temp = []
			for i1 in res1(item):
					temp.append(dir1[i1])
			hor_gene_name.append(temp)
			continue

		hor_gene_name.append(dir1[item])

	rec_gene_name = []
	for item in d1['rec_uniprot'].tolist():
		if item == 'empty0':
			rec_gene_name.append('empty0')
			continue

		if item[0] == '[':
			temp = []
			for i1 in res1(item):
					temp.append(dir1[i1])
			rec_gene_name.append(temp)
			continue

		rec_gene_name.append(dir1[item])
	d1['hor_gene_name'] = hor_gene_name
	d1['rec_gene_name'] = rec_gene_name
	cols = ['hor_cell_id','hor_cell_name','hor_id','hor_name','hor_ensembl','hor_uniprot','hor_gene_name',
			'rec_id','rec_name','rec_ensembl','rec_uniprot','rec_gene_name','rec_cell_id','rec_cell_name']
	d1 = d1[cols]
	d1.to_csv('G:\\Dataset\\Endo_types\\testing_2.csv')


#res_empty()
#final_resolve()
add_column()
print("finished")