# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 05:59:26 2022

@author: Sarah
"""


# Don't forget to change type_run in convertfile.py after you upload it Python Anywhere--this is about the path for the files

from bs4 import BeautifulSoup, Tag
import pandas as pd
import os
import functionmodules as fm
import convertfile
import re
import fitz
import json
import create_intro as ci
from xhtml2pdf import pisa
from PIL import Image


from itertools import chain

current_year = fm.current_year_for_book
rev_proc = fm.rev_proc_for_book

# DO NOT FORGET TO CHANGE THIS WHEN YOU UPLOAD IT!!!

# location = 'home'
location = 'PA'

location_dictionary = {'home': 'CodeRegs/RegDictionaryWithJPG.txt',
                       'PA': 'CodeRegs/RegDictionaryWithJPGForPA.txt'}

correct_reg_dict = location_dictionary[location]

max_length = 450
code_file_name = '04BCode'
reg_file_name = '05BRegs'
path_short = 'CodeRegs/FilesForBook'
code_dictionary_entry = 'Code sections you listed on your spreadsheet'
reg_dictionary_entry = 'Reg sections you listed on your spreadsheet'

possible_include_dict = {'Edited IRC Table of Contents (All Classes)': f'{path_short}/01TOCEdited.pdf',
                         'Inflation Rev. Proc.': f'{path_short}/02InflationRevProc.pdf',
                         'Depreciation Rev. Proc.': f'{path_short}/03DepreciationRevProc.pdf', code_dictionary_entry: code_file_name, reg_dictionary_entry: reg_file_name}

intro_language = {'Edited IRC Table of Contents (All Classes)': ci.table_contents_info,
                  'Inflation Rev. Proc.': ci.inflation_info,
                  'Depreciation Rev. Proc.': ci.depreciation_info,
                  code_dictionary_entry: ci.selected_sections_code_info,
                  reg_dictionary_entry: ci.selected_sections_regs_info}

possible_files_list = list(possible_include_dict.keys())

type_run = convertfile.type_run

def find_the_code_section(x):
    return x.split('.', 1)[1].split('-', 1)[0]


def find_code_for_usc_26(x):
    return x.rsplit('/', 1)[1][1:].replace('\u2013', '-')


def find_the_number(x):
    try:
        return int(x)
    except:
        pattern = r"\d+\("
        match_no_letter = re.search(pattern, x)
        match = re.match(r'^\d+', x)
        if match_no_letter:
            return int(match.group()) + .1
        else:
            return int(match.group()) + .2


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


def bookmark_mark(item):
    return f'<p>headingsixstart***{item}***headingsixend</p>'


# Pull the sections that you want from the code and the regs. Run these on the files that have no notes except prospective amendment notes, that you have created by running create_clean_files

# createRegsFile()

def fix_subsection(x):
    if isinstance(x, str):
        x = x.replace(" ", "")
        return re.sub('[^a-zA-Z,]', ',', x).lower()
    else:
        return 'all'


def process_code_excel(sectionsToUse):
    code_df = pd.read_excel(sectionsToUse, sheet_name=0)

    if code_df.empty or code_df['Code'].isna().all():
        # Return empty DataFrame with expected columns
        return pd.DataFrame(columns=['Code', 'SubsectionList', 'NumberToSort'])

    # get rid of empty rows
    code_df = code_df[code_df['Code'].notna()]

    if code_df.empty:
        return pd.DataFrame(columns=['Code', 'SubsectionList', 'NumberToSort'])

    # remove spaces from the subsections list
    code_df['SubsectionClean'] = code_df['Subsection'].apply(
        lambda x: fix_subsection(x))
    code_df['SubsectionList'] = code_df['SubsectionClean'].apply(
        lambda x: create_list_from_string(x))

    # sort the columns, noting that some of them are numbers and some are strings

    code_df = code_df.groupby('Code')['SubsectionList'].apply(
        lambda x: merge_lists(x)).reset_index()
    code_df['NumberToSort'] = code_df['Code'].apply(
        lambda x: find_the_number(x))
    code_df = code_df.sort_values(by=['NumberToSort'])

    return code_df


def extract_section_and_specific(regulation):
    # Split at the period first
    after_period = regulation.split('.', 1)[1]
    
    # Check if there's a hyphen
    if '-' in after_period:
        # Original logic for regulations with hyphens
        section = after_period.split('-', 1)[0]
        specific = find_the_number(after_period.split('-', 1)[1])
    else:
        # For regulations without hyphens
        section = after_period
        specific = 0
    
    return section, specific

# Apply the function


def process_regs_excel(sectionsToUse):

    regs_df = pd.read_excel(sectionsToUse, sheet_name=1)
    
    if regs_df.empty or regs_df['Regulation'].isna().all():
        # Return empty DataFrame with expected columns
        return pd.DataFrame(columns=['Regulation', 'SubsectionList', 'Section', 'Specific', 'NumberToSort'])
    
    # get rid of empty rows

    regs_df = regs_df[regs_df['Regulation'].notna()]

 
    if regs_df.empty:
        return pd.DataFrame(columns=['Regulation', 'SubsectionList', 'Section', 'Specific', 'NumberToSort'])

    regs_df['Regulation'] = regs_df['Regulation'].astype(str)

    # get the sections and specific reg from the overall regulation
    regs_df['Intro'] = regs_df['Regulation'].apply(
        lambda x: x.split('.', 1)[0])

    # remove spaces from the subsections list
    regs_df['SubsectionClean'] = regs_df['Subsection'].apply(
        lambda x: fix_subsection(x))
    regs_df['SubsectionList'] = regs_df['SubsectionClean'].apply(
        lambda x: create_list_from_string(x))
    # sort the columns, noting that some of them are numbers and some are strings

    regs_df = regs_df.groupby('Regulation')['SubsectionList'].apply(
        lambda x: merge_lists(x)).reset_index()
    regs_df[['Section', 'Specific']] = regs_df['Regulation'].apply(
    lambda x: pd.Series(extract_section_and_specific(x))
)
    
    regs_df['NumberToSort'] = regs_df['Section'].apply(
        lambda x: find_the_number(x))
    regs_df = regs_df.sort_values(by=['NumberToSort', 'Specific'])

    return regs_df

def parse26(sectionsToUse, outputTitle):

    introtext = '<root>'
    endingtext = '</root>'

    df = process_code_excel(sectionsToUse)

    if df.empty:
        file = open(outputTitle, 'w', encoding='utf-8')
        file.write(introtext + endingtext)
        file.close()
        return "", []

    code_sections_list = df['Code'].tolist()

    subsections_list = df['SubsectionList'].tolist()
    #listified = [x.split(",") for x in subsections_list]

    lookupdict = dict(zip(code_sections_list, subsections_list))

    with open('CodeRegs/CodeDictionary.txt', 'r', encoding='utf8') as fp:
        codestring = fp.read()
    code_dict = json.loads(codestring)

    textstring = ""
    error_string = ""
    # include the relevant sections

    for item in code_sections_list:
        try:
            textstring += bookmark_mark(item)

            subsection_dict = code_dict[str(item)]

            textstring += subsection_dict['num_title_string']
            selected_subsections = lookupdict[item]
            if selected_subsections[0] in ['all', 'All', ""]:
                selected_subsections = list(subsection_dict.keys())[1:]
            for subsection in selected_subsections:
                textstring += subsection_dict[subsection]

        except:
            error_string += f"Section {item}, "
            code_sections_list.remove(item)

    file = open(outputTitle, 'w', encoding='utf-8')
    file.write(introtext)
    file.write(textstring)
    file.write(endingtext)
    file.close()

    return error_string[:-2], code_sections_list


def replace_text_in_file(file_path, old_text, new_text):
    with open(file_path, 'r') as file:
        content = file.read()

    modified_content = content.replace(old_text, new_text)

    with open(file_path, 'w') as file:
        file.write(modified_content)


def convert_to_html(inputtitle, outputtitle):
    convertfile.convert_file_to_html(inputtitle, outputtitle)


def convert_code_to_html(inputtitle, outputtitle, timenum):
    interim_title = f'saved_code/interim_{timenum}.html'

    convertfile.convert_file_to_html(inputtitle, interim_title)

    replace_dict = {'Thephaseoutamount': "The phaseout amount", 'Thephaseoutpercentageis': 'The phaseout percentage is',
                    '<b>The applicable</b><b>recovery period</b><b>is:</b>': '<b>The applicable recovery period is:</b>'}

    with open(interim_title, 'r', encoding='utf-8') as file:
        content = file.read()

    for item in replace_dict.keys():
        content = content.replace(item, replace_dict[item])

    with open(outputtitle, 'w', encoding='utf-8') as file:
        file.write(content)


def parseRegs(sectionsToUse, outputTitle):

    # create the intro and endtext that allows the css file

    if type_run == 'home':
        introtext = """<!doctype html>
        <html>
          <head>
          <meta charset="utf-8">
            <link href="/mnt/c/Users/sbl083/Dropbox/Python/taxwebsite/CodeRegs/regsStyleFast.css" rel="stylesheet" />
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

    # create the file
    df = process_regs_excel(sectionsToUse)

    if df.empty:
        file = open(outputTitle, 'w', encoding='utf-8')
        file.write(introtext + endtext)
        file.close()
        return "", []  

    reg_sections_list = df['Regulation'].tolist()
    subsections_list = df['SubsectionList'].tolist()

    lookupdict = dict(zip(reg_sections_list, subsections_list))

    with open(correct_reg_dict, 'r', encoding='utf8') as fp:
        regstring = fp.read()
    reg_dict = json.loads(regstring)

    textstring = introtext
    error_string = ""

    messed_up_list = ['1.1041-1T', '1.263(a)-3', '1.263A-1']

    for item in reg_sections_list:
        item = item.strip()
        try:
            textstring += bookmark_mark(item)
            selected_subsections = lookupdict[item]
            if selected_subsections[0] in ['all', 'All', ""] or item in messed_up_list:
                textstring += reg_dict[item].replace('§ ', '§')
            else:
                soup = BeautifulSoup(reg_dict[item], 'lxml')
                section_identifier = f"{item}"
                section_num_and_title = soup.find('h4')
                num_heading = str(section_num_and_title).replace('§ ', '§')
                textstring += f"{num_heading}"
                for subsection in selected_subsections:
                    subsection_identifier = f"p-{section_identifier}({subsection})"
                    subsection_to_add = soup.find(
                        'div', {'id': subsection_identifier})
                    if str(subsection_to_add) == "None":
                        error_string += f"Section {subsection_identifier[2:]}, "
                    else:
                        textstring += (str(subsection_to_add))
        except:
            error_string += f"Section {item}, "
            reg_sections_list.remove(item)

    def uppercase_match(match):
        # Return the original <h1> tags but with the inner text converted to uppercase
        return '<h4>' + match.group(1).upper() + '</h4>'

    textstring += endtext
    textstring = re.sub(r'<h4>(.*?)</h4>', uppercase_match,
                        textstring, flags=re.DOTALL)
    textstring = re.sub(r'headingsixstart', '<h6>', textstring)
    textstring = re.sub(r'headingsixend', '</h6>',textstring)
    file = open(outputTitle, 'w', encoding='utf-8')
    file.write(textstring)
    file.close()

    return error_string[:-2], reg_sections_list


