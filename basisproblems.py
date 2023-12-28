# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 14:21:25 2020

@author: carso
"""
import numpy as np
import random
import math
from datetime import date
import names
import json
import functionmodules as fm
import statistics
import animalsbycountry as abc

def gift_basis(asset_value,transferor_basis,later_sale_price,transferor,transferee):
    
    transferor_gain = 0
    relationship = random.choice(["family members","good friends"])
    
    if transferor_basis > asset_value and later_sale_price < asset_value:           
        recipient_basis = asset_value
            
    else:
        recipient_basis = transferor_basis
        
    if transferor_basis > asset_value and later_sale_price > asset_value and later_sale_price < transferor_basis:
        recipient_gain = 0
    else:
        recipient_gain = later_sale_price - recipient_basis
    
    specific_prob = f' {transferor} gives the property to {transferee}. {transferor} and {transferee} are {relationship}.'
    
    return(transferor_gain,recipient_basis,recipient_gain,specific_prob)
    
def part_gift(asset_value,transferor_basis,transferor_sale_price,later_sale_price,transferor,transferee):
    
    transferor_gain = max(0,transferor_sale_price-transferor_basis)
    
    relationship = random.choice(["family members","good friends"])
    
    if asset_value > transferor_basis:
        recipient_basis = max(transferor_basis,transferor_sale_price)
        recipient_gain = later_sale_price - recipient_basis
    
    #1.1015-4(a) here -- “For determining loss, the unadjusted basis of the property in the hands of the transferee shall not be greater than the fair market value of the property at the time of such transfer." This is relevant only when amount paid < fair market value < adjusted basis.
    
    elif asset_value < transferor_basis:

#and now do the regular dual basis analysis.        
        if later_sale_price > transferor_basis:
            recipient_basis = transferor_basis
            recipient_gain = later_sale_price - recipient_basis
            
        elif later_sale_price < asset_value:
            recipient_basis = asset_value
            recipient_gain = later_sale_price - recipient_basis
            
        elif later_sale_price < transferor_basis and later_sale_price > asset_value:
            recipient_basis = transferor_basis
            recipient_gain = 0
            
    
    specific_prob = f' {transferor} sells the property to {transferee} for {fm.ac(transferor_sale_price)}. {transferor} and {transferee} are {relationship}.'
    
    return(transferor_gain,recipient_basis,recipient_gain,specific_prob)
    
def part_donation(asset_value,transferor_basis,transferor_sale_price,later_sale_price,transferor,transferee):
    
    transferor_sale_basis = int(round(transferor_basis * (transferor_sale_price/asset_value)))
    
    transferor_gain = transferor_sale_price - transferor_sale_basis
    
    recipient_basis = transferor_sale_price + (transferor_basis - transferor_sale_basis)
   
    recipient_gain = later_sale_price - recipient_basis
    
    specific_prob = specific_prob = f' {transferor} sells the property to an organization that is tax-exempt under Section 501(c)(3) for {fm.ac(transferor_sale_price)}.'
    
    return(transferor_gain,recipient_basis,recipient_gain,specific_prob)
    
def death_basis(asset_value,later_sale_price,transferor,transferee):
    
    transferor_gain = 0
    recipient_basis = asset_value
    
    recipient_gain = later_sale_price - recipient_basis
    
    specific_prob = f' {transferor} dies and leaves the property to {transferee}.'
    
    return(transferor_gain,recipient_basis,recipient_gain,specific_prob)
    
def spouse_basis(asset_value,transferor_basis,later_sale_price,transferor,transferee):
    
    transferor_gain = 0
    recipient_basis = transferor_basis
    
    recipient_gain = later_sale_price - recipient_basis
    
    specific_prob = f' {transferor} and {transferee} are divorcing each other. {transferor} gives the property to {transferee} incident to that divorce.'
    
    return(transferor_gain,recipient_basis,recipient_gain,specific_prob)
    
def basis_problems():
    person1 = fm.create_person()
    person2 = fm.create_person()
        
    asset_value = 1000*random.randint(20,50)
    
    numbers_list = [asset_value]
    
    while True:
        transferor_basis = fm.generate_random_item(asset_value)
        if abs(transferor_basis-asset_value) > 1000:
            numbers_list.append(transferor_basis)
            break
           
    while True:
        transferor_sale_price = fm.generate_random_item(asset_value,50,90) 
        if transferor_sale_price not in numbers_list:
            numbers_list.append(transferor_sale_price)
            break
    
    while True:    
        later_sale_price = fm.generate_random_item(asset_value)
        if later_sale_price not in numbers_list:
            numbers_list.append(later_sale_price)
            break
      
    gain_to_transferor_proportionate_basis = transferor_sale_price - int(round(transferor_basis * (transferor_sale_price/asset_value)))
    gain_to_transferor_basis_first = max(0,transferor_sale_price - transferor_basis)
    no_gain_to_transferor = 0
    
    #possble basis to transferor
    recipient_basis_fmv = asset_value
    recipient_basis_transferred = transferor_basis
    recipient_basis_first = max(transferor_sale_price, transferor_basis)
    recipient_proportionate_basis = transferor_sale_price + (transferor_basis - int(round(transferor_basis * (transferor_sale_price/asset_value))))
    random_recipient_proportionate_basis = fm.generate_random_item(recipient_proportionate_basis)
    
    no_gain_to_recipient = 0
    fully_taxable_transfer = asset_value - transferor_basis
    
    possible_answers_gain_to_transferor = [gain_to_transferor_proportionate_basis, gain_to_transferor_basis_first,no_gain_to_transferor,fully_taxable_transfer]
    
    possible_answers_later_gain_to_recipient = [no_gain_to_recipient,later_sale_price - recipient_basis_fmv,later_sale_price - recipient_basis_transferred, later_sale_price - recipient_basis_first,later_sale_price - recipient_proportionate_basis,later_sale_price-random_recipient_proportionate_basis,later_sale_price-transferor_sale_price]
    
    transferor_gain_q = f' How much gain or loss does {person1.name} recognize due to {person1.poss} transfer of the property to {person2.name}?'
    recipient_gain_q = f' How much gain or loss does {person2.name} recognize due to {person2.poss} sale of the property for {fm.ac(later_sale_price)}?'

    possible_questions = [transferor_gain_q,recipient_gain_q]
    
    prob_part_one = f'{person1.name} owns property that is worth {fm.ac(asset_value)}, with a basis of {fm.ac(transferor_basis)}.'
    
    judgements = {later_sale_price-random_recipient_proportionate_basis:'This number was randomly generated.',fully_taxable_transfer:'Was this a sale for full fair market value?'}
    
    
    #type_problem = random.choice(['part donation','part gift','gift','death','spouse'])
    
    type_problem = random.choice(['spouse'])
    
    
    #set question: if part donation, ask only about the initial transferor. Otherwise, ask about either first or second transfer.
    if type_problem == 'part donation':
        prob_part_two = ''
        question_lang = f' How much gain or loss does {person1.name} recognize due to {person1.poss} transfer of the property to the 501(c)(3) organization?'

    else:
        prob_part_two = f' Several years later, {person2.name} sells the property for {fm.ac(later_sale_price)}.' 
        question_lang = random.choice(possible_questions)
    
    #set up questions and judgements
    if type_problem == 'gift':
        [transferor_gain,recipient_basis,recipient_gain,specific_prob] = gift_basis(asset_value,transferor_basis,later_sale_price,person1.name,person2.name)
        
        if question_lang == transferor_gain_q:

            judgements[transferor_gain]='Correct! The donor recognizes no gain in a pure gift situation.'
            judgements[fully_taxable_transfer] = 'Does a donor recognize gain in a pure gift situation?'
 
        if question_lang == recipient_gain_q:
            
            if transferor_basis > asset_value:
                
                if later_sale_price > transferor_basis:
            
                    judgements[recipient_gain] = f'<p>Correct! Because the value at the initial transfer was less than the basis, the dual basis rule applies as described in <a href="https://www.law.cornell.edu/uscode/text/26/1015" target="_new" rel="noreferrer">Section 1015(a)</a>. Here, however, the ultimate sale price was greater than the basis in the hands of the transferor, so the recipient uses the transferred basis. {person2.name} therefore recognizes {fm.ac(later_sale_price)} - {fm.ac(recipient_basis)} = {fm.ac(recipient_gain)}.</p>'
            
                elif later_sale_price < asset_value:
                    
                    judgements[recipient_gain]=f'<p>Correct! Because the value at the initial transfer was less than the basis, the dual basis rule applies as described in <a href="https://www.law.cornell.edu/uscode/text/26/1015" target="_new" rel="noreferrer">Section 1015(a)</a>. Because the ultimate sale price was less than the value of the asset at the time of transfer, the recipient must use that value as the basis for determining loss. {person2.name} therefore recognizes {fm.ac(later_sale_price)} - {fm.ac(recipient_basis)} = {fm.ac(recipient_gain)}.</p>'
                    
                else:
                    
                    judgements[recipient_gain]='<p>Correct! Because the value at the initial transfer was less than the basis, the dual basis rule applies as described in <a href="https://www.law.cornell.edu/uscode/text/26/1015" target="_new" rel="noreferrer">Section 1015(a)</a>. Here, the ultimate sale price was greater than the value of the asset at the time of transfer, but less than the basis to the transferor, so the recipient has neither gain nor loss on the subsequent sale.</p>'
            
            else:
                
                judgements[recipient_gain]=f'Correct! Because the basis at the initial transfer was not greater than the fair market value at the time of transfer, the recipient takes a transferred basis from the donor. {person2.name} therefore recognizes {fm.ac(later_sale_price)} - {fm.ac(recipient_basis)} = {fm.ac(recipient_gain)}.'
            
    elif type_problem == 'part gift':    
        [transferor_gain,recipient_basis,recipient_gain,specific_prob] = part_gift(asset_value,transferor_basis,transferor_sale_price,later_sale_price,person1.name,person2.name)
        
        if question_lang == transferor_gain_q:
            
            if transferor_gain == 0:
            
                judgements[transferor_gain]='Correct! The donor recovers basis first, and thus recognizes gain only to the extent the value of the sold portion exceeds the basis of the property. Here, the basis exceeds the sale price, so the transferor recognizes no gain.'
                judgements[gain_to_transferor_proportionate_basis]='<p>How is basis recovered on a part gift / part sale? Compare the basis recovery for property that is transferred through part donation / part sale, as described in <a href="https://www.law.cornell.edu/uscode/text/26/1011" target="_new" rel="noreferrer">Section 1011(b)</a>.</p>'
            
            else:
            
                judgements[transferor_gain]='Correct! The donor recovers basis first, and thus recognizes gain only to the extent the value of the sold portion exceeds the basis of the property.'
                
                judgements[gain_to_transferor_proportionate_basis]='<p>How is basis recovered on a part gift / part sale? Compare the basis recovery for property that is transferred through part donation / part sale, as described in <a href="https://www.law.cornell.edu/uscode/text/26/1011" target="_new" rel="noreferrer">Section 1011(b)</a>.</p>'
                judgements[no_gain_to_transferor]='If this were a pure gift, there would be no gain to the transferor. But there is some compensation transferred here.'
        
        if question_lang == recipient_gain_q:    

            judgements[later_sale_price - recipient_proportionate_basis]='How is basis recovered for the original transferor--basis first, or basis proportionate? And how does that affect the basis to the recipient?'
            
            #if dual basis rule is implicated
            if asset_value < transferor_basis and transferor_sale_price < asset_value:
    
                if later_sale_price < transferor_basis and later_sale_price > asset_value:
                    
                    judgements[recipient_gain]='<p>Correct! Under <a href="https://www.law.cornell.edu/cfr/text/26/1.1015-4" target="_new" rel="noreferrer">Section 1.1015-4(a)</a>, in a part gift/part sale transaction the basis to the recipient is usually the greater of (a) the amount the recipient paid for the property, or (b) the basis of the transferor in the property, but for determining loss, the basis of the property in the recipient cannot exceed the fair market value of the property at the time the property was transferred to the recipient. Here, the later sale price was less than the basis of the transferor and greater than the fair market value at transfer, so {person2.name} recognizes neither gain nor loss.</p>'
                
                elif later_sale_price > recipient_basis:
                
                    judgements[recipient_gain]=f'<p>Correct! Under <a href="https://www.law.cornell.edu/cfr/text/26/1.1015-4" target="_new" rel="noreferrer">Section 1.1015-4(a)</a>, in a part gift/part sale transaction the basis to the recipient is the greater of (a) the amount the recipient paid for the property, or (b) the basis of the transferor in the property. The dual basis rule could have been relevant, because the fair market value at the part gift/part sale was less than the basis, but because the recipient ultimately sold the property for more than its basis to the recipient at the time of the part gift/part sale,the dual basis rule had no effect. {person2.name} therefore recognizes {fm.ac(later_sale_price)} - {fm.ac(recipient_basis)} = {fm.ac(recipient_gain)}.</p>'

                
                else:
                
                    judgements[recipient_gain]=f'<p>Correct! Under <a href="https://www.law.cornell.edu/cfr/text/26/1.1015-4" target="_new" rel="noreferrer">Section 1.1015-4(a)</a>, in a part gift/part sale transaction the basis to the recipient is usually the greater of (a) the amount the recipient paid for the property, or (b) the basis of the transferor in the property, but for determining loss, the basis of the property in the recipient cannot exceed the fair market value of the property at the time the property was transferred to the recipient. {person2.name} therefore recognizes {fm.ac(later_sale_price)} - {fm.ac(recipient_basis)} = {fm.ac(recipient_gain)}.</p>'
                    
            
            else: #if dual basis rule is not triggered
               judgements[recipient_gain]=f'<p>Correct! Under <a href="https://www.law.cornell.edu/cfr/text/26/1.1015-4" target="_new" rel="noreferrer">Section 1.1015-4(a)</a>, the basis to the recipient is the greater of (a) the amount the recipient paid for the property, or (b) the basis of the transferor in the property. {person2.name} therefore recognizes {fm.ac(later_sale_price)} - {fm.ac(recipient_basis)} = {fm.ac(recipient_gain)}.</p>'
              
            
        
    elif type_problem == 'part donation':
        [transferor_gain,recipient_basis,recipient_gain,specific_prob] = part_donation(asset_value,transferor_basis,transferor_sale_price,later_sale_price,person1.name,person2.name)
        
        judgements[transferor_gain]='<p>Correct! Under <a href="https://www.law.cornell.edu/cfr/text/26/1011" target="_new" rel="noreferrer">Section 1011(b)</a> the donor recovers basis proportionately.</p>'
        judgements[gain_to_transferor_basis_first]='<p>How is basis recovered on a part donation / part sale? Consider <a href="https://www.law.cornell.edu/cfr/text/26/1011" target="_new" rel="noreferrer">Section 1011(b)</a>. Compare the basis recovery for property that is transferred through part gift / part sale.</p>'
        
        if gain_to_transferor_basis_first == 0:
        
            judgements[no_gain_to_transferor]='<p>If this were a pure donation, the transferor would recognize no gain or loss. But the tax-exempt organization does transfer some compensation. Also, is basis recovered on a part donation / part sale? Consider <a href="https://www.law.cornell.edu/cfr/text/26/1011" target="_new" rel="noreferrer">Section 1011(b)</a>. Compare the basis recovery for property that is transferred through part gift / part sale.</p>'
        
        else:
 
            judgements[no_gain_to_transferor]='If this were a pure donation, the transferor would recognize no gain or loss. But the tax-exempt organization does transfer some compensation.'
        
        
    elif type_problem == 'death':
        [transferor_gain,recipient_basis,recipient_gain,specific_prob] = death_basis(asset_value,later_sale_price,person1.name,person2.name)
        
        if question_lang == transferor_gain_q:
            judgements[transferor_gain]='Correct! The transferor recognizes no gain in a transfer at death.'
        
        if question_lang == recipient_gain_q:
            judgements[recipient_gain]=f'<p>Correct! Under <a href="https://www.law.cornell.edu/cfr/text/26/1014" target="_new" rel="noreferrer">Section 1014(a)</a>, the basis of the asset is set to the fair market value at the time of death. Therefore {person2.name} recognizes {fm.ac(later_sale_price)} - {fm.ac(asset_value)} = {fm.ac(recipient_gain)} on the subsequent sale.</p>'
            judgements[later_sale_price - recipient_basis_transferred]='<p>What happens to the basis of an asset that is transferred due to death? Consider <a href="https://www.law.cornell.edu/cfr/text/26/1014" target="_new" rel="noreferrer">Section 1014(a)</a>.</p>'
        
    elif type_problem == 'spouse':
        [transferor_gain,recipient_basis,recipient_gain,specific_prob] = spouse_basis(asset_value,transferor_basis,later_sale_price,person1.name,person2.name)
       
        if question_lang == transferor_gain_q:
            judgements[transferor_gain]='Correct! There is no gain or loss on the gift of property between spouses.'
            
        if question_lang == recipient_gain_q:
            if asset_value < transferor_basis and later_sale_price < transferor_basis:
                judgements[recipient_gain]=f'Correct! The basis of the property is always transferred between spouses, even if the fair market value of the asset at transfer is less than the basis and thus the dual basis rule would apply in a gift situation between people who are not spouses. {person1.name} therefore recognizes {fm.ac(later_sale_price)} - {fm.ac(recipient_basis)} = {fm.ac(recipient_gain)}.'
            else:
                judgements[recipient_gain]=f'Correct! The basis of the property is always transferred between spouses. {person1.name} therefore recognizes {fm.ac(later_sale_price)} - {fm.ac(recipient_basis)} = {fm.ac(recipient_gain)}.'
    
    
    if question_lang == recipient_gain_q:
        correct = recipient_gain
        possibleanswers = possible_answers_later_gain_to_recipient
    
    else:    
        correct = transferor_gain
        possibleanswers = possible_answers_gain_to_transferor

    problem_facts = prob_part_one + specific_prob + prob_part_two
    
    problem = problem_facts + question_lang

    (possibleanswers, judgements) = fm.random_answer_pot(possibleanswers,judgements,3,40,150)

    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    print([problem,cleananswers,judgements_json,correct])
    

basis_problems()