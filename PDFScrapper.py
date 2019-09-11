import PyPDF2
import csv

# Open the pdf
pdfFileObj = open(r'../PDFs/Artificial_Intelligence–A strategy_for_European_startups-2018.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
# The data is on page 8, as python is 0 indexed we need to get page 7
pageObj = pdfReader.getPage(7)
# Split the data based on new lines
data_list = pageObj.extractText().split('\n')
# Get the indexes of the First and last country
us_index = data_list.index(r'United States')
russia_index = data_list.index(r'Russia')
# Get the name of the countries
country_list = data_list[us_index:russia_index+1]
# Get the startups counts
startup_list = [data_list[russia_index+2][data_list[russia_index+2].index('0')+1:]]
startup_list.extend([i.strip('\n') for i in data_list[russia_index+3:russia_index+10]])
line = data_list[russia_index+10]
startup_list.extend([line[i:i+2] for i in range(0, len(line), 2)])
startup_list.append(data_list[russia_index+11][:2])
# Zipped list
zip_list = (list(zip(country_list, startup_list)))

# Start writing to the CSV file
with open('startup.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    # Write the column headings first
    writer.writerow(['Country', 'No of startups'])
    for row in zip_list:
        writer.writerow(row)

print('CSV  writing done!!!!')

