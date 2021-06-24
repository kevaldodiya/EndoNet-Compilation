import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
driver = webdriver.Firefox(firefox_binary=binary, executable_path=r'C:\\geckodriver.exe')

def Union(lst1, lst2):
	final_list = list(set(lst1) | set(lst2))
	return final_list

def Diff(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))

def H_for(end_id):

	driver.get('http://endonet.sybig.de/search/')
	element = driver.find_element_by_id("searchForm:searchInput")
	element.send_keys(end_id)
	element.send_keys(Keys.ENTER)
	timeout = 5

	try:
		element_present = EC.presence_of_element_located((By.ID, 'element_id'))
		WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
		print ("Timed out")
	driver.switch_to_window(driver.window_handles[0])

	names = driver.find_elements_by_xpath("//h1")
	final_name,compo_k,compo_uni = 'empty0',[],[]
	uniprot,ensembl,kegg,lipid_map,lipid_bank = 'empty0','empty0','empty0','empty0','empty0'
	for name in names:
		n1 = name.text.split(": ")
		if n1[0] == 'Details for messenger / hormone':
			final_name = n1[1]

	comps = driver.find_elements_by_id('hormoneForm:j_idt82')
	if len(comps)>0: 
		comps1 = comps[0].find_elements_by_xpath('.//a[@href]')
		for c1 in comps1:
			c2 = c1.get_attribute("href").split('/')
			if c2[3] == 'uniprot':
				compo_uni.append(c1.text)
				continue
			if c2[2] == 'www.genome.jp':
				compo_k.append(c1.text)
	
	elements = 'empty0'
	elements = driver.find_elements_by_xpath('//div[4]/div[1]/form/table[2]')
	if len(elements)<=0 or elements == 'empty0':
		print('not loaded')
		return final_name,compo_k,compo_uni,uniprot,ensembl,kegg,lipid_map,lipid_bank,1
	else:
		elems = elements[0].find_elements_by_xpath('.//a[@href]')
		for el in elems:
			ls = el.get_attribute('href').split('/')
			if ls[3] == 'uniprot':
				uniprot = el.text
				continue
			if ls[2] == 'www.ensembl.org':
				ensembl = el.text
				continue
			if ls[2] == 'www.genome.jp':
				kegg = el.text
				continue
			if ls[2] == 'www.lipidmaps.org':
				lipid_map = el.text
				continue
			if ls[2] == 'lipidbank.jp':
				lipid_bank = el.text
				continue

		return final_name,compo_k,compo_uni,uniprot,ensembl,kegg,lipid_map,lipid_bank,0

def resolve(ls1):
	final_ls = []
	for element in ls1:
		if element == '[]':
			continue
		templist = [re.sub('[^A-Za-z0-9]+', '', x) for x in element.split(', ') ]
		final_ls = final_ls + templist
	return final_ls


def add_data():
	d1 = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_H_final.csv')
	d1 = d1.drop(columns = ['Unnamed: 0.1'])
	avail_hormones = d1['Endo_id'].tolist()
	d2 = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_R.csv')
	d3 = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_T.csv')
	final_ls = Diff( list(set(resolve(d2['binding_hormones'].tolist()) + resolve(d3['Transported hormone'].tolist()))) , list(set(avail_hormones)) )
	final_ls.sort()
	print("sorting finished")
	ls_H =[]
	ls_H_finished = []
	not_loaded = []
	i =0

	starting =0
	total =0
	f = 0

	for ind in range(len(final_ls)):
		el = final_ls[ind]
		if el[2] == 'H':
			total = total+1
			if f == 0:
				f=1
				starting = ind

	for ind in range(0,len(final_ls)):
		el = final_ls[ind]
		i = i +1
		if i%4 == 0:
			print((i-starting)/float(total)*100 )
			
		if el[2] == 'H':
			driver.delete_all_cookies()
			name,compo_k,compo_uni,uniprot,ensembl,kegg,lipid_map,lipid_bank,flag = H_for(el)

			ls_H.append([el,name,compo_k,compo_uni,uniprot,ensembl,kegg,lipid_map,lipid_bank ])
			temp = pd.DataFrame(ls_H, columns = ['Endo_id','name','compo_kegg','compo_uni','uniprot','ensembl','kegg','lipid_map','lipid_bank' ])
			ls_H_finished.append([el,ind])
			temp1 = pd.DataFrame(ls_H_finished,columns = ['Endo_id','index'])
			temp.to_csv('G:\\Dataset\\Endo_types\\EndoNet_H_2.csv')
			temp1.to_csv('G:\\Dataset\\Endo_types\\EndoNet_H_finished_ind_2.csv')
		else:
			print("out of syllabus",el)


