import os
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import schedule
import time
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
#pip install requests beautifulsoup4 PyMuPDF schedule
# Configuration

current_date = date.today()
url = 'https://www.tcmb.gov.tr/wps/wcm/connect/tr/tcmb+tr/main+menu/istatistikler/parasal+ve+finansal+istatistikler/haftalik+para+ve+banka+istatistikleri'  # Replace with the actual URL
pdf_directory = './pdfs'
pdf_filename = str(current_date)+".pdf"
pdf_filepath = os.path.join(pdf_directory, pdf_filename)
previous_link_file = 'previous_link.txt'
data_output_file = 'extracted_data.txt'
proccessing_data = 'proccessing_data.txt'
M1 = "./M1"
M2 = "./M2"
M3 = "./M3"
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page_num in range(len(pdf)):
            page = pdf.load_page(page_num)
            text += page.get_text()
    return text

def get_M1_data(data_link=data_output_file):
    with open(data_link, 'r') as f:
        data = f.readlines()
        last_date = data[1]
        i=0
        while True:
            if("M1=" in data[i]):
                last_M1=data[i+1]
                break
            else:
                i = i+1
        while True:
            if("Dolaşımdaki Para" in data[i]):
                last_dolasim=data[i+1]
                break
            else:
                i = i+1
        while True:
            if("Vadesiz Mevduat (TL)" in data[i]):
                last_vadesiz=data[i+1]
                break
            else:
                i = i+1
        while True:
            if("Vadesiz Mevduat (YP)" in data[i]):
                last_vadesiz_yp=data[i+1]
                break
            else:
                i = i+1
    with open("M1/M1_Total.txt", 'a+') as f:  
        f.write("\n"+last_date.rstrip()+"\t"+last_M1.rstrip())      
    with open("M1/M1_Circulating.txt", 'a+') as f:  
        f.write("\n"+last_date.rstrip()+"\t"+last_dolasim.rstrip())  
    with open("M1/M1_Saving-AccountsTL.txt", 'a+') as f:  
        f.write("\n"+last_date.rstrip()+"\t"+last_vadesiz.rstrip())  
    with open("M1/M1_Saving-AccountsYP.txt", 'a+') as f:  
        f.write("\n"+last_date.rstrip()+"\t"+last_vadesiz_yp.rstrip())     
        
def store_data(data):
    with open(proccessing_data, 'w') as f:
        f.write(data)
        
def get_M2_data(data_link=proccessing_data):
    with open(data_link, 'r') as f:
        data = f.readlines()
        last_date = data[1]
        i=0
        while True:
            if("M2=" in data[i]):
                last_M2=data[i+1]
                break
            else:
                i = i+1
        while True:
            if("Vadeli Mevduat (TL)" in data[i]):
                last_vadesiz_TL_M2=data[i+1]
                break
            else:
                i = i+1
        while True:
            if("Vadeli Mevduat (YP)" in data[i]):
                last_vadesiz_YP_M2=data[i+1]
                break
            else:
                i = i+1
    with open("M2/M2_Total.txt", 'a+') as f:  
        f.write("\n"+last_date.rstrip()+"\t"+last_M2.rstrip())
    with open("M2/M2_Saving-AccountsTL.txt", 'a+') as f:  
        f.write("\n"+last_date.rstrip()+"\t"+last_vadesiz_TL_M2.rstrip())  
    with open("M2/M2_Saving-AccountsYP.txt", 'a+') as f:  
        f.write("\n"+last_date.rstrip()+"\t"+last_vadesiz_YP_M2.rstrip())     
# Iterate over all files in the folder

def graph(file_path):
    # Path to the .txt file
    with open(file_path, 'r') as f:
        data = f.readlines()
        x_axis = data[0].split()[0]
        y_axis = data[0].split()[1]
    
    # Read the data from the .txt file
    df = pd.read_csv(file_path, delim_whitespace=True)

    # Convert DATE to datetime format
    df[x_axis] = pd.to_datetime(df[x_axis], format='%d.%m.%Y')

    # Convert M1SL to integer (handling large numbers)
    df[y_axis] = df[y_axis].str.replace('.', '').astype('Int64')

    print(df)

    # Plotting
    plt.figure(figsize=(20, 10))
    plt.plot(df[x_axis], df[y_axis], marker='o')

    # Formatting the plot
    plt.title('Money Supply Over Time')
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.xticks(rotation=45)
    plt.grid(True)

    # Show plot
    plt.tight_layout()
    plt.savefig(x_axis+" "+y_axis+"_graph.png")
    
"""
for filename in os.listdir(pdf_directory):
    #print(filename)
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_directory, filename)
        text = extract_text_from_pdf(pdf_path)
        store_data(text)
        get_M2_data()
        """
def make_graph(Mx):
    for filename in os.listdir(Mx):
    #print(filename)
        if filename.endswith(".txt"):
            pdf_path = os.path.join(Mx, filename)
            graph(pdf_path)