def createSelectedCodeRegsHTML(sectionsToUse, timenum):
    code_error_list, code_list = parse26(
        sectionsToUse, f'saved_code/codefillertitle.{timenum}.xml')
    convert_code_to_html(
        f'saved_code/codefillertitle.{timenum}.xml', f'saved_code/codefillertitle.{timenum}.html', f'{timenum}')
    reg_error_list, reg_sections_list = parseRegs(
        sectionsToUse, f'saved_code/regfillertitle.{timenum}.html')
    if len(code_error_list) > 2:
        if len(reg_error_list) > 2:
            all_errors = f"{code_error_list}, {reg_error_list}"
        else:
            all_errors = f"{code_error_list}"
    else:
        all_errors = f"{reg_error_list}"

    return all_errors, reg_sections_list, code_list


def convert_to_pdf(input_html, output_pdf):

    with open(input_html, 'r', encoding='utf-8') as html_file:
        source_html = html_file.read()
    with open(output_pdf, "w+b") as result_file:
        pisa_status = pisa.CreatePDF(source_html, dest=result_file)
        return not pisa_status.err
    #pdfkit.from_file(input_html, output_pdf,options=options)


def add_page_numbers(input_path, output_path, pagenumbers):
    # this adds page numbers and also adds in the footers with what the reg or code section is on the page
    
    # Open the PDF file
    pdf = fitz.open(input_path)

    num_pages = len(pdf)

    if num_pages > max_length:

        pdf.save(output_path)
        pdf.close()

    else:
        font_size = 10  # Replace with your desired font size
        font_name = "TiRo"

        # keep a running list for the footers
        bookmark_list = [" "]

        # Iterate over each page
        for i, page in enumerate(pdf):
            # Get the page number

            if i >= 2:

                # The idea here is actually i + 1 (because i starts at 0) - 2 (because we are skipping the first two pages)
                page_number = i - 1

                # Get the dimensions of the page
                page_width = page.rect.width
                page_height = page.rect.height

                # pull out the text of the page
                text = page.get_text()
                # this next line is because on the Linux operating system, the spaces between words in the PDF that's generated by pdfkit (in "convert_to_pdf" above) are slightly too large, and then when PyMuPdf pulls out the text, it can't recognize the spaces and puts \uFFFD instead. When pypdf pulls it out it puts multiple spaces between the words, but that's addressing the same problem. It works fine on Windows but not Linux, and Pythonanywhere is Linux. See https://www.pythonanywhere.com/forums/topic/33332/
                text = text.replace('\uFFFD', ' ')

                # search for the patterns in the page for the footers
                def extract_matches(text):
                        pattern = r'\*\*\*(.*?)\*\*\*'
                        match = re.findall(pattern, text)
                        return match

                matches = extract_matches(text)

                cover_page_matches = re.search('Cover Page',text)

                # if it is a cover page, there shouldn't be a footer. I put "Cover Page" in white text on all the cover pages. It's a space so that the footer from the previous page doesn't carry over
                if cover_page_matches:
                    bookmark = " "
                    bookmark_list.append(bookmark)

                # if the pattern matches, the first match is what goes in the footer, and the last match goes in the list. This is for both the code and the regs
                elif matches:
                    bookmark = f"§{matches[0]}"
                    bookmark_to_add = f"§{matches[-1]}"
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
                    # right side of the page, assuming each character is roughly the size of the font
                    bookmark_x = page_width - len(bookmark) * font_size

                y = page_height - 20  # Adjust the position vertically

                # Add the page number
                if pagenumbers:
                    annot = page.add_freetext_annot(
                        (page_number_x, y, page_number_x + 40, y + 20), str(page_number))
                    annot.update(fontname=font_name, fontsize=font_size)

                # Add the footer
                if bookmark:
                    annot = page.add_freetext_annot(
                        (bookmark_x, y, bookmark_x + len(bookmark) * font_size, y + 20), bookmark)
                    annot.update(fontname=font_name, fontsize=font_size)

        # Save the modified PDF to the output path

        pdf.save(output_path)
        pdf.close()

    return num_pages