def empty_resolve():
	d1 = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_H_final.csv')
	d1 = d1.drop(columns= ['Unnamed: 0'])
	inds =  d1.index[d1['name'] == 'empty0'].tolist()

	for ind in inds:
		driver.delete_all_cookies()
		name,compo_k,compo_uni,uniprot,ensembl,kegg,lipid_map,lipid_bank,flag = H_for(d1.at[ind,'Endo_id'])
		d1.at[ind,'name'] = name
		d1.at[ind,'compo_kegg'] = compo_k
		d1.at[ind,'compo_uni'] = compo_uni
		d1.at[ind,'uniprot'] = uniprot
		d1.at[ind,'ensembl'] = ensembl
		d1.at[ind,'kegg'] = kegg
		d1.at[ind,'lipid_map'] = lipid_map
		d1.at[ind,'lipid_bank'] = lipid_bank
		d1.to_csv('G:\\Dataset\\Endo_types\\EndoNet_H_final.csv')
def get_data():
	d1 = pd.read_csv('G:\\Dataset\\EndoNet_P_resolve.csv')
	d1 = d1.drop(columns= ['Unnamed: 0'])
	d2 = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_C.csv')
	d2 = d2.drop(columns= ['Unnamed: 0'])
	d3 = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_S_v2.csv')
	d3 = d3.drop(columns= ['Unnamed: 0'])

	ls1 = d1['c1'].tolist()
	ls2 = d1['c2'].tolist()
	final_ls = Union(ls1,ls2)
	final_ls = list(set(final_ls + d3['sec_hormone'].tolist() + resolve(d2['sec_hormones'].tolist())))
	final_ls.sort()
	print("sorting finished")
	ls_H =[]
	ls_H_finished = []
	not_loaded = []
	i =3301

	starting =0
	total =0
	f = 0

	for ind in range(len(final_ls)):
		el = final_ls[ind]
		if el[2] == 'H':
			total = total+1
			if f == 0:
				f=1
				starting = ind

	for ind in range(3302,len(final_ls)):
		el = final_ls[ind]
		i = i +1
		if i%4 == 0:
			print((i-starting)/float(total)*100 )

		if el[2] == 'C':
			print("finished C")

		elif el[2] == 'D':
			print("left D")
		
		elif el[2] == 'S':
			print("left S")

		elif el[2] == 'H':
			driver.delete_all_cookies()
			name,compo_k,compo_uni,uniprot,ensembl,kegg,lipid_map,lipid_bank,flag = H_for(el)

			if flag ==1:
				not_loaded.append(el)
				t1 = pd.DataFrame(not_loaded,columns=['Endo_id'])
				t1.to_csv('G:\\Dataset\\Endo_types\\EndoNet_H_not_loaded_2.csv')

			ls_H.append([el,name,compo_k,compo_uni,uniprot,ensembl,kegg,lipid_map,lipid_bank ])
			temp = pd.DataFrame(ls_H, columns = ['Endo_id','name','compo_kegg','compo_uni','uniprot','ensembl','kegg','lipid_map','lipid_bank' ])
			ls_H_finished.append([el,ind])
			temp1 = pd.DataFrame(ls_H_finished,columns = ['Endo_id','index'])
			temp.to_csv('G:\\Dataset\\Endo_types\\EndoNet_H_2.csv')
			temp1.to_csv('G:\\Dataset\\Endo_types\\EndoNet_H_finished_ind_2.csv')

		elif el[2] == 'I':
			print("left I")

		elif el[2] == 'T':
			print("left T")

		elif el[2] == 'R':
			print("left R")

		elif el[2] == 'Q':
			print("left Q")

		else:
			print("out of syllabus",el)

def testing(end_id):
	driver.delete_all_cookies()
	name,compo_k,compo_uni,uniprot,ensembl,kegg,lipid_map,lipid_bank,flag = H_for(end_id)
	
	print(name)
	print(compo_k)
	print(compo_uni)
	print(uniprot)
	print(ensembl)
	print(kegg)
	print(lipid_bank)
	print(lipid_map)
	
#testing('ENH00276')
#get_data()
#empty_resolve()
add_data()
print('finished')
