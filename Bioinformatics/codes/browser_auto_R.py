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

def uni_for(end_id):
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
	uniprot = []
	comps = driver.find_elements_by_id('j_idt20:j_idt73')
	if len(comps)>0:
		elems = comps[0].find_elements_by_xpath('.//a[@href]')
		for elem in elems:
			c2 = elem.get_attribute('href').split('/')
			if c2[3] == 'uniprot':
				uniprot.append(elem.text)
	return uniprot

def R_for(end_id):

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
	final_name,ana_st,binding_hormones = 'empty0',[],[]
	uniprot,ensembl = 'empty0','empty0'

	names = driver.find_elements_by_xpath("//h1")
	for name in names:
		n1 = name.text.split(": ")
		if n1[0] == 'Details for receptor':
			final_name = n1[1]

	comps = driver.find_elements_by_xpath('//div[4]/div[1]/form/table/tbody')
	if len(comps)>0: 
		comps1 = comps[0].find_elements_by_xpath('.//a[@href]')
		for c1 in comps1:
			c2 = c1.get_attribute("href").split('/')
			print(c2)
			if c2[3] == 'uniprot':
				uniprot = c1.text
				continue
			if c2[2] == 'www.ensembl.org':
				ensembl = c1.text

	#print(uniprot,ensembl)
	comps = driver.find_elements_by_id('j_idt20:j_idt89_list')
	if len(comps)>0:
		elems = comps[0].find_elements_by_xpath('.//a[@href]')
		for elem in elems:
			c2 = elem.get_attribute("href").split('/')
			if c2[3] == 'hormone':
				binding_hormones.append(c2[4])
	#print(binding_hormones)
	comps = driver.find_elements_by_id('j_idt20:j_idt118_list')
	if len(comps)>0:
		elems = comps[0].find_elements_by_xpath('.//h3')
		for elem in elems:
			els = elem.find_elements_by_xpath('.//a[@href]')
			c2 = els[0].get_attribute("href").split('/')
			if c2[3] == 'cell':
				ana_st.append(c2[4])

	#print(ana_st)
	return final_name,uniprot,ensembl,binding_hormones,ana_st
	

def resolve(ls1):
	final_ls = []
	for element in ls1:
		if element == '[]':
			continue
		templist = [re.sub('[^A-Za-z0-9]+', '', x) for x in element.split(', ') ]
		final_ls = final_ls + templist
	return final_ls

def empty_resolve():
	d1 = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_R.csv')
	d1 = d1.drop(columns= ['Unnamed: 0'])
	inds =  d1.index[d1['name'] == 'empty0'].tolist()

	for ind in inds:
		driver.delete_all_cookies()
		name,uniprot,ensembl,binding_hormones,ana_st = R_for(d1.at[ind,'Endo_id'])
		d1.at[ind,'name'] = name
		d1.at[ind,'uniprot'] = uniprot
		d1.at[ind,'ensembl'] = ensembl
		d1.at[ind,'binding_hormones'] = binding_hormones
		d1.at[ind,'anatomical structure'] = ana_st
		d1.to_csv('G:\\Dataset\\Endo_types\\EndoNet_R.csv')

def uniprot_resolve():
	d1 = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_R.csv')
	d1 = d1.drop(columns= ['Unnamed: 0'])
	inds =  d1.index[d1['uniprot'] == 'empty0'].tolist()
	for ind in inds:
		driver.delete_all_cookies()
		uniprot = uni_for(d1.at[ind,'Endo_id'])
		d1.at[ind,'uniprot'] = uniprot
		d1.to_csv('G:\\Dataset\\Endo_types\\EndoNet_R.csv')

