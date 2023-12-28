# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 17:33:03 2020

@author: Lawsky
"""
import functionmodules as fm
import random
import statutorylanguage as sl

instruction_language = '''
All language to evaluate is drawn from the Internal Revenue Code. Nonetheless, use this page only to practice evaluating statutory language, not to learn actual law. The numbers may not make real-world sense or the law may have changed.

Enter numbers as digits only, no commas or dollar signs.

Enter percentages as two-digit numbers. For example, enter 14% as 14. 

Click "Generate Problem" to begin.'''

def statute_problem(type_problem='random'):
    
    if type_problem=='random':
        picked = random.choice(sl.full_list)
    else:
        picked = type_problem
    #picked = sl.test_object
    
    values_list = []
    value_lang = ''
    
    # list of things to instantiate
    problem_dictionary = picked.input_dict
    
    list_of_variables = [*problem_dictionary]
    
    #determine how to pick values
    power_of_ten = picked.power_of_ten
           
    #generate the values
    for n in range(len(list_of_variables)):
        item = list_of_variables[n]
        if problem_dictionary[item] == 'default':
            value = random.randint(50,100)*1000
        else: 
            start = problem_dictionary[item].seed_start
            end = problem_dictionary[item].seed_end
            if problem_dictionary[item].seed_amount == 'previous':
                seed_value = values_list[n-1]
            else:
                seed_value = problem_dictionary[item].seed_amount    
            value = fm.generate_random_pot(seed_value,power_of_ten,start,end)
        
        if problem_dictionary[item] == 'default':        
            value_lang += f"The {item} is {fm.as_curr(value)}. "
            
        elif problem_dictionary[item].seed_type == 'nocurr':
            value_lang += f"The {item} is {value}. "

        elif power_of_ten < -1:
            value_lang += f"The {item} is {value} cents."
        
        else:       
            value_lang += f"The {item} is {fm.as_curr(value)}. "
        

        values_list.append(value)
 
    #create problem language
    if picked.ask_lang == 'default':
        eval_lang = "the correct evaluation of the statement"
    else:
        eval_lang = picked.ask_lang

    problem = f"The statement to evaluate is: '{picked.lang_to_eval}.' {value_lang}<br><br>What is {eval_lang}?"
    
    #create answer
    
    if len(values_list) == 1:
        answer = int(round(picked.func_to_eval(values_list[0])))
    elif len(values_list) == 2:
        answer = int(round(picked.func_to_eval(values_list[0],values_list[1])))
    elif len(values_list) == 3:
        answer = int(round(picked.func_to_eval(values_list[0],values_list[1],values_list[2])))

    return([problem,answer])
    #print([problem,answer])

