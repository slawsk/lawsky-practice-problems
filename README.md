# lawsky-practice-problems
This repository contains all the code for [Lawsky Practice Problems](https://www.lawskypracticeproblems.org/). This code has been used in the past to generate tax problems [to test the capabilities of large language models](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4476325). The only difference at this point is that I have commented out the page that creates the selected Code and Regulations, because the files I would need to upload for that are enormous, and the file structure if that's included is a little complex. I will try to get that cleaned up so I can upload the full version (but that page is definitely the least interesting of what this website provides).

You can use it for that or for anything else, subject to the terms of [the license under which I have made this code available](https://www.gnu.org/licenses/agpl-3.0.en.html). There are almost certainly mistakes in this code; I will keep it up to date to some degree, but I will not necessarily push all changes to this respository right away. And I learned how to program by writing this code, so there are also definitely some...interesting programming choices here. 

If you create a project or write a paper using this code please let me know, so that I can add a link to your project on the [Practice Problems website](https://www.lawskypracticeproblems.org/otherprojects). I would also very much appreciate it if you would credit me and this repository in your project.

A few notes about setting this up, if you want to run the whole thing:
- Add an empty folder within the directory where you're running it called saved_files (the program needs this file to store some temporary files it generates).
- Use the requirements.txt file to create the virtual environment to get this running.
- The main program, the one that creates the website, is taxproblemsnocoderegs.py
- The substantive files, the ones that have the problems in them, are basictaxproblems.py, for the basic tax problems, and partnershiptaxproblems.py, for the partnership tax problems. This is probably the most useful materials; these are the files that were used to generate the problems for the LLM paper, for example.
