import re

#Open the file in read mode and read its contents into a string
with open('div_notepad.txt', "r") as oldfile:
     text = oldfile.read()

#Remove end of lines
text = text.replace('\n', ' ')
years = ['2022', '2023', '2024']

#Annual ("A") needs to be followed by a year to be replaced, so we don't replace "A" in a Class A ETF/company
frequency_years = [year + ' ;' + ' A' for year in years]

#replace anything that is identical to the freq_years
for freq_year in frequency_years:
    text = re.sub(r' {}'.format(freq_year), ' {}\n'.format(freq_year), text)

frequency = ["Q", "M", "S"]
#replace if it match the freq and if it is a single word
for freq in frequency:
    #replace "Q", "M" and "S", if it is a perfect match (it won't change the word "EQUITY" even if we search for "Q")
    text = re.sub(r'\b {}\b'.format(freq), ' {}\n'.format(freq), text)

#Split the modified text into a list of lines
lines = text.split("\n")
#Save the first line because it is already correct
first_line = lines[0]
#create variables
modified_lines = []
modified_lines_final = []

#loop trought the lines except the first one
for line in lines[1:]:
    #Skip the first character (a space) for all lines except for the first one
    modified_line = line[1:]
    #Add the individual line into lines, which represents the text file
    modified_lines.append(modified_line)

#Skip first line of the loop
for modified_line in modified_lines[1:]:
    modified_line = re.sub(r'(\d+\.\d+)', '; \\1 ;', modified_line)
  #  modified_line = re.sub(r'(\b\w+\b) (\b\w+\b)', '\\1 ;\\2', modified_line)
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

   # modified_line_final[i] = re.sub(r'(\d+\.\d+)', '; \\1', modified_line_final)
    modified_lines_final.append(modified_line_final)

#Iterate over the list of lines
for i in range(len(modified_lines_final)):
    words = modified_lines_final[i].split()
    words.insert(1, ';')
    #reconstruct the sentences
    modified_lines_final[i] = ' '.join(words)

#Join the modified lines back into a single string
modified_text = "\n".join(modified_lines_final)

#Combine the first line with the result of the operations
modified_text = first_line + "\n" + modified_text

#add a coma to convert the dates and add a semi colon for all years
for year in years:
    modified_text = modified_text.replace(year, ', ' + year + ' ;')

#Output the final result in a new text file
with open('div_notepad2.txt', "w") as f:
    f.write(modified_text)