import os
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import schedule
import time
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt
import make_graph
#pip install requests beautifulsoup4 PyMuPDF schedule
# Configuration
current_date = date.today()
url = 'https://www.tcmb.gov.tr/wps/wcm/connect/tr/tcmb+tr/main+menu/istatistikler/parasal+ve+finansal+istatistikler/haftalik+para+ve+banka+istatistikleri'  # Replace with the actual URL
pdf_directory = './pdfs'
pdf_filename = str(current_date)+".pdf"
pdf_filepath = os.path.join(pdf_directory, pdf_filename)
previous_link_file = 'previous_link.txt'
data_output_file = 'extracted_data.txt'

# Function to fetch the PDF link
def fetch_pdf_link():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pdf_link = soup.find('a', class_='pdf type-link', title=True, href=True)
    if pdf_link:
        return 'https://www.tcmb.gov.tr'+pdf_link['href']
    return None

# Function to download the PDF
def download_pdf(pdf_url):
    response = requests.get(pdf_url)
    with open(pdf_filepath, 'wb') as f:
        f.write(response.content)

# Function to extract data from the PDF
def extract_pdf_data():
    with fitz.open(pdf_filepath) as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text

# Function to store the extracted data
def store_data(data):
    with open(data_output_file, 'w') as f:
        f.write(data)

# Main function to check and update the PDF
def check_and_update_pdf():
    pdf_link = fetch_pdf_link()
    if not pdf_link:
        print("No PDF link found.")
        return

    # Read the previous link if it exists
    previous_link = None
    if os.path.exists(previous_link_file):
        with open(previous_link_file, 'r') as f:
            previous_link = f.read().strip()

    # Compare the current link with the previous link
    if pdf_link != previous_link:
        print("New PDF link found, downloading...")
        download_pdf(pdf_link)
        
        # Extract data from the new PDF
        data = extract_pdf_data()
        
        # Store the extracted data
        store_data(data)
        
        # Update the stored previous link
        with open(previous_link_file, 'w') as f:
            f.write(pdf_link)
        
        make_graph.get_M1_data()   
        make_graph.make_graph(make_graph.M1)
        make_graph.get_M2_data() 
        make_graph.make_graph(make_graph.M2)
    else:
        print("PDF link has not changed.")
        


# Schedule the script to run daily
schedule.every().day.at("09:00").do(check_and_update_pdf)  # Adjust the time as needed

if __name__ == "__main__":
    if not os.path.exists(pdf_directory):
        os.makedirs(pdf_directory)
        
    # Run the initial check immediately
    check_and_update_pdf()
    # Keep the script running to maintain the schedule
    while True:
        schedule.run_pending()
        time.sleep(60*60)  # Check every 1/2 day if a scheduled task is pending 60*60*12