def add_data():
	'''
	d1 = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_R.csv')
	d1 = d1.drop(columns = ['Unnamed: 0'])
	avail_hormones = d1['Endo_id'].tolist()
	d2 = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_Q.csv')
	d3 = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_H_info.csv')
	final_ls = Diff( list(set(resolve(d2['receptor'].tolist()) + resolve(d3['receptor_id'].tolist()))) , list(set(avail_hormones)) )
	'''
	d1 = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_R.csv')
	h_tar = pd.read_csv("G:\\Dataset\\Endo_types\\EndoNet_H_target.csv")
	ls = [x for x in h_tar['target_receptor'].tolist() if x != 'empty0']
	final_ls = Diff( ls , d1['Endo_id'].tolist())
	final_ls.sort()
	print("sorting finished")
	ls_R =[]
	ls_R_finished = []
	i =0

	for ind in range(0,len(final_ls)):
		el = final_ls[ind]
		i = i +1
		if i%4 == 0:
			print(i/len(final_ls)*100 )

		if el[2] == 'R':
			driver.delete_all_cookies()
			name,uniprot,ensembl,binding_hormones,ana_st = R_for(el)
			ls_R.append([el,name,uniprot,ensembl,binding_hormones,ana_st ])
			temp = pd.DataFrame(ls_R, columns = ['Endo_id','name','uniprot','ensembl','binding_hormones','anatomical structure'])
			ls_R_finished.append([el,ind])
			temp1 = pd.DataFrame(ls_R_finished,columns = ['Endo_id','index'])
			temp.to_csv('G:\\Dataset\\Endo_types\\EndoNet_R_2.csv')
			temp1.to_csv('G:\\Dataset\\Endo_types\\EndoNet_R_ind_2.csv')

		else:
			print("out of syllabus",el)
def get_data():
	d_main = pd.read_csv('G:\\Dataset\\EndoNet_P_resolve.csv')
	d_main = d_main.drop(columns= ['Unnamed: 0'])

	d_c = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_C.csv')
	d_c = d_c.drop(columns= ['Unnamed: 0'])

	d_d = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_D_v2_final.csv')
	d_d = d_d.drop(columns= ['Unnamed: 0'])

	d_i = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_I.csv')
	d_i = d_i.drop(columns= ['Unnamed: 0'])

	d_t = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_T.csv')
	d_t = d_t.drop(columns= ['Unnamed: 0'])

	ls1 = d_main['c1'].tolist()
	ls2 = d_main['c2'].tolist()
	final_ls = Union(ls1,ls2)
	final_ls = list(set(final_ls + d_d['receptor'].tolist() + resolve(d_c['receptors'].tolist()) + d_i['Influenced by receptor'].tolist() + d_t['Target receptor'].tolist() ) )
	final_ls.sort()
	print("sorting finished")
	ls_R =[]
	ls_R_finished = []
	i =0

	starting =0
	total =0
	f = 0

	for ind in range(len(final_ls)):
		el = final_ls[ind]
		if el[2] == 'R':
			total = total+1
			if f == 0:
				f=1
				starting = ind

	for ind in range(0,len(final_ls)):
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
			print('done H')

		elif el[2] == 'I':
			print("left I")

		elif el[2] == 'T':
			print("left T")

		elif el[2] == 'R':
			driver.delete_all_cookies()
			name,uniprot,ensembl,binding_hormones,ana_st = R_for(el)
			ls_R.append([el,name,uniprot,ensembl,binding_hormones,ana_st ])
			temp = pd.DataFrame(ls_R, columns = ['Endo_id','name','uniprot','ensembl','binding_hormones','anatomical structure'])
			ls_R_finished.append([el,ind])
			temp1 = pd.DataFrame(ls_R_finished,columns = ['Endo_id','index'])
			temp.to_csv('G:\\Dataset\\Endo_types\\EndoNet_R.csv')
			temp1.to_csv('G:\\Dataset\\Endo_types\\EndoNet_R_ind.csv')

		elif el[2] == 'Q':
			print("left Q")

		else:
			print("out of syllabus",el)

def testing(end_id):
	name,uniprot,ensembl,binding_hormones,ana_st = R_for(end_id)
	print(name)
	print(uniprot)
	print(ensembl)
	print(binding_hormones)
	print(ana_st)

	
#testing('ENR01104')
#get_data()
##empty_resolve()
#uniprot_resolve()
ans = uni_for('ENR01104')
print(ans)
print('finished')
