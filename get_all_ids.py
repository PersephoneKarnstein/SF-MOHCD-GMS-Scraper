import tkinter as tk
from tkinter import ttk
from tkinter import *
import numpy as np 
import warnings, tkFileDialog, shutil, sys, os

warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)

import time, re, openpyxl
from selenium import webdriver
from bs4 import BeautifulSoup

global usrname, pwd, names, workbookname
usrname = ""
pwd = ""

class GMS_Login:
	global usrname, pwd
	def __init__(self):
		# frame = Frame(master)
		# frame.pack()
		self.root = Tk()
		self.label = Label(self.root, text="Enter your GMS login")
		self.label.pack(side=TOP)
		self.usrlabel = Label(self.root, text="Username:")
		self.usrlabel.pack()
		self.f = Entry(self.root)
		self.f.pack()
		self.pwdlabel = Label(self.root, text="Password:")
		self.pwdlabel.pack()
		self.e=Entry(self.root, show="*")
		self.e.pack()
		self.button = Button(self.root, text="Go", command=self.get_creds)
		self.button.pack()
		# self.root.bind('<Return>', self.get_creds)
		self.root.mainloop()

	def get_creds(self):
		# self.usrname = self.f.get()
		# self.pwd = self.e.get()
		# print(self.usrname, self.pwd)
		globals()["usrname"] = self.f.get()
		globals()["pwd"] = self.e.get()
		self.root.destroy()

app = GMS_Login()
usrname = globals()["usrname"]
pwd = globals()["pwd"]
# print(usrname, pwd)


class Check_names(tk.Tk):

	def __init__(self, *args, **kwargs):
		globals()["names"] = np.empty([1,4], dtype=str)
		############################################


		############Initialize the GUI#############
		###########################################
		tk.Tk.__init__(self, *args, **kwargs)

		progressvar = IntVar()
		progressvar.set(0)
		self.progress = ttk.Progressbar(self, orient="horizontal", variable=progressvar, length=200, mode="determinate")
		self.progress.pack()

		self.bytes = 0.
		self.maxbytes = 67.*50.
		# self.progressvar=0
		self.progress["maximum"] = self.maxbytes
		self.label = Label(self, text="Starting up...")
		self.label.pack()
		self.update()
		############################################

		def name_search(self):
			driver = webdriver.Chrome("C:\chromedriver")
			driver.get('https://gms.sfmohcd.org')
			search_box = driver.find_element_by_name('login')
			search_box.send_keys(globals()["usrname"])
			search_box = driver.find_element_by_name('pw')
			search_box.send_keys(globals()["pwd"])
			time.sleep(np.random.rand()*2)
			driver.find_element_by_css_selector('input[type=\"submit\"]').click() #log in
			driver.switch_to_default_content()
			driver.switch_to_frame('main')
			time.sleep(np.random.rand()*2)
			driver.find_element_by_xpath('//*[@id="PageContents"]/div/div[3]').click() #go to job readiness
			time.sleep(np.random.rand()*2)
			driver.find_element_by_link_text("Clients").click() #go to "clients"
			driver.find_element_by_xpath('//*[@id="PageContents"]/table[3]/tbody/tr/td[1]/table/tbody/tr[4]/td/table/tbody/tr[6]/td[2]').click() #navigate to "all clients"

			while True:
				try:
					time.sleep(np.random.rand()*2)
					soup = BeautifulSoup(driver.page_source, "html.parser")
					pagecontents = soup.find_all(id="PageContents")[0]
					tables = pagecontents.find_all("table")
					pagenum = str(tables[5].find(style="color:#FFCC33").get_text())
					for n in np.arange(50)+1:
						try:
							time.sleep(np.random.rand()*1)
							personname = str(tables[6].find_all("tr")[n].get_text().split("\n")[1].strip())
							self.label.configure(text = "Page "+pagenum+" of 67: Checking "+personname) #update the text in self.label 
							progressvar.set(progressvar.get()+1)
							self.update()
							self.lift()

							driver.find_element_by_xpath('//*[@id="PageContents"]/table[6]/tbody/tr['+str(n)+']/td[1]/a').click()
							soup2 = BeautifulSoup(driver.page_source, "html.parser")
							title = soup2.find(class_="titlebar").get_text(strip=True)
							if "CONTACT INFORMATION" in title:
								uploadID = str(driver.find_element_by_name("ClientID~0").get_attribute("value"))
								dob = str(driver.find_element_by_name("DOB~0").get_attribute("value"))
								# print(uploadID)
								try:
									globals()["names"] = np.vstack((globals()["names"], [personname.split(", ")[1].strip(), personname.split(", ")[0].strip(), dob, uploadID] ))
								except IndexError:
									globals()["names"] = np.vstack((globals()["names"], [personname.split(", ")[0].strip(), "", dob, uploadID] ))
								driver.back()
								driver.switch_to_frame('main')
							else:
								driver.back()
								driver.switch_to_frame('main')
						except IndexError: break
					driver.find_element_by_xpath('//*[@id="PageContents"]/table[5]/tbody/tr/td[3]/a').click()
				except: break

			self.label.configure(text = "Done!") #update the text in self.label 
			progressvar.set(self.maxbytes)
			self.update()
			globals()["names"] = globals()["names"][1:]

			wb2 = openpyxl.Workbook()
			ws2 = wb2.active
			paste_range = ws2["A1":"D"+str(len(globals()["names"]))]
			for col in [1,2,3,4]:
				for row in np.arange(len(globals()["names"]))+1: ws2.cell(column=col, row=row, value=globals()["names"][row-1][col-1])
			wb2.save("foo.xlsx")

			self.destroy()

		name_search(self)
		self.mainloop()


app = Check_names()
# app.mainloop()
print(globals()["names"])
