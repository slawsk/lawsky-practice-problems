# Lawsky Practice Problems
This repository contains all the code for [Lawsky Practice Problems](https://www.lawskypracticeproblems.org/). This code has been used in the past to generate tax problems [to test the capabilities of large language models](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4476325). 

You can use it for that or for anything else, subject to the terms of [the license under which I have made this code available](https://www.gnu.org/licenses/agpl-3.0.en.html). There are almost certainly mistakes in this code; I will keep it up to date to some degree, but I will not necessarily push all changes to this respository right away. And I learned how to program by writing this code, so there are also definitely some...interesting programming choices here. 

If you create a project or write a paper using this code please let me know, so that I can add a link to your project on the [Practice Problems website](https://www.lawskypracticeproblems.org/otherprojects). I would also very much appreciate it if you would credit me and this repository in your project.

A few notes about setting this up, if you want to run the whole thing:
- Use the requirements.txt file to create the virtual environment to get this running.
- The substantive files, the ones that have the problems in them, are basictaxproblems.py, for the basic tax problems, and partnershiptaxproblems.py, for the partnership tax problems. This is probably the most useful material here; these are the files that were used to generate the problems for the LLM paper, for example.
- The main program, the one that creates the website, is taxproblems.py
- The structure of this repository is the structure that matches running the whole website (e.g., the location of files within CodeRegs, the existence of the folders saved_code and saved_files).
- The files for the part of the website to generate the code and regs selected sections are very large and thus are zipped in this repository
