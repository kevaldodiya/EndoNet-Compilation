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

def resol(ls1):
	final_ls = []
	for element in ls1:
		if element == '[]':
			continue
		templist = [re.sub('[^A-Za-z0-9]+', '', x) for x in element.split(', ') ]
		final_ls = final_ls + templist
	return final_ls

def C_for(end_id):
	driver.get('http://endonet.sybig.de/search/')
	element = driver.find_element_by_id("searchForm:searchInput")
	element.send_keys(end_id)
	element.send_keys(Keys.ENTER)
	timeout = 7

	try:
		element_present = EC.presence_of_element_located((By.ID, 'element_id'))
		WebDriverWait(driver, timeout).until(element_present)
	except TimeoutException:
		print ("Timed out")

	driver.switch_to_window(driver.window_handles[0])
	cytomer,list_super_s,list_sub_s = 'empty0','empty0','empty0'
	final_name = 'empty0'
	hormones,receptors = [],[]
	larger_st,sub_st =[],[]

	checking  = driver.find_elements_by_xpath("//h1")
	if checking[0].text != 'EndoNet':
		return final_name,cytomer,hormones,receptors,larger_st,sub_st

	elems = driver.find_elements_by_xpath("//a[@href]")
	for elem in elems:
		ls = elem.get_attribute("href").split('/')
		if ls[0] == 'javascript:void(0)':
			continue
		if ls[2] == 'cytomer.bioinf.med.uni-goettingen.de':
			cytomer = elem.text
	

	names = driver.find_elements_by_xpath("//h1")
	for name in names:
		n1 = name.text.split(": ")
		if n1[0] == 'Details for anatomical structure':
			final_name = n1[1]


	elems = driver.find_elements_by_xpath("//h3/a[@href]")
	for elem in elems:
		ls = elem.get_attribute("href").split('/')
		if ls[0] == 'javascript:void(0)':
			continue
		if ls[3] == 'hormone':
			hormones.append(ls[4])
		elif ls[3] == 'receptor':
			receptors.append(ls[4]) 
		
	
	list_super_s = driver.find_element_by_id("j_idt63_list")
	if list_super_s != 'empty0':
		elems = list_super_s.find_elements_by_xpath(".//a[@href]")
		for elem in elems:
			larger_st.append(elem.get_attribute("href").split('/')[4] )
	

	list_sub_s = driver.find_element_by_id("j_idt77_list")
	if list_sub_s != 'empty0':
		elems = list_sub_s.find_elements_by_xpath(".//a[@href]")
		for elem in elems:
			sub_st.append(elem.get_attribute("href").split('/')[4] )
	
	return final_name,cytomer,hormones,receptors,larger_st,sub_st


d1 = pd.read_csv('G:\\Dataset\\Endo_types\\EndoNet_C.csv')
d1 = d1.drop(columns= ['Unnamed: 0'])
d2 = pd.read_csv('G:\\Dataset\\EndoNet_P_resolve.csv')
d2 = d2.drop(columns= ['Unnamed: 0'])
#ls1 = d1['large_struct'].tolist() + d1['substruct'].tolist()
#ls1 = set(resol(ls1))
ls_resol = d1['Endo_id'].tolist()
ls1 = d2['c1'].tolist()
ls2 = d2['c2'].tolist()
final_ls = Union(ls1,ls2)
final_ls.sort()
print("sorting finished")

#final_ls = Diff(ls1,ls2)
final_ls.sort()

ls_C =[]
ls_C_finished = []
i =0

cytomer = 'empty1'
#uniprot,ensembl,Hormone = S_for('ENS01240')
#print(uniprot, ensembl, Hormone)

starting =0
total =0
f = 0
listforC = []
for ind in range(len(final_ls)):
	el = final_ls[ind]
	if el[2] == 'C':
		listforC.append(el)
		total = total+1
		if f == 0:
			f=1
			starting = ind

final_ls = Diff(listforC,ls_resol)
'''
name,cytomer,hormones,receptors,larger_st,sub_st = C_for("ENC00575")
print(name)
print(cytomer)
print(hormones)
print(receptors)
print(larger_st)
print(sub_st)
'''
for ind in range(0,len(final_ls)):
	el = final_ls[ind]
	i = i +1
	if i%4 == 0:
		print((i-starting)/float(total)*100 )

	if el[2] == 'C':
		driver.delete_all_cookies()
		name,cytomer,hormones,receptors,larger_st,sub_st = C_for(el)
		ls_C.append([el,name,cytomer,hormones,receptors,larger_st,sub_st])
		temp = pd.DataFrame(ls_C, columns = ['Endo_id','name','cytomer','sec_hormones','receptors','large_struct','substruct'])
		ls_C_finished.append([el,ind])
		temp1 = pd.DataFrame(ls_C_finished,columns = ['Endo_id','index'])
		temp.to_csv('G:\\Dataset\\Endo_types\\EndoNet_C_2.csv')
		temp1.to_csv('G:\\Dataset\\Endo_types\\EndoNet_C_finished_ind_2.csv')

	elif el[2] == 'D':
		print("left D")
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
		print("left S")
		'''
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
		'''

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

