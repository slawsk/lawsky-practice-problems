# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 10:26:09 2023

@author: Sarah
"""
import functionmodules as fm
import convertfile

introtext = convertfile.introtext

current_year = fm.current_year_for_book
rev_proc = fm.rev_proc_for_book

intro_info = f"""
{introtext}
    <body>
    <h2>Introduction</h2>
    <p>This book was generated from the website <a href="https://www.lawskypracticeproblems.org/codeandregs">https://www.lawskypracticeproblems.org/codeandregs</a>, which was coded by Sarah Lawsky, a professor at the University of Illinois College of Law. To the extent anything in this book could be subject to copyright, it is freely available under the <a href = "https://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International license</a>--roughly speaking, you can share this or use it for any purpose, just so long as you give appropriate credit, distribute the material so other people can use it under the same terms, and don't create any additional restrictions.</p>
            <p>This book contains the following materials. It is designed for tax courses taught in {current_year}.</p>"""


table_contents_info = """
<h2>Edited Table of Contents</h2>
<p>The edited table of contents is not the table of contents of this volume. Rather, it is an edited table of contents of the entire Internal Revenue Code (USC title 26), to provide a sense of the structure of the Code.</p>
"""

inflation_info = f"""
<h2>Inflation-Adjusting Revenue Procedure</h2>
<p>This revenue procedure, {rev_proc}, provides inflation adjustments for {current_year}.</p>
"""

depreciation_info = """
<h2>Depreciation Revenue Procedure (Excerpts)</h2>
<p>This revenue procedure, Rev. Proc. 87-57, provides tables to assist with determining depreciation.</p>
"""

selected_sections_code_info = f"""
<h2>Selected Sections of the Internal Revenue Code</h2>
<p>The selected sections of the Internal Revenue Code are from a government website, <a href="https://uscode.house.gov/download/download.shtml">https://uscode.house.gov/download/download.shtml</a>. This Code is up to date as of {fm.code_updated}.</p>
"""

selected_sections_regs_info = f"""
<h2>Selected Sections of Regulations</h2>
<p>The selected sections of the regulations, 26 CFR, are from a government website, 
<a href="https://www.ecfr.gov/current/title-26">https://www.ecfr.gov/current/title-26/</a>.  
These regulations are up to date as of {fm.regs_updated}. 
</p>
"""

about_info = """
</body>
</html>
"""
