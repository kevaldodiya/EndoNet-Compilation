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


def D_for(end_id):
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
	cell,receptor = 'empty0','empty0'
	for elem in elems:
		ls = elem.get_attribute("href").split('/')
		if ls[0] == 'javascript:void(0)':
			continue
		if ls[3] == 'receptor' and ls[4][:2] == 'EN':
			receptor = ls[4]
		if ls[3] == 'cell':
			cell = ls[4]
			break

	return cell,receptor

def get_data():
	d1 = pd.read_csv('G:\\Dataset\\EndoNet_P_resolve.csv')
	d1 = d1.drop(columns= ['Unnamed: 0'])
	ls1 = d1['c1'].tolist()
	ls2 = d1['c2'].tolist()
	final_ls = Union(ls1,ls2)
	final_ls.sort()
	print("sorting finished")
	ls_D =[]
	ls_D_finished = []
	i =0

	starting =0
	total =0
	f = 0

	for ind in range(len(final_ls)):
		el = final_ls[ind]
		if el[2] == 'D':
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
			driver.delete_all_cookies()
			cell,receptor = D_for(el)
			ls_D.append([el,cell,receptor])
			temp = pd.DataFrame(ls_D, columns = ['Endo_id','cell','receptor' ])
			ls_D_finished.append([el,ind])
			temp1 = pd.DataFrame(ls_D_finished,columns = ['Endo_id','index'])
			temp.to_csv('G:\\Dataset\\Endo_types\\EndoNet_D_v2_2.csv')
			temp1.to_csv('G:\\Dataset\\Endo_types\\EndoNet_D_v2_ind_2.csv')
		elif el[2] == 'S':
			print("left S")

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

def testing(end_id):
	cell,receptor = D_for(end_id)
	print(cell)
	print(receptor)

def empty_resolve():
	d1 = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_D_v2_final.csv')
	d1 = d1.drop(columns= ['Unnamed: 0'])
	inds =  d1.index[d1['cell'] == 'empty0'].tolist()
	i =0
	for ind in inds:
		el = d1.at[ind,'Endo_id']
		i = i +1
		if i%4 == 0:
			print(i/len(inds))

		driver.delete_all_cookies()
		cell,receptor = D_for(el)
		d1.at[ind,'cell'] = cell
		d1.at[ind,'receptor'] = receptor
		d1.to_csv('G:\\Dataset\\Endo_types\\EndoNet_D_v2_final_test.csv')
		


empty_resolve()
print('finished')
