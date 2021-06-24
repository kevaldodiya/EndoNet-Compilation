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
	timeout = 6

	try:
		element_present = EC.presence_of_element_located((By.ID, 'element_id'))
		WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
		print ("Timed out")
	driver.switch_to_window(driver.window_handles[0])

	names = driver.find_elements_by_id("hormoneForm:bindingsTbl_head")
	target,receptors = [],[]

	if len(names) <=0:
		return target,receptors

	for name in names[0].find_elements_by_xpath('.//a[@href]'):
		receptors.append( name.get_attribute("href").split('/')[4] )

	names = driver.find_elements_by_id("hormoneForm:bindingsTbl_data")
	cells = names[0].find_elements_by_tag_name("tr")
	#print(len(cells) )
	for ind in range(len(cells)):
		line = cells[ind]
		t = line.find_elements_by_id("hormoneForm:bindingsTbl:"+str(ind)+":tissueLink")
		if len(t) <=0:
			return target,receptors
		cell_id = t[0].get_attribute("href").split("/")[4]
		for block_ind in range(len(receptors)):
			temp = driver.find_elements_by_id('hormoneForm:bindingsTbl:'+str(ind)+':j_idt168:'+str(block_ind)+':j_idt171')
			if len(temp) <=0:
				continue
			target.append([receptors[block_ind] , cell_id ])

	return target,receptors

def resolve(ls1):
	final_ls = []
	for element in ls1:
		if element == '[]':
			continue
		templist = [re.sub('[^A-Za-z0-9]+', '', x) for x in element.split(', ') ]
		final_ls = final_ls + templist
	return final_ls

def empty_resolve():
	d1 = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_H_target.csv')
	d1 = d1.drop(columns= ['Unnamed: 0'])
	inds = d1.index[d1['target_receptor'] == 'empty0'].tolist()
	ls_H = []
	for ind in inds:
		driver.delete_all_cookies()
		el = d1.at[ind,'Endo_id']
		target,receptors = H_for(d1.at[ind,'Endo_id'])
		dt = {}
		for item in target:
			dt[item[0]] = 1
			ls_H.append([el] + item )

		for item in receptors:
			if item not in dt:
				ls_H.append([el,item,'empty0'])
					
		if len(target) <=0 and len(receptors) <=0:
			ls_H.append([el,'empty0','empty0'])

	d1 = d1.drop(inds)
	d1.to_csv('G:\\Dataset\\Endo_types\\EndoNet_H_target.csv')
	temp = pd.DataFrame(ls_H, columns = ['Endo_id','target_receptor','target_cell'])
	temp.drop_duplicates(keep = 'first',inplace = True)
	temp.to_csv('G:\\Dataset\\Endo_types\\EndoNet_H_target_2.csv')

def add_data():
	d1 = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_H_final.csv')
	d1 = d1.drop(columns= ['Unnamed: 0'])

	d2 = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_H_target.csv')
	d2 = d2.drop(columns= ['Unnamed: 0']) 
	total_hors = d1['Endo_id'].tolist()
	final_ls = Diff( list(set(total_hors)),list(set(d2['Endo_id'].tolist())) )
	final_ls.sort()
	print('sorting finished')
	ls_H = []
	i = 0
	for ind in range(0,len(final_ls)):
		el = final_ls[ind]
		i = i+1
		if i%4 == 0:
			print(i/float(len(final_ls))*100)

		driver.delete_all_cookies()
		target,receptors = H_for(el)
		dt = {}
		for item in target:
			dt[item[0]] = 1
			ls_H.append([el] + item )

		for item in receptors:
			if item not in dt:
				ls_H.append([el,item,'empty0'])
					
		if len(target) <=0 and len(receptors) <=0:
			ls_H.append([el,'empty0','empty0'])

	temp = pd.DataFrame(ls_H, columns = ['Endo_id','target_receptor','target_cell'])
	temp.drop_duplicates(keep = 'first',inplace = True)
	temp.to_csv('G:\\Dataset\\Endo_types\\EndoNet_H_target_2.csv')

def get_data():
	d1 = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_H_final.csv')
	d1 = d1.drop(columns= ['Unnamed: 0'])

	final_ls = d1['Endo_id'].tolist()
	final_ls.sort()
	print("sorting finished")

	ls_H =[]
	ls_H_finished = []
	i =0

	for ind in range(0,len(final_ls)):
		el = final_ls[ind]
		i = i +1
		if i%4 == 0:
			print(i/float(len(final_ls))*100 )

		if el[2] == 'H':
			driver.delete_all_cookies()
			target,receptors = H_for(el)
			d1 = {}
			for item in target:
				d1[item[0]] = 1
				ls_H.append([el] + item )

			for item in receptors:
				if item not in d1:
					ls_H.append([el,item,'empty0'])
					
			if len(target) <=0 and len(receptors) <=0:
				ls_H.append([el,'empty0','empty0'])

			temp = pd.DataFrame(ls_H, columns = ['Endo_id','target_receptor','target_cell'])
			ls_H_finished.append([el,ind])
			temp1 = pd.DataFrame(ls_H_finished,columns = ['Endo_id','index'])
			temp.to_csv('G:\\Dataset\\Endo_types\\EndoNet_H_target.csv')
			temp1.to_csv('G:\\Dataset\\Endo_types\\EndoNet_H_target_ind.csv')

		else:
			print("Out of syllabus",el)

def testing(end_id):
	driver.delete_all_cookies()
	target,receptors = H_for(end_id)
	print(target)
	print(receptors)
		
#testing('ENH00007')
#get_data()
#empty_resolve()
add_data()
print('finished')
