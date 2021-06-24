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
	info,cells =[],[]

	names = driver.find_elements_by_id("j_idt20:j_idt118_list") # 
	if len(names) <= 0:
		return info

	items = names[0].find_elements_by_tag_name('h3')
	for item in items:
		els = item.find_element_by_xpath('.//a[@href]')
		ls = els.get_attribute('href').split('/')
		cells.append( [ls[4] , els.text] )

	for ind in range(len(cells) ):
		els = driver.find_elements_by_id('j_idt20:j_idt118:'+str(ind)+':j_idt134_list')
		if len(els) <= 0:
			info.append([cells[ind][0],cells[ind][1],'empty0','empty0'])
			continue
		comps = els[0].find_elements_by_xpath('.//a[@href]')
		for comp in comps:
			ls = comp.get_attribute('href').split('/')
			#print(ls)
			if ls[3] == 'hormone':
				info.append([ cells[ind][0],cells[ind][1],ls[4],comp.text ])
	
	return info

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


def add_data():
	d1 = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_R.csv')
	d1 = d1.drop(columns = ['Unnamed: 0'])
	final_ls = list(set(d1['Endo_id'].tolist()))
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
			info =  R_for(el)

			for item in info:
				ls_R.append([el] + item )
			temp = pd.DataFrame(ls_R, columns = ['Endo_id','cell_id','cell_name','Hormone_id','Hormone'])
			ls_R_finished.append([el,ind])
			temp1 = pd.DataFrame(ls_R_finished,columns = ['Endo_id','index'])
			temp.to_csv('G:\\Dataset\\Endo_types\\EndoNet_R_info.csv')
			temp1.to_csv('G:\\Dataset\\Endo_types\\EndoNet_R_info_finished_ind.csv')
		else:
			print("out of syllabus",el)


def testing(end_id):
	info = R_for(end_id)
	print(info)

testing('ENR01336')
#add_data()
print('finished')
