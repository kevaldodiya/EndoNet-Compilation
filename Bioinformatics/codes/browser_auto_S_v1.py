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

def final_conv(end_id):
	#print(end_id)
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
	elems = driver.find_elements_by_xpath("//a[@href]")
	uniprot = 'empty'
	ensembl = 'empty'
	
	for elem in elems:
		ls = elem.get_attribute("href").split('/')
		#print(ls)
		if ls[0] == 'javascript:void(0)':
			continue

		if ls[2] == 'ca.expasy.org':
			uniprot = ls[4]
		if ls[2] == 'www.ensembl.org':
			ensembl = ls[5].split('=')[1]
			break
	
	return uniprot,ensembl

def S_for(end_id):
	#print("starting D")
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
	elems = driver.find_elements_by_xpath("//a[@href]")
	uniprot,ensembl,Hormone = 'empty0','empty0','empty0'
	for elem in elems:
		ls = elem.get_attribute("href").split('/')
		#print(ls)
		
		if ls[0] == 'javascript:void(0)':
			continue
		if ls[3] == 'hormone':
			Hormone = ls[4]
			uniprot,ensembl = final_conv(Hormone)
			break

	#print("finished final_cov")
	return uniprot,ensembl,Hormone


d1 = pd.read_csv('G:\\Dataset\\EndoNet_P_resolve.csv')
d1 = d1.drop(columns= ['Unnamed: 0'])
ls1 = d1['c1'].tolist()
ls2 = d1['c2'].tolist()
final_ls = Union(ls1,ls2)
final_ls.sort()
print("sorting finished")
ls_S =[]
ls_S_finished = []
i =7227
uniprot = 'empty1'
ensembl = 'empty1'
Hormone = 'empty1'
#uniprot,ensembl,Hormone = S_for('ENS01240')
#print(uniprot, ensembl, Hormone)

starting =0
total =0
f = 0

for ind in range(len(final_ls)):
	el = final_ls[ind]
	if el[2] == 'S':
		total = total+1
		if f == 0:
			f=1
			starting = ind

driver.delete_all_cookies()
for ind in range(7228,len(final_ls)):
	el = final_ls[ind]
	i = i +1
	if i%4 == 0:
		driver.delete_all_cookies()
		print((i-starting)/float(total)*100 )

	if el[2] == 'C':
		print("left C")

	elif el[2] == 'D':
		print("finished D")
		'''
		uniprot = 'empty1'
		ensembl = 'empty1'
		uniprot,ensembl = D_for(el)

		ls_D.append([el,uniprot,ensembl])
		temp = pd.DataFrame(ls_D, columns = ['Endo_id','uniprot','ensembl'])
		ls_D_finished.append([el,i])
		temp1 = pd.DataFrame(ls_D_finished,columns = ['Endo_id','index'])
		temp.to_csv('G:\\Dataset\\Endo_types\\EndoNet_D_2.csv')
		temp1.to_csv('G:\\Dataset\\Endo_types\\EndoNet_D_finished_ind_2.csv')
		'''
		
	elif el[2] == 'S':
		#print("starting S")
		uniprot = 'empty1'
		ensembl = 'empty1'
		Hormone = 'empty1'
		uniprot,ensembl,Hormone = S_for(el)

		ls_S.append([el,uniprot,ensembl,Hormone])
		temp = pd.DataFrame(ls_S, columns = ['Endo_id','uniprot','ensembl','Hormone'])
		ls_S_finished.append([el,i])
		temp1 = pd.DataFrame(ls_S_finished,columns = ['Endo_id','index'])
		temp.to_csv('G:\\Dataset\\Endo_types\\EndoNet_S_2.csv')
		temp1.to_csv('G:\\Dataset\\Endo_types\\EndoNet_S_finished_ind_2.csv')

	elif el[2] == 'H':
		print("left H")

	elif el[2] == 'I':
		print("left I")

	elif el[2] == 'T':
		print("left T")

	elif el[2] == 'R':
		print("left R")

	elif el[2] == 'Q':
		print("left Q")

	else:
		print("out of syllabus",el )



print('finished')
