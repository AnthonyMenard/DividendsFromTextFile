import re
import datetime
import os

#Define the path to look at the files
path = r'C:\Users\tony1\Desktop\Test'
file_name = 'dividends.txt'

#Define the path
os.chdir(path)

#Open the file in read mode and read its contents into a string
with open(file_name, "r") as oldfile:
     text = oldfile.read()

#Remove end of lines
text = text.replace('\n', ' ')

#Find today's year
today = datetime.date.today()
year = today.year

#create a list and convert it in string
years = [year-1, year, year+1]
years = [str(year) for year in years]

#Annual ("A") needs to be followed by a year to be replaced, so we don't replace "A" in a Class A ETF/company
frequency_years = [year + ' A' for year in years]

#replace anything that is identical to the freq_years
for freq_year in frequency_years:
    text = re.sub(r' {}'.format(freq_year), ' {}\n'.format(freq_year), text)

frequency = ["Q", "M", "S"]
#replace if it match the freq and if it is a single word
for freq in frequency:
    #replace "Q", "M" and "S", if it is a perfect match (it won't change the word "EQUITY" even if we search for "Q")
    text = re.sub(r'\b {}\b'.format(freq), ' {}\n'.format(freq), text)

#add end of line if "page number of number" fits
text = re.sub(r'(page \d+\ of \d+)',' \\1\n', text)
#Split the modified text into a list of lines

lines = text.split("\n")

#Remove empty string in the list
while("" in lines):
    lines.remove("")

#Add a space to the first one to be identical to other lines
lines[0] = " " + lines[0]
#create variables
modified_lines = []
modified_lines_final = []

#loop trought the lines
for line in lines:

    #Skip the first character (a space)
    modified_line = line[1:]

    #add semi colons around a decimal (the dividend)
    modified_line = re.sub(r'(\d+\.\d+)', '; \\1 ;', modified_line)

    #Add the individual line into lines, which represents the text file
    #modified_lines.append(modified_line) #useless

    #If the first character is a digit

    if modified_line[0].isdigit():
        #Then remove the 3 first characters
        modified_line_final = modified_line[3:]
        #If there is another digit as the first character
        if modified_line_final[0].isdigit():
            # then remove the 3 first characters again
            modified_line_final = modified_line_final[3:]
    else:
        #If no digits as the first character, then keep it as is
        modified_line_final = modified_line

    #generate the final text file
    modified_lines_final.append(modified_line_final)

#Iterate over the list of lines
for i in range(len(modified_lines_final)):

    #split into words
    words = modified_lines_final[i].split()
    #add a semi colon after the first word
    words.insert(1, ';')
    #reconstruct the sentences
    modified_lines_final[i] = ' '.join(words)

#Join the modified lines back into a single string
modified_text = "\n".join(modified_lines_final)

#add a coma to convert the dates and add a semi colon for all years
space_years = [" " + year for year in years]
for year in space_years:
    modified_text = modified_text.replace(year,',' + year + ' ;')
modified_text = modified_text.replace(' ; ', ';')

#Output the final result in a new text file
with open('dividends_cleaned.txt', "w") as f:
    f.write(modified_text)