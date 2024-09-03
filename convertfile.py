# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 14:27:50 2023

@author: Sarah
"""

from bs4 import BeautifulSoup
import re

type_run = 'home'


if type_run == 'home':
    introtext = '''<!DOCTYPE html>
    <head>
    <meta charset="UTF-8">
    <link href="../CodeRegs/codeStyleFast.css" rel="stylesheet" />

    </head>'''


def uppercase_match(match):
    # Return the original <h1> tags but with the inner text converted to uppercase
    return '<h1>' + match.group(1).upper() + '</h1>'

def convert_file_to_html(inputtitle,outputtitle):
    
    # Parse the XML file
    with open(inputtitle, "r",encoding='utf-8') as f:
        contents = f.read()
    
    soup = BeautifulSoup(contents, 'lxml')
    
    # Define tag replacements
    tag_replacements = {'paragraph':'div', 
      'root':'body', 
      'ref':'a', 
      'subclause':'div', 
      'continuation':'div', 
      'subparagraph':'div',  
      'section':'div', 
      'subsection':'div', 
      'clause':'div',
      'num':'heading'}
        
    
    for elem in soup.find_all('num'):
            elem.name = 'heading'
    # Special handling for heading tags
    
    for heading in soup.find_all('heading'):
        if heading.parent.name == 'section':
            heading.name = 'h1'
        elif heading.parent.name == 'subsection':
            heading.name = 'h2'
        elif heading.parent.name == 'paragraph':
            heading.name = 'h3'
        elif heading.parent.name == 'subparagraph':
            heading.name = 'h4'
        else:
            heading.name = 'h5'  # or whatever other tag you want as a default
    
    attrs_to_remove = ['class', 'id', 'identifier', 'style','value','xmlns','content']  # add more as needed
    for tag in soup():
        for attr in attrs_to_remove:
            del tag[attr]
    
    tags_to_remove = ['chapeau','content','p','root']
    for remove_tag in tags_to_remove:
        for item in soup.find_all(remove_tag):
            item.replace_with_children()
    
    for tag, replacement in tag_replacements.items():
        for elem in soup.find_all(tag):
            if tag == 'paragraph':
                elem['class'] = 'paragraph'
            elif tag == 'subparagraph':
                elem['class'] = 'subparagraph'
            # elif tag == 'num':
            #     elem['class'] = 'number'
            elif tag == 'clause':
                elem['class'] = 'clause'
            elif tag == 'subclause':
                elem['class'] = 'subclause'
            elem.name = replacement
    
    
    # Remove certain attributes from all tags
    soupystring = str(soup)
 
    for i in range(1,6):
        soupystring = soupystring.replace(f"</h{i}><h{i}>", "")
    soupystring = re.sub(r'<h1>(.*?)</h1>', uppercase_match, soupystring, flags=re.DOTALL)     
    soupystring = soupystring.replace("\u2000",'')
    soupystring = soupystring.replace("\u202f",'')
    soupystring = re.sub(r'(?<!\))</h3>', '</h3>\u2014', soupystring)
    soupystring = re.sub(r'(?<!\))</h4>', '</h4>\u2014', soupystring)
    soupystring = re.sub(r'(?<!\))</h5>', '</h5>\u2014', soupystring)
    soupystring = re.sub(r'headingsixstart', '<h6>', soupystring)
    soupystring = re.sub(r'headingsixend', '</h6>', soupystring)
    
    # Write out the modified soup as HTML
    with open(outputtitle, "w",encoding='utf-8') as f:
        f.write(introtext+soupystring)

