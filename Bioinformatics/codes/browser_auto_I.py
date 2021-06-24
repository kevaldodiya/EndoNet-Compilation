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


def I_for(end_id):
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
	elems = driver.find_elements_by_xpath('//h1')
	inf,inf_sec, inf_by_r,inf_by_c = 'empty0','empty0','empty0','empty0'
	for el in elems:
		ls = el.text.split(': ')
		if ls[0] == 'Details for influence':
			inf = ls[1].split(' ')[0]

	elems = driver.find_elements_by_id("secView:j_idt104")
	if len(elems) <=0 :
		return inf,inf_sec, inf_by_r,inf_by_c
	inf_sec = elems[0].text[15:]
	elems = driver.find_elements_by_id('c2rView:j_idt145')
	els = elems[0].find_elements_by_xpath('.//a[@href]')
	
	for elem in els:
		ls = elem.get_attribute("href").split('/')
		#print(ls)
		if ls[0] == 'javascript:void(0)':
			continue
		
		if ls[3] == 'receptor':
			inf_by_r ='ENR' + ls[4].split('=')[1].zfill(5)
			continue

		if ls[3] == 'cell':
			inf_by_c ='ENC' + ls[4].split('=')[1].zfill(5)
			break
		
	return inf,inf_sec, inf_by_r,inf_by_c

def get_data():
	d1 = pd.read_csv('G:\\Dataset\\EndoNet_P_resolve.csv')
	d1 = d1.drop(columns= ['Unnamed: 0'])
	ls1 = d1['c1'].tolist()
	ls2 = d1['c2'].tolist()
	final_ls = Union(ls1,ls2)
	final_ls.sort()
	print("sorting finished")
	ls_I =[]
	ls_I_finished = []
	i =0

	starting =0
	total =0
	f = 0

	for ind in range(len(final_ls)):
		el = final_ls[ind]
		if el[2] == 'I':
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
			print("left H")

		elif el[2] == 'I':
			driver.delete_all_cookies()
			inf,inf_sec, inf_by_r,inf_by_c = I_for(el)
			ls_I.append([el,inf_sec, inf_by_r,inf_by_c,inf ])
			temp = pd.DataFrame(ls_I, columns = ['Endo_id','Influenced secretion','Influenced by receptor','ana. struct of receptor','influence' ])
			ls_I_finished.append([el,ind])
			temp1 = pd.DataFrame(ls_I_finished,columns = ['Endo_id','index'])
			temp.to_csv('G:\\Dataset\\Endo_types\\EndoNet_I.csv')
			temp1.to_csv('G:\\Dataset\\Endo_types\\EndoNet_I_ind.csv')

		elif el[2] == 'T':
			print("left T")

		elif el[2] == 'R':
			print("left R")

		elif el[2] == 'Q':
			print("left Q")

		else:
			print("out of syllabus",el )

def testing(end_id):
	inf,inf_sec, inf_by_r,inf_by_c = I_for(end_id)
	print(inf_sec)
	print(inf_by_r)
	print(inf_by_c)
	print(inf)

def empty_resolve():
	d1 = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_I.csv')
	d1 = d1.drop(columns= ['Unnamed: 0'])
	inds =  d1.index[d1['Influenced secretion'] == 'empty0'].tolist()
	i =0
	for ind in inds:
		el = d1.at[ind,'Endo_id']
		i = i +1
		if i%4 == 0:
			print(i/len(inds))

		driver.delete_all_cookies()
		inf,inf_sec, inf_by_r,inf_by_c = I_for(el)
		d1.at[ind,'influence'] = inf
		d1.at[ind,'ana. struct of receptor'] = inf_by_c
		d1.at[ind,'Influenced by receptor'] = inf_by_r
		d1.at[ind,'Influenced secretion'] = inf_sec
		d1.to_csv('G:\\Dataset\\Endo_types\\EndoNet_I_test.csv')
		

#testing('ENI00471')
get_data()
print('finished')
