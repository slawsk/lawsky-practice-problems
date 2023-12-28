# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 05:59:26 2022

@author: Sarah
"""

from bs4 import BeautifulSoup
import pandas as pd
import os
import functionmodules as fm
import convertfile
# import cchardet
# import time
import re
import fitz
import json
# import pdfkit
import create_intro as ci
# import pypandoc
# import regex
from xhtml2pdf import pisa
from PIL import Image
#from weasyprint import HTML

from itertools import chain

current_year = fm.current_year_for_book
rev_proc = fm.rev_proc_for_book

#DO NOT FORGET TO CHANGE THIS WHEN YOU UPLOAD IT!!!

location = 'home'
#location = 'PA'

location_dictionary = {'home':'CodeRegs/RegDictionaryWithJPG.txt',
                       'PA':'CodeRegs/RegDictionaryWithJPGForPA.txt'}

correct_reg_dict = location_dictionary[location]

max_length = 450
code_file_name = '04BCode'
reg_file_name = '05BRegs'
path_short = 'CodeRegs/FilesForBook' 
code_dictionary_entry = 'Code sections you listed on your spreadsheet'
reg_dictionary_entry = 'Reg sections you listed on your spreadsheet'

possible_include_dict = {'Edited IRC Table of Contents (All Classes)':f'{path_short}/01TOCEdited.pdf','Edited IRC Table of Contents (Fed Tax)':'CodeRegs/TOCBasic.pdf','Edited IRC Table of Contents (Corporate Tax)':'CodeRegs/TOCCorporate.pdf','Edited IRC Table of Contents (Partnership Tax)':'CodeRegs/TOCPartnership.pdf','Inflation Rev. Proc.':f'{path_short}/02InflationRevProc.pdf','Depreciation Rev. Proc.':f'{path_short}/03DepreciationRevProc.pdf',code_dictionary_entry:code_file_name,reg_dictionary_entry:reg_file_name}

intro_language = {'Edited IRC Table of Contents (All Classes)':ci.table_contents_info,'Edited IRC Table of Contents (Fed Tax)':ci.table_contents_info,'Edited IRC Table of Contents (Corporate Tax)':ci.table_contents_info,'Edited IRC Table of Contents (Partnership Tax)':ci.table_contents_info,'Inflation Rev. Proc.':ci.inflation_info,'Depreciation Rev. Proc.':ci.depreciation_info, code_dictionary_entry:ci.selected_sections_code_info ,reg_dictionary_entry:ci.selected_sections_regs_info}

possible_files_list = list(possible_include_dict.keys())

# all_code_title_xml = f'CodeNoNotes_{current_year}.xml'
# all_code_title_html = f'CodeNoNotes_{current_year}.html'
# all_regs_title = f'RegsNoNotes_{current_year}.html'



type_run = convertfile.type_run

def find_the_code_section(x):
    return x.split('.', 1)[1].split('-',1)[0]

def find_code_for_usc_26(x):
    return x.rsplit('/', 1)[1][1:].replace('\u2013', '-')

def find_the_number(x):
    try: 
        return int(x)
    except:
        pattern = r"\d+\("
        match_no_letter = re.search(pattern,x)
        match = re.match(r'^\d+', x)        
        if match_no_letter:
            return int(match.group())+.1
        else:
            return int(match.group())+.2

def create_list_from_string(stringtocheck):
    if 'all' in stringtocheck:
        return ['all']
    else:
        initial_list = stringtocheck.split(",")
        return sorted(list(set(initial_list)))

def merge_lists(listoflists):
    merged_lists = sorted(list(set(list(chain(*listoflists)))))
    if 'all' in merged_lists:
        return ['all']
    else:
        return merged_lists

###AT LEAST ANNUALLY, OR WHEN LAW CHANGES
###Download the files for the code and regulations.

###Fix the problem in 1.704-2(m), 1.751-1(g), 1.1001-2(c), that the /div is in the wrong place and the regulations don't print:
###Replace <div id="p-1.704-2(m)"><p class="indent-1" data-title="1.704-2(m)"><span class="paragraph-hierarchy"><span class="paren">(</span>m<span class="paren">)</span></span> <em class="paragraph-heading">Examples.</em>  The principles of this section are illustrated by the following examples: </p></div> with <div id="p-1.704-2(m)"><p class="indent-1" data-title="1.704-2(m)"><span class="paragraph-hierarchy"><span class="paren">(</span>m<span class="paren">)</span></span> <em class="paragraph-heading">Examples.</em>  The principles of this section are illustrated by the following examples: </p> and replace  that particular liability to the extent of the increase in minimum gain with respect to that liability.</p> </div> with  that particular liability to the extent of the increase in minimum gain with respect to that liability.</p> </div> </div>
### Replace <div id="p-1.751-1(g)"><p class="indent-1" data-title="1.751-1(g)"><span class="paragraph-hierarchy"><span class="paren">(</span>g<span class="paren">)</span></span> <em class="paragraph-heading">Examples.</em>  Application of the provisions of section 751 may be illustrated by the following examples: </p></div> with <div id="p-1.751-1(g)"><p class="indent-1" data-title="1.751-1(g)"><span class="paragraph-hierarchy"><span class="paren">(</span>g<span class="paren">)</span></span> <em class="paragraph-heading">Examples.</em>  Application of the provisions of section 751 may be illustrated by the following examples: </p> AND REPLACE <p>(2) <em>The part of the distribution not under section 751(b).</em> The analysis under this subparagraph should be made in accordance with the principles illustrated in paragraph (e)(2) of examples 3, 4, and 5 of this paragraph.</p> </div> with <p>(2) <em>The part of the distribution not under section 751(b).</em> The analysis under this subparagraph should be made in accordance with the principles illustrated in paragraph (e)(2) of examples 3, 4, and 5 of this paragraph.</p> </div> </div>
### Replace <div id="p-1.1001-2(c)"><p class="indent-1" data-title="1.1001-2(c)"><span class="paragraph-hierarchy"><span class="paren">(</span>c<span class="paren">)</span></span> <em class="paragraph-heading">Examples.</em>  The provisions of this section may be illustrated by the following examples. In each example assume the taxpayer uses the cash receipts and disbursements method of accounting, makes a return on the basis of the calendar year, and sells or disposes of all property which is security for a given liability. </p></div> with <div id="p-1.1001-2(c)"><p class="indent-1" data-title="1.1001-2(c)"><span class="paragraph-hierarchy"><span class="paren">(</span>c<span class="paren">)</span></span> <em class="paragraph-heading">Examples.</em>  The provisions of this section may be illustrated by the following examples. In each example assume the taxpayer uses the cash receipts and disbursements method of accounting, makes a return on the basis of the calendar year, and sells or disposes of all property which is security for a given liability. </p> AND REPLACE <p class="inline-paragraph">In 1980, F transfers to a creditor an asset with a fair market value of $6,000 and the creditor discharges $7,500 of indebtedness for which F is personally liable. The amount realized on the disposition of the asset is its fair market value ($6,000). In addition, F has income from the discharge of indebtedness of $1,500 ($7,500 − $6,000).</p> </div> with <p class="inline-paragraph">In 1980, F transfers to a creditor an asset with a fair market value of $6,000 and the creditor discharges $7,500 of indebtedness for which F is personally liable. The amount realized on the disposition of the asset is its fair market value ($6,000). In addition, F has income from the discharge of indebtedness of $1,500 ($7,500 − $6,000).</p> </div> </div>

### Related to Section 1061(a)(2), in the Code, replace paragraphs (3) and (4) of sections\u202f<ref class=\"footnoteRef\" idref=\"fn002161\">1</ref> 1222 by substituting \u201c3 years\u201d for \u201c1 year\u201d,</content>\n</paragraph>\n<continuation class=\"indent0 firstIndent0\" style=\"-uslm-lc:I10\">shall be treated as short-term capital gain with replace paragraphs (3) and (4) of sections [sic] 1222 by substituting \u201c3 years\u201d for \u201c1 year\u201d,</content>\n</paragraph>\n<continuation class=\"indent0 firstIndent0\" style=\"-uslm-lc:I10\">shall be treated as short-term capital gain

###Run create_clean_files()
### Move Code Dictionary and Reg Dictionary to CodeRegs

###Add the current updated Revenue Procedure to FilesForBook

###update the current year for the book year in fm.current_year_for_book
###update the current Rev Proc for the book year in fm.rev_proc_for_book

###Update the introduction to FilesForBook (this can be automated to some extent)

#### Don't forget to change type_run in convertfile.py after you upload it Python Anywhere--this is about the path for the files

#TO RUN ANNUALLY

def create26NoNotes():
    #URL: https://uscode.house.gov/download/download.shtml
    #when you update the code, make sure to change code_updated in functionmodules
    with open('CodeRegs/GovernmentDownloads/usc26.xml',encoding='utf8') as fp:
        soup = BeautifulSoup(fp,'xml')
    to_remove = ["note","notes","sourceCredit"]
    for r in to_remove:
        for p in soup.find_all(r):
            p.decompose()
            
    div_elements = soup.find_all('section')
    div_library={}
    for div in div_elements:
        
        section_number = div.num
        section_title = div.heading
        section_number_and_title = f"<section>{section_number}{section_title}</section>"
        section_number_and_title = section_number_and_title.replace('\u2013', '-')
        
        subsection_elements = div.find_all('subsection')
        new_dict = {}
        new_dict['num_title_string']=section_number_and_title
    
    
        if subsection_elements:
            for item in subsection_elements:
                subsection_number = item.get("identifier").rsplit('/', 1)[1]
                new_dict[subsection_number]=str(item)
        
        else:
            num_tag = div.find('num')
            if num_tag is not None:
               num_tag.decompose()

            heading_tag = div.find('heading')
            if heading_tag is not None:
                heading_tag.decompose()

            new_dict['all']=str(div)
        
        div_library[find_code_for_usc_26(div.get("identifier"))]=new_dict
    
    with open('CodeDictionary.txt','w',encoding='utf-8') as txt_file:
       txt_file.write(json.dumps(div_library))

#this creates the Regs files with no notes; use this as the input for creating the Code and regs. Run this annually.
def createRegsFile():
    #URL: https://www.ecfr.gov/current/title-26/chapter-I/subchapter-A/part-1 , save the HTML file
    # for the 15a installment sale regs, https://www.ecfr.gov/current/title-26/chapter-I/subchapter-A/part-15a
    # For the 301 regs, go to here and save the relevant regs with the appropriate titles (see below): https://www.ecfr.gov/current/title-26/chapter-I/subchapter-F/part-301/subpart-ECFR5ffaf3310af6b61
    
    
    
    
    
    #string together all the relevant regulations
    reg_string = ''
    directory = 'CodeRegs/GovernmentDownloads/RegFiles'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        with open(f,encoding='utf8') as infile:
            data = infile.read()
            reg_string = reg_string+data
        
    soup = BeautifulSoup(reg_string,'lxml')
    
    #get rid of the editorial notes
    for p in soup.find_all('div',attrs={"class":"editorial-note"}):
        p.decompose()
        
    #get rid of the citations    
    for p in soup.find_all('p',attrs={"class":"citation"}):
            p.decompose()


    div_library = {}
    div_elements = soup.find_all("div", attrs={"class": "section"})
    for div in div_elements:
        div_library[str(div.get("id"))]=str(div) 

    with open('RegDict.txt','w',encoding='utf-8') as txt_file:
        txt_file.write(json.dumps(div_library))
    
        
    #Now create the correct regulation dictionaries with the JPGS
    def replace_text_in_file(file_path_in,file_path_out,location):
        # Regular expression pattern for matching the URLs
        url_pattern = r'https://img\.federalregister\.gov/.+?/'
    
        # Read the original content of the file
        with open(file_path_in, 'r', encoding='utf-8') as file:
            content = file.read()
    
        # Replace the URLs using the regex pattern
        if location == 'home':
            content = re.sub(url_pattern, "../CodeRegs/jpg_pictures/", content)
        elif location == 'PA':
            content = re.sub(url_pattern, "/home/slawsky/taxappfiles/CodeRegs/jpg_pictures/", content)
    
        # Replace .png with .jpg
        content = content.replace(".png", ".jpg")
    
        # Write the modified content back to the file
        with open(file_path_out, 'w', encoding='utf-8') as file:
            file.write(content)
    
    replace_text_in_file('RegDict.txt','RegDictionaryWithJPGForPA.txt',"PA")
    replace_text_in_file('RegDict.txt','RegDictionaryWithJPG.txt',"home")


def create_clean_files():
    create26NoNotes()
    createRegsFile()

#create_clean_files()

#Pull the sections that you want from the code and the regs. Run these on the files that have no notes, that you have created by running create_clean_files  

def fix_subsection(x):
    if isinstance(x, str):
        x= x.replace(" ","")
        return re.sub('[^a-zA-Z,]', ',', x).lower()
    else:
        return 'all'

def process_code_excel(sectionsToUse):
    code_df=pd.read_excel(sectionsToUse,sheet_name = 0)
    
    #get rid of empty rows
    code_df = code_df[code_df['Code'].notna()]
    
    
    #remove spaces from the subsections list
    code_df['SubsectionClean']=code_df['Subsection'].apply(lambda x: fix_subsection(x) )
    code_df['SubsectionList']=code_df['SubsectionClean'].apply(lambda x: create_list_from_string(x))
    
    #sort the columns, noting that some of them are numbers and some are strings
    
 
    code_df = code_df.groupby('Code')['SubsectionList'].apply(lambda x: merge_lists(x)).reset_index()
    code_df['NumberToSort']=code_df['Code'].apply(lambda x: find_the_number(x))
    #print(code_df['SubsectionList'].dtypes)
    #print(code_df['SubsectionList'].apply(type).value_counts())
    code_df = code_df.sort_values(by=['NumberToSort'])
 
    return code_df

def process_regs_excel(sectionsToUse):
    
    regs_df=pd.read_excel(sectionsToUse,sheet_name = 1)  
    #get rid of empty rows
  
    regs_df = regs_df[regs_df['Regulation'].notna()]
  
    #get the sections and specific reg from the overall regulation
    regs_df['Intro']=regs_df['Regulation'].apply(lambda x: x.split('.', 1)[0])

    #remove spaces from the subsections list
    regs_df['SubsectionClean']=regs_df['Subsection'].apply(lambda x: fix_subsection(x) )
    regs_df['SubsectionList']=regs_df['SubsectionClean'].apply(lambda x: create_list_from_string(x))
    #sort the columns, noting that some of them are numbers and some are strings
     
    regs_df = regs_df.groupby('Regulation')['SubsectionList'].apply(lambda x: merge_lists(x)).reset_index()
    regs_df['Section']=regs_df['Regulation'].apply(lambda x: x.split('.', 1)[1].split('-',1)[0])
    regs_df['Specific']=regs_df['Regulation'].apply(lambda x: find_the_number(x.split('.', 1)[1].split('-',1)[1]))
    regs_df['NumberToSort']=regs_df['Section'].apply(lambda x: find_the_number(x))
    regs_df = regs_df.sort_values(by=['NumberToSort','Specific'])

    return regs_df

def parse26(sectionsToUse,outputTitle):
   
    introtext = '<root>'
    endingtext = '</root>'
   
    df=process_code_excel(sectionsToUse)
    
    code_sections_list = df['Code'].tolist()
    subsections_list=df['SubsectionList'].tolist()
    #listified = [x.split(",") for x in subsections_list]

   
    lookupdict = dict(zip(code_sections_list,subsections_list))
 
    with open('CodeRegs/CodeDictionary.txt','r',encoding='utf8') as fp:
        codestring = fp.read()
    code_dict = json.loads(codestring)
    
    textstring = ""
    error_string = ""
    #include the relevant sections
    try:
        for item in code_sections_list:
            subsection_dict = code_dict[str(item)]
            
            textstring += subsection_dict['num_title_string']
            selected_subsections = lookupdict[item]
            if selected_subsections[0] in ['all','All',""]:
                selected_subsections = list(subsection_dict.keys())[1:]
            for subsection in selected_subsections:
                textstring+=subsection_dict[subsection]
    
    except:
        error_string += f"Section {item}, "
    
    file = open(outputTitle, 'w',encoding='utf-8')
    file.write(introtext)
    file.write(textstring)
    file.write(endingtext)
    file.close()
   
    return error_string[:-2],code_sections_list



def replace_text_in_file(file_path, old_text, new_text):
    with open(file_path, 'r') as file:
        content = file.read()

    modified_content = content.replace(old_text, new_text)

    with open(file_path, 'w') as file:
        file.write(modified_content)    

def convert_to_html(inputtitle,outputtitle):
    convertfile.convert_file_to_html(inputtitle, outputtitle)
    
def convert_code_to_html(inputtitle,outputtitle,timenum):
    interim_title = f'saved_code/interim_{timenum}.html'
    
    convertfile.convert_file_to_html(inputtitle,interim_title)
    
    replace_dict = {'Thephaseoutamount':"The phaseout amount",'Thephaseoutpercentageis':'The phaseout percentage is', '<b>The applicable</b><b>recovery period</b><b>is:</b>': '<b>The applicable recovery period is:</b>'}
    
    with open(interim_title, 'r',encoding='utf-8') as file:
        content = file.read()
    
    for item in replace_dict.keys():
        content = content.replace(item,replace_dict[item])
    
    with open(outputtitle, 'w',encoding='utf-8') as file:
        file.write(content)   
        
        
def parseRegs(sectionsToUse,outputTitle):
    
    #create the intro and endtext that allows the css file
    
    if type_run == 'home':
        introtext = """<!doctype html>
        <html>
          <head>
          <meta charset="utf-8">
            <link href="../CodeRegs/regsStyleFast.css" rel="stylesheet" />
          </head>
          <body>"""
    else:
        introtext = """<!doctype html>
        <html>
          <head>
          <meta charset="utf-8">
            <link href="/home/slawsky/taxappfiles/CodeRegs/regsStyleFast.css" rel="stylesheet" />
          </head>
          <body>"""  
        
    endtext = """  </body>
    </html>"""
    
    
    #create the file
    df=process_regs_excel(sectionsToUse)
    
    reg_sections_list = df['Regulation'].tolist()
    subsections_list=df['SubsectionList'].tolist()
    #listified = [x.split(",") for x in subsections_list]

    lookupdict = dict(zip(reg_sections_list,subsections_list))
   
    with open(correct_reg_dict,'r',encoding='utf8') as fp:
        regstring = fp.read()
    reg_dict = json.loads(regstring)
    
    textstring = introtext
    error_string = ""
    
    messed_up_list = ['1.1041-1T','1.263(a)-3','1.263A-1']
    
 
    for item in reg_sections_list:
        item = item.strip()
        try:
            selected_subsections = lookupdict[item]
            if selected_subsections[0] in ['all','All',""] or item in messed_up_list:        
                textstring += reg_dict[item].replace('§ ','§')
            else:
                soup = BeautifulSoup(reg_dict[item],'lxml')   
                section_identifier=f"{item}"
                section_num_and_title = soup.find('h4')
                num_heading = str(section_num_and_title).replace('§ ','§')
                textstring += f"{num_heading}"
                for subsection in selected_subsections:
                    subsection_identifier = f"p-{section_identifier}({subsection})"
                    subsection_to_add = soup.find('div',{'id':subsection_identifier})
                    if str(subsection_to_add) == "None":
                        error_string+=f"Section {subsection_identifier[2:]}, "
                    else:
                        textstring += (str(subsection_to_add))
        except:
            error_string += f"Section {item}, "
    
    def uppercase_match(match):
        # Return the original <h1> tags but with the inner text converted to uppercase
        return '<h4>' + match.group(1).upper() + '</h4>'
    
    textstring += endtext
    textstring  = re.sub(r'<h4>(.*?)</h4>', uppercase_match, textstring, flags=re.DOTALL)         
    #textstring  = re.sub(r'<a[^>]*>.*?</a>', '', textstring )
    file = open(outputTitle, 'w',encoding='utf-8')
    file.write(textstring)
    file.close()
    
    return error_string[:-2],reg_sections_list

def createSelectedCodeRegsHTML(sectionsToUse,timenum):
    code_error_list,code_list = parse26(sectionsToUse,f'saved_code/codefillertitle.{timenum}.xml')
    convert_code_to_html(f'saved_code/codefillertitle.{timenum}.xml',f'saved_code/codefillertitle.{timenum}.html',f'{timenum}')
    reg_error_list,reg_sections_list = parseRegs(sectionsToUse,f'saved_code/regfillertitle.{timenum}.html')
    if len(code_error_list) > 2:
        if len(reg_error_list) > 2:
            all_errors = f"{code_error_list}, {reg_error_list}"
        else:
            all_errors = f"{code_error_list}"
    else:
        all_errors = f"{reg_error_list}"

    return all_errors,reg_sections_list,code_list 
    

def convert_to_pdf(input_html, output_pdf):
 
    with open(input_html, 'r', encoding='utf-8') as html_file:
        source_html = html_file.read()
    with open(output_pdf, "w+b") as result_file:
        pisa_status = pisa.CreatePDF(source_html, dest=result_file)
        return not pisa_status.err
    #pdfkit.from_file(input_html, output_pdf,options=options)

def add_page_numbers(input_path,output_path,pagenumbers):
    #this adds page numbers and also adds in the footers with what the reg or code section is on the page
    
    
    # Open the PDF file
    pdf = fitz.open(input_path)
  
    num_pages = len(pdf)
  
    if num_pages > max_length:
      
        pdf.save(output_path)
        pdf.close()
        
    else:
        font_size = 10  # Replace with your desired font size
        font_name = "TiRo"
    
        # These patterns are for adding the footers
        code_pattern = r'§\d+[a-zA-Z]?(-\d+)?\.\s'  ##FOOTERS DO NOT WORK
        #reg_pattern = r"§\d+(\.\d+)?([a-zA-Z]?)-(\d+|[a-zA-Z]+)"
        #reg_pattern = r"(§[0-9A-Z\(\)]+\.[A-Z0-9()-]+) (?=[^a-z]+\.)"
        reg_pattern = r"§\d+[a-zA-Z]*(?:\([a-zA-Z]+\))?\.\d+[a-zA-Z]?(?:\([a-zA-Z]\))?-[a-zA-Z\d]+"
        cover_page_pattern = 'Cover Page'
    
        code_regex = re.compile(code_pattern)
        reg_regex = re.compile(reg_pattern)
        cover_page_regex = re.compile(cover_page_pattern)
    
        # keep a running list for the footers
        bookmark_list = [" "]
     
    
        # Iterate over each page
        for i, page in enumerate(pdf):
            # Get the page number
          
            if i >= 2:
                
                page_number = i - 1 # The idea here is actually i + 1 (because i starts at 0) - 2 (because we are skipping the first two pages)
            
                # Get the dimensions of the page
                page_width = page.rect.width
                page_height = page.rect.height
    
                # pull out the text of the page
                text = page.get_text()
                #this next line is because on the Linux operating system, the spaces between words in the PDF that's generated by pdfkit (in "convert_to_pdf" above) are slightly too large, and then when PyMuPdf pulls out the text, it can't recognize the spaces and puts \uFFFD instead. When pypdf pulls it out it puts multiple spaces between the words, but that's addressing the same problem. It works fine on Windows but not Linux, and Pythonanywhere is Linux. See https://www.pythonanywhere.com/forums/topic/33332/ 
                text = text.replace('\uFFFD', ' ')
               
                #search for the patterns in the page for the footers
                cover_page_matches = cover_page_regex.findall(text)
                code_matches = [match.group() for match in code_regex.finditer(text)]
                reg_matches = [match.group() for match in reg_regex.finditer(text)]
                #reg_matches = reg_regex.findall(text)
                
                
                #if it is a cover page, there shouldn't be a footer. I put "Cover Page" in white text on all the cover pages. It's a space so that the footer from the previous page doesn't carry over
                if cover_page_matches:
                    bookmark = " "
                    bookmark_list.append(bookmark)
                
                # if the code pattern matches, the first match is what goes in the footer, and the last match goes in the list. This is for both the code and the regs    
                elif code_matches:
                    bookmark = f"Code {code_matches[0][:-2]}"
                    bookmark_to_add =  f"Code {code_matches[-1][:-2]}"
                    bookmark_list.append(bookmark_to_add)
                elif reg_matches:
                    
                    bookmark = f"Reg. {reg_matches[0]}"
                    bookmark_to_add = f"Reg. {reg_matches[-1]}"
                    bookmark_list.append(bookmark_to_add)
                # if there wasn't a match, put the last item on the bookmark list into the footer. This is what makes the footer be the last section that started on a previous page if there are no matches.    
                else:
                    bookmark = bookmark_list[-1]
                
    
                # Calculate the position for the page number
                page_number_x = page_width / 2 - 20  # center of the page
                
                # Position for the footer text depends on page number
                if page_number % 2 == 0:  # even page number
                    bookmark_x = 20  # left side of the page
                else:  # odd page number
                    bookmark_x = page_width - len(bookmark) * font_size  # right side of the page, assuming each character is roughly the size of the font
    
                y = page_height - 20  # Adjust the position vertically
                
                # Add the page number
                if pagenumbers:
                    annot = page.add_freetext_annot((page_number_x, y, page_number_x + 40, y + 20), str(page_number))
                    annot.update(fontname=font_name, fontsize=font_size)
                
                # Add the footer
                if bookmark:
                    annot = page.add_freetext_annot((bookmark_x, y, bookmark_x + len(bookmark) * font_size, y + 20), bookmark)
                    annot.update(fontname=font_name, fontsize=font_size)
    
        # Save the modified PDF to the output path
      
        pdf.save(output_path)
        pdf.close()

    return num_pages

def add_bookmarks(document,codelist,outputname):

    doc = fitz.open(document)
    toc = doc.get_toc()
  
    for item in codelist:       
        #Define the string to search for. The regs don't have a period after them, but the code sections do. You have to search for the code section with a period after it or it will find the reg for example §1 in §1.61-1.
        if "." in str(item) and "-" in str(item):
            pattern = fr'§{item}'
            to_add = pattern 
        else:
            pattern = fr'§{item}.'
            to_add = pattern[:-1] #get rid of the period

        # Search for the string on each page
        for i in range(len(doc)):
            page = doc[i]
            text = page.get_text()
            # Search for the string. make the search case insensitive
            patterntosearch = re.escape(str(pattern))
            compiled_pattern = re.compile(patterntosearch, re.IGNORECASE)
            
            # if the pattern is found on the page, add a bookmark to the page in the table of contents. the "2" in the list to append is because the Code and Reg sections are the second level of bookmarks, embedded under the first-level bookmarks of Code and Regulations. The first level of bookmarks goes in in merge_pdf and then this gets called after that function.                
            if re.search(compiled_pattern,text):
                toc.append([2, to_add, i + 1])
                break
          
    toc = sorted(toc, key=lambda x: x[2])
    # Set the table of contents
    doc.set_toc(toc)
    
    doc.save(f'{outputname}')

def merge_pdfs(file_paths, output_path):

    merger = fitz.open()
    toc = []
    current_page = 1  # We start from page 1

    for file in file_paths:
        
         pdf = fitz.open(file)
        
        # Extract text from the first page of the pdf
         page = pdf[0]  # Get first page
         text = page.get_text()  # Extract the text
        
         # Assume the title is the first line of text on the page
         for line in text.split('\n'):
            # Remove leading/trailing whitespace
            line = line.strip()
        
            # If the line is not empty, use it as the title
            if line:
                title = line
                break  # Split the text by newline and get the first line
         
         if "§" not in title:
             toc.append([1, title, current_page])  # Use title as the bookmark title
             
         current_page += pdf.page_count  # Update current_page
         merger.insert_pdf(pdf)  # Now insert the contents of this file
         # toc = sorted(toc, key=lambda x: x[2])

    merger.set_toc(toc)  # Set the TOC on the merged document

    merger.save(f'{output_path}')
    merger.close()
    
def create_code_book(bookname,sectionsToUse,timenum,orderlist,pagenumbers):
    
    #create the HTML files with just the code and regulation sections that you want
    introduction_string = ci.intro_info
    path_short = 'CodeRegs/FilesForBook'  
    all_errors, reg_section_list,code_sections_list = createSelectedCodeRegsHTML(sectionsToUse,timenum)
    code_name = f'{code_file_name}.{timenum}.pdf'
    reg_name = f'{reg_file_name}.{timenum}.pdf'
    filler_title_pdf = f'saved_code/allfillertitle.{timenum}.pdf'
    
    numbered_name = f'saved_code/numbered_{bookname}.pdf'
    all_section_list = code_sections_list + reg_section_list
   
    #convert the code html to PDF
    convert_to_pdf(f'saved_code/codefillertitle.{timenum}.html',f"saved_code/{code_name}") 
    #convert the reg html to PDF
   
    convert_to_pdf(f'saved_code/regfillertitle.{timenum}.html',f"saved_code/{reg_name}")
    
    #add cover pages
    
    possible_include_dict[code_dictionary_entry] = f"saved_code/{code_name}"
    possible_include_dict[reg_dictionary_entry] =  f"saved_code/{reg_name}"
    
    
    if orderlist:
      
        dir_list_2 = [f"{possible_include_dict[x]}" for x in orderlist]
      
        if code_dictionary_entry in orderlist:
            code_sections_index = dir_list_2.index(possible_include_dict[code_dictionary_entry])
            dir_list_2.insert(code_sections_index,f'{path_short}/04ACodeCoverSheet.pdf')
       
        if reg_dictionary_entry in orderlist: 
            reg_sections_index = dir_list_2.index(possible_include_dict[reg_dictionary_entry])
            dir_list_2.insert(reg_sections_index,f'{path_short}/05ARegCoverSheet.pdf')
        
        for item in orderlist:
            introduction_string += intro_language[item]
        
        introduction_string += ci.about_info
        
        intro_title_base = f'saved_code/00Intro.{timenum}'
        with open(f'{intro_title_base}.html', 'w') as f:
                f.write(introduction_string)
        convert_to_pdf(f'{intro_title_base}.html',f'{intro_title_base}.pdf')
        
        dir_list_2.insert(0,f'{intro_title_base}.pdf')
        dir_list_2.insert(0,f'{path_short}/00ACover.pdf')
      
    else:
        
        files_to_include = ['Edited IRC Table of Contents (All Classes)','Inflation Rev. Proc.','Depreciation Rev. Proc.',code_dictionary_entry,reg_dictionary_entry] 
        for item in files_to_include:
            introduction_string += intro_language[item]
            
        introduction_string += ci.about_info
        
        intro_title_base = f'saved_code/00Intro.{timenum}'
        with open(f'{intro_title_base}.html', 'w') as f:
                f.write(introduction_string)
        convert_to_pdf(f'{intro_title_base}.html',f'{intro_title_base}.pdf')
        
        dir_list = sorted(os.listdir(path_short))
        dir_list_2 = [f'{path_short}/{x}' for x in dir_list]
        dir_list_2.insert(1,f'{intro_title_base}.pdf')
        dir_list_2.insert(-1,f"saved_code/{code_name}")
        dir_list_2.append(f"saved_code/{reg_name}")
        
        #dir_list_2.insert(0,f'{intro_title_base}.pdf')
    
    #merge all the PDFs to create the whole book   
  
    merge_pdfs(dir_list_2,filler_title_pdf)
    
    
    num_pages = add_page_numbers(f"{filler_title_pdf}", f'{numbered_name}',pagenumbers)
    
    os.remove(f"{filler_title_pdf}")
    os.rename( f'{numbered_name}',f"{filler_title_pdf}")
    
    
    add_bookmarks(f"{filler_title_pdf}",all_section_list,f"saved_code/{bookname}.pdf")
    
    if num_pages > max_length:
        footer_error = f"Because the number of pages in your PDF was greater than {max_length}, the program was unable to add footers or page numbers."
    else:
        footer_error = ""




    #add the page numbers    


    return all_errors, footer_error
    
# this function is if you want to play around with this without generating the whole files first--it's just checking to see what the merger version looks like
def create_book_from_files(code_html,reg_html,orderlist):
    code_name = 'saved_code/04BCode.pdf'
    reg_name = 'saved_code/05BRegs.pdf'
    #convert the code html to PDF
    
    convert_to_pdf(code_html,code_name) 
    
    #convert the reg html to PDF
    
    convert_to_pdf(reg_html,reg_name)
    
    path_short = 'CodeRegs/FilesForBook'    
    
    if orderlist:
        dir_list = orderlist
    else:    
        dir_list = sorted(os.listdir(path_short))
        dir_list_2 = [f'{path_short}/{x}' for x in dir_list]
        dir_list_2.insert(-1,code_name)
        dir_list_2.append(reg_name)
    
    #merge all the PDFs to create the whole book
    
    merge_pdfs(dir_list_2,'pdftitle')

def create_intro():
    
    introduction_string = ci.intro_info
    for item in possible_files_list:
        introduction_string += intro_language[item]
    introduction_string += ci.about_info
    
    intro_title_base = 'CodeRegs/FilesForBook/00BIntro'
    with open(f'{intro_title_base}.html', 'w') as f:
            f.write(introduction_string)
    convert_to_pdf(f'{intro_title_base}.html',f'{intro_title_base}.pdf')

#convert_to_pdf('saved_code/codefillertitle.1692593126.660765.html','saved_code/test.pdf')
#print(process_code_excel('CodeAndRegSectionsToUseShort.xlsx'))
#create_intro()
#convert_code_to_html('saved_code/codehtmltest.xml','saved_code/codehtmltest2.html','12356')
 
#parse26('CodeRegs/CodeAndRegSectionsToUse.xlsx','codefillertitle.xml')
#convert_code_to_html('codefillertitle.xml','codefillertitle.html',6)
#create26NoNotes()
  
#createCodeAndRegs('usc26.xml','Section26NoNotes.xml','codesectionstouse.xlsx','SelectedSections20230226.xml','title-26-reg.htm','regsectionstouse.xlsx','SelectedRegulations20230223.html')

#createRegs('title-26-all.htm','regsectionstouse.xlsx','SelectedRegulations20230226.html')
#createCode('usc26.xml','Section26NoNotes.xml','codesectionstousepartnership.xlsx','SelectedPshipSections20221226.xml')

#createRegsFile()

#create26NoNotes()