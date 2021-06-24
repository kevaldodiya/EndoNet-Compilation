import pandas as pd
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


def Q_for(end_id):
	driver.get('http://endonet.sybig.de/search/')
	element = driver.find_element_by_id("searchForm:searchInput")
	element.send_keys(end_id)
	element.send_keys(Keys.ENTER)
	timeout = 4

	try:
		element_present = EC.presence_of_element_located((By.ID, 'element_id'))
		WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
		print ("Timed out")

	driver.switch_to_window(driver.window_handles[0])
	receptor,cell,phenotype,activity = 'empty0','empty0','empty0','empty0'
	elms = driver.find_elements_by_xpath('//h1')
	for el in elms:
		ls = el.text.split(': ')
		if ls[0] == 'Details for phenotype trigger':
			activity = ls[1]
	
	els = driver.find_elements_by_xpath('//a[@href]')
	for elem in els:
		ls = elem.get_attribute("href").split('/')
		if ls[0] == 'javascript:void(0)':
			continue

		if ls[3] == 'receptor' and ls[4][:2] == 'EN':
			receptor = ls[4]
			continue

		if ls[3] == 'cell' and ls[4][:2] == 'EN':
			cell = ls[4]
			continue
		if ls[3] == 'phenotype':
			phenotype = ls[4]
			break
	
	return receptor,cell,phenotype,activity 

def get_data():
	d1 = pd.read_csv('G:\\Dataset\\EndoNet_P_resolve.csv')
	d1 = d1.drop(columns= ['Unnamed: 0'])
	ls1 = d1['c1'].tolist()
	ls2 = d1['c2'].tolist()
	final_ls = Union(ls1,ls2)
	final_ls.sort()
	print("sorting finished")

	ls_Q =[]
	ls_Q_finished = []
	i =0

	starting =0
	total =0
	f = 0

	for ind in range(len(final_ls)):
		el = final_ls[ind]
		if el[2] == 'Q':
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
			print("Done C")

		elif el[2] == 'D':
			print('Done D')

		elif el[2] == 'S':
			print("Done S")

		elif el[2] == 'H':
			print("Done H")

		elif el[2] == 'I':
			print('Done I')

		elif el[2] == 'T':
			print("Done T")

		elif el[2] == 'R':
			print("left R")

		elif el[2] == 'Q':
			driver.delete_all_cookies()
			receptor,cell,phenotype,activity  = Q_for(el)
			ls_Q.append([el,receptor,cell,phenotype,activity  ])
			temp = pd.DataFrame(ls_Q, columns = ['Endo_id','receptor','cell','phenotype','activity' ])
			ls_Q_finished.append([el,ind])
			temp1 = pd.DataFrame(ls_Q_finished,columns = ['Endo_id','index'])
			temp.to_csv('G:\\Dataset\\Endo_types\\EndoNet_Q.csv')
			temp1.to_csv('G:\\Dataset\\Endo_types\\EndoNet_Q_ind.csv')

		else:
			print("out of syllabus",el )

def testing(end_id):
	receptor,cell,phenotype,activity  = Q_for(end_id)
	print(receptor)
	print(cell)
	print(phenotype)
	print(activity)


def empty_resolve():
	d1 = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_T.csv')
	d1 = d1.drop(columns= ['Unnamed: 0'])
	inds =  d1.index[d1['Transported hormone'] == 'empty0'].tolist()
	i =0
	for ind in inds:
		el = d1.at[ind,'Endo_id']
		i = i +1
		if i%4 == 0:
			print(i/len(inds))

		driver.delete_all_cookies()
		source,target = T_for(el)
		d1.at[ind,'Transported hormone'] = source
		d1.at[ind,'Target receptor'] = target
		d1.to_csv('G:\\Dataset\\Endo_types\\EndoNet_T.csv')
		

#testing('ENQ00313')
get_data()
#empty_resolve()
print('finished')