def add_bookmarks(inputname, section_list, outputname):
    doc = fitz.open(inputname)
    toc = doc.get_toc()
    
    # Extract page text 
    page_texts = [(i, page.get_text()) for i, page in enumerate(doc)]
    
    # search for each bookmark
    for item in section_list:
        pattern = re.compile(rf'\*\*\*{re.escape(str(item))}\*\*\*', re.IGNORECASE)
        
        for page_num, text in page_texts:
            if pattern.search(text):
                toc.append([2, f'§ {item}', page_num + 1])
                break  
    
    toc.sort(key=lambda x: (x[2], x[0]))
    doc.set_toc(toc)
    doc.save(outputname)



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

        if "***" not in title:
            # Use title as the bookmark title
            toc.append([1, title, current_page])
    
        current_page += pdf.page_count  # Update current_page
        merger.insert_pdf(pdf)  # Now insert the contents of this file


    merger.set_toc(toc)  # Set the TOC on the merged document

    merger.save(f'{output_path}')
    merger.close()


def create_code_book(bookname, sectionsToUse, timenum, orderlist, pagenumbers):
    import time
    start = time.time()

    # create the HTML files with just the code and regulation sections that you want
    introduction_string = ci.intro_info
    path_short = 'CodeRegs/FilesForBook'
    
    # Check if sheets are empty before processing
    code_df = process_code_excel(sectionsToUse)
    regs_df = process_regs_excel(sectionsToUse)
    
    code_is_empty = code_df.empty
    regs_is_empty = regs_df.empty
    print(f"Excel processing: {time.time() - start:.2f}s")
    
    start = time.time()
    all_errors, reg_section_list, code_sections_list = createSelectedCodeRegsHTML(
        sectionsToUse, timenum)
    print(f"create Selected Code Regs HTML: {time.time() - start:.2f}s")
    
    start = time.time()
    
    code_name = f'{code_file_name}.{timenum}.pdf'
    reg_name = f'{reg_file_name}.{timenum}.pdf'
    filler_title_pdf = f'saved_code/allfillertitle.{timenum}.pdf'

    numbered_name = f'saved_code/numbered_{bookname}.pdf'
    all_section_list = code_sections_list + reg_section_list

    # Only convert code html to PDF if not empty
    if not code_is_empty:

        convert_to_pdf(
            f'saved_code/codefillertitle.{timenum}.html', f"saved_code/{code_name}")
        possible_include_dict[code_dictionary_entry] = f"saved_code/{code_name}"

    # Only convert reg html to PDF if not empty
    if not regs_is_empty:

        convert_to_pdf(
            f'saved_code/regfillertitle.{timenum}.html', f"saved_code/{reg_name}")
        possible_include_dict[reg_dictionary_entry] = f"saved_code/{reg_name}"

    if orderlist:
        # Filter orderlist to exclude empty sections
        filtered_orderlist = []
        for item in orderlist:
            if item == code_dictionary_entry and code_is_empty:
                continue
            elif item == reg_dictionary_entry and regs_is_empty:
                continue
            else:
                filtered_orderlist.append(item)

        dir_list_2 = [f"{possible_include_dict[x]}" for x in filtered_orderlist]

        # Only add code cover page if code sections exist
        if code_dictionary_entry in filtered_orderlist:
            code_sections_index = dir_list_2.index(
                possible_include_dict[code_dictionary_entry])
            dir_list_2.insert(code_sections_index,
                              f'{path_short}/04ACodeCoverSheet.pdf')

        # Only add reg cover page if reg sections exist
        if reg_dictionary_entry in filtered_orderlist:
            reg_sections_index = dir_list_2.index(
                possible_include_dict[reg_dictionary_entry])
            dir_list_2.insert(reg_sections_index,
                              f'{path_short}/05ARegCoverSheet.pdf')

        # Only add intro language for sections that exist
        for item in filtered_orderlist:
            introduction_string += intro_language[item]

        introduction_string += ci.about_info

        intro_title_base = f'saved_code/00Intro.{timenum}'
        with open(f'{intro_title_base}.html', 'w') as f:
            f.write(introduction_string)
        convert_to_pdf(f'{intro_title_base}.html', f'{intro_title_base}.pdf')

        dir_list_2.insert(0, f'{intro_title_base}.pdf')
        dir_list_2.insert(0, f'{path_short}/00ACover.pdf')

    else:
        # Default file inclusion, but exclude empty sections
        files_to_include = ['Edited IRC Table of Contents (All Classes)', 'Inflation Rev. Proc.',
                            'Depreciation Rev. Proc.']
        
        # Only include if not empty
        if not code_is_empty:
            files_to_include.append(code_dictionary_entry)
        if not regs_is_empty:
            files_to_include.append(reg_dictionary_entry)
            
        for item in files_to_include:
            introduction_string += intro_language[item]

        introduction_string += ci.about_info

        intro_title_base = f'saved_code/00Intro.{timenum}'
        with open(f'{intro_title_base}.html', 'w') as f:
            f.write(introduction_string)
        convert_to_pdf(f'{intro_title_base}.html', f'{intro_title_base}.pdf')

        dir_list = ['00ACover.pdf','01TOCEdited.pdf','02InflationRevProc.pdf','03DepreciationRevProc.pdf']
        dir_list_2 = [f'{path_short}/{x}' for x in dir_list]
        dir_list_2.insert(1, f'{intro_title_base}.pdf')
        
        # Only add code and reg files if they're not empty
        if not code_is_empty:
            dir_list_2.append(f"{path_short}/04ACodeCoverSheet.pdf")
            dir_list_2.append(f"saved_code/{code_name}")
        if not regs_is_empty:
            dir_list_2.append(f"{path_short}/05ARegCoverSheet.pdf")
            dir_list_2.append(f"saved_code/{reg_name}")

    # merge all the PDFs to create the whole book
    print(f"created PDFS: {time.time() - start:.2f}s")
    
    start = time.time()

    merge_pdfs(dir_list_2, filler_title_pdf)
    print(f"merged pdfs: {time.time() - start:.2f}s")
    
    start = time.time()

    num_pages = add_page_numbers(
        f"{filler_title_pdf}", f'{numbered_name}', pagenumbers)
    print(f"added page numbers: {time.time() - start:.2f}s")
    
    start = time.time()

    os.remove(f"{filler_title_pdf}")
    os.rename(f'{numbered_name}', f"{filler_title_pdf}")
    
    add_bookmarks(f"{filler_title_pdf}", all_section_list,
                  f"saved_code/{bookname}.pdf")
    print(f"added bookmarks: {time.time() - start:.2f}s")
    
    start = time.time()

    if num_pages > max_length:
        footer_error = f"Because the number of pages in your PDF was greater than {max_length}, the program was unable to add footers or page numbers."
    else:
        footer_error = ""

    return all_errors, footer_error

