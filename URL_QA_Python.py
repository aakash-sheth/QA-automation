#Importing important libraries
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import numpy as np
try:
	print("------------------------------------WDG-CRM-Build And Deploy---------------------------------------")
	#Taking the input from the user for the 'View as webpage' Link
	link_ViewAsWebPage = Request(input("Enter the 'View as webpage' link For the Email You want To do QA: "))

	#Taking the input from the user for the URL matrix to be compared and printing the URL
	print("Please make Sure before giving the path of URL matrix, the coulums have 'Full URL' (in the same format as mentioned) ")
	excl_URLMatrix = input("Enter the path of URL Matrix from your Local Drive: (Just drag and drop the file in cmd) ")
	data_URLMatrix = pd.read_excel(excl_URLMatrix.replace('"',""))
	df_URLMatrix = pd.DataFrame(data_URLMatrix)
	lst_FullURL = list(df_URLMatrix["Full URL"])
	print(lst_FullURL)

	html = urlopen(link_ViewAsWebPage) # Insert your URL to extract
	bsObj = BeautifulSoup(html.read(),"lxml");
	lst_URLOfQA =[]
	lst_Status = []
	lst_alias = []
	print("Now all the link will start getting extracted, please wait for some time(time = No.of links x 1sec)")
	for link in bsObj.find_all('a'):
		link_redirect = link.get('href')
		#print(link_redirect)
		data = requests.request("GET", link_redirect)
		link_direct = data.url
		#link_status = link_direct.getcode()
		time.sleep(0.5)
		#lst_Status.append(link_status)
		print(link_direct)
		lst_URLOfQA.append(link_direct)

	lst_URLOfQA = lst_URLOfQA[1:]
	print(lst_URLOfQA)
	lst_Comparision = [True if lst_FullURL[i] == lst_URLOfQA[i] else False  for i in range(len(lst_FullURL))]
	print(lst_Comparision)
	df_ResultURL = pd.concat([df_URLMatrix,pd.DataFrame(lst_URLOfQA),pd.DataFrame(lst_Status),pd.DataFrame(lst_Comparision)], axis=1, ignore_index=True, keys = ["Placement", "Orignal URL", "Email URL", "Status of URL", "Comparision"])
	df_ResultURL.columns = ["Placements", "Full URL", "Destination URL", "Comparision"]
	df_ResultURL.head()
	df_ResultURL.to_excel(excel_writer="URL_Matrix_comparision.xlsx", index=False)
	#G:\Python\QA automation\QA_Automation-master\URL_Matrix.xlsx
except exception as e:
	print(e)
	print("We are sorry for the glictch !! \n please look if you had made any mistake")
finally:
	print("Please make a note that the 'URL_Matrix_comparision.xlsx' will be dowloaded at your 'Downloads' folder ")
	input("Hit any key to exit")
