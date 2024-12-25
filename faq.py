# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 15:17:14 2019

@author: Lawsky
"""

import functionmodules as fm

MAX_QUIZ_QUESTIONS = fm.MAX_QUIZ_QUESTIONS

general_faq = """  
This website is created and maintained by [Sarah Lawsky](https://www.sarahlawsky.org/), a professor at [Northwestern Pritzker School of Law](http://www.law.northwestern.edu/faculty/profiles/SarahLawsky/). The [Open Source page](https://www.lawskypracticeproblems.org/otherprojects) provides information about the underlying code.

The material generated by the website is made available under the [Creative Commons Attribution-ShareAlike 4.0 International license](https://creativecommons.org/licenses/by-sa/4.0/), which means, roughly, that you can share this or use it for any purpose, just so long as you give appropriate credit, distribute the material so other people can use it under the same terms, and don't create any additional restrictions.

You can [read more](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3876486) about the website and the pedagogical goals that motivate it.

**Q: Who is this website for?**<br>
A: Anyone who wants to use it. A professor can use to generate problems, code books, or quizzes for teaching, or to give students direct access to it; a student can use it to practice for tax class or create code books; or anything else. 

**Q: Does the website take into account inflation adjustments?**<br>
A: Yes. Problems, rate graphs, and rate calculations take into account inflation adjustments.

**Q: I found a mistake! I have a suggestion!**<br>
A: If you find an error or have a suggestion, please [let me know](http://www.law.northwestern.edu/faculty/profiles/SarahLawsky/). """


practice_problems_faq = """
**Q: What does the Practice Problems page do?** <br>
A: It generates multiple-choice practice problems for federal income tax and partnership tax. The problems are a random selection of facts, names, and randomly (but thoughtfully) generated numbers about a range of federal income tax topics and partnership tax topics. You decide whether you want to focus on federal income tax or partnership tax, and then you can pick a particular topic within that subject, or you can have the website to pick both a topic and problem within that subject at random. 

**Q: Are the answers also random?** <br>
A: Mostly, no. The multiple-choice answers are based on mistakes people commonly make (though the list of possible answers may include one or more random answers).

**Q: What happens once I pick an answer?** <br>
A: If you pick a wrong answer, the website usually provides a substantive hint about what you did wrong. A right answer usually returns a full explanation. In many of the explanations of answers both right and wrong, there is a link to the relevant code section. 

**Q: Do the questions repeat?**<br>
A: The chance of a particular problem's ever repeating precisely the same way is extremely, extremely small. There are a *lot* of different possible problems (though not actually infinitely many). That the numbers and names change doesn't necessarily provide conceptually different questions, of course. But different types of problems toggle a bunch of different facts and relationships between the numbers, all of which do change the problem conceptually. For example, for like-kind exchanges, there are five different facts than can toggle (asset is personal use or business use, whether there is debt relief and whom that debt relief favors (someone who provides boot or not), etc.) and four different questions. For installment sales there are even more toggles; for unrestricted property as compensation, many fewer. """


statutes_faq = """
**Q: What is the point of the Statutes page?** <br>
A: The Statutes page allows people to practice reading and understanding language from the Internal Revenue Code. You don't need any tax knowledge to work these problems, and the problems aren't meant to teach substantive law. Rather, the Statutes page is to help people get more comfortable reading and applying language from the Code.

**Q: But there are a lot of other parts of reading a statute. This is just, like, little word problems.**<br>
A: Yes! The Statutes page may help develop the skill of translating a small amount of technical language into a formula, and it may give students more confidence when it comes to tackling the statute. The Statutes page does not help develop the skill of, for example, following cross-references, or understanding how different portions of the Code interact with each other, or applying canons of construction, or any of the many, many other skills that go into reading, understanding, and interpreting the Code."""

quizzes_faq = """ 
**Q: I downloaded a quiz answer sheet, and the file is called "taxquiz" (normal) but then there is a really long string of numbers after that (less normal). What is that string of numbers?**<br>
A: That is the [Unix timestamp](https://en.wikipedia.org/wiki/Unix_time) of the moment you generated that answer sheet. You can translate that into a more comprehensible date by entering that number into a [converter](https://www.epochconverter.com/). For example, there's a file in my downloads called taxquiz.1733662191.974549.docx. When I put 1733662191.974549 into the converter, it tells me I generated that quiz on Sunday, December 8, 2024 12:49:51.974 PM Greenwich Mean Time. This approach means, among other things, that every quiz answer sheet you download will have a unique filename.

"""

attribution = "This website is created and maintained by [Sarah Lawsky](https://www.sarahlawsky.org/), a tax law professor at [Northwestern Pritzker School of Law](http://www.law.northwestern.edu/faculty/profiles/SarahLawsky/). The website uses [Dash](https://plot.ly/dash/) and [Python](https://www.python.org/) and is freely available under the [Creative Commons Attribution-ShareAlike 4.0 International license](https://creativecommons.org/licenses/by-sa/4.0/)."

quiz_explanation = f"""This page generates quizzes for the subject you have selected (either Federal Income Tax or Partnership Tax). These quizzes likely do not replicate the complexity of actual quizzes or tests you may take, but they may help you drill the basics. 

To take the quiz, enter the number of questions the quiz should have, up to {MAX_QUIZ_QUESTIONS}; select topics; and click "Generate Quiz." You will receive that many questions, on those topics, generated from the same program that generates the problems on the [Practice Problems page](https://www.lawskypracticeproblems.org/). 

Select your answers for all the questions and then click "Submit Answers." 

The website will tell you how many you got right and supply the correct answers and explanations. You can download the problems and answer key, and you can reset the page to do another quiz."""


problem_page_intro = f"""Assume that the law for {str(fm.current_year)} applies in all years.
      
Select the problem topic and click "Submit Topic." If no topic is selected, the website picks a random topic.
      
"""

partnership_addl_info = """The number to the left of each topic is the relevant chapter or section of [Wootton & Lawsky, Partnership Taxation](https://www.amazon.com/Exam-Pro-Partnership-Taxation-Objective-ebook/dp/B082B9FBBP/)."""

codeandregsdownload = f"""
Create a PDF of selected tax Code and regulation sections for {fm.current_year_for_book} for almost any U.S. federal tax class."""

codeandregs = f"""
**Q: What exactly is in this Selected Sections book?**<br>
A: The default items included in this book are:
* the sections and subsections of the Code and regulations that you select, with bookmarks in the PDF for each section,
* an edited table of contents for the whole IRC,
* the inflation-adjusting Revenue Procedure for {fm.current_year_for_book} ({fm.rev_proc_for_book}), and 
* excerpts from Rev. Proc. 87-57, the depreciation tables.

**Q: Where is the content coming from?**<br>
A: The Code sections contained in this book are from the [Office of Law Revision Counsel](http://uscode.house.gov/download/download.shtml) and are current through {fm.code_updated}. The regulation sections are from the [eCFR](https://www.ecfr.gov/current/title-26/chapter-I/subchapter-A/part-1) and are current through {fm.regs_updated}. Specifically, this website includes, from the US Code, [all of Title 26](https://uscode.house.gov/download/download.shtml); and from the 26 CFR Chapter I regulations, [Subchapter A, Part 1](https://www.ecfr.gov/current/title-26/chapter-I/subchapter-A/part-1); [Subchapter A, Part 15a](https://www.ecfr.gov/current/title-26/chapter-I/subchapter-A/part-15a) (good installment sale regs in here!); [Subchapter B, Part 25](https://www.ecfr.gov/current/title-26/chapter-I/subchapter-B/part-25); [Subchapter B, Part 20](https://www.ecfr.gov/current/title-26/chapter-I/subchapter-B/part-20); [Subchapter B, Part 26](https://www.ecfr.gov/current/title-26/chapter-I/subchapter-B/part-26); and [Subchapter F, Part 301](https://www.ecfr.gov/current/title-26/chapter-I/subchapter-F/part-301/subpart-ECFR5ffaf3310af6b61).

**Q: Why did you do this?**<br>
A: Internal Revenue Code and regulation sections are the most important reading for any federal tax course. There are four problems with commercial selected Code and regs books. First, commercial selected sections books are expensive: $100 or more for information that is freely available. Second, they are too long: they contain far more sections than any one class needs, because they are trying to meet the needs of many different classes. Third, they are too short: a professor might want to assign some sections that aren't in a particular commercially edited book. Fourth, they may go out of date quickly, as the law might change, and inflation adjustments do change. 

In contrast, this Selected Sections is available for free; the book you create will include exactly the sections and subsections you want; and it is easy to update as the law and year change.

**Q: I don't have a list of all the sections I need. Do you have spreadsheets that people use for various actual tax classes, so I can generate a book for myself anyway?** <br>
A: Yes. Keeping in mind that of course not everyone assigns the same sections for every class, so these may not include all of what you need and may also have extra sections you don't need (indeed, that's part of what motivated this project), here are spreadsheets from law professors for Selected Sections books for, respectively, [Federal Income Tax](/assets/FITCodeAndRegSections.xlsx); [Corporate Tax](/assets/CorporateCodeAndRegSections.xlsx); [Partnership Tax](/assets/PartnershipCodeAndRegSections.xlsx); and [Estate and Gift Tax](/assets/EstateGiftCodeAndRegSections.xlsx).

**Q:I like a hard copy better.**<br>
A: Me too. Luckily, in addition to the "printing out the PDF" option, there are a number of options for nicely-bound hard copies of PDFs print-on-demand for cost, maybe even including your school's bookstore or copy center. For example, you can [buy a bound hard copy of the Selected Sections PDF I created for my Basic Tax class](https://bit.ly/FedIncomeTaxSelectedSections) for cost at Lulu.com, just because I uploaded it there (it doesn't cost anything to upload it, and I don't get any money if you buy it).

**Q:What are those long strings of numbers in the file name of the Selected Sections book I downloaded?**<br>
A: That is the [Unix timestamp](https://en.wikipedia.org/wiki/Unix_time) of the moment you generated that Selected Sections book. You can translate that into a more comprehensible date by entering that number into a [converter](https://www.epochconverter.com/). For example, there's a file in my downloads called SelectedSections.1687277065.726598.pdf. When I put 1687277065.726598 into the converter, it tells me I generated that particular Selected Sections book on Tuesday, June 20, 2023 4:04:25.726 PM Greenwich Mean Time."""

code_template_explanation = """Create an Excel spreadsheet listing the Code and regulation sections and subsections you want in your Selected Sections book, and format it so that the program can process it. The simplest way to do this is to [download this sample spreadsheet](/assets/FITCodeAndRegSections.xlsx) and modify it--essentially, use it as a template. Here are some tips:
* The first worksheet of the spreadsheet includes your Code sections, and the second worksheet includes your Regs section.
* Leave the column names as they are: on the Code worksheet, the columns are "Code" and "Subsection"; on the Regs worksheet, the columns are "Regulation" and "Subsection".
* If you want to include all of the subsections for a section, put "all" in the "Subsection" column, or leave it blank.
* If you want to include only some of the subsections, put the ones you want to include in the "Subsection" column, with a comma separating the subsections.

Here are some things you don't have to worry about:
* It doesn't matter what order you enter the sections on the spreadsheet; the book will have the sections in numerical order.
* If you include the same section more than once in the spreadsheet, the book will include the section only once and include all the subsections you have listed in the various rows, in order, and only once.

"""

code_pick_explanation = """If you want, pick what to include in your book and in what order. It's fine if you skip this step and don't make any choices here; in that case, the table of contents will be the longer table of contents, the book will include all other possible items, and the document will have page numbers."""

code_upload_explanation = """Upload the Excel spreadsheet with the Code and regulation sections and subsections that you want in your Selected Sections book. 

The computer will automatically start creating your book once you have uploaded your spreadsheet. When the book is ready, you will see a message in Step 4 below providing a link you can click to download your book."""


be_patient = """Be patient--the processing can take a couple of minutes. Do not click on anything else on this page while you are waiting."""

other_projects_info = """The website is coded with [Dash](https://plot.ly/dash/) and [Python](https://www.python.org/). You can use [the code for this website](https://github.com/slawsk/lawsky-practice-problems/), including the code for generating the practice problems, for anything, subject to the terms of [the license under which I have made this code available](https://www.gnu.org/licenses/agpl-3.0.en.html).

If you build a project using this code, please let me know, so I can add a link and a description on this page."""

other_projects_list = """John J. Nay, David Karamardian, Sarah B. Lawsky, Wenting Tao, Meghana Bhat, Raghav Jain, Aaron Travis Lee, Jonathan H. Choi, and Jungo Kasai, [Large Language Models as Tax Attorneys: A Case Study in Legal Capabilities Emergence](https://royalsocietypublishing.org/doi/epdf/10.1098/rsta.2023.0159), 381 Phil. Transactions of the Royal Society A (2024), uses the code underlying this website to generate problems to assess the capabilities of large language models to answer tax law questions.

Andrew Mitchel, [check-the-box practice problems with graphics](https://www.andrewmitchel.com/resources/practice/check_the_box) representing the entity to be classified; [blog post explaining the new practice problems](https://www.andrewmitchel.com/blog/2024_12_lawksy-practice-problems).
"""