# this function is if you want to play around with this without generating the whole files first--it's just checking to see what the merger version looks like


def create_book_from_files(code_html, reg_html, orderlist):
    code_name = 'saved_code/04BCode.pdf'
    reg_name = 'saved_code/05BRegs.pdf'
    # convert the code html to PDF

    convert_to_pdf(code_html, code_name)

    # convert the reg html to PDF

    convert_to_pdf(reg_html, reg_name)

    path_short = 'CodeRegs/FilesForBook'

    if orderlist:
        dir_list = orderlist
    else:
        dir_list = sorted(os.listdir(path_short))
        dir_list_2 = [f'{path_short}/{x}' for x in dir_list]
        dir_list_2.insert(-1, code_name)
        dir_list_2.append(reg_name)

    # merge all the PDFs to create the whole book

    merge_pdfs(dir_list_2, 'pdftitle')


def create_intro():

    introduction_string = ci.intro_info
    for item in possible_files_list:
        introduction_string += intro_language[item]
    introduction_string += ci.about_info

    intro_title_base = 'CodeRegs/FilesForBook/00BIntro'
    with open(f'{intro_title_base}.html', 'w') as f:
        f.write(introduction_string)
    convert_to_pdf(f'{intro_title_base}.html', f'{intro_title_base}.pdf')


def test_local():
    import time
    
    # CONFIGURE THESE:
    excel_file = 'test_sections_long.xlsx'  # Path to your Excel file with code/reg sections
    output_name = 'test_book'           # Name for output PDF (will be saved_code/test_book.pdf)
    timenum = int(time.time())      
    
    order_list = None
    
    add_page_numbers_flag = True
    
    print(f"Starting book generation...")
    print(f"Excel file: {excel_file}")
    print(f"Output: saved_code/{output_name}.pdf")
    print(f"Time ID: {timenum}")
    print("-" * 60)
    

    all_errors, footer_error = create_code_book(
            bookname=output_name,
            sectionsToUse=excel_file,
            timenum=timenum,
            orderlist=order_list,
            pagenumbers=add_page_numbers_flag
        )
        
    print("-" * 60)
    print("COMPLETE!")
    print(f"Output file: saved_code/{output_name}.pdf")
        
    if all_errors:
            print("\nErrors encountered:")
            print(all_errors)
        
    if footer_error:
            print("\nFooter warning:")
            print(footer_error)
            
