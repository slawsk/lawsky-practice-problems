# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 06:28:35 2019

@author: carso
"""


import numpy as np
import random
import math
from datetime import date
import names
import json
import functionmodules as fm
import businessentities as be
import animalsbycountry as abc
import currency as curr
import depreciation as dp


#Implementation
#Here are all the things to update when you write a new function: functions_list

functions_list = ['a random type of problem','1.4 Check the box','1.6 Section 199A qualified business income deduction','2.1 Transfers to a partnership: nonrecognition','2.2 Transfers to a partnership: basis and holding period','4.2 Required taxable years','6.1 Varying interests rule','7.2 Section 724']

true_functions_list = functions_list[1:]

def check_the_box():
    per_se_choice = random.choice(['per se','eligible'])
    if per_se_choice == 'per se':
        entity = be.pick_per_se_entity()
    else: 
        entity = be.pick_other_entity()
        
    if entity.entity_suffix == '':
        suffix_fancy = ''
    else:
        suffix_fancy = f', {entity.entity_suffix},'
    
    
    problem_lang = f"{entity.entity_name}{suffix_fancy} is organized in {entity.location} as {fm.pick_a_an(entity.entity_type)} {entity.entity_type}. {entity.entity_name} {entity.member_language} {entity.liability_language} Is {entity.entity_name} eligible to check the box?" 

    no_because_per_se = f'No, because {fm.pick_a_an(entity.entity_type)} {entity.entity_type} organized in {entity.location} is a per se corporation.'
    yes_default_DRE = 'Yes, and its default status is a disregarded entity.'
    yes_default_partnership = 'Yes, and its default status is a partnership.'
    yes_default_corp = 'Yes, and its default status is a corporation.'
    yes_elect_DRE = 'Yes, and its elective status is a disregarded entity.'
    yes_elect_partnership = 'Yes, and its elective status is a partnership.'
    yes_elect_corp = 'Yes, and its elective status is a corporation.'
    
    general_explanation = 'Under <a href="https://www.law.cornell.edu/cfr/text/26/301.7701-3" target="_new" rel="noreferrer">Treas. Reg. 301.7701-3(a)</a>, an entity is eligible to elect its business classification if and only if it is not classified as a corporation under <a href="https://www.law.cornell.edu/cfr/text/26/301.7701-2" target="_new" rel="noreferrer">Treas. Reg. 301.7701-2(b)</a>--that is, if and only if it is not a per se corporation.'
    
    general_statement_no_per_se = f'{fm.pick_a_an(entity.entity_type).capitalize()} {entity.entity_type} is not a per se corporation under this regulation and is therefore eligible to check the box.'
    
    question_1 = "If so, what is its default status if there is no election under the check-the-box rules?"
    
    
    question_2 = "If so, what type of entity will it be if there is an election under the check-the-box rules (that is, if the entity does not take default status under the check-the-box rules)?"
    
    question = random.choice([question_1,question_2])
    
    problem = f'{problem_lang} {question}'
   
    judgements = {}
    if question == question_1:
        possibleanswers = [no_because_per_se,yes_default_DRE,yes_default_partnership,yes_default_corp]
        if per_se_choice == 'per se':
            correct = no_because_per_se
            for item in possibleanswers:
                if item == correct:
                    if entity.location in be.state:
                        explanation = f'<p>That is correct. {general_explanation} {fm.to_capital(fm.pick_a_an(entity.entity_type))} {entity.entity_type} organized in {entity.location} is a per se corporation under <a href="https://www.law.cornell.edu/cfr/text/26/301.7701-2" target="_new" rel="noreferrer">Treas. Reg. 301.7701-2(b)(1)</a>.</p>'
                    else:
                        explanation = f'<p>That is correct. {general_explanation} {fm.to_capital(fm.pick_a_an(entity.entity_type))} {entity.entity_type} organized in {entity.location} is a per se corporation under <a href="https://www.law.cornell.edu/cfr/text/26/301.7701-2" target="_new" rel="noreferrer">Treas. Reg. 301.7701-2(b)(8)</a>.</p>'

                else:
                    explanation = f'<p>Consider what constitutes a per se corporation, as described in <a href="https://www.law.cornell.edu/cfr/text/26/301.7701-2" target="_new" rel="noreferrer">Treas. Reg. 301.7701-2(b)</a>.</p>'
                
                judgements[item]=explanation  
                
                
        if per_se_choice == 'eligible':
            correct = f'Yes, and its default status is {fm.pick_a_an(entity.default_choice)} {entity.default_choice}.'
            for item in possibleanswers:
                if entity.foreign_US =='foreign':
                    if item == correct:
                        explanation = f'<p>That is correct. {general_explanation} {general_statement_no_per_se} <a href="https://www.law.cornell.edu/cfr/text/26/301.7701-3" target="_new" rel="noreferrer">Treas. Reg. 301.7701-3(b)(2)(i)</a> states that a foreign entity in which {entity.liability_language[:-1].lower()} and that {entity.member_language[:-1].lower()} defaults to {fm.pick_a_an(entity.default_choice)} {entity.default_choice}.</p>'
                    elif item == no_because_per_se:
                        explanation = f'<p>Consider what constitutes a per se corporation, as described in <a href="https://www.law.cornell.edu/cfr/text/26/301.7701-2" target="_new" rel="noreferrer">Treas. Reg. 301.7701-2(b)</a>.</p>'
                    else:   
                         explanation = f'<p>Consider the default status discussed in <a href="https://www.law.cornell.edu/cfr/text/26/301.7701-3" target="_new" rel="noreferrer">Treas. Reg. 301.7701-3(b)(2)(i)</a>. Focus on how many members the entity has and whether any member has unlimited liability.</p>'
                else:
                    if item == correct:
                        explanation = f'<p>That is correct. {general_explanation} {general_statement_no_per_se} <a href="https://www.law.cornell.edu/cfr/text/26/301.7701-3" target="_new" rel="noreferrer">Treas. Reg. 301.7701-3(b)(1)</a> states a domestic (U.S.) entity which {entity.member_language[:-1].lower()} defaults to {fm.pick_a_an(entity.default_choice)} {entity.default_choice}.</p>'
                    elif item == no_because_per_se:
                        explanation = f'<p>Consider what constitutes a per se corporation, as described in <a href="https://www.law.cornell.edu/cfr/text/26/301.7701-2" target="_new" rel="noreferrer">Treas. Reg. 301.7701-2(b)</a>.</p>'
                    else:
                        explanation = f'<p>Consider the default status discussed in <a href="https://www.law.cornell.edu/cfr/text/26/301.7701-3" target="_new" rel="noreferrer">Treas. Reg. 301.7701-3(b)(1)</a>. Focus on how many members the entity has.</p>'
                judgements[item]=explanation
            
    if question == question_2:
        possibleanswers = [no_because_per_se,yes_elect_DRE,yes_elect_partnership,yes_elect_corp]
        if per_se_choice == 'per se':
            correct = no_because_per_se
            for item in possibleanswers:
                if item == correct:
                    if entity.location in be.state:
                        explanation = f'<p>That is correct. {general_explanation} {fm.to_capital(fm.pick_a_an(entity.entity_type))} {entity.entity_type} organized in {entity.location} is a per se corporation under <a href="https://www.law.cornell.edu/cfr/text/26/301.7701-2" target="_new" rel="noreferrer">Treas. Reg. 301.7701-2(b)(1)</a>.</p>'
                    else:
                        explanation = f'<p>That is correct. {general_explanation} {fm.to_capital(fm.pick_a_an(entity.entity_type))} {entity.entity_type} organized in {entity.location} is a per se corporation under <a href="https://www.law.cornell.edu/cfr/text/26/301.7701-2" target="_new" rel="noreferrer">Treas. Reg. 301.7701-2(b)(8)</a>.</p>'

                else:
                    explanation = f'<p>Consider what constitutes a per se corporation, as described in <a href="https://www.law.cornell.edu/cfr/text/26/301.7701-2" target="_new" rel="noreferrer">Treas. Reg. 301.7701-2(b)</a>.</p>'
                
                judgements[item]=explanation  
                
                
        if per_se_choice == 'eligible':
            correct = f'Yes, and its elective status is {fm.pick_a_an(entity.elect_choice)} {entity.elect_choice}.'
            for item in possibleanswers:
                if entity.foreign_US == 'foreign':
                    if item == correct:
                        if entity.liability_language == 'At least one member of the entity has unlimited liability.':
                            explanation = f'<p>That is correct. {general_explanation} {general_statement_no_per_se} <a href="https://www.law.cornell.edu/cfr/text/26/301.7701-3" target="_new" rel="noreferrer">Treas. Reg. 301.7701-3(b)(2)(i)</a> states that a foreign entity in which {entity.liability_language[:-1].lower()} may elect to be {fm.pick_a_an(entity.elect_choice)} {entity.elect_choice}.</p>'
                        else:     
                            explanation = f'<p>That is correct. {general_explanation} {general_statement_no_per_se} <a href="https://www.law.cornell.edu/cfr/text/26/301.7701-3" target="_new" rel="noreferrer">Treas. Reg. 301.7701-3(b)(2)(i)</a> states that a foreign entity in which {entity.liability_language[:-1].lower()} and that {entity.member_language[:-1].lower()} may elect to be {fm.pick_a_an(entity.elect_choice)} {entity.elect_choice}.</p>'
                    elif item == no_because_per_se:
                        explanation = f'<p>Consider what constitutes a per se corporation, as described in <a href="https://www.law.cornell.edu/cfr/text/26/301.7701-2" target="_new" rel="noreferrer">Treas. Reg. 301.7701-2(b)</a>.</p>'
                    else:   
                         explanation = f'<p>Consider the elective status discussed in <a href="https://www.law.cornell.edu/cfr/text/26/301.7701-3" target="_new" rel="noreferrer">Treas. Reg. 301.7701-3(a) and (b)</a>. Focus on how many members the entity has and whether any member has unlimited liability.</p>'
                else:
                    if item == correct:
                        explanation = f'<p>That is correct. {general_explanation} {general_statement_no_per_se} <a href="https://www.law.cornell.edu/cfr/text/26/301.7701-3" target="_new" rel="noreferrer">Treas. Reg. 301.7701-3(b)(1)</a> states a domestic (U.S.) entity which is not a per se corporation may, regardless of its number of members, elect into {fm.pick_a_an(entity.elect_choice)} {entity.elect_choice}.</p>'
                    elif item == no_because_per_se:
                        explanation = f'<p>Consider what constitutes a per se corporation, as described in <a href="https://www.law.cornell.edu/cfr/text/26/301.7701-2" target="_new" rel="noreferrer">Treas. Reg. 301.7701-2(b)</a>.</p>'
                    else:
                        explanation = f'<p>Consider the elective status discussed in <a href="https://www.law.cornell.edu/cfr/text/26/301.7701-3" target="_new" rel="noreferrer">Treas. Reg. 301.7701-3(a)(1)</a> for domestic (U.S.) entities.</p>'
                judgements[item]=explanation
    
    formattedjudgements = fm.format_dict(judgements,formatting='words')
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = possibleanswers
    return([problem,cleananswers,judgements_json,correct])       

def investment_partnership():

    [person1,person2,person3]=fm.create_group(3)
    entity_list = fm.entity_list_generate(4)
    
    currency_type = random.choice(curr.currency_list)
    precious_metal_type = random.choice(curr.precious_metals_list)
    stock_traded = random.choice(['is','is not'])    
    precious_metal_contributor_use = random.choice(["held for investment","used in the active conduct of a trade or business"])

    
    bad_assets = [['cash that the partnership has no plan to immediately reinvest','cash','What is the significance of the fact that the partnership does not have a plan to reinvest the cash?'], #0
                  [f'stock in {entity_list[0]}, Inc., which {stock_traded} readily marketable','stock','Does it matter whether the stock is readily marketable?'], #1
                  [f'an option to purchase stock in {entity_list[1]}, Inc.. The stock {stock_traded} readily marketable','option','Does it matter whether the underlying stock is readily marketable?'], #2
                  [f'an interest in {entity_list[2]}, a real estate investment trust','REIT interest',''], #3
                  [f'an interest in {entity_list[3]}, a publicly traded partnership','interest in the publicly traded partnership',''],#4
                  [f'{currency_type}, a type of non-US currency', f'{currency_type}',''],#5
                  [f'an amount of {precious_metal_type} that was {precious_metal_contributor_use} and that the partnership will hold for investment',f'{precious_metal_type}',f'What is the significance, if any, of how the {precious_metal_type} was used and will be used?']] #6

    good_assets = [['land that the partnership will hold for investment','land','Does it matter that the land will be held for investment?'], #0
                   ['land that the partnership will use in the active conduct of a trade or business','land',''], #1
                   [f'an amount of {precious_metal_type} that was {precious_metal_contributor_use} and that the partnership will use in the active conduct of its trade or business',f'{precious_metal_type}',f'What is the significance, if any, of how the {precious_metal_type} was used and will be used?'], #2
                   ['a collection of assets that the partnership will use in the active conduct of its trade or business','collection',''], #3
                   ['cash that the partnership plans to use to purchase assets that the partnership will use in the active conduct of its trade or business','cash','What is the significance of the plan to use the cash to purchase assets for use in the active conduct of trade or business of the partnership?']] #4
    
    all_assets = bad_assets + good_assets
    
    asset_list= []
    price_list = []
    difference_list = []
    total_fmv = 0
    bad_fmv = 0
    good_fmv = 0
    
    person_dict = {
        person1.name:[],
        person2.name:[],
        person3.name:[]}
    
    person_list = list(person_dict)

    
    for n in range(0,3):
        while True:
            asset = random.choice(all_assets)
            if asset in bad_assets:
                type_asset = 'bad'
            elif asset in good_assets:
                type_asset = 'good'
                
            if asset not in asset_list:
                asset_list.append(asset)
                break
        
        while True:
            if type_asset == 'bad':
                fmv = 1000*random.randint(40,100)
                bad_fmv += fmv
            elif type_asset == 'good':
                fmv = 1000*random.randint(5,60)
                good_fmv += fmv
            basis = fm.generate_random_item(fmv,70,110)
            difference = abs(fmv-basis)
            if fmv not in price_list and basis not in price_list and fmv != basis and difference not in difference_list:
                total_fmv += fmv               
                price_list.append(fmv)
                price_list.append(basis)
                difference_list.append(difference)
                break
        
        if asset[1] != 'cash':
            person_problem_language_2 = f". The {asset[1]} has a fair market value of {fm.as_curr(fmv)} and a basis of {fm.as_curr(basis)}."
            gain_loss = fmv - basis
            
        else: 
            person_problem_language_2 = f". The amount of cash is {fm.as_curr(fmv)}."
            gain_loss = 0
        
        person_problem_language = f"{person_list[n]} contributes {asset[0]}" + person_problem_language_2
        
        person_dict[person_list[n]].append(person_problem_language)#0
        person_dict[person_list[n]].append(gain_loss)#1
        person_dict[person_list[n]].append(fmv) #2
        person_dict[person_list[n]].append(basis) #3
        person_dict[person_list[n]].append(asset[1]) #4
        person_dict[person_list[n]].append(asset[2]) #5
        
    while True:    
        question_person = random.choice([person1,person2,person3])
        if person_dict[question_person.name][4] != 'cash':
            break
    
    person_1_lang = person_dict[person1.name][0]
    person_2_lang = person_dict[person2.name][0]
    person_3_lang = person_dict[person3.name][0]
    
    person_1_hint = person_dict[person1.name][5]
    person_2_hint = person_dict[person2.name][5]
    person_3_hint = person_dict[person3.name][5]
    
    if person_1_hint == '' and person_2_hint == '' and person_3_hint == '':
        hint_language = ''
    
    else:
        hint_language = f'For example: {person_1_hint} {person_2_hint} {person_3_hint}'
    
    problem = f'{person1.name}, {person2.name}, and {person3.name} form a partnership. {person_1_lang} {person_2_lang} {person_3_lang} How much gain or loss does {question_person.name} recognize due to {question_person.poss} contribution to the partnership?'

    if (bad_fmv / total_fmv) > .8:
        investment_partnership = 'yes'
    else:
        investment_partnership = 'no'
    
    gain_loss_realized = person_dict[question_person.name][1]

    fmv_contributed_asset = person_dict[question_person.name][2]
    
    basis_contributed_asset = person_dict[question_person.name][3]

    possibleanswers = [0,gain_loss_realized,fmv_contributed_asset,basis_contributed_asset]
    
    judgements = {}
    
    if investment_partnership == 'no': 
        correct = 0
        judgements[correct] = f'<p>Correct. This is not an investment partnership, because {fm.as_percent(bad_fmv/total_fmv)} of the assets are so-called bad assets, and in order to be an investment partnership, more than 80% of the assets must be so-called bad assets. Therefore, no gain or loss is recognized on the contribution of assets, under the general rule of <a href="https://www.law.cornell.edu/uscode/text/26/721" target="_new">Section 721</a>.</p>'
        
        if gain_loss_realized < 0:
            judgements[gain_loss_realized] = f'<p>What is the general rule for whether gain or loss is recognized on the contribution to a partnership? Consider <a href="https://www.law.cornell.edu/uscode/text/26/721" target="_new">Section 721</a>. <br><br>Additionally, given that a loss is realized, does it matter whether this is an investment partnership?</p>'
        
        else:
            judgements[gain_loss_realized] = f'<p>What is the general rule for whether gain or loss is recognized on the contribution to a partnership? Consider <a href="https://www.law.cornell.edu/uscode/text/26/721" target="_new">Section 721</a>. <br><br>Additionally, is this an investment partnership? Consider especially <a href="https://www.law.cornell.edu/cfr/text/26/1.351-1" target="_new">Section 1.351-1(c)(1)(ii)(a)</a> and the list of assets in <a href="https://www.law.cornell.edu/uscode/text/26/351" target="_new">Section 351(e)(1)(B)</a>. {hint_language} </p>'
            
            
        judgements[fmv_contributed_asset] = f'<p>What is the general rule for whether gain or loss is recognized on the contribution to a partnership? Consider <a href="https://www.law.cornell.edu/uscode/text/26/721" target="_new">Section 721</a>. <br><br>Additionally, is this an investment partnership? Consider especially <a href="https://www.law.cornell.edu/cfr/text/26/1.351-1" target="_new">Section 1.351-1(c)(1)(ii)(a)</a> and the list of assets in <a href="https://www.law.cornell.edu/uscode/text/26/351" target="_new">Section 351(e)(1)(B)</a>. {hint_language} <br><br>Finally, even if it were an investment partnership, would the entire fair market value of the asset be recognized on the contribution? Consider the language of <a href="https://www.law.cornell.edu/uscode/text/26/721" target="_new">Section 721(a) and (b)</a>.</p>'
        judgements[basis_contributed_asset] = f'<p>What is the general rule for whether gain or loss is recognized on the contribution to a partnership? Consider <a href="https://www.law.cornell.edu/uscode/text/26/721" target="_new">Section 721</a>. <br><br>Additionally, is this an investment partnership? Consider especially <a href="https://www.law.cornell.edu/cfr/text/26/1.351-1" target="_new">Section 1.351-1(c)(1)(ii)(a)</a> and the list of assets in <a href="https://www.law.cornell.edu/uscode/text/26/351" target="_new">Section 351(e)(1)(B)</a>. {hint_language} <br><br>Finally, even if it were an investment partnership, what amount would be recognized on the contribution? Consider the language of <a href="https://www.law.cornell.edu/uscode/text/26/721" target="_new">Section 721(a) and (b)</a>.</p>'
        
    elif gain_loss_realized < 0:
        correct = 0
        judgements[correct] = f'<p>Correct. This is an investment partnership, because {fm.as_percent(bad_fmv/total_fmv)} of the assets are so-called bad assets, and in order to be an investment partnership, more than 80% of the assets must be so-called bad assets. However, <a href="https://www.law.cornell.edu/uscode/text/26/721" target="_new">Section 721</a> does not permit the recognition of loss on a contribution to an investment partnership; rather, it requires the recognition of gain. Because {question_person.name} realized {fm.as_curr(abs(gain_loss_realized))} of loss, no gain or loss is recognized.</p>'
        judgements[gain_loss_realized] = f'<p>You are correct that this is an investment partnership, because {fm.as_percent(bad_fmv/total_fmv)} of the assets are so-called bad assets, and in order to be an investment partnership, more than 80% of the assets must be so-called bad assets. However, does <a href="https://www.law.cornell.edu/uscode/text/26/721" target="_new">Section 721</a> permit the recognition of loss on a contribution to an investment partnership?</p>' 
        judgements[fmv_contributed_asset] = f'<p>You are correct that this is an investment partnership, because {fm.as_percent(bad_fmv/total_fmv)} of the assets are so-called bad assets, and in order to be an investment partnership, more than 80% of the assets must be so-called bad assets. But what amount is recognized on the contribution? Consider the language of <a href="https://www.law.cornell.edu/uscode/text/26/721" target="_new">Section 721(a) and (b)</a>.</p>'
        judgements[basis_contributed_asset] = f'<p>You are correct that this is an investment partnership, because {fm.as_percent(bad_fmv/total_fmv)} of the assets are so-called bad assets, and in order to be an investment partnership, more than 80% of the assets must be so-called bad assets. But what amount is recognized on the contribution? Consider the language of <a href="https://www.law.cornell.edu/uscode/text/26/721" target="_new">Section 721(a) and (b)</a>.</p>'
    
    else:
        correct = gain_loss_realized
        judgements[correct] = f'<p>Correct. This is an investment partnership, because {fm.as_percent(bad_fmv/total_fmv)} of the assets are so-called bad assets, and in order to be an investment partnership, more than 80% of the assets must be so-called bad assets. Therefore, <a href="https://www.law.cornell.edu/uscode/text/26/721" target="_new">Section 721(b)</a> requires the recognition of gain. {question_person.name} realized and must recognize {fm.as_curr(gain_loss_realized)} of gain.</p>'
        judgements[0] = f'<p>It is true that the general rule under <a href="https://www.law.cornell.edu/uscode/text/26/721" target="_new">Section 721(a)</a> is that no gain or loss is recognized on the contribution of assets to a partnership. <br><br> But consider <a href="https://www.law.cornell.edu/uscode/text/26/721" target="_new">Section 721(b)</a>. Is this an investment partnership? Consider especially <a href="https://www.law.cornell.edu/cfr/text/26/1.351-1" target="_new">Section 1.351-1(c)(1)(ii)(a)</a> and the list of assets in <a href="https://www.law.cornell.edu/uscode/text/26/351" target="_new">Section 351(e)(1)(B)</a>. {hint_language}</p>'
        judgements[fmv_contributed_asset] = f'<p>You are correct that this is an investment partnership, because {fm.as_percent(bad_fmv/total_fmv)} of the assets are so-called bad assets, and in order to be an investment partnership, more than 80% of the assets must be so-called bad assets. But what amount is recognized on the contribution? Consider the language of <a href="https://www.law.cornell.edu/uscode/text/26/721" target="_new">Section 721(a) and (b)</a>.</p>'
        judgements[basis_contributed_asset] = f'<p>You are correct that this is an investment partnership, because {fm.as_percent(bad_fmv/total_fmv)} of the assets are so-called bad assets, and in order to be an investment partnership, more than 80% of the assets must be so-called bad assets. But what amount is recognized on the contribution? Consider the language of <a href="https://www.law.cornell.edu/uscode/text/26/721" target="_new">Section 721(a) and (b)</a>.</p>'
        
    (possibleanswers, judgements) = fm.random_answer(possibleanswers,judgements)
    
    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return([problem,cleananswers,judgements_json,correct]) 

def transfers_to_partnership():
    
    class ContributedAsset:
        def __init__(self,name,fmv,basis,class_asset,divided_fmv_lang,divided_exchanged_lang,percent,amount_tacked):
            self.name = name
            self.fmv = fmv
            self.class_asset = class_asset
            self.basis = basis
            self.divided_fmv_lang = divided_fmv_lang
            self.divided_exchanged_lang = divided_exchanged_lang
            self.percent = percent
            self.amount_tacked = amount_tacked
    
    person1=fm.create_person()
    
    capital_assets = ['tract of land','amount of stock','amount of stock options','building','amount of goodwill']
    
    section_1231_assets = []
    
    section_1231_assets_class = list(dp.full_asset_list)
     
    for n in section_1231_assets_class:
        new_1231_asset = n.name
        section_1231_assets.append(new_1231_asset)
    
    other_assets = [f'patent created by {person1.name}', f'invention created by {person1.name}', f'design created by {person1.name}', f'secret formula created by {person1.name}', f'copyright created by {person1.name}', f'literary composition created by {person1.name}', f'musical composition created by {person1.name}', f'artistic composition created by {person1.name}',f"accounts receivable from {person1.name}'s business", f"set of supplies {person1.name} regularly used in {person1.poss} business","collection of inventory"]

    all_assets = capital_assets + section_1231_assets + other_assets
    
    partnership_name = random.choice(abc.animals_by_country_dict['English'])

    asset_list_name = []
    asset_list = []
    price_list = []
    tack_fmv = total_fmv = no_tack_fmv = tack_basis = no_tack_basis = total_basis = tack_correct = 0    
    assets_acquired_language = ""
    number_assets = 3
    tack_dict = {}


    while True:

        for n in range(number_assets):

            while True:
                fmv = 1000*random.randint(50,100)
                basis = fm.generate_random_item(fmv,10,45)

                if fmv not in price_list and basis not in price_list and fmv != basis:
                    price_list.append(fmv)
                    price_list.append(basis)
                    break

            if n == 0:
                asset = random.choice(other_assets)
                class_asset = "other"
                asset_list_name.append(asset)

            elif n == 1:
                asset = random.choice(capital_assets+section_1231_assets)
                if asset in capital_assets:
                    class_asset = 'capital'
                else:
                    class_asset = '1231'
                asset_list_name.append(asset)

            else:
                while True:
                    asset = random.choice(all_assets)
                    if asset in capital_assets:
                        class_asset = 'capital'
                    elif asset in section_1231_assets:
                        class_asset = '1231'
                    elif asset in other_assets:
                        class_asset = 'other'

                    if asset not in asset_list_name:
                        asset_list_name.append(asset)
                        break

            tack_dict = {'capital':fmv,'1231':basis,'other':0}

            fullasset = ContributedAsset(asset,fmv,basis,class_asset,'','',0,tack_dict[class_asset])

            asset_list.append(fullasset)

            asset_language_1 = f"{fm.pick_a_an(fullasset.name)} {fullasset.name} with a fair market value of {fm.as_curr(fullasset.fmv)} and a basis of {fm.as_curr(fullasset.basis)}"

            if n < number_assets-1:
                asset_language_0 = ''
                asset_language_3 = "; "
            else:
                asset_language_0 = "and "
                asset_language_3 = "."

            if asset in section_1231_assets:
                asset_language_2 = f" that {person1.name} uses in {person1.poss} trade or business (all of the gain is due to depreciation)"
            else:
                asset_language_2 = ""

            assets_acquired_language += (asset_language_0 + asset_language_1 + asset_language_2 + asset_language_3)


        asset_choice = random.choice(asset_list)

        partner_basis = f"{person1.name}'s basis in {partnership_name}"
        partnership_question = f"{partnership_name}'s basis in and holding period for the {asset_choice.name}"
        partner_hp = f"{person1.name}'s holding period in {person1.poss} interest in {partnership_name}"

        partner_questions = [partner_basis,partner_hp]

        type_partner_question = random.choice(partner_questions)

        possiblequestions = [type_partner_question,partnership_question]
        question = random.choice(possiblequestions)

        problem = f"{person1.name} contributes the following to {partnership_name}, LLC, which is taxed as a partnership, in exchange for an interest in {partnership_name}: {assets_acquired_language} Which of the following is accurate with respect to {question}?"


        for n in asset_list:
            tack_correct += n.amount_tacked
            total_fmv += n.fmv
            total_basis += n.basis
            if n.class_asset != 'other':
                tack_basis += n.basis
                tack_fmv += n.fmv


        if tack_correct != tack_fmv:
            depreciation_lang = 'Gain subject to recapture is treated as a separate asset that is not a capital asset or a 1231 asset, under <a href="https://www.law.cornell.edu/uscode/text/26/1.1223-3" target="_new">Treas. Reg. 1.1223-3(e)</a>.'
        else:
            depreciation_lang = ''

        percent_tack = tack_correct / total_fmv
        percent_no_tack = (total_fmv - tack_correct) / total_fmv

        percent_fmv = tack_fmv / total_fmv
        percent_no_tack_fmv = (total_fmv - tack_fmv) / total_fmv

        percent_tack_basis = tack_basis / total_basis
        percent_no_tack_basis = (total_basis - tack_basis) / total_basis


        percent_list = [percent_tack,percent_tack_basis]

        as_percent_list = list(map(fm.as_percent,percent_list))
        # making sure that numbers for basis and FMV don't accidentally work out to be the same
        if len(as_percent_list) == len(set(as_percent_list)):
            break

    judgements = {}
    
    if question == partner_hp:
            
        all_tack_answer = f"{person1.name}'s holding period in {partnership_name} is entirely tacked."
        no_tack_answer = f"{person1.name}'s holding period in {partnership_name} starts fresh upon {person1.poss} contribution to {partnership_name}."
        percent_tack_answer = f"{fm.as_percent(percent_tack)} of the holding period in {partnership_name} is tacked and {fm.as_percent(percent_no_tack)} starts upon {person1.name}'s contribution to {partnership_name}."
        basis_percent_tack_answer = f"{fm.as_percent(percent_tack_basis)} of the holding period in {partnership_name} is tacked and {fm.as_percent(percent_no_tack_basis)} starts upon {person1.name}'s contribution to {partnership_name}."
        fmv_tack_answer = f"{fm.as_percent(percent_fmv)} of the holding period in {partnership_name} is tacked and {fm.as_percent(percent_no_tack_fmv)} starts upon {person1.name}'s contribution to {partnership_name}."

        correct = percent_tack_answer

        possibleanswers = [all_tack_answer,no_tack_answer,percent_tack_answer,basis_percent_tack_answer]
        section_1231_items_in_list = any(item in section_1231_assets for item in asset_list_name)

        
        judgements[all_tack_answer] = '<p>Does <a href="https://www.law.cornell.edu/uscode/text/26/1223" target="_new">Section 1223(1)</a> apply, or does <a href="https://www.law.cornell.edu/uscode/text/26/1223" target="_new">Section 1223(2)</a> apply?</p>'
        judgements[no_tack_answer] = f'<p>Consider <a href="https://www.law.cornell.edu/uscode/text/26/1223" target="_new">Section 1223</a>. How is the basis of {person1.name}\'s interest in {partnership_name} determined?</p>'
        judgements[percent_tack_answer] = f'<p>Correct. The holding period is divided under <a href="https://www.law.cornell.edu/uscode/text/26/1223" target="_new">Section 1223(1)</a>, which permits tacking only for the portion of the partnership interest received in exchange for capital assets and Section 1231 assets. {depreciation_lang} Under <a href="https://www.law.cornell.edu/uscode/text/26/1.1223-3" target="_new">Treas. Reg. 1.1223-3(b)</a>, the percent of the partnership interest that receives a tacked holding period is determined based on the relative fair market values of the capital assets and Section 1231 assets, on the one hand, and the other assets, on the other.</p>'
        judgements[basis_percent_tack_answer] = '<p>You are correct that the holding period is divided under <a href="https://www.law.cornell.edu/uscode/text/26/1223" target="_new">Section 1223(1)</a>, which permits tacking only for the portion of the partnership interest received in exchange for capital assets and Section 1231 assets. Consider <a href="https://www.law.cornell.edu/uscode/text/26/1.1223-3" target="_new">Treas. Reg. 1.1223-3(b)</a>, however, as you consider how to determine what percent of the partnership interest receives a tacked holding period.</p>'

        if section_1231_items_in_list:
            possibleanswers.append(fmv_tack_answer)
            judgements[fmv_tack_answer] = '<p>You are correct that the fair market value of the tacked assets is compared to the fair market value of the non-tacked assets. But what is the treatment of gain subject to recapture? Consider <a href="https://www.law.cornell.edu/uscode/text/26/1.1223-3" target="_new">Treas. Reg. 1.1223-3(e)</a>.</p>'
    
    elif question == partner_basis:
        
        divided_fmv_total = divided_exchanged_total = ''
        counter = 0 

        
        for item in asset_list:
            
            counter += 1
            
            item.percent = (item.fmv/total_fmv)
            item.divided_fmv_lang  = f" in {fm.as_percent(item.percent)} of the interest is {fm.as_curr(item.fmv)}"
            item.divided_exchanged_lang = f" in {fm.as_percent(item.percent)} of the interest is {fm.as_curr(item.basis)}"
            
            if counter < len(asset_list):
                
                divided_fmv_total += f'{item.divided_fmv_lang},'
                divided_exchanged_total += f'{item.divided_exchanged_lang},'

            else:
                
                divided_fmv_total += f'and {item.divided_fmv_lang}'
                divided_exchanged_total += f'and {item.divided_exchanged_lang}'

        divided_fmv = f"{person1.name}'s interest is divided into three parts. The basis{divided_fmv_total}."
        divided_exchanged = f"{person1.name}'s interest is divided into three parts. The basis{divided_exchanged_total}."
        single_fmv = f"{person1.name} has a single basis in {person1.poss} interest of {fm.as_curr(total_fmv)}."
        single_exchanged = f"{person1.name} has a single basis in {person1.poss} interest of {fm.as_curr(total_basis)}."
    
        correct = single_exchanged
    
        possibleanswers = [divided_fmv,divided_exchanged,single_exchanged,single_fmv]
        
        judgements[divided_exchanged] = judgements[divided_fmv]=f'<p>Consider <a href="https://www.law.cornell.edu/uscode/text/26/722" target="_new">Section 722</a>. Does {person1.name} have a divided partnership interest with respect to {person1.poss} basis?</p>'
        judgements[single_fmv] = f'You are correct that {person1.name} has an undivided interest with respect to {person1.poss} basis. But consider <a href="https://www.law.cornell.edu/uscode/text/26/722" target="_new">Section 722</a>.</p>'
        judgements[single_exchanged] = f'<p>Correct. Under <a href="https://www.law.cornell.edu/uscode/text/26/722" target="_new">Section 722</a>, {person1.name} has a single, undivided interest with respect to {person1.poss} basis, equal to the sum of the basis of the property contributed (plus cash contributed and gain, if any, from the rules regarding contributions to investment company-like partnerships).</p>'
    
    
    elif question == partnership_question:
        
        short_asset = asset_choice.name.replace(f"created by {person1.name}","")
        
        tack_answer = f" {partnership_name}'s holding period in the {short_asset} is tacked."
        no_tack_answer = f" {partnership_name}'s holding period in the {short_asset} starts fresh."
    
        fmv_basis_answer = f"{partnership_name}'s basis in the {short_asset} is {fm.as_curr(asset_choice.fmv)}."
        transferred_basis_answer = f"{partnership_name}'s basis in the {short_asset} is {fm.as_curr(asset_choice.basis)}."
    
        tack_fmv = fmv_basis_answer + tack_answer
        no_tack_fmv = fmv_basis_answer + no_tack_answer 
        tack_transferred = transferred_basis_answer + tack_answer
        no_tack_transferred = transferred_basis_answer+ no_tack_answer 
        
        correct = tack_transferred
        
        possibleanswers = [tack_fmv,no_tack_fmv,tack_transferred,no_tack_transferred]
        
        judgements[tack_fmv]='<p>It is correct that the holding period is tacked under <a href="https://www.law.cornell.edu/uscode/text/26/1223" target="_new">Section 1223(2)</a>. But if the holding period is tacked under that subsection, what must be true about the basis of the property? Consider <a href="https://www.law.cornell.edu/uscode/text/26/723" target="_new">Section 723</a>.</p>'
        judgements[tack_transferred]=f'<p>Correct. The basis in the hands of {partnership_name} is the same as it was in the hands of {person1.name}, under <a href="https://www.law.cornell.edu/uscode/text/26/723" target="_new">Section 723</a>, and the holding period is tacked under <a href="https://www.law.cornell.edu/uscode/text/26/1223" target="_new">Section 1223(2)</a>.</p>'
        
        if asset in other_assets:
            judgements[no_tack_fmv]='<p>Does <a href="https://www.law.cornell.edu/uscode/text/26/1223" target="_new">Section 1223(1)</a> apply, or does <a href="https://www.law.cornell.edu/uscode/text/26/1223" target="_new">Section 1223(2)</a> apply? Additionally, with respect to the basis, consider <a href="https://www.law.cornell.edu/uscode/text/26/723" target="_new">Section 723</a>.</p>'
            judgements[no_tack_transferred]=f'<p>It is correct that the basis in the hands of {partnership_name} is the same as it was in the hands of {person1.name}, under <a href="https://www.law.cornell.edu/uscode/text/26/723" target="_new">Section 723</a>. With respect to the holding period, does <a href="https://www.law.cornell.edu/uscode/text/26/1223" target="_new">Section 1223(1)</a> apply, or does <a href="https://www.law.cornell.edu/uscode/text/26/1223" target="_new">Section 1223(2)</a> apply?</p>'
        
        else:
            judgements[no_tack_fmv]='<p>With respect to the basis, consider <a href="https://www.law.cornell.edu/uscode/text/26/723" target="_new">Section 723</a>. With respect to the holding period, consider <a href="https://www.law.cornell.edu/uscode/text/26/1223" target="_new">Section 1223</a>.</p>'
            judgements[no_tack_transferred]=f'<p>It is correct that the basis in the hands of {partnership_name} is the same as it was in the hands of {person1.name}, under <a href="https://www.law.cornell.edu/uscode/text/26/723" target="_new">Section 723</a>. With respect to the holding period, consider <a href="https://www.law.cornell.edu/uscode/text/26/1223" target="_new">Section 1223</a>.</p>'
        
    formattedjudgements = judgements
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers,'words')
    return([problem,cleananswers,judgements_json,correct])   
    

def qbi():
    person1 = fm.create_person()
    
    
    person1_status = random.choice(['married filing jointly','single'])
    
    qbi_threshold = fm.qbi_dict[person1_status.title()][0]
    
    phaseout_size = fm.qbi_dict[person1_status.title()][1]
    
    stdev = fm.rates_dict[person1_status.title()].standard_deduction
    
    #[size[0],(a)(2) limit[1],cap_gain[2]]
    #size: 0 = below threshold, 1 = above threshold
    #(a)(2) limit: 0 = taxable income - cap gain above 20% qbi, 1 = 20% taxable income - cap gain below qbi 
    #cap_gain: 0 = no cap gain, 1 = cap gain
   
    
    type_business = []
    
    for n in range(0,3):
        next = random.randint(0,1)
        type_business.append(next)
        
    
    
   #generate total taxable income
    if type_business[0] == 0:
        
        taxable_income = fm.nearestthousand(random.randint(20000,qbi_threshold-1000))  
        
    elif type_business[0] == 1:
        
        taxable_income = fm.nearestthousand(qbi_threshold+phaseout_size+random.randint(10000,400000))  
        
    
    #generate qbi - if type_business[1] is 0, then there is plenty of taxable income to take all of the QBI. That is, qbi is less than taxable income
    if type_business[1] == 0:    
        
        qbi_type = fm.generate_random_item(taxable_income,50,90)

    #here qbi is greater than taxable income
    elif type_business[1] == 1:
        
        qbi_type = fm.generate_random_item(taxable_income,105,120)
        
    
    #add in cap gain if necessary
    #no cap gain
    if type_business[2] == 0:   

        cap_gain = 0
    
    #yes cap gain
    elif type_business[2] == 1:
        
        #different answer depending on whether 20 percent taxable limitation applies
        #if limitation does not apply make sure taxable income minus cap gain stays bigger than qbi
        if type_business[1] == 0:
            
            cap_gain = fm.generate_random_item((taxable_income - qbi_type),20,80) 
            
        #if it doesn't apply, it doesn't matter how much cap gain there is
        elif type_business[1] == 1:
            
            cap_gain = fm.generate_random_item(taxable_income,10,40)

#pick what kind of business
    
    sstb_dict = {'medical clinic':['clinic','doctor','nurse'],'veterinary clinic':['clinic','veterinarian'],'dental clinic':['clinic','orthodontist','dentist'],'physical therapy clinic':['clinic','physical therapist'],'law firm':['firm','lawyer'],'actuarial firm':['firm','actuary'], 'theater company':['company','individual'], 'consulting business':['business','consultant'], 'financial services firm':['firm','consultant'], 'brokerage services firm':['firm','broker'],'movie production company':['company','individual']} 
    
    qtob_dict = {'engineering firm':['firm','mechanical engineer','geotechnical engineer','civil engineer','electrical engineer','chemical engineer'],'architectural firm':['firm','architect'],'bicycle store':['store','individual'],'pet supply store':['store','individual'],'real estate rental business':['rental business','active owner'],'health club that does not provide any personal training':['health club','individual'],'delivery business':['delivery business','individual']}
    
    all_items = fm.merge(sstb_dict,qtob_dict)
    
    sstb = [*sstb_dict]
    qtob = [*qtob_dict]                   
        
    type_tb = random.choice([sstb,qtob])
    
    business = random.choice(type_tb)
    
    business_short = all_items[business][0]
        
    owner_type = random.choice(all_items[business][1:])
    
    percent_ownership = .1*random.randint(1,9)
    
    net_income_llc = (qbi_type + stdev) / percent_ownership
    
    w_2_limitation_pick = random.choice(['yes','no'])
    
    #w_2 percentage is either 50% or 25%. let's say 50% for now
    w2per = .5
    w2text = int(w2per*100)
    
    #this limitation will apply if 50% of the W-2 wages are less than 20% of the qbi type income
    if w_2_limitation_pick == 'yes':
        
        w_2_wages_indiv = fm.generate_random_item(w2per*qbi_type,60,90)
        
    elif w_2_limitation_pick == 'no':
        
        w_2_wages_indiv = fm.generate_random_item(w2per*qbi_type,105,120)

    w_2_wages = int(fm.nearestthousand(w_2_wages_indiv / percent_ownership))

    deductions = int(fm.nearestthousand(w_2_wages*1.5))

    total_income_llc = int(fm.nearestthousand(net_income_llc + deductions))

    employee_pick = random.choices(['yes','no'],weights=[2,8])[0]
        
    if employee_pick == 'no':
        
        person_sentence = f'{person1.name} is {fm.pick_a_an(owner_type)} {owner_type} who owns {fm.pick_a_an(owner_type)} {fm.as_percent(percent_ownership)} interest in {fm.pick_a_an(business)} {business}. The {business_short} is organized as an LLC and taxed as a partnership. Each member receives a proportional amount of all items.'                        
 
    elif employee_pick == 'yes':
    
        person_sentence = f'{person1.name} is an employee of {fm.pick_a_an(business)} {business}. The {business_short} is organized as an LLC and taxed as a partnership. {person1.name} receives a salary from the {business_short} of {fm.as_curr(taxable_income+stdev)}.'
    
    if type_business[2] == 1:
        
        cap_gain_phrase = f', which includes {fm.as_curr(cap_gain)} of net capital gain'
    
    elif type_business[2] == 0:
    
        cap_gain_phrase = f', which includes no net capital gain'
        
    
    problem = f"{person_sentence} <br><br>The LLC has {fm.as_curr(total_income_llc)} of gross income each year. The LLC also has {fm.as_curr(deductions)} of deductions, which includes {fm.as_curr(w_2_wages)} of W-2 wages. None of the deductions is separately stated. Assume for purposes of this problem that 50% of W-2 wages exceeds the sum of 25% of W-2 wages and 2.5% of the unadjusted basis immediately after acquisition (UBIA) of qualified property. <br><br>{person1.name} is {person1_status} and has taxable income of {fm.as_curr(taxable_income)}{cap_gain_phrase}. How much of a deduction, if any, may {person1.name} take under Section 199A?"
    
    allocated_w_2_wages = int(w_2_wages*percent_ownership)
    w2_limit_final = int(w2per*allocated_w_2_wages)
    qbi_type_final = int(percent_ownership*(total_income_llc - deductions))
    qbi_deduction_final = int(.2*qbi_type_final)
    taxable_income_limit = int(.2*(taxable_income - cap_gain))
    
    deduction_with_ti_limit = min(qbi_deduction_final,taxable_income_limit)
    deduction_with_w2_limit = min(qbi_deduction_final,w2_limit_final)
    deduction_with_both_limits = min(deduction_with_w2_limit,taxable_income_limit)    

#explanations
    
    judgements = {}

    possibleanswers = [0,qbi_deduction_final,deduction_with_w2_limit,deduction_with_ti_limit,deduction_with_both_limits]


    if employee_pick == 'yes':
        
        correct = 0
        
        if taxable_income < qbi_threshold:
            
            judgements[0] = f"<p>Correct. The trade or business of being an employee is never a qualified trade or business. There is no exception available even though {person1.name}'s taxable income is less than the threshold amount plus {fm.as_curr(phaseout_size)}: the exception for small business in <a href='https://www.law.cornell.edu/uscode/text/26/199A' target='_new' rel='noreferrer'>Section 199A</a>(d)(3) applies only to the 'specified service trade or business' prong.</p>"
            judgements[qbi_deduction_final] = judgements[deduction_with_w2_limit] = judgements[deduction_with_ti_limit] = judgements[deduction_with_both_limits] = "<p>Consider the language in <a href='https://www.law.cornell.edu/uscode/text/26/199A' target='_new' rel='noreferrer'>Section 199A</a>(d)(3)(A)(i). There is an exception related to the definition of 'qualified trade or business' for taxpayers with lower incomes, but is such an exception available here?</p>"
            
        else:
              
            judgements[0] = "<p>Correct. Under <a href='https://www.law.cornell.edu/uscode/text/26/199A' target='_new' rel='noreferrer'>Section 199A</a>(d)(1), the trade or business of being an employee is never a qualified trade or business.</p>"
            judgements[qbi_deduction_final] = judgements[deduction_with_w2_limit] = judgements[deduction_with_ti_limit] = judgements[deduction_with_both_limits] = "<p>Consider <a href='https://www.law.cornell.edu/uscode/text/26/199A' target='_new' rel='noreferrer'>Section 199A</a>(d)(1)(B).</p>"

    elif business in sstb:
        
        if taxable_income < qbi_threshold:
  
            correct = deduction_with_ti_limit
            
            judgements[0] = f"<p>It is true that the {business} is a specified service trade or business. But consider the amount of {person1.name}'s taxable income, together with <a href='https://www.law.cornell.edu/uscode/text/26/199A' target='_new' rel='noreferrer'>Section 199A</a>(d)(3).</p>"
            
            
            if taxable_income_limit > qbi_deduction_final:
 
                ti_compare_lang = f"Therefore, because 20% of qualified business income is less than the taxable income limitation, the taxable income limitation does not reduce the available deduction."
            
            else:
                
                ti_compare_lang = f"Therefore, because 20% of qualified business income is greater than the taxable income limitation, the taxable income limitation reduces the available deduction."
            
            ti_language = f"20% of the qualified business income equals 20% of {fm.as_curr(qbi_type_final)}, which equals {fm.as_curr(qbi_deduction_final)}. 20% of taxable income less capital gain equals 20% of {fm.as_curr(taxable_income-cap_gain)}, for a total of {fm.as_curr(taxable_income_limit)}. {ti_compare_lang}" 
            
            judgements[deduction_with_ti_limit]=f"<p>Correct. {person1.name}'s taxable income is {fm.as_curr(taxable_income)}, which is less than the threshold amount of {fm.as_curr(qbi_threshold)}. Therefore <a href='https://www.law.cornell.edu/uscode/text/26/199A' target='_new' rel='noreferrer'>Section 199A</a>(d)(3) permits {person1.name} to take the 199A deduction even though {fm.pick_a_an(business)} {business} is a specified service trade or business under <a href='https://www.law.cornell.edu/uscode/text/26/199A' target='_new' rel='noreferrer'>Section 199A</a>(d)(1)(A). The taxable income limitation could apply. {ti_language}</p>"
            
            #applying w-2 limit as well as ti limit
            if deduction_with_ti_limit != deduction_with_both_limits:
                
                judgements[deduction_with_both_limits] = f"<p>Consider <a href='https://www.law.cornell.edu/uscode/text/26/199A' target='_new' rel='noreferrer'>Section 199A</a>(b)(3).</p>"
            
            # applying the w-2 limit but not the ti limit
            if deduction_with_ti_limit != deduction_with_w2_limit:
                
                judgements[deduction_with_w2_limit] = f"<p>Consider <a href='https://www.law.cornell.edu/uscode/text/26/199A' target='_new' rel='noreferrer'>Section 199A</a>(b)(3).</p>"
            
            #applying neither ti nor w-2 limit - this will be different only if ti limit applies
            if deduction_with_ti_limit != qbi_deduction_final:
                
                judgements[qbi_deduction_final] = f"<p>It is true that {person1.name}'s taxable income is less than the threshold amount of {fm.as_curr(qbi_threshold)}. But does that affect whether the limitation of <a href='https://www.law.cornell.edu/uscode/text/26/199A' target='_new' rel='noreferrer'>Section 199A</a>(a)(2) applies?</p>"
            
        elif taxable_income > qbi_threshold + phaseout_size:
            
            correct = 0
 
            judgements[0]=f"<p>Correct. {fm.pick_a_an(business).capitalize()} {business} is a specified service trade or business under <a href='https://www.law.cornell.edu/uscode/text/26/199A' target='_new' rel='noreferrer'>Section 199A</a>(d)(1)(A). {person1.name}'s taxable income is {fm.as_curr(taxable_income)}, which is greater than the amount at which the <a href='https://www.law.cornell.edu/uscode/text/26/199A' target='_new' rel='noreferrer'>Section 199A</a>(d)(2) exception is fully phased out. Therefore {person1.name} may not take any deduction under <a href='https://www.law.cornell.edu/uscode/text/26/199A' target='_new' rel='noreferrer'>Section 199A</a>.</p>"
            
            judgements[qbi_deduction_final] = judgements[deduction_with_w2_limit] = judgements[deduction_with_ti_limit] = judgements[deduction_with_both_limits] = f"<p>Consider <a href='https://www.law.cornell.edu/uscode/text/26/199A' target='_new' rel='noreferrer'>Section 199A</a>(d)(1)(A).</p>"
      
    elif business in qtob:
        
        judgements[0]=f"<p>Is {fm.pick_a_an(business)} {business} a specified service trade or business under <a href='https://www.law.cornell.edu/uscode/text/26/199A' target='_new' rel='noreferrer'>Section 199A</a>(d)(1)(A)?</p>"
        
        w2_lang = f"20% of qualified business income is 20% of {fm.as_curr(qbi_type_final)}, or {fm.as_curr(qbi_deduction_final)}. {w2text}% of {person1.name}'s allocation of W-2 wages is {w2text}% of the W-2 wages allocable to {person1.name} of {fm.as_curr(allocated_w_2_wages)}, or {fm.as_curr(w2_limit_final)}."
        
        if taxable_income < qbi_threshold: 
            
            correct = deduction_with_ti_limit

            #language if w-2 limit would apply
            if qbi_deduction_final != deduction_with_w2_limit :
                w2_compare_lang = f"20% of qualified business income is greater than the W-2 limitation. But"
                   
            #deduction if w-2 limit would not apply    
            elif qbi_deduction_final == deduction_with_w2_limit:
                w2_compare_lang = f"20% of qualified business income is less than the W-2 limitation. But even if it were greater,"  

            if taxable_income_limit > qbi_deduction_final:
 
                ti_compare_lang = f"Therefore, because 20% of qualified business income is less than the taxable income limitation, the taxable income limitation does not reduce the available deduction."
            
            else:
                
                ti_compare_lang = f"Therefore, because 20% of qualified business income is greater than the taxable income limitation, the taxable income limitation reduces the available deduction."
            
            ti_language = f"20% of the qualified business income equals 20% of {fm.as_curr(qbi_type_final)}, which equals {fm.as_curr(qbi_deduction_final)}. 20% of taxable income less capital gain equals 20% of {fm.as_curr(taxable_income-cap_gain)}, for a total of {fm.as_curr(taxable_income_limit)}. {ti_compare_lang}" 

            judgements[correct] = f"<p>Correct. The {business_short} is a qualified trade or business. {w2_lang} {w2_compare_lang} {person1.name}'s taxable income is less than the threshold amount of {fm.as_curr(qbi_threshold)}. Thus {person1.name} is not subject to the W-2 limitation under <a href='https://www.law.cornell.edu/uscode/text/26/199A' target='_new' rel='noreferrer'>Section 199A</a>(b)(3). <br><br>{ti_language}</p>" 

            if deduction_with_ti_limit != qbi_deduction_final:
                
                judgements[qbi_deduction_final] = f"<p>Consider the amount of {person1.name}'s the taxable income less capital gain and <a href='https://www.law.cornell.edu/uscode/text/26/199A' target='_new' rel='noreferrer'>Section 199A</a>(b)(3).</p>"
                
                
            if deduction_with_ti_limit != deduction_with_w2_limit:    
                
                judgements[deduction_with_w2_limit] = f"<p>Consider <a href='https://www.law.cornell.edu/uscode/text/26/199A' target='_new' rel='noreferrer'>Section 199A</a>(b)(3).</p>" 
           
        elif taxable_income > qbi_threshold + phaseout_size:
                        
            correct  = deduction_with_both_limits  
           
            # create language for w_2 limitation
            if w2_limit_final < qbi_deduction_final:
                
                w_2_compare_lang = "Therefore, because the W-2 limitation is less than 20% of the qualified business income, the W-2 limitation reduces the combined QBI."
                
            else:
                
                w_2_compare_lang = "Therefore, because the W-2 limitation is greater than 20% of the qualified business income, the W-2 limitation does not reduce the combined QBI."

            
            
            #create language for taxable income limitation
            if taxable_income_limit > w2_limit_final:
 
                ti_compare_lang = f"Because the deduction after applying the W-2 limitation is less than the taxable income limitation, the taxable income limitation does not reduce the available deduction."
            
            else:
                
                ti_compare_lang = f"Because the deduction after applying the W-2 limitation is greater than the taxable income imitation, the taxable income limitation reduces the available deduction."
                
            ti_language = f"After applying the W-2 limitation, apply the taxable income less cap gain limitation. The lesser of 20% of qualified business income and {w2text}% of W-2 wages is {fm.as_curr(deduction_with_w2_limit)}. 20% of taxable income less capital gain equals 20% of {fm.as_curr(taxable_income-cap_gain)}, which equals {fm.as_curr(taxable_income_limit)}. {ti_compare_lang}" 
                
            judgements[deduction_with_both_limits] = f"<p>Correct. The {business_short} is a qualified trade or business. {person1.name}'s taxable income is {fm.as_curr(taxable_income)}, which is greater than the threshold amount plus the phaseout range. <br><br>{w2_lang} {w_2_compare_lang} <br><br>{ti_language} Therefore, the final deduction amount is {fm.as_curr(deduction_with_both_limits)}.</p>"
            
            if qbi_deduction_final != correct:
                
                judgements[qbi_deduction_final] =  f"<p>Check the two possible limitations. Consider the amount of {person1.name}'s the taxable income less capital gain and <a href='https://www.law.cornell.edu/uscode/text/26/199A' target='_new' rel='noreferrer'>Section 199A</a>(b)(3). Also consider the amount of W-2 wages allocable to {person1.name}, and consider <a href='https://www.law.cornell.edu/uscode/text/26/199A' target='_new' rel='noreferrer'>Section 199A</a>(a). Does either or both of these limitations reduce the deduction?</p>"
            
            elif qbi_deduction_final != deduction_with_ti_limit and deduction_with_ti_limit != correct:
             
                judgements[deduction_with_ti_limit] = f"<p>Consider the amount of W-2 wages allocable to {person1.name}, and consider <a href='https://www.law.cornell.edu/uscode/text/26/199A' target='_new' rel='noreferrer'>Section 199A</a>(a).</p>"
                
            elif deduction_with_w2_limit not in [deduction_with_ti_limit,correct,qbi_deduction_final]:
                
                judgements[deduction_with_w2_limit] = f"<p>Consider the amount of {person1.name}'s the taxable income less capital gain and <a href='https://www.law.cornell.edu/uscode/text/26/199A' target='_new' rel='noreferrer'>Section 199A</a>(b)(3).</p>"
    
    while True:
        [possibleanswers,judgements] = fm.random_answer_hund(possibleanswers,judgements)
        if len(set(possibleanswers)) > 4:
            break
    
    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)

    return([problem,cleananswers,judgements_json,correct])   

def taxable_year():
    
    #set some variables that will apply for all the types
    year_ends = ['1/31','2/28','3/31','4/30','5/31','6/30','7/31','8/31','9/30','10/31','11/30','12/31']
    
    judgements = {}
    
    partnership_name = random.choice(abc.animals_by_country_dict['English'])
    
    name_list = [partnership_name]
    partner_dict = {}
    
    holdings_language_list = []
    holdings_language = ''
    
    number_good_partners = random.randint(2,4)

    good_taxable_year = random.choice(year_ends[:-1])

    taxable_year_list = ['12/31',good_taxable_year]
    
    #select the type of problem

    class PartnerInfo:
         def __init__(self,name,taxable_year,percent_interest):
            self.name = name
            self.taxable_year = taxable_year
            self.percent_interest = percent_interest


    class YearProblemType:
        def __init__(self,name,interest_floor,interest_ceiling,total_ceiling,total_floor):
            self.name = name
            self.interest_floor = interest_floor
            self.interest_ceiling = interest_ceiling
            self.total_ceiling = total_ceiling
            self.total_floor = total_floor
            
    #the list is [interest_floor,interest_ceiling,total_ceiling,total_floor] for the "good" partners
    majority = YearProblemType('majority',1,40,90,50)
    principal_partner = YearProblemType('principal partner',5,10,50,0)
    least_aggregate_deferral = YearProblemType('least aggregate deferral',0,45,90,60)

    alltypes=[majority,principal_partner,least_aggregate_deferral]
    type_prob = random.choice(alltypes)
    
    number_good_partners = random.randint(2,3)

#This works for all three kinds of problem
    
    def create_good_partners(number_good_partners,name_list,good_taxable_year,type_prob):
        for n in range(number_good_partners):     
            entity_name = random.choice(abc.animals_by_country_dict['English'])
            name_list.append(entity_name)
            type_entity = random.choice(["Inc.,","LLC,"])
            entity = f"{entity_name}, {type_entity}"
            if type_prob.name != 'least aggregate deferral':
                partner_dict[entity] = good_taxable_year
            else:
                while True:
                    taxable_year = random.choice(year_ends[:-1])
                    if taxable_year not in taxable_year_list:
                        taxable_year_list.append(taxable_year)
                        break
                partner_dict[entity] = taxable_year
        return(partner_dict,name_list)
    
    if type_prob != least_aggregate_deferral:
        number_other_partners = random.randint(1,2)
        good_taxable_year = random.choice(year_ends[:-1])        
    elif type_prob == least_aggregate_deferral:
        number_other_partners = 0
        good_taxable_year = '12/31'

    taxable_year_list = ['12/31',good_taxable_year]
    setlist = set(taxable_year_list)
    taxable_year_list = list(setlist)

    #this works for all types for good partners            
    def create_good_interests(number_type_partners,input_dict,output_dict,type_prob):
        
        while True:
            percent_total = 0
            for n in input_dict.keys():
                output_dict[n] = input_dict[n] 
            for n in partner_dict.keys():            
                percent_interest = random.randint(type_prob.interest_floor,type_prob.interest_ceiling)
                value = input_dict[n]
                output_dict[n] = [value, percent_interest]
                percent_total += percent_interest
            if percent_total > type_prob.total_floor and percent_total < type_prob.total_ceiling:
                break      
        return(output_dict,percent_total)  

    (partner_dict,name_list) = create_good_partners(number_good_partners,name_list,good_taxable_year,type_prob)
        
    (partner_dict_new,percent_total) = create_good_interests(number_good_partners,partner_dict,{},type_prob)

#now we have all the information about the good partners: partner: [year end, percent interest]    

#when we do the other partners, we have to go type by type, because it's so different. For deferral we have no "other partners"

    percent_remaining = 100 - percent_total

    if type_prob == majority:
        number_other_partners = random.randint(1,2)
        for n in range(number_other_partners):
            sh_type = random.choice(['individual','entity'])            
            if sh_type == 'individual':
                while True:
                    partner = fm.create_person().name
                    if partner not in name_list:
                        break
                taxable_year = '12/31'
                name_list.append(partner)
            else:
                while True:
                    entity_name = random.choice(abc.animals_by_country_dict['English'])
                    if entity_name not in name_list:
                        break
                type_entity = random.choice(["Inc.","LLC,"])
                partner = f"{entity_name}, {type_entity}"
                while True:
                    taxable_year = random.choice(year_ends[:-1])
                    if taxable_year != good_taxable_year:
                        taxable_year_list.append(taxable_year)
                        break
                name_list.append(entity_name)
            if n == number_other_partners-1:
                percent_interest = percent_remaining
            else:
                percent_interest =  int(fm.generate_random_item_ones(percent_remaining,30,70))
            percent_remaining = percent_remaining - percent_interest
            partner_dict_new[partner] = [taxable_year,percent_interest]
            percent_total += percent_interest       

    elif type_prob == principal_partner:
        percent_first_group = int(random.choice([16,20]))
        percent_second_group = int(random.choice([15,18]))
        percent_third_group = percent_remaining - percent_first_group - percent_second_group
        shareholders_first_group = int(percent_first_group / 4)
        shareholders_second_group = int(percent_second_group  / 3)
        shareholders_third_group = int(percent_third_group)
        other_dict = {shareholders_first_group:['4'],shareholders_second_group:['3'],shareholders_third_group:['1']}
        number_other_partners = 0
        for n in other_dict.keys():
            number_other_partners += n
            while True:
                taxable_year = random.choice(year_ends[:-1])
                if taxable_year not in taxable_year_list:
                    taxable_year_list.append(taxable_year)
                    other_dict[n].append(taxable_year)
                    break
    
    elif type_prob == least_aggregate_deferral:
        number_other_partners = 1
        percent_interest = percent_remaining
        while True:
            entity_name = random.choice(abc.animals_by_country_dict['English'])
            if entity_name not in name_list:
                break
        type_entity = random.choice(["Inc.","LLC,"])
        partner = f"{entity_name}, {type_entity}"
        while True:
            taxable_year = random.choice(year_ends[:-1])
            if taxable_year not in taxable_year_list:
                taxable_year_list.append(taxable_year)
                break
        partner_dict_new[partner] = [taxable_year,percent_interest]

    total_partners = number_good_partners + number_other_partners

### PROBLEM ###
    
    for n in partner_dict_new.keys():
        taxable_year_end = partner_dict_new[n][0]
        percent_interest = partner_dict_new[n][1]
        holdings_lang_partner = f"{n} holds a {percent_interest} percent interest in {partnership_name} and has a taxable year ending {taxable_year_end}. "
        holdings_language_list.append(holdings_lang_partner)
    
    if type_prob == principal_partner:
        for n in other_dict.keys():
            number_shareholders = n
            percent_per_shareholder = other_dict[n][0]
            group_taxable_year = other_dict[n][1]
            holdings_language_group = f"A group of {number_shareholders} members holds interests in {partnership_name}; each member holds a {percent_per_shareholder} percent interest in {partnership_name}, and each has a taxable year ending {group_taxable_year}. "
            holdings_language_list.append(holdings_language_group)
        
    random.shuffle(holdings_language_list)
    
    for n in holdings_language_list:
        holdings_language = holdings_language + n
            
    problem = f"{partnership_name}, LLC, has {total_partners} members. {holdings_language}{partnership_name}'s revenue is spread evenly across the calendar year. Which of the following is the most accurate statement about {partnership_name}'s taxable year?"
    
### ANSWERS ###
    # create the answer text language
    def create_ans_text(x):
        ans_text = f"{partnership_name}'s required taxable year end is {x}."
        return ans_text
    
    #create the list of possible answers
    no_year = f"{partnership_name} has no required taxable year end."
    possibleanswers = [no_year]
    for n in taxable_year_list:
        n_ans = create_ans_text(n)
        possibleanswers.append(n_ans)
    
    #note the correct answer for majority and principal partner
    if type_prob != least_aggregate_deferral:
        correct = create_ans_text(good_taxable_year)

    # figure out the right answer for least aggregate deferral    
    else:
        deferral_dict = {}
        aggregate_deferral_lang = ''
        for n in taxable_year_list:
            year_end = n
            total_deferral = 0
            partnership_month_end = int(year_end.split('/')[0])
            for partner in partner_dict_new.keys():
                partner_month_end = int(partner_dict_new[partner][0].split('/')[0])
                partner_month_deferral = (partner_month_end - partnership_month_end) % 12
                partner_weighted_deferral = (partner_dict_new[partner][1]/100)*partner_month_deferral
                print(n,partner_weighted_deferral)
                total_deferral += partner_weighted_deferral
            aggregate_deferral_lang += f'The aggregate deferral for {n} is {total_deferral} months. '
            deferral_dict[total_deferral] = n
        least_deferral = min(deferral_dict.keys())
        least_deferral_year = deferral_dict[least_deferral]
        least_deferral_rounded = round(least_deferral,2)
        correct = least_deferral_year
    
#### JUDGEMENTS ####
    
    judgements[no_year] = f"<p>Consider <a href='https://www.law.cornell.edu/uscode/text/26/706' target='_new' rel='noreferrer'>Section 706</a>(b)(1)(B). Do any of the required taxable years described there apply to {partnership_name}?</p>"
        
    for n in taxable_year_list:
        
        if n != correct:
            
            judgements[create_ans_text(n)] =  f"<p>Consider <a href='https://www.law.cornell.edu/uscode/text/26/706' target='_new' rel='noreferrer'>Section 706</a>(b)(1)(B). Do any of the required taxable years described there apply to {partnership_name}?</p>"
    
    if type_prob == majority:
    
        judgements[create_ans_text(good_taxable_year)] = f"<p>Correct. The members with the taxable year ending {good_taxable_year} hold more than 50 percent of the interests in the LLC. Under <a href='https://www.law.cornell.edu/uscode/text/26/706' target='_new' rel='noreferrer'>Section 706</a>(b)(1)(B), the LLC therefore has a majority interest taxable year, which will be the required taxable year.</p>"
     
    elif type_prob == principal_partner:   
         
         judgements[create_ans_text(good_taxable_year)] = f"<p>Correct. There is no majority taxable year, but all of the members who own at least 5 percent of the LLC have the same taxable year. Under <a href='https://www.law.cornell.edu/uscode/text/26/706' target='_new' rel='noreferrer'>Section 706</a>(b)(1)(B), because there is no majority interest taxable year, but there is a principal partner taxable year, the principal partner taxable year is the required taxable year.</p>"
    
    elif type_prob == least_aggregate_deferral:   
         
         judgements[create_ans_text(correct)] = f"<p>Correct. There is no majority taxable year, because there is no single taxable year that is the taxable year of a group of members who in aggregate hold a majority interest. There is no principal partner taxable year, because not all of the members who own at least 5 percent of the LLC have the same taxable year. Therefore, under <a href='https://www.law.cornell.edu/uscode/text/26/706' target='_new' rel='noreferrer'>Section 706</a>(b)(1)(B), the taxable year is the taxable year ending {correct}, because that is the taxable year that results in the least aggregate deferral, {least_deferral_rounded}, weighting months deferred for each member by the interest that member holds.</p>"
    
    formattedjudgements = fm.format_dict(judgements,"words")
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers,"words")
    return([problem,cleananswers,judgements_json,correct])   
    
def shifting_interests():
    [person1,person2]=fm.create_group()
    partnership = fm.pick_entity_name(type='partnership')
    
    initial_interest = 5*random.randint(3,18)
    initial_interest_percent = initial_interest/100
    
    while True:
        post_sale_rough = fm.generate_random_item_ones(initial_interest,20,90)
        post_sale_interest = fm.nearest_x(post_sale_rough,5)
        if post_sale_interest != initial_interest:
            break
    
    post_sale_interest_percent = post_sale_interest/100
    
    fraction_of_year = random.randint(2,8)
    percent_year_before_sale = 1/fraction_of_year
    percent_year_after_sale = 1 - percent_year_before_sale
    
    
    earnings_before = random.randint(3,100)*1000
    earnings_after = random.randint(3,100)*1000
    total_earnings = earnings_before + earnings_after
        
    closing_of_books_answer = int( (initial_interest_percent*earnings_before) + (post_sale_interest_percent*earnings_after) )
    proration_answer = int( percent_year_before_sale * initial_interest_percent * total_earnings + percent_year_after_sale * post_sale_interest_percent*total_earnings)
    #some wrong answers
    average_interest = int( total_earnings * (initial_interest_percent + post_sale_interest_percent)/2)
    
    
    allocation_dict = {'interim closing of the books':closing_of_books_answer,'proration':proration_answer}

    type_allocation = random.choice([*allocation_dict])
    
    problem = f"{person1.name} has a {initial_interest} percent interest in {partnership}, an LLC that is taxed as a partnership and that has a calendar taxable year. Exactly 1/{fraction_of_year} of the way through {fm.current_year}, {person1.name} sells a portion of {person1.poss} interest in the partnership to {person2.name}, so that after the sale, {person1.name} has a {post_sale_interest} percent interest in {partnership}. Before the sale to {person2.name}, {partnership}, earns {fm.as_curr(earnings_before)}. After the sale, {partnership}, earns {fm.as_curr(earnings_after)}. {partnership}, adheres to the varying interests rule by using the {type_allocation} method. How much income does {partnership}, pass through to {person1.name} in {fm.current_year}?"
    
    possibleanswers = [closing_of_books_answer,proration_answer,average_interest]
    
    judgements = {}

    correct = allocation_dict[type_allocation]
    
    if type_allocation == 'interim closing of the books':
        
        judgements[correct] = f'Correct. Under the interim closing of the books method, {person1.name} gets {initial_interest} percent of the {fm.as_curr(earnings_before)} the LLC earned before the sale, and {post_sale_interest} percent of the {fm.as_curr(earnings_after)} the LLC earned after the sale.'

        judgements[proration_answer] = f'This answer would be right if the income were smoothed throughout the year. But {partnership}, uses the interim closing of the books method.'

    elif type_allocation == 'proration':
        
        judgements[correct] = f'Correct. The proration method effectively smooths the income over the year and then gives each partner their proportionate amount of that smoothed income. In this situation, there was {fm.as_curr(total_earnings)} for the year. For 1/{fraction_of_year} of the year, {person1.name} gets {initial_interest} percent of that total amount. For the remainder of the year, {person1.name} gets {post_sale_interest} percent of that amount.'
        
        judgements[closing_of_books_answer] = f"This would be correct if {partnership}, used the closing of the books method. But it chose the proration method."

     
    [possibleanswers,judgements] = fm.random_answer_pot(possibleanswers,judgements,1)
    [possibleanswers,judgements] = fm.random_answer_pot(possibleanswers,judgements,0)

    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return([problem,cleananswers,judgements_json,correct])  

def Section_724():
    person1 = fm.create_person()
    judgements={}

    
    receivables = fm.Section724Asset('unrealized receivables','724(a)','ordinary','capital',.2)
    inventory = fm.Section724Asset('inventory','724(b)','ordinary','capital',.2)
    capital = fm.Section724Asset('a capital asset','724(c)','capital','ordinary',.5)
    
    contributed = random.choice([receivables,inventory,capital])
    
    asset_fmv = 1000*random.randint(3,15)
    
    
    while True:
        asset_basis = fm.generate_random_basis(asset_fmv,2,contributed.lossprobability)
        if asset_fmv != asset_basis:
            break
   
    while True:
        asset_fmv_sale = fm.generate_random_pot(asset_fmv,2)
        if asset_fmv_sale != asset_basis:
            break
    
    contribution_date = fm.pick_random_date_this_year()
    
    morethanfiveyears = random.choice([True,False])
    
    if morethanfiveyears == True:
        sale_date = fm.date_after(contribution_date,soonest=1900,latest=2100)
    else:
        sale_date = fm.date_after(contribution_date,soonest=50,latest=1700)
    

    
    problem = f"On {fm.full_date(contribution_date)}, {person1.name} contributes property to an LLC of which {person1.nom} is a member. The property constitutes {contributed.assettype} in the hands of {person1.name}, but the property is {fm.pick_a_an(contributed.partnershiptypegain)} {contributed.partnershiptypegain} asset in the hands of the LLC. At the time of the contribution, the value of the property was {fm.ac(asset_fmv)} and the basis of the property in the hands of {person1.name} was {fm.ac(asset_basis)}. On {fm.full_date(sale_date)}, the LLC sells the asset for {fm.ac(asset_fmv_sale)}. What is the character of the gain or loss on the sale of the property?"
    
    possibleanswers = ['capital','ordinary','some is capital and some is ordinary']
    
    
    if asset_fmv_sale > asset_fmv:
        gainlanguage = "All the gain is recharacterized, even gain that accrued during the time the inventory was held by the LLC."
    elif asset_fmv_sale < asset_basis:
        gainlanguage = "Both gain and loss are recharacterized."
    else:
        gainlanguage = ""
    
    if contributed == receivables:
        correct = 'ordinary'

        if morethanfiveyears==True:
            datelanguage = 'The accounts receivable were sold more than five years after contribution, but that does not prevent recharacterization. There is no time limitation on the recharacterization of accounts receivable under Section 724.'
            judgements['capital']='Is there a time limitation on the recharacterization of accounts receivable under Section 724(a)?'
        else:
            datelanguage = ""
 
        judgements[correct]=f"Correct. Under Section 724(a), the LLC's gain or loss from property that was accounts receivable in the hands of the contributing member is characterized as ordinary. {datelanguage} {gainlanguage}"
        judgements['some is capital and some is ordinary']="Is there a limit on the amount that is recharacterized? Consider the flush language of Section 724(a)."
        judgements['capital']="Consider Section 724(a)."
        
    
    elif contributed == inventory:
        if morethanfiveyears == True:
            correct = contributed.partnershiptypegain
            judgements[correct]=f"Correct. There is no recharacterization under Section {contributed.subsection} for {contributed.assettype} after five years have passed. See the flush language in Section {contributed.subsection}."
            judgements[contributed.partnertypegain]=f"Consider the amount of time that has passed and the flush language in Section {contributed.subsection}."
        
        else:
            correct = 'ordinary'
            judgements[correct]=f"Correct. Under Section 724(b), the LLC's gain or loss from property that was inventory in the hands of the contributing member is characterized as ordinary. {gainlanguage}"
            judgements['some is capital and some is ordinary']="Is there a limit on the amount that is recharacterized? Consider the flush language of Section 724(b)."
            judgements['capital']=f"Consider Section 724(b)."
            
    elif contributed == capital:
        if asset_fmv < asset_basis:
            if morethanfiveyears == True:
                correct = 'ordinary'
                judgements[correct]=f"Correct. There is no recharacterization under Section {contributed.subsection} for {contributed.assettype} after five years have passed. See the flush language in Section {contributed.subsection}."
                judgements[contributed.partnertypegain]=f"Consider the amount of time that has passed and the flush language in Section {contributed.subsection}."                        
            elif asset_fmv_sale < asset_fmv:
                correct='some is capital and some is ordinary'
                judgements[correct]="Correct. Under Section 724(c), the LLC's loss from the sale of an asset that was a capital asset in the hands of the contributing member is recharacterized as capital, but only to the extent of that there was a loss in the asset when it was contributed."
                judgements['capital']="Is all of the loss recharacterized? Consider the flush language of Section 724(c)."
            elif asset_fmv_sale > asset_fmv and asset_fmv_sale < asset_basis:
                correct='capital'
                judgements[correct]="Correct. Under Section 724(c), the LLC's loss from the sale of an asset that was a capital asset in the hands of the contributing member is recharacterized as capital to the extent of that there was a loss in the asset when it was contributed. Here, there is less loss on the sale than there was when the asset was contributed, so all of the loss on the sale is recharacterized."
                judgements['some is capital and some is ordinary']='How much loss was there in the asset when it was contributed? How much loss is there on the sale? Consider the flush langage of Section 724(c).'
            elif asset_fmv_sale > asset_basis:
                correct='ordinary'
                judgements[correct]="Correct. Only loss is recharacterized under Section 724(c)."
                judgements['capital']=judgements['some is capital and some is ordinary']="Consider Section 724(c). Is gain recharacterized under that subsection?"
        elif asset_fmv > asset_basis:
            correct='ordinary'
            judgements[correct]="Correct. Under Section 724(c), recharacterization occurs only if there is loss when the asset is contributed."
            judgements['capital']=judgements['some is capital and some is ordinary']="Consider Section 724(c). Is there recharacterization under that subsection when contributed property has a built-in gain?"
            
    formattedjudgements = judgements
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers,'words')
    return([problem,cleananswers,judgements_json,correct])   


def assign_function(fn):
    if fn == "a random type of problem":
        fn_pick = random.choice(true_functions_list)
    else:
        fn_pick = fn 
        
    return(fn_pick)


def function_picker(fn_pick):
    fn = assign_function(fn_pick)
    if fn == '1.4 Check the box':
        return(check_the_box())
    elif fn == '1.6 Section 199A qualified business income deduction':
        return(qbi())
    elif fn == '2.2 Transfers to a partnership: basis and holding period':
        return(transfers_to_partnership())
    elif fn == '2.1 Transfers to a partnership: nonrecognition':
        return(investment_partnership())
    elif fn == '4.2 Required taxable years':
        return(taxable_year())
    elif fn == '6.1 Varying interests rule':
        return(shifting_interests())
    elif fn == '7.2 Section 724':
        return(Section_724())
        