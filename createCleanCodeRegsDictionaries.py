# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 05:59:26 2022

@author: Sarah
"""

# AT LEAST ANNUALLY, OR WHEN LAW CHANGES
# Download the files for the code and regulations.
# Run create_clean_files()
# Move Code Dictionary, Reg Dictionary, RegDictionaryWithJPG, RegDictionaryWithJPGForPA to CodeRegs

# You may need to do image extraction again - see CodeRegs/ImageExtraction

# Add the current updated Revenue Procedure to FilesForBook
# Add the cover page to it as well

# update the current year for the book year in fm.current_year_for_book
# update the current Rev Proc for the book year in fm.rev_proc_for_book
# update the current of date for the code and regs in functionmodules

# Update the introduction to FilesForBook (this can be automated to some extent)
# Add the correct revenue procedure in FilesForBooks/ AND in assets/

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

type_run = fm.type_run

location_dictionary = {'home': 'CodeRegs/RegDictionaryWithJPG.txt',
                       'pa': 'CodeRegs/RegDictionaryWithJPGForPA.txt'}

correct_reg_dict = location_dictionary[type_run]

max_length = 450
code_file_name = '04BCode'
reg_file_name = '05BRegs'
path_short = 'CodeRegs/FilesForBook'
code_dictionary_entry = 'Code sections you listed on your spreadsheet'
reg_dictionary_entry = 'Reg sections you listed on your spreadsheet'

possible_include_dict = {'Edited IRC Table of Contents (All Classes)': f'{path_short}/01TOCEdited.pdf', 'Edited IRC Table of Contents (Fed Tax)': 'CodeRegs/TOCBasic.pdf', 'Edited IRC Table of Contents (Corporate Tax)': 'CodeRegs/TOCCorporate.pdf',
                         'Edited IRC Table of Contents (Partnership Tax)': 'CodeRegs/TOCPartnership.pdf', 'Inflation Rev. Proc.': f'{path_short}/02InflationRevProc.pdf', 'Depreciation Rev. Proc.': f'{path_short}/03DepreciationRevProc.pdf', code_dictionary_entry: code_file_name, reg_dictionary_entry: reg_file_name}

intro_language = {'Edited IRC Table of Contents (All Classes)': ci.table_contents_info, 'Edited IRC Table of Contents (Fed Tax)': ci.table_contents_info, 'Edited IRC Table of Contents (Corporate Tax)': ci.table_contents_info,
                  'Edited IRC Table of Contents (Partnership Tax)': ci.table_contents_info, 'Inflation Rev. Proc.': ci.inflation_info, 'Depreciation Rev. Proc.': ci.depreciation_info, code_dictionary_entry: ci.selected_sections_code_info, reg_dictionary_entry: ci.selected_sections_regs_info}

possible_files_list = list(possible_include_dict.keys())

# all_code_title_xml = f'CodeNoNotes_{current_year}.xml'
# all_code_title_html = f'CodeNoNotes_{current_year}.html'
# all_regs_title = f'RegsNoNotes_{current_year}.html'

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

def replace_with_dict(text, replace_dict):
    for key, value in replace_dict.items():
        text = re.sub(key, value, text)
    return text

def replace_in_value(text, old, new):
    return text.replace(old, new)

# Fix the problem in 1.704-2(m), 1.751-1(g), 1.1001-2(c), 1.119, that the /div is in the wrong place and the regulations don't print:

reg_replace_dict= {
'1.461-4':{'Consequently, V incurs $20,00 for the 1993 taxable year.':'Consequently, V incurs [$20,000] for the 1993 taxable year.'},
'1.707-1':{'Similarly, a partner who receives guaranteed payments is not regarded as an employee of the partnership for the purposes of withholding of tax at source, deferred compensation plans, etc. The provisions of this paragraph may be illustrated by the following examples:</p></div>':'Similarly, a partner who receives guaranteed payments is not regarded as an employee of the partnership for the purposes of withholding of tax at source, deferred compensation plans, etc. The provisions of this paragraph may be illustrated by the following examples:</p>',
"702(a), the partnership has a $10,000 ordinary loss and $30,000 in capital gains. X's 30 percent distributive shares of these amounts are $3,000 ordinary loss and $9,000 capital gain. In addition, X has received a $10,000 guaranteed payment which is ordinary income to him.</p></div>":"702(a), the partnership has a $10,000 ordinary loss and $30,000 in capital gains. X's 30 percent distributive shares of these amounts are $3,000 ordinary loss and $9,000 capital gain. In addition, X has received a $10,000 guaranteed payment which is ordinary income to him.</p></div></div>"},
'1.704-2':{'<div id="p-1.704-2(m)"><p class="indent-1" data-title="1.704-2(m)"><span class="paragraph-hierarchy"><span class="paren">(</span>m<span class="paren">)</span></span> <em class="paragraph-heading">Examples.</em>  The principles of this section are illustrated by the following examples:</p></div>': '<div id="p-1.704-2(m)"><p class="indent-1" data-title="1.704-2(m)"><span class="paragraph-hierarchy"><span class="paren">(</span>m<span class="paren">)</span></span> <em class="paragraph-heading">Examples.</em>  The principles of this section are illustrated by the following examples:</p>',
"that particular liability to the extent of the increase in minimum gain with respect to that liability.</p> </div>": "that particular liability to the extent of the increase in minimum gain with respect to that liability.</p> </div> </div>"},
'1.751-1':{'<div id="p-1.751-1(g)"><p class="indent-1" data-title="1.751-1(g)"><span class="paragraph-hierarchy"><span class="paren">(</span>g<span class="paren">)</span></span> <em class="paragraph-heading">Examples.</em>  Application of the provisions of section 751 may be illustrated by the following examples:</p></div>': '<div id="p-1.751-1(g)"><p class="indent-1" data-title="1.751-1(g)"><span class="paragraph-hierarchy"><span class="paren">(</span>g<span class="paren">)</span></span> <em class="paragraph-heading">Examples.</em>  Application of the provisions of section 751 may be illustrated by the following examples:</p>',
"<p>(2) <em>The part of the distribution not under section 751(b).</em> The analysis under this subparagraph should be made in accordance with the principles illustrated in paragraph (e)(2) of examples 3, 4, and 5 of this paragraph.</p> </div>": "<p>(2) <em>The part of the distribution not under section 751(b).</em> The analysis under this subparagraph should be made in accordance with the principles illustrated in paragraph (e)(2) of examples 3, 4, and 5 of this paragraph.</p> </div> </div>"},
'1.1001-2':{'<div id="p-1.1001-2(c)"><p class="indent-1" data-title="1.1001-2(c)"><span class="paragraph-hierarchy"><span class="paren">(</span>c<span class="paren">)</span></span> <em class="paragraph-heading">Examples.</em>  The provisions of this section may be illustrated by the following examples. In each example assume the taxpayer uses the cash receipts and disbursements method of accounting, makes a return on the basis of the calendar year, and sells or disposes of all property which is security for a given liability.</p></div>': '<div id="p-1.1001-2(c)"><p class="indent-1" data-title="1.1001-2(c)"><span class="paragraph-hierarchy"><span class="paren">(</span>c<span class="paren">)</span></span> <em class="paragraph-heading">Examples.</em>  The provisions of this section may be illustrated by the following examples. In each example assume the taxpayer uses the cash receipts and disbursements method of accounting, makes a return on the basis of the calendar year, and sells or disposes of all property which is security for a given liability.</p>',
 '<p class="inline-paragraph">In 1980, F transfers to a creditor an asset with a fair market value of $6,000 and the creditor discharges $7,500 of indebtedness for which F is personally liable. The amount realized on the disposition of the asset is its fair market value ($6,000). In addition, F has income from the discharge of indebtedness of $1,500 ($7,500 − $6,000).</p> </div>': '<p class="inline-paragraph">In 1980, F transfers to a creditor an asset with a fair market value of $6,000 and the creditor discharges $7,500 of indebtedness for which F is personally liable. The amount realized on the disposition of the asset is its fair market value ($6,000). In addition, F has income from the discharge of indebtedness of $1,500 ($7,500 − $6,000).</p> </div> </div>'},
 '1.119-1':{'<div id="p-1.119-1(f)"><p class="indent-1" data-title="1.119-1(f)"><span class="paragraph-hierarchy"><span class="paren">(</span>f<span class="paren">)</span></span> <em class="paragraph-heading">Examples.</em>  The provisions of section 119 may be illustrated by the following examples:</p></div>': '<div id="p-1.119-1(f)"><p class="indent-1" data-title="1.119-1(f)"><span class="paragraph-hierarchy"><span class="paren">(</span>f<span class="paren">)</span></span> <em class="paragraph-heading">Examples.</em>  The provisions of section 119 may be illustrated by the following examples:</p>',
'<p class="inline-paragraph">A hospital maintains a cafeteria on its premises where all of its 230 employees may obtain a meal during their working hours. No charge is made for these meals. The hospital furnishes such meals in order to have each of 210 of the employees available for any emergencies that may occur, and it is shown that each such employee is at times called upon to perform services during his meal period. Although the hospital does not require such employees to remain on the premises during meal periods, they rarely leave the hospital during their meal period. Since the hospital furnishes meals to each of substantially all of its employees in order to have each of them available for emergency call during his meal period, all of the hospital employees who obtain their meals in the hospital cafeteria may exclude from their gross income the value of such meals.</p> </div>':'<p class="inline-paragraph">A hospital maintains a cafeteria on its premises where all of its 230 employees may obtain a meal during their working hours. No charge is made for these meals. The hospital furnishes such meals in order to have each of 210 of the employees available for any emergencies that may occur, and it is shown that each such employee is at times called upon to perform services during his meal period. Although the hospital does not require such employees to remain on the premises during meal periods, they rarely leave the hospital during their meal period. Since the hospital furnishes meals to each of substantially all of its employees in order to have each of them available for emergency call during his meal period, all of the hospital employees who obtain their meals in the hospital cafeteria may exclude from their gross income the value of such meals.</p></div></div>'},
'1.304-2':{'<div id="p-1.304-2(c)"><p class="indent-1" data-title="1.304-2(c)"><span class="paragraph-hierarchy"><span class="paren">(</span>c<span class="paren">)</span></span> The application of section 304(a)(1) may be illustrated by the following examples:</p></div>':'<div id="p-1.304-2(c)"><p class="indent-1" data-title="1.304-2(c)"><span class="paragraph-hierarchy"><span class="paren">(</span>c<span class="paren">)</span></span> The application of section 304(a)(1) may be illustrated by the following examples:</p>',
'<p class="inline-paragraph">Corporation X and corporation Y each have outstanding 100 shares of common stock. H, an individual, W, his wife, S, his son, and G, his grandson, each own 25 shares of stock of each corporation. H sells all of his 25 shares of stock of corporation X to corporation Y. Since both before and after the transaction H owned directly and constructively 100 percent of the stock of corporation X, and assuming that section 302(b)(1) is not applicable, the amount received by him for his stock of corporation X is treated as a dividend to him to the extent of the earnings and profits of corporation Y.</p></div>':'<p class="inline-paragraph">Corporation X and corporation Y each have outstanding 100 shares of common stock. H, an individual, W, his wife, S, his son, and G, his grandson, each own 25 shares of stock of each corporation. H sells all of his 25 shares of stock of corporation X to corporation Y. Since both before and after the transaction H owned directly and constructively 100 percent of the stock of corporation X, and assuming that section 302(b)(1) is not applicable, the amount received by him for his stock of corporation X is treated as a dividend to him to the extent of the earnings and profits of corporation Y.</p></div></div>'},
'1.304-3':{'<div id="p-1.304-3(b)"><p class="indent-1" data-title="1.304-3(b)"><span class="paragraph-hierarchy"><span class="paren">(</span>b<span class="paren">)</span></span> Section 304(a)(2) may be illustrated by the following example:</p></div>':'<div id="p-1.304-3(b)"><p class="indent-1" data-title="1.304-3(b)"><span class="paragraph-hierarchy"><span class="paren">(</span>b<span class="paren">)</span></span> Section 304(a)(2) may be illustrated by the following example:</p>','''<p class="inline-paragraph">Corporation M has outstanding 100 shares of common stock which are owned as follows: B, 75 shares, C, son of B, 20 shares, and D, daughter of B, 5 shares. Corporation M owns the stock of Corporation X. B sells his 75 shares of Corporation M stock to Corporation X. Under section 302(b)(3) this is a termination of B's entire interest in Corporation M and the full amount received from the sale of his stock will be treated as payment in exchange for this stock, provided he fulfills the requirements of section 302(c)(2) (relating to an acquisition of an interest in the corporations).</p>''':'''<p class="inline-paragraph">Corporation M has outstanding 100 shares of common stock which are owned as follows: B, 75 shares, C, son of B, 20 shares, and D, daughter of B, 5 shares. Corporation M owns the stock of Corporation X. B sells his 75 shares of Corporation M stock to Corporation X. Under section 302(b)(3) this is a termination of B's entire interest in Corporation M and the full amount received from the sale of his stock will be treated as payment in exchange for this stock, provided he fulfills the requirements of section 302(c)(2) (relating to an acquisition of an interest in the corporations).</p></div>'''},
'1.305-2':{'<div id="p-1.305-2(b)"><p class="indent-1" data-title="1.305-2(b)"><span class="paragraph-hierarchy"><span class="paren">(</span>b<span class="paren">)</span></span> <em class="paragraph-heading">Examples.</em>  The application of section 305(b)(1) may be illustrated by the following examples:</p></div>':'<div id="p-1.305-2(b)"><p class="indent-1" data-title="1.305-2(b)"><span class="paragraph-hierarchy"><span class="paren">(</span>b<span class="paren">)</span></span> <em class="paragraph-heading">Examples.</em>  The application of section 305(b)(1) may be illustrated by the following examples:</p>','of the distribution to which section 301 applies is $1 per share whether the shareholder elects to take cash or stock and whether the shareholder is an individual or a corporation. Such amount will also be used in determining the dividend paid deduction of corporation X and the reduction in earnings and profits of corporation X.</p></div>':'of the distribution to which section 301 applies is $1 per share whether the shareholder elects to take cash or stock and whether the shareholder is an individual or a corporation. Such amount will also be used in determining the dividend paid deduction of corporation X and the reduction in earnings and profits of corporation X.</p></div></div>'},
'1.305-3':{'<div id="p-1.305-3(e)"><p class="indent-1" data-title="1.305-3(e)"><span class="paragraph-hierarchy"><span class="paren">(</span>e<span class="paren">)</span></span> <em class="paragraph-heading">Examples.</em>  The application of section 305(b)(2) to distributions of stock and section 305(c) to deemed distributions of stock may be illustrated by the following examples:</p></div>':'<div id="p-1.305-3(e)"><p class="indent-1" data-title="1.305-3(e)"><span class="paragraph-hierarchy"><span class="paren">(</span>e<span class="paren">)</span></span> <em class="paragraph-heading">Examples.</em>  The application of section 305(b)(2) to distributions of stock and section 305(c) to deemed distributions of stock may be illustrated by the following examples:</p>','<p>(iii) <em>Effective date.</em> This <em>Example 15</em> applies to stock issued on or after December 20, 1995. For previously issued stock, see <a href="/on/2024-07-25/title-26/section-1.305-3#p-1.305-3(e)" class="cfr external">§ 1.305-3(e)</a> <em>Example (15)</em> (as contained in the <a href="/on/2024-07-25/title-26/part-1" class="cfr external">26 CFR part 1</a> edition revised April 1, 1995).</p></div>':'<p>(iii) <em>Effective date.</em> This <em>Example 15</em> applies to stock issued on or after December 20, 1995. For previously issued stock, see <a href="/on/2024-07-25/title-26/section-1.305-3#p-1.305-3(e)" class="cfr external">§ 1.305-3(e)</a> <em>Example (15)</em> (as contained in the <a href="/on/2024-07-25/title-26/part-1" class="cfr external">26 CFR part 1</a> edition revised April 1, 1995).</p></div></div>'},
'1.305-4':{'<div id="p-1.305-4(b)"><p class="indent-1" data-title="1.305-4(b)"><span class="paragraph-hierarchy"><span class="paren">(</span>b<span class="paren">)</span></span> <em class="paragraph-heading">Examples.</em>  The application of section 305(b)(3) may be illustrated by the following examples:</p></div>':'<div id="p-1.305-4(b)"><p class="indent-1" data-title="1.305-4(b)"><span class="paragraph-hierarchy"><span class="paren">(</span>b<span class="paren">)</span></span> <em class="paragraph-heading">Examples.</em>  The application of section 305(b)(3) may be illustrated by the following examples:</p>',' can reasonably be expected to result in the receipt of preferred stock by some common shareholders and the receipt of common stock by other common shareholders, the distribution is a distribution of property to which section 301 applies.</p></div>':' can reasonably be expected to result in the receipt of preferred stock by some common shareholders and the receipt of common stock by other common shareholders, the distribution is a distribution of property to which section 301 applies.</p></div></div>'},
'1.83-1':{'with respect to such property.</p>\n</div>\n<div id=\"p-1.83-1(f)\"><p class=\"indent-1\" data-title=\"1.83-1(f)\"><span class=\"paragraph-hierarchy\"><span class=\"paren\">(</span>f<span class=\"paren\">)</span></span> <em class=\"paragraph-heading\">Examples.</em>  The provisions of this section may be illustrated by the following examples:</p></div>\n<div class=\"example\">':'with respect to such property.</p>\n</div>\n<div id=\"p-1.83-1(f)\"><p class=\"indent-1\" data-title=\"1.83-1(f)\"><span class=\"paragraph-hierarchy\"><span class=\"paren\">(</span>f<span class=\"paren\">)</span></span> <em class=\"paragraph-heading\">Examples.</em>  The provisions of this section may be illustrated by the following examples:</p>\n<div class=\"example\">','Under <a class=\"cfr external\" href=\"/on/2024-07-25/title-26/section-1.83-4#p-1.83-4(b)(2)\">\u00a7 1.83-4(b)(2)</a>, I\'s basis in the X corporation stock is $120 per share.</p>\n</div>\n\n</div>':'Under <a class=\"cfr external\" href=\"/on/2024-07-25/title-26/section-1.83-4#p-1.83-4(b)(2)\">\u00a7 1.83-4(b)(2)</a>, I\'s basis in the X corporation stock is $120 per share.</p>\n</div></div>\n\n</div>'}
}

code_replace_dict = {'paragraphs (3) and (4) of sections\u202f<ref class=\"footnoteRef\" idref=\"fn002161\">1</ref> 1222 by substituting \u201c3 years\u201d for \u201c1 year\u201d,</content>\n</paragraph>\n<continuation class=\"indent0 firstIndent0\" style=\"-uslm-lc:I10\">shall be treated as short-term capital gain':'paragraphs (3) and (4) of sections [sic] 1222 by substituting \u201c3 years\u201d for \u201c1 year\u201d,</content>\n</paragraph>\n<continuation class=\"indent0 firstIndent0\" style=\"-uslm-lc:I10\">shall be treated as short-term capital gain',
                     "\u2153":" 1/3"
                     
}


# TO RUN ANNUALLY

def createStatuteNoNotes(titlenumber):
    # URL: https://uscode.house.gov/download/download.shtml
    # when you update the code, make sure to change code_updated in functionmodules
    with open(f'OtherStatutes/GovernmentDownloads/usc{titlenumber}.xml', encoding='utf8') as fp:
        soup = BeautifulSoup(fp, 'xml')

    soup_str = str(soup)

# Convert the string back to a BeautifulSoup object
    soup = BeautifulSoup(soup_str, 'xml')

    to_remove = ["note", "notes", "sourceCredit"]
    for r in to_remove:
        for p in soup.find_all(r):
            p.decompose()

    div_elements = soup.find_all('section')
    div_library = {}
    for div in div_elements:

        section_number = div.num
        section_title = div.heading
        section_number_and_title = f"<section>{section_number}{section_title}</section>"
        section_number_and_title = section_number_and_title.replace(
            '\u2013', '-')

        subsection_elements = div.find_all('subsection')
        new_dict = {}
        new_dict['num_title_string'] = section_number_and_title

        if subsection_elements:
            for item in subsection_elements:
                subsection_number = item.get("identifier").rsplit('/', 1)[1]
                new_dict[subsection_number] = str(item)

        else:
            num_tag = div.find('num')
            if num_tag is not None:
                num_tag.decompose()

            heading_tag = div.find('heading')
            if heading_tag is not None:
                heading_tag.decompose()

            new_dict['all'] = str(div)

        div_library[find_code_for_usc_26(div.get("identifier"))] = new_dict


    with open(f'OtherStatutes/Code{titlenumber}Dictionary.txt', 'w', encoding='utf-8') as txt_file:
        txt_file.write(json.dumps(div_library))



def create26NoNotes():
    # URL: https://uscode.house.gov/download/download.shtml
    # when you update the code, make sure to change code_updated in functionmodules
    with open('CodeRegs/GovernmentDownloads/usc26.xml', encoding='utf8') as fp:
        soup = BeautifulSoup(fp, 'xml')

    soup_str = str(soup)

# Perform the replacements

    soup_str = replace_with_dict(soup_str, code_replace_dict)

# Convert the string back to a BeautifulSoup object
    soup = BeautifulSoup(soup_str, 'xml')

    to_remove = ["note", "notes", "sourceCredit"]
    for r in to_remove:
        for p in soup.find_all(r):
            p.decompose()

    div_elements = soup.find_all('section')
    div_library = {}
    for div in div_elements:

        section_number = div.num
        section_title = div.heading
        section_number_and_title = f"<section>{section_number}{section_title}</section>"
        section_number_and_title = section_number_and_title.replace(
            '\u2013', '-')

        subsection_elements = div.find_all('subsection')
        new_dict = {}
        new_dict['num_title_string'] = section_number_and_title

        if subsection_elements:
            for item in subsection_elements:
                subsection_number = item.get("identifier").rsplit('/', 1)[1]
                new_dict[subsection_number] = str(item)

        else:
            num_tag = div.find('num')
            if num_tag is not None:
                num_tag.decompose()

            heading_tag = div.find('heading')
            if heading_tag is not None:
                heading_tag.decompose()

            new_dict['all'] = str(div)

        div_library[find_code_for_usc_26(div.get("identifier"))] = new_dict



    # div_library['274']['o'] = new_274


    with open('CodeRegs/CodeDictionary.txt', 'w', encoding='utf-8') as txt_file:
        txt_file.write(json.dumps(div_library))



# this creates the Regs files with no notes; use this as the input for creating the Code and regs. Run this annually.


def createRegsFile():
    # URL: https://www.ecfr.gov/current/title-26/chapter-I/subchapter-A/part-1 , save the HTML file
    # for the 15a installment sale regs, https://www.ecfr.gov/current/title-26/chapter-I/subchapter-A/part-15a
    # For the 301 regs, go to here and save the relevant regs with the appropriate titles (see below): https://www.ecfr.gov/current/title-26/chapter-I/subchapter-F/part-301/subpart-ECFR5ffaf3310af6b61
    # for the 25 regs, go to https://www.ecfr.gov/current/title-26/chapter-I/subchapter-B/part-25
    # for the 20 regs, go to https://www.ecfr.gov/current/title-26/chapter-I/subchapter-B/part-20
    # for the 26 regs, https://www.ecfr.gov/current/title-26/chapter-I/subchapter-B/part-26

    # string together all the relevant regulations
    reg_string = ''
    directory = 'CodeRegs/GovernmentDownloads/RegFiles'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        with open(f, encoding='utf8') as infile:
            data = infile.read()
            reg_string = reg_string + data



    soup = BeautifulSoup(reg_string, 'lxml')

    # get rid of the editorial notes
    for p in soup.find_all('div', attrs={"class": "editorial-note"}):
        p.decompose()

    # get rid of the citations
    for p in soup.find_all('p', attrs={"class": "citation"}):
        p.decompose()

    div_library = {}
    div_elements = soup.find_all("div", attrs={"class": "section"})
    for div in div_elements:
        div_library[str(div.get("id"))] = str(div)



    for key, replacements in reg_replace_dict.items():
        if key in div_library:
            # Get the current value from the full dictionary
            current_value = div_library[key]

            # Perform the replacement
            for old_text, new_text in replacements.items():
                current_value = replace_in_value(current_value, old_text, new_text)

            # Update the value in the full dictionary
            div_library[key] = current_value



    with open('CodeRegs/RegDict.txt', 'w', encoding='utf-8') as txt_file:
        txt_file.write(json.dumps(div_library))




    # Now create the correct regulation dictionaries with the JPGS
    def replace_text_in_file(file_path_in, file_path_out, location):
        # Regular expression pattern for matching the URLs
        url_pattern = r'https://img\.federalregister\.gov/.+?/'

        # Read the original content of the file
        with open(file_path_in, 'r', encoding='utf-8') as file:
            content = file.read()

        # Replace the URLs using the regex pattern
        if location == 'home':
            content = re.sub(url_pattern, "../CodeRegs/jpg_pictures/", content)
        elif location == 'PA':
            content = re.sub(
                url_pattern, "/home/slawsky/taxappfiles/CodeRegs/jpg_pictures/", content)

        # Replace .png with .jpg
        content = content.replace(".png", ".jpg")

        # Write the modified content back to the file
        with open(file_path_out, 'w', encoding='utf-8') as file:
            file.write(content)

    # replace_text_in_file('CodeRegs/RegDict.txt', 'CodeRegs/RegDictionaryWithJPGForPA.txt', "PA")
    replace_text_in_file('CodeRegs/RegDict.txt', 'CodeRegs/RegDictionaryWithJPG.txt', "home")

def create_clean_files():
    print("creating code dictionary")
    create26NoNotes()
    print("creating reg dictionary")
    createRegsFile()


titlelist= [11,15,18,21,28,31,42,52]
    
def create_clean_titles(titlelist):
    map(createStatuteNoNotes,titlelist)

# create_clean_files()

create26NoNotes()

# createRegsFile()

