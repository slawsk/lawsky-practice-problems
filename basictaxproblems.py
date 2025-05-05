# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 06:28:35 2019

@author: carso
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 05:45:43 2019

@author: carso
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 11:28:49 2019

@author: sbl083
"""
# to add function: write function; update functions_list, function_picker, random_picker

# =============================================================================
# table of contents:
# Imports
# Inflation Adjustments
# Defining Terms
# Defining Functions
# Implementation
# =============================================================================

# Imports

import numpy as np
import numpy_financial as npf
import random
import math
from datetime import date
import names
import json
import functionmodules as fm
import statistics
import animalsbycountry as abc
import depreciation as dp
import pandas as pd

# Defining Functions


def rates_problems(type_problem="random"):

    [person1, person2] = fm.create_group()
    married = fm.RatesProb(
        f"{person1.name} and {person2.name} are married and file jointly.",
        "their",
        fm.married,
    )
    single = fm.RatesProb(
        f"{person1.name} is single and files as a single person.",
        person1.poss,
        fm.single,
    )
    hoh = fm.RatesProb(
        f"{person1.name} is single and files as a head of household.",
        person1.poss,
        fm.hoh,
    )
    filing_types = [married, single, hoh]
    status = random.choice(filing_types)
    df = status.type_taxpayer.brackets
    bracket_choice = random.randint(0, df.index.max())

    bottom_bracket = df.at[bracket_choice, "BottomOfBracket"]
    top_bracket = df.at[bracket_choice, "TopOfBracket"]
    base_to_add = df.at[bracket_choice, "AmountToAdd"]

    AGI = random.randint(bottom_bracket, top_bracket)

    marginal_rate = fm.rates_facts_marginal(status.type_taxpayer, AGI)

    if bracket_choice == df.index.max():
        explanation_brackets = (
            f"{status.pronouns} taxable income is above {fm.ac(bottom_bracket)}"
        )
    else:
        explanation_brackets = f"{status.pronouns} taxable income is between {fm.ac(bottom_bracket)} and {fm.ac(top_bracket)}"

    if type_problem == "random":
        type_problem = random.choice(["marginal", "owed"])

    if type_problem == "marginal":

        problem = f"{status.factsentence} {status.pronouns.capitalize()} taxable income in {str(fm.current_year)} is {fm.ac(AGI)}. What is {status.pronouns} marginal tax rate?"
        correct = marginal_rate
        correct_explanation = f'<p>Correct. Because {status.factsentence[:-1]} and {explanation_brackets}, under <a href="/assets/InflationRevProc.pdf" target="_new">{fm.current_rev_proc}</a>, the relevant marginal rate is {fm.as_percent(correct)}.</p>'
        judgements = {correct: correct_explanation}
        possibleanswers = fm.reformat(fm.rates_list, "percent")
        formattedjudgements = fm.format_dict(judgements, "percent")
        cleananswers = [fm.as_percent(correct)] + possibleanswers
        cleananswers = list(set(cleananswers))

        judgements_json = json.dumps(formattedjudgements)

        return [problem, cleananswers, judgements_json, correct]

    else:
        problem = f"{status.factsentence} {status.pronouns.capitalize()} taxable income in {str(fm.current_year)} is {fm.ac(AGI)}. Assume that there are no available credits. Rounded to the nearest dollar, what is {status.pronouns} total tax owed?"

        correct = int(round(fm.tax_owed_answer(status.type_taxpayer, AGI), 0))

        tax_on_marginal_rate = int(marginal_rate * AGI)
        tax_owed_married = int(fm.tax_owed_answer(fm.married, AGI))
        tax_owed_hoh = int(fm.tax_owed_answer(fm.hoh, AGI))
        tax_owed_single = int(fm.tax_owed_answer(fm.single, AGI))

        tax_owed_list = [tax_owed_married, tax_owed_hoh, tax_owed_single]

        possibleanswers = [correct, tax_on_marginal_rate]

        correct_explanation = f'<p>Correct. Because {status.factsentence[:-1]} and {explanation_brackets}, under <a href="/assets/InflationRevProc.pdf" target="_new">{fm.current_rev_proc}</a>, the tax owed equals the sum of {fm.ac(int(base_to_add))} plus {fm.as_percent(marginal_rate)} multiplied by the excess of {fm.ac(AGI)} over {fm.ac(bottom_bracket)}, for a total of {fm.ac(correct)}.</p>'

        judgements = {correct: correct_explanation}

        if bracket_choice == 0:
            for i in range(0, 3):
                [possibleanswers, judgements] = fm.random_answer_pot(
                    possibleanswers, judgements, 0
                )

        else:
            judgements[tax_on_marginal_rate] = (
                "This would be the correct answer if the marginal rate were applied to all of the earnings of the taxpayer."
            )
            for item in tax_owed_list:
                if item != correct:
                    possibleanswers.append(item)
                    judgements[item] = (
                        "What type of taxpayer is this (single, married, head of household)?"
                    )

        [possibleanswers, judgements] = fm.random_answer_pot(
            possibleanswers, judgements, 0
        )

        formattedjudgements = fm.format_dict(judgements)
        cleananswers = fm.create_clean_answers(possibleanswers)
        judgements_json = json.dumps(formattedjudgements)

        return [problem, cleananswers, judgements_json, correct]


def tvm():

    value = random.randint(1000, 200000)
    initial_rate = random.randint(2, 15)
    length_time = random.randint(3, 25)

    question_dict = {
        "present value": {
            "calculator link": "'https://www.calculatorsoup.com/calculators/financial/present-value-calculator.php'",
            "opposite": "future value",
            "relevant function": npf.pv,
            "when receive": f"in {length_time} years",
            "value when": "now",
        },
        "future value": {
            "calculator link": "'https://www.calculatorsoup.com/calculators/financial/future-value-calculator.php'",
            "opposite": "present value",
            "relevant function": npf.fv,
            "when receive": "now",
            "value when": f"in {length_time} years",
        },
    }

    type_problem = random.choice(list(question_dict.keys()))
    type_prob_dict = question_dict[type_problem]
    calculator_link = type_prob_dict["calculator link"]
    opposite = type_prob_dict["opposite"]
    relevant_function = type_prob_dict["relevant function"]
    value_when = type_prob_dict["value when"]
    when_receive = type_prob_dict["when receive"]

    problem = f"What is the {type_problem} {value_when} of receiving {fm.ac(value)} {when_receive} if the relevant interest rate is {initial_rate}% and interest is compounded annually?"
    correct = -int(
        relevant_function(initial_rate / 100, length_time, 0, value, when="end")
    )
    explanation = f'<p>Correct. Use a time value of money calculator, such as the one at <a href={calculator_link} target="_new" rel="noreferrer">Calculator Soup</a>. For {opposite}, enter {fm.ac(value)}. The number of periods is {length_time}. The interest rate is {initial_rate}%, and compounding is once per period, or annual compounding.</p>'

    monthly_compounding = -int(
        relevant_function(initial_rate / 1200, length_time * 12, 0, value, when="end")
    )

    semiannual_compounding = -int(
        relevant_function(initial_rate / 200, length_time * 2, 0, value, when="end")
    )

    monthly_compounding_correct_periods = -int(
        relevant_function(initial_rate / 1200, length_time, 0, value, when="end")
    )

    semiannual_compounding_correct_periods = -int(
        relevant_function(initial_rate / 200, length_time, 0, value, when="end")
    )

    possibleanswers = [
        correct,
        monthly_compounding,
        semiannual_compounding,
        monthly_compounding_correct_periods,
        semiannual_compounding_correct_periods,
    ]

    judgements = {
        correct: explanation,
        monthly_compounding: "This would be the correct answer for monthly compounding (i.e., compounding 12 times per period).",
        semiannual_compounding: "This would be the correct answer for semiannual compounding (i.e., compounding 2 times per period).",
        monthly_compounding_correct_periods: f"This would be the correct answer for {length_time} months, with an annual rate of {initial_rate}%, and thus a monthly rate of 1/12 of that.",
        semiannual_compounding_correct_periods: f"This would be the correct answer for {length_time} six-month periods, with an annual rate of {initial_rate}%, and thus a semiannual rate of 1/2 of that.",
    }

    possibleanswers, judgements = fm.random_answer_ones(possibleanswers, judgements)

    formattedjudgements = fm.format_dict(judgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    judgements_json = json.dumps(formattedjudgements)
    return [problem, cleananswers, judgements_json, correct]


def gross_up(type_problem="random"):
    person = fm.create_person()
    employer = random.choice(abc.animals_by_country_dict["English"])

    if person.gender == "nonbinary":
        correctreceive = "receive"
    else:
        correctreceive = "receives"

    payment = 1000 * random.randint(3, 30)
    marginal_rate = random.randint(25, 50)
    marginal_rate_calc = marginal_rate / 100

    problem = f"{person.name} receives a bonus payment of {fm.ac(payment)} from {person.poss} employer, {employer}, Inc. {employer}, Inc., wants to pay the tax that {person.name} will owe due to the bonus, so that {person.name} will truly have, in {person.poss} pocket, the full bonus of {fm.ac(payment)}, even after taxes are paid. Assume that the entire payment will be taxed at the rate of {marginal_rate}% (this includes all taxes that {person.name} would owe). What is the total amount that {employer}, Inc., should pay {person.name}, to reach the goal of {person.name} benefiting from the full target bonus amount? Put another way, what is the total payment, including the gross-up for taxes?"

    correct = int(round(payment / (1 - marginal_rate_calc)))
    one_gross_up = int(round(payment + (marginal_rate_calc * payment)))
    amount_extra_one_gross_up = int(round((marginal_rate_calc * payment)))
    correct_amount_extra = int(round(marginal_rate_calc * correct))

    possibleanswers = [
        correct,
        one_gross_up,
        amount_extra_one_gross_up,
        correct_amount_extra,
    ]

    judgements = {
        correct: f'<p>Correct! {person.name} will owe tax on the total amount {person.nom} {correctreceive}, under, for example, <a href="https://supreme.justia.com/cases/federal/us/279/716/" target="_new">Old Colony Trust v. Commissioner</a>. In order to end up with {fm.ac(payment)}, {person.nom} will have to receive some amount such that after tax is paid on that total, {person.nom} will have {fm.ac(payment)} left. Total - Tax on Total = {fm.ac(payment)}. The tax on the total will be the total times the marginal rate, so Total - (Rate x Total) = {fm.ac(payment)}, or Total = {fm.ac(payment)} / (1 - Rate). Here, the marginal rate is {marginal_rate}%, and {fm.ac(payment)} / (1 - {marginal_rate}%) = {fm.ac(correct)}.</p>',
        one_gross_up: f"This includes the {fm.ac(amount_extra_one_gross_up)} tax on the target amount of the bonus payment of {fm.ac(payment)}. What about the tax that will be owed on that additional {fm.ac(amount_extra_one_gross_up)} itself?",
        amount_extra_one_gross_up: f"This is the tax on the target amount of the bonus payment of {fm.ac(payment)}. But what about the tax that will be owed on the payment of the tax? Additionally, the problem asks for the total amount that {person.name} will receive.",
        correct_amount_extra: f"This is the correct extra amount; the problem asks for the total amount that {person.name} will receive.",
    }

    possibleanswers, judgements = fm.random_answer_ones_off_target(
        possibleanswers, judgements, correct, start=80, end=130
    )
    possibleanswers, judgements = fm.random_answer_ones_off_target(
        possibleanswers, judgements, correct, start=80, end=130
    )
    possibleanswers, judgements = fm.random_answer_ones_off_target(
        possibleanswers, judgements, correct_amount_extra, start=80, end=120
    )

    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


def bonds_COD(problem_type="random"):
    [person1, person2, person3] = fm.create_group(size=3)

    # pick the relevant values for calculating present value
    future_value = 5000 * random.randint(3, 15)
    time = 5 * random.randint(2, 6)
    initial_rate = random.randint(4, 8)
    pmt = future_value * initial_rate / 100
    future_rate = initial_rate + random.randint(1, 3)
    time_passed = random.randint(2, 8)

    present_value = npf.pv(
        future_rate / 100, time - time_passed, pmt, future_value, when="end"
    )
    present_value_int = int(round(present_value))

    sold_stuff = random.choice(["equipment", "supplies", "goods", "machinery"])

    corporation_name = fm.pick_entity_name()

    buyer = person2.name

    year_sold = fm.current_year - random.randint(1, 3)

    holdverb = fm.CorrectVerb("hold", "holds")

    if person1.gender == "nonbinary":
        correcthold = holdverb.nbv
    else:
        correcthold = holdverb.bv

    problem_166 = f"{corporation_name}, whose business is manufacturing {sold_stuff}, sold {sold_stuff} to {person1.name} in {year_sold} for {fm.ac(future_value)} on credit. In {fm.current_year}, after {person1.name} has paid off {fm.ac(-present_value_int)} of the debt, {corporation_name}, determines that {person1.name} will be unable to pay back the rest of the debt and accordingly cancels the debt. How much loss or deduction does this cancellation generate for {corporation_name}, and what is the character of that loss or deduction?"

    problem_165 = f"{person1.name} buys a bond from {corporation_name}, when the bond is originally issued, for {fm.ac(future_value)}. The bond pays {fm.ac(future_value)} in {str(time)} years and pays {fm.ac(int(pmt))} of interest at the end of each year {person1.nom} {correcthold} it, compounded annually. {person1.name} holds the bond for investment purposes. After {person1.name} has held the bond for {str(time_passed)} years, {person1.name} sells the bond to {buyer}, for the market value of the bond at that time. At the time of the sale, the relevant market interest rate is {str(future_rate)} percent, compounded annually. How much loss does the sale of the bond generate for {person1.name}, and what is the character of the loss?"

    if problem_type == "random":
        problem = random.choice([problem_166, problem_165])
    else:
        prob_type_dict = {"165": problem_165, "166": problem_166}
        problem = prob_type_dict["problem_type"]

    correctnumber = int(future_value + round(present_value))
    no_lossnumber = int(round(abs(present_value)))
    random_no_lossnumber = int(
        abs((no_lossnumber - round(0.8 * random.random() * no_lossnumber)))
    )
    randomnumber = int(abs(random_no_lossnumber - future_value))

    correct_num_ordinary = f"Ordinary loss of {fm.ac(correctnumber)}"

    correct_num_capital = f"Capital loss of {fm.ac(correctnumber)}"

    no_loss_ordinary = f"Ordinary loss of {fm.ac(no_lossnumber)}"

    no_loss_capital = f"Capital loss of {fm.ac(no_lossnumber)}"

    rand_num_ordinary = f"Ordinary loss of {fm.ac(randomnumber)}"

    rand_num_capital = f"Capital loss of {fm.ac(randomnumber)}"

    zero = "No loss"

    if problem == problem_165:

        correct = correct_num_capital

        possibleanswers = [
            zero,
            correct_num_ordinary,
            correct_num_capital,
            no_loss_ordinary,
            no_loss_capital,
            rand_num_ordinary,
            rand_num_capital,
        ]
        judgements = {
            correct_num_capital: f'<p>Correct! The interest rate went up, so the value of the bond went down. More specifically, the buyer will demand a return of {str(future_rate)} percent, the current market rate. The future value of the bond is {fm.ac(future_value)}. There are {str(time)} - {str(time_passed)} = {str(time-time_passed)} years left before the payment of {fm.ac(future_value)}. The present value of {fm.ac(future_value)} in {str(time-time_passed)} years at an interest rate of {str(future_rate)} percent is {fm.ac(no_lossnumber)}. The bond has a basis of {fm.ac(future_value)}, so selling it for {fm.ac(no_lossnumber)} results in a loss of {fm.ac(no_lossnumber)} - {fm.ac(future_value)} = {fm.ac(correctnumber)}. The buyer was not the initial lender, so the loss is a capital loss, under <a href="https://www.law.cornell.edu/uscode/text/26/165" target="_new" rel="noreferrer">Section 165</a>.</p>',
            correct_num_ordinary: "You have the amount right. But who purchased the debt?",
            no_loss_ordinary: "The question asks for the total loss, not the value of the bond at sale. Also, who purchased the debt?",
            no_loss_capital: "The question asks for the total loss, not the value of the bond at sale.",
            rand_num_ordinary: "Try again. Consider, also, who purchased the debt.",
            rand_num_capital: "You have the character right; try again with the number.",
            zero: '<p>A loss is permitted here. Consider <a href="https://www.law.cornell.edu/uscode/text/26/165" target="_new">Section 165</a>.</p>',
        }

    if problem == problem_166:

        full_amount_ordinary = f"Ordinary loss of {fm.ac(future_value)}"

        full_amount_capital = f"Capital loss of {fm.ac(future_value)}"

        possibleanswers = [
            zero,
            correct_num_ordinary,
            correct_num_capital,
            no_loss_ordinary,
            no_loss_capital,
            full_amount_ordinary,
            full_amount_capital,
        ]

        judgements = {
            correct_num_ordinary: f'<p>Correct! When the debt was cancelled by the initial lender, there was an ordinary (bad debt) loss, under <a href="https://www.law.cornell.edu/uscode/text/26/166" target="_blank" rel="noreferrer">Section 166</a>, in the amount that went unpaid.</p>',
            correct_num_capital: '<p>You have the amount right. But consider <a href="https://www.law.cornell.edu/uscode/text/26/61" target="_new">Section 61(a)(11)</a>. What is its counterpart on the seller side?</p>',
            no_loss_ordinary: "You have the character right; with respect to the number, this is the amount that was paid. How much was left unpaid?",
            no_loss_capital: "This is the amount that was paid. How much was left unpaid? Also, consider the source of the debt relief (i.e., the initial lender).",
            full_amount_capital: "Consider the amount of the loss: is the entire debt forgiven? Consider, also, the source of the debt relief (i.e., the initial lender).",
            full_amount_ordinary: "You have the character right. Consider the amount of the loss: is the entire debt forgiven?",
            zero: '<p>A loss is permitted here. Consider <a href="https://www.law.cornell.edu/uscode/text/26/166" target="_new">Section 166</a>.</p>',
        }

        correct = correct_num_ordinary

    judgements_json = json.dumps(judgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


def bonds_simple():
    [person1, person2, person3] = fm.create_group(size=3)

    # pick the relevant values for calculating present value
    future_value = 5000 * random.randint(3, 15)
    time = 5 * random.randint(2, 6)
    initial_rate = random.randint(4, 8)
    pmt = int(future_value * initial_rate / 100)
    future_rate = initial_rate + random.randint(1, 3)
    time_passed = random.randint(2, 8)

    present_value = npf.pv(
        future_rate / 100, time - time_passed, pmt, future_value, when="end"
    )
    present_value_int = int(round(present_value))

    sold_stuff = random.choice(["equipment", "supplies", "goods", "machinery"])

    corporation_name = fm.pick_entity_name()

    buyer = person2.name

    year_sold = fm.current_year - random.randint(1, 3)

    holdverb = fm.CorrectVerb("hold", "holds")

    if person1.gender == "nonbinary":
        correcthold = holdverb.nbv
    else:
        correcthold = holdverb.bv

    problem = f"{person1.name} buys a bond from {corporation_name}, when the bond is originally issued, for {fm.ac(future_value)}. The bond pays {fm.ac(future_value)} in {str(time)} years and pays {fm.ac(int(pmt))} of interest at the end of each year {person1.nom} {correcthold} it, compounded annually. {person1.name} holds the bond for investment purposes. After {person1.name} has held the bond for {str(time_passed)} years, {person1.name} sells the bond to {buyer}, for the market value of the bond at that time. At the time of the sale, the relevant market interest rate is {str(future_rate)} percent, compounded annually. How much loss does the sale of the bond generate for {person1.name}?"

    correct = int(future_value + round(present_value))
    no_loss = int(round(abs(present_value)))

    judgements = {
        correct: f"Correct! The interest rate went up, so the value of the bond went down. More specifically, the buyer, {buyer}, will demand a return of {str(future_rate)} percent, the current market rate. The future value of the bond is {fm.ac(future_value)}. There are {str(time)} - {str(time_passed)} = {str(time-time_passed)} years left before the payment of {fm.ac(future_value)}. The present value of {fm.ac(future_value)} in {str(time-time_passed)} years at an interest rate of {str(future_rate)} percent is {fm.ac(no_loss)}. The bond has a basis of {fm.ac(future_value)}, so selling it for {fm.ac(no_loss)} results in a loss of {fm.ac(no_loss)} - {fm.ac(future_value)} = -{fm.ac(correct)}."
    }

    possibleanswers = [correct, no_loss, 0, future_value, pmt]

    possibleanswers, judgements = fm.random_answer_ones(possibleanswers, judgements)

    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


def COD_simple():

    person = fm.create_person()

    initial_loan_seed = random.randint(30, 60)

    while True:
        loan = 1000 * initial_loan_seed
        paid_off = 1000 * random.randint(10, 29)
        forgiven = loan - paid_off
        if forgiven == loan - paid_off:
            break

    sold_stuff = random.choice(["equipment", "supplies", "goods", "machinery"])

    sale_year = fm.current_year - random.randint(1, 4)

    forgiver = fm.pick_entity_name()

    forgiven = loan - paid_off

    problem = f"{forgiver}, whose business is manufacturing, sold {sold_stuff} to {person.name} for {fm.ac(loan)} on credit in {sale_year}. {person.name}'s assets far exceed {person.poss} liabilities, but in {fm.current_year}, after {person.name} has paid off {fm.ac(paid_off)} of the debt, {forgiver}, determines that {person.name} will be not pay back the rest of the debt and accordingly cancels the debt. How much income, if any, does this cancellation generate for {person.name}?"

    possibleanswers = [loan, paid_off, forgiven, 0]

    correct = forgiven

    judgements = {
        correct: f"{person.name} has income to the extent of the cancelled debt, that is, the remaining debt after the amount he paid off. {fm.ac(loan)} - {fm.ac(paid_off)} = {fm.ac(forgiven)}. Section 61(a)(11)."
    }

    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


def satisfy_debt():

    # way it is paid back,additional income, additional language for correct answer, additional language for no additional income]
    class SatisfyAnswer:
        def __init__(self, langwaypaid, addlincome, langcorrect, langnoadd):
            self.langwaypaid = langwaypaid
            self.addlincome = addlincome
            self.langcorrect = langcorrect
            self.langnoadd = langnoadd

    person = fm.create_person()

    if person.gender == "nonbinary":
        correcthas = "have"
    else:
        correcthas = "has"

    # when does she borrow
    date_borrow = fm.month_day(fm.pick_random_date())

    # how much does she borrow
    borrowing = random.randint(5, 30) * 1000

    # when does she pay it back
    year_return = fm.current_year + random.randint(2, 7)

    # how much does she pay back? Will always be less than or equal to amount borrowed
    pays_back = random.randint(1, (borrowing / 1000) - 1) * 1000
    basis = pays_back - fm.nearesthundred(random.randint(1, round(0.8 * pays_back)))

    # how does she pay it back?
    cash_paid = SatisfyAnswer(f"paying cash of {fm.ac(pays_back)}", 0, "", "")
    services_performed = SatisfyAnswer(
        f"performing services worth {fm.ac(pays_back)}",
        pays_back,
        f"In addition, {person.nom} {correcthas} compensation income due to using services to satisfy the debt.",
        "What about the provision of services? There should not be an incentive to satisfy debt with services.",
    )
    asset_transferred = SatisfyAnswer(
        f"transferring an asset worth {fm.ac(pays_back)} with a basis of {fm.ac(basis)}",
        pays_back - basis,
        f"In addition, {person.nom} {correcthas} gain due to the disposition of the asset equal to the value of the asset, {fm.ac(pays_back)}, minus its basis, {fm.ac(basis)}, which equals {fm.ac(pays_back-basis)}.",
        "What about the disposition of the asset? There should not be an incentive to satisfy debt with appreciated assets.",
    )

    possible_methods = [cash_paid, services_performed, asset_transferred]
    method = random.choice(possible_methods)

    # total income
    COD_income = borrowing - pays_back
    additional_income = method.addlincome

    # provide possible answers
    correct = COD_income + additional_income
    no_additional_income = COD_income
    extra_additional = correct + random.randint(2, 5) * 1000
    no_income = 0
    randanswer = fm.generate_random_item(correct, 80, 120)

    # ask the question
    problem = f"On {date_borrow}, {fm.current_year}, {person.name} borrows {fm.ac(borrowing)} from the bank. On {date_borrow}, {str(year_return)}, {person.name} is permitted to satisfy the debt by {method.langwaypaid}. How much total income does {person.name} have due to {person.poss} repayment of the debt?"

    possibleanswers = [correct, extra_additional, no_income, randanswer]

    extra_correct = method.langcorrect

    judgements = {
        correct: f"That is correct. {person.name} has cancellation of indebtedness income equal to the difference between the amount {person.nom} owed, {fm.ac(borrowing)}, and the amount {person.nom} paid in full satisfaction of the loan, {fm.ac(pays_back)}--that is, {fm.ac(COD_income)}. {extra_correct}",
        no_income: f"It is true that usually paying back debt does not involve income. But did {person.name} pay back the entire debt?",
        randanswer: "That number was randomly generated. Try again.",
        extra_additional: "That number was randomly generated. Try again.",
    }

    if no_additional_income not in possibleanswers:
        judgements[no_additional_income] = method.langnoadd
        possibleanswers.append(no_additional_income)

    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


# the first type of property as compensation problem - restricted property
def restricted_property(type_problem="random"):
    person = fm.create_person()

    if person.gender == "nonbinary":
        correctdoes = "do"
    else:
        correctdoes = "does"

    # property received
    value_at_grant = random.randint(5, 25)
    number_of_shares = 5 * random.randint(2, 10)
    hiring_date = fm.month_day(fm.pick_random_date())
    employer = random.choice(abc.animals_by_country_dict["English"])

    # vesting
    value_at_vest = value_at_grant + random.randint(1, 10)
    years_until_vest = random.randint(3, 6)
    year_vest = fm.current_year + years_until_vest

    # pick type of restriction
    additional_work = f"{person.nom} {correctdoes} not work for {employer} for {str(years_until_vest)} years"
    increase_value = f"the total earnings of {employer} do not increase each year for {str(years_until_vest)} years"
    restriction = random.choice([additional_work, increase_value])

    while True:
        amount_paid_at_grant = round(random.random() * value_at_grant)
        if amount_paid_at_grant != value_at_grant and amount_paid_at_grant > 0:
            break

    # decide whether the person makes an 83(b) election
    election_83 = random.choice([True, False])

    # forfeit
    if type_problem == "forfeit":
        forfeit = True
    else:
        forfeit = random.choice([True, False])
    while True:
        value_at_forfeit = round((1 + random.random()) * value_at_grant)
        if value_at_forfeit != value_at_grant and value_at_forfeit != value_at_vest:
            break
    years_until_forfeit = random.randint(1, years_until_vest - 1)
    year_forfeit = fm.current_year + years_until_forfeit

    # sale
    value_at_sale = value_at_vest + random.randint(1, 10)
    years_until_sale = random.randint(1, 8)
    year_sale = year_vest + years_until_sale

    # the problems
    intro_lang = f"{person.name} is hired by {employer}, Inc., on {hiring_date}, {str(fm.current_year)}. On {person.poss} first day of work, when the stock trades at {fm.ac(value_at_grant)} per share, {person.name} acquires {str(number_of_shares)} shares of {employer} stock for {fm.ac(amount_paid_at_grant)} per share, as contemplated by {person.poss} employment agreement. The stock is a capital asset in {person.name}'s hands. "

    restriction_lang = f"As part of the terms of {person.poss} employment, if {restriction}, {person.name} must return the stock. Anyone to whom {person.name} transfers the stock is subject to the same restriction. "

    if election_83:
        election_lang = f" {person.name} makes an election under Section 83(b) with respect to the stock. "
    else:
        election_lang = f" {person.name} makes no elections with respect to the stock. "

    if forfeit:
        outcome_lang = f"The vesting requirement imposed is not met as of {str(year_forfeit)}, and {person.name} must forfeit the stock in {str(year_forfeit)}, when the stock is worth {fm.ac(value_at_forfeit)} per share. "
    else:
        outcome_lang = f"When the restriction expires and the stock vests in {str(year_vest)}, it is worth {fm.ac(value_at_vest)}. {person.name} sells the shares in {str(year_sale)}, when the stock is worth {fm.ac(value_at_sale)} per share. "

    problem_facts = intro_lang + restriction_lang + election_lang + outcome_lang

    # possible questions
    question_corp_deduct_grant = f"How much may {employer} deduct per share in {str(fm.current_year)} due to the grant of the shares?\n"
    question_corp_deduct_vest = f"How much may {employer} deduct per share in {str(year_vest)} due to the vesting of the shares?\n"
    question_include_grant = f"How much income must {person.name} include per share in {str(fm.current_year)} due to the grant of the shares?\n"
    question_include_vest = f"How much income must {person.name} include per share in {str(year_vest)} due to the vesting of the shares?\n"
    question_deduct_forfeit = f"How much of a deduction or loss does {person.name} have per share in {str(year_forfeit)} due to the forfeit of the shares?\n"
    question_include_forfeit = f"How much income must {employer} include per share in {str(year_forfeit)} due to the forfeit of the shares?\n"
    question_include_sale = f"How much income must {person.name} include per share in {str(year_sale)} due to the sale of the shares?\n"

    if forfeit:
        addl_questions = [question_include_forfeit, question_deduct_forfeit]
    else:
        addl_questions = [
            question_include_sale,
            question_corp_deduct_vest,
            question_include_vest,
        ]

    possible_questions = [
        question_corp_deduct_grant,
        question_include_grant,
    ] + addl_questions

    if type_problem == "random":
        question_lang = random.choice(possible_questions)
    elif type_problem == "employer":
        if forfeit:
            question_lang = question_corp_deduct_grant
        else:
            question_lang = random.choice(
                [question_corp_deduct_grant, question_corp_deduct_vest]
            )
    elif type_problem == "employee":
        if forfeit:
            question_lang = random.choice(
                [question_include_grant, question_deduct_forfeit]
            )
        else:
            question_lang = random.choice(
                [question_include_grant, question_include_vest, question_include_sale]
            )
    elif type_problem == "forfeit":
        question_lang = random.choice(
            [question_deduct_forfeit, question_include_forfeit]
        )

    value_at_grant_ordinary = f"{fm.ac(value_at_grant)} ordinary deduction"
    value_at_grant_capital = f"{fm.ac(value_at_grant)} capital loss"
    amount_paid_at_grant_ordinary = f"{fm.ac(amount_paid_at_grant)} ordinary deduction"
    amount_paid_at_grant_capital = f"{fm.ac(amount_paid_at_grant)} capital loss"
    value_at_forfeit_ordinary = f"{fm.ac(value_at_forfeit)} ordinary deduction"
    value_at_forfeit_capital = f"{fm.ac(value_at_forfeit)} capital loss"

    if election_83 and forfeit:

        if question_lang == question_deduct_forfeit:
            possibleanswers = [
                f"{fm.ac(0)}",
                value_at_grant_ordinary,
                value_at_grant_capital,
                amount_paid_at_grant_ordinary,
                amount_paid_at_grant_capital,
                value_at_forfeit_ordinary,
                value_at_forfeit_capital,
            ]

        else:
            possibleanswers = [
                0,
                value_at_grant,
                amount_paid_at_grant,
                value_at_grant - amount_paid_at_grant,
                value_at_forfeit,
                value_at_forfeit - amount_paid_at_grant,
                value_at_sale - value_at_vest,
            ]

        if (
            question_lang == question_corp_deduct_grant
            or question_lang == question_include_grant
        ):

            correct = value_at_grant - amount_paid_at_grant
            judgements = {
                correct: '<p>That is correct. Because there was an election under <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(b)</a>, the employee includes, and the employer deducts, the difference between the value at grant and the amount paid at grant.</p>',
                value_at_grant: "What about the amount paid for the property?",
                0: '<p>Remember: there was a <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(b)</a> election.</p>',
            }

        if question_lang == question_deduct_forfeit:

            correct = amount_paid_at_grant_capital
            judgements = {
                correct: f'<p>That is correct. Because {person.name} made an election under <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(b)</a> and the stock is a capital asset in {person.poss} hands, <a href="https://www.law.cornell.edu/cfr/text/26/1.83-2" target="_new" rel="noreferrer">Treas. Reg. 1.83-2(a)</a> permits a capital loss equal to the amount paid for the stock, reduced by the amount {person.nom} received on forfeit. In this case, because {person.nom} received nothing on forfeit, the capital loss equals {fm.ac(amount_paid_at_grant)} per share.</p>',
                amount_paid_at_grant_ordinary: '<p>That is the correct amount, but what is the character? Consider <a href="https://www.law.cornell.edu/cfr/text/26/1.83-2" target="_new" rel="noreferrer">Treas. Reg. 1.83-2(a)</a>.</p>',
                0: '<p>It is true that the statute says no deduction allowed. But consider <a href="https://www.law.cornell.edu/cfr/text/26/1.83-2" target="_new">Treas. Reg. 1.83-2(a)</a>.</p>',
            }
            judgements[value_at_forfeit_ordinary] = judgements[
                value_at_forfeit_capital
            ] = judgements[value_at_grant_capital] = judgements[
                value_at_grant_ordinary
            ] = '<p>Consider <a href="https://www.law.cornell.edu/cfr/text/26/1.83-2" target="_new">Treas. Reg. 1.83-2(a)</a>.</p>'

        if question_lang == question_include_forfeit:
            correct = value_at_grant - amount_paid_at_grant
            judgements = {
                correct: "That is correct. The corporation had the benefit of a deduction, and must unwind that benefit when it gets the property back.",
                value_at_grant: f"What about the amount {person.name} paid for the stock at grant?",
                0: f'<p>Remember: there was a <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(b)</a> election. What did {employer} get to do when the restricted stock was granted?</p>',
            }

    if election_83 and not forfeit:
        possibleanswers = [
            0,
            value_at_grant,
            amount_paid_at_grant,
            value_at_grant - amount_paid_at_grant,
            value_at_vest,
            value_at_sale,
            value_at_vest - amount_paid_at_grant,
            value_at_sale - amount_paid_at_grant,
            value_at_sale - value_at_grant,
            value_at_sale - value_at_vest,
        ]

        if (
            question_lang == question_corp_deduct_grant
            or question_lang == question_include_grant
        ):
            correct = value_at_grant - amount_paid_at_grant
            judgements = {
                correct: '<p>That is correct. Because there was an election under <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(b)</a>, the employee includes, and the employer deducts, the difference between the value at grant and the amount paid at grant.</p>',
                value_at_grant: "What about the amount paid for the property?",
                0: '<p>Remember: there was an election under <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(b)</a>.</p>',
            }

        if (
            question_lang == question_corp_deduct_vest
            or question_lang == question_include_vest
        ):
            correct = 0
            judgements = {
                correct: '<p>That is correct. Because there was an election under <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83</a>, the compensation event occurred at grant, and there is no income for the employee, or associated deduction for the employer, when the property vests.</p>',
                value_at_vest
                - amount_paid_at_grant: '<p>Remember: there was a <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(b)</a> election.</p>',
                value_at_vest: '<p>Remember: there was a <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(b)</a> election. (Also, what about the amount paid at grant for the stock?)</p>',
            }

        if question_lang == question_include_sale:
            correct = value_at_sale - value_at_grant
            judgements = {
                correct: f"That is correct. The amount included in the sale is the gain from the sale of the stock, that is, the difference between the amount received, {fm.ac(value_at_sale)}, and the basis of the stock. The basis of the stock equals the amount paid for the stock--in this case, {fm.ac(amount_paid_at_grant)}--plus the amount previously included in gross income with respect to the stock--in this case, {fm.ac(value_at_grant-amount_paid_at_grant)}.",
                value_at_sale: "What about the basis of the stock?",
                value_at_sale
                - value_at_vest: '<p>What about the election under <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(b)</a>?</p>',
            }

    if (not election_83) and forfeit:
        if question_lang == question_deduct_forfeit:
            possibleanswers = [
                0,
                value_at_grant_ordinary,
                value_at_grant_capital,
                amount_paid_at_grant_ordinary,
                amount_paid_at_grant_capital,
                value_at_forfeit_ordinary,
                value_at_forfeit_capital,
            ]

        else:
            possibleanswers = [
                0,
                value_at_grant,
                amount_paid_at_grant,
                value_at_grant - amount_paid_at_grant,
                value_at_forfeit,
                value_at_forfeit - amount_paid_at_grant,
                value_at_sale - value_at_vest,
            ]

        if question_lang == question_corp_deduct_grant or question_include_grant:

            correct = 0
            judgements = {
                correct: '<p>That is correct. Because there was no election under <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(b)</a>, there is no income for the employee under <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">83(a)</a>, or associated deduction for the employer under <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">83(h)</a>, until the property vests.</p>',
                value_at_grant
                - amount_paid_at_grant: '<p>Remember: there was no <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(b)</a> election. Is the property subject to substantial risk of forfeiture and nontransferable?</p>',
                value_at_grant: '<p>Remember: there was no <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(b)</a> election. Is the property subject to substantial risk of forfeiture and nontransferable? (Also, what about the amount paid at grant for the stock?)</p>',
            }

        if question_lang == question_deduct_forfeit:

            correct = amount_paid_at_grant_ordinary
            judgements = {
                correct: f'<p>That is correct. Because {person.name} made no elections with respect to the stock, <a href="https://www.law.cornell.edu/cfr/text/26/1.83-1" target="_new" rel="noreferrer">Treas. Reg. 1.83-1(b)(2)</a> permits an ordinary deduction for the amount paid for the stock reduced by the amount received on forfeiture. In this case, because {person.name} received nothing on forfeiture, {person.nom} may take an ordinary deduction of {fm.ac(amount_paid_at_grant)} per share.</p>',
                amount_paid_at_grant_capital: '<p>That is the correct amount, but what is the character? Consider <a href="https://www.law.cornell.edu/cfr/text/26/1.83-1" target="_new" rel="noreferrer">Treas. Reg. 1.83-1(b)(2)</a>.</p>',
                0: '<p>It is true that the statute says no deduction allowed. But consider <a href="https://www.law.cornell.edu/cfr/text/26/1.83-1" target="_new">Treas. Reg. 1.83-1(b)(2)</a>.</p>',
            }
            judgements[value_at_forfeit_ordinary] = judgements[
                value_at_forfeit_capital
            ] = judgements[value_at_grant_capital] = judgements[
                value_at_grant_ordinary
            ] = '<p>Consider <a href="https://www.law.cornell.edu/cfr/text/26/1.83-2" target="_new">Treas. Reg. 1.83-1(b)(2)</a>.</p>'

        elif question_lang == question_include_forfeit:
            correct = 0
            judgements = {
                correct: f"That is correct. {employer} has taken no deduction with respect to this transfer, and thus has no income when the stock is returned.",
                amount_paid_at_grant: f"Did {employer} take a deduction with respect to this amount?",
            }

    if not election_83 and not forfeit:
        possibleanswers = [
            0,
            value_at_grant,
            amount_paid_at_grant,
            value_at_grant - amount_paid_at_grant,
            value_at_vest,
            value_at_sale,
            value_at_vest - amount_paid_at_grant,
            value_at_sale - amount_paid_at_grant,
            value_at_sale - value_at_grant,
            value_at_sale - value_at_vest,
        ]

        if (
            question_lang == question_corp_deduct_grant
            or question_lang == question_include_grant
        ):
            correct = 0
            judgements = {
                correct: '<p>That is correct. Because there was no election under <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(b)</a>, there is no income for the employee under <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">83(a)</a>, or associated deduction for the employer under <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">83(h)</a>, until the property vests.</p>',
                value_at_grant
                - amount_paid_at_grant: '<p>Remember: there was no <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(b)</a> election. Is the property subject to substantial risk of forfeiture and nontransferable?</p>',
                value_at_grant: '<p>Remember: there was no <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(b)</a> election. Is the property subject to substantial risk of forfeiture and nontransferable? (Also, what about the amount paid at grant for the stock?)</p>',
            }

        if (
            question_lang == question_corp_deduct_vest
            or question_lang == question_include_vest
        ):
            correct = value_at_vest - amount_paid_at_grant
            judgements = {
                correct: '<p>That is correct. Because there was no <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(b)</a> election, income for the employee under <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">83(a)</a>, and the associated deduction for the employer under <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">83(h)</a>, occur when the property vests.</p>',
                value_at_grant
                - amount_paid_at_grant: '<p>Remember: there was no <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(b)</a> election. Is the property subject to substantial risk of forfeiture and nontransferable?</p>',
                value_at_vest: "What about the amount paid for the stock?",
            }

        if question_lang == question_include_sale:
            correct = value_at_sale - value_at_vest
            judgements = {
                correct: f"That is correct. The amount included in income due to the sale is the gain from the sale of the stock, that is, the difference between the amount received {fm.ac(value_at_sale)} and the basis of the stock. The basis of the stock equals the amount paid for the stock--in this case, {fm.ac(amount_paid_at_grant)}--plus the amount previously included in gross income with respect to the stock--in this case, {fm.ac(value_at_vest-amount_paid_at_grant)}.",
                value_at_sale
                - value_at_grant: '<p>Remember: there was no <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(b)</a> election.</p>',
                value_at_vest: "What about the amount paid for the stock?",
            }

    problem = problem_facts + question_lang

    if question_lang == question_deduct_forfeit:
        kindformat = "words"
    else:
        kindformat = "cash"

    formattedjudgements = fm.format_dict(judgements, formatting=kindformat)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers, kindofformatting=kindformat)
    return [problem, cleananswers, judgements_json, correct]


# second type of property as comp problem--options as comp
def options_as_comp():

    person = fm.create_person()

    # underlying shares received
    value_at_grant = random.randint(5, 25)
    strike_price = value_at_grant
    number_of_shares = 5 * random.randint(2, 10)
    hiring_date = fm.month_day(fm.pick_random_date())
    employer = random.choice(abc.animals_by_country_dict["English"])

    # decide whether option has FMV and value of option
    readily_asc_FMV = random.choice(["yes", "no"])

    numbers_list = [value_at_grant * number_of_shares, strike_price * number_of_shares]

    while True:
        value_of_option = number_of_shares * random.randint(3, 10)
        if value_of_option not in numbers_list:
            break

    # exercise
    value_at_exercise = value_at_grant + random.randint(1, 10)
    exercise_date = fm.month_day(fm.pick_random_date())
    years_until_exercise = random.randint(3, 6)
    exercise_year = fm.current_year + years_until_exercise

    # sale
    value_at_sale = value_at_exercise + random.randint(1, 10)
    years_until_sale = random.randint(1, 8)
    year_sale = exercise_year + years_until_sale

    # possible questions

    question_corp_deduct_grant = f"  How much may {employer} deduct in {str(fm.current_year)} due to the grant of the option?\n"
    question_corp_deduct_exercise = f"  How much may {employer} deduct in {str(exercise_year)} due to the exercise of the option?\n"
    question_include_grant = f"  How much income does {person.name} include due to the grant of the option?\n"
    question_include_exercise = f"  How much income does {person.name} include in {str(exercise_year)} due to the exercise of the option?\n"
    question_include_sale = f"  How much income does {person.name} include in {str(year_sale)} due to the sale of the shares?\n"

    # three kinds of options: FMV at grant, no FMV at grant, ISOs

    # FMV at grant: tax consequences to

    intro_lang = f"{person.name}, an employee of {employer}, Inc., receives from {employer} on {hiring_date}, {str(fm.current_year)}, an unrestricted, nonforfeitable option to purchase {str(number_of_shares)} shares of {employer} stock for {fm.ac(strike_price)} a share."

    if readily_asc_FMV == "yes":
        value_lang = f" The option is publicly traded and has a fair market value of {fm.ac(value_of_option)}."
    if readily_asc_FMV == "no":
        value_lang = f" The option is not publicly traded and does not have a readily ascertainable fair market value."

    exercise_lang = f" On {exercise_date}, {str(exercise_year)}, {person.name} exercises the option when the stock is worth {fm.ac(value_at_exercise)} a share. In {str(year_sale)}, {person.name} sells the stock for {fm.ac(value_at_sale)} a share. The option is not an incentive stock option (ISO)."

    problem_facts = intro_lang + value_lang + exercise_lang

    # possibleanswers_per_share = [0,value_at_grant,value_at_exercise,value_at_exercise-strike_price,value_at_sale,value_at_sale-strike_price,value_at_sale-value_at_grant]
    possibleanswers = [
        0,
        value_at_grant * number_of_shares,
        value_at_exercise * number_of_shares,
        (value_at_exercise - strike_price) * number_of_shares,
        value_at_sale * number_of_shares,
        (value_at_sale - strike_price) * number_of_shares,
        (value_at_sale - value_at_exercise) * number_of_shares,
        (value_at_sale - value_at_grant) * number_of_shares,
        value_of_option,
        (value_at_sale - strike_price) * number_of_shares - value_of_option,
    ]

    FMV_nonzero = [question_corp_deduct_grant, question_include_grant]
    no_FMV_nonzero = [
        question_corp_deduct_exercise,
        question_include_exercise,
        question_include_sale,
    ]
    possible_FMV_types = (FMV_nonzero, no_FMV_nonzero)

    if readily_asc_FMV == "yes":
        question_lang_pre = random.choices(possible_FMV_types, weights=[70, 30])

    else:
        question_lang_pre = random.choices(possible_FMV_types, weights=[30, 70])

    question_lang_list = question_lang_pre

    question_lang = random.choice(question_lang_list[0])

    problem = problem_facts + question_lang

    # first, no readily ascertainable FMV

    if readily_asc_FMV == "no":

        if (
            question_lang == question_corp_deduct_grant
            or question_lang == question_include_grant
        ):
            correct = 0
            judgements = {
                correct: f'<p>That is correct. Because the option does not have a readily ascertainable fair market value, there is no income for the employee, or associated deduction for the employer, until the option is exercised, under <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(e)(3)</a>.</p>',
                value_at_grant
                * number_of_shares: "Remember: this is an option. Additionally, the option itself has no readily ascertainable fair market value.",
            }

        if (
            question_lang == question_corp_deduct_exercise
            or question_lang == question_include_exercise
        ):
            correct = (value_at_exercise - strike_price) * number_of_shares
            judgements = {
                correct: f'<p>That is correct. Because there was no readily ascertainable fair market value, income for the employee, and the associated deduction for the employer, occur when the option is exercised, under <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(e)(3)</a>. The value at that time equals the difference between the total value received, that is, the value of the shares, {fm.ac(value_at_exercise)}, minus the strike price, {fm.ac(strike_price)}, times the number of shares.</p>',
                0: "Remember: this option did not have a readily ascertainable fair market value at grant.",
                value_at_exercise
                * number_of_shares: "What about the amount paid for the stock?",
            }

        if question_lang == question_include_sale:
            correct = (value_at_sale - value_at_exercise) * number_of_shares
            judgements = {
                correct: "That is correct. The amount included in the sale is the gain from the sale of the stock, that is, the difference between the amount received ("
                + fm.ac(value_at_sale)
                + ") and the basis of the stock. The basis of the stock equals the amount paid for the stock (in this case, "
                + fm.ac(strike_price)
                + ") plus the amount previously included in gross income with respect to the stock (in this case, "
                + fm.ac(value_at_exercise - strike_price)
                + ") times the number of shares.",
                (value_at_sale - strike_price)
                * number_of_shares: "This assumes the basis at sale was equal to the amount paid for the stock. What about the amount included in income when the option was exercised?",
            }

    if readily_asc_FMV == "yes":

        if (
            question_lang == question_corp_deduct_grant
            or question_lang == question_include_grant
        ):
            correct = value_of_option
            judgements = {
                correct: "That is correct. Because the option has a readily ascertainable fair market value, there is income for the employee, and the associated deduction for the employer, when the option is granted. It is just like receiving any other property as compensation.",
                0: "This option has a readily ascertainable fair market value.",
                value_at_grant * number_of_shares: "Remember: this is an option.",
            }

        if (
            question_lang == question_corp_deduct_exercise
            or question_lang == question_include_exercise
        ):
            correct = 0
            judgements = {
                correct: f'<p>That is correct. Because there was a readily ascertainable fair market value, the compensation event occurred at grant, and there is no income at exercise, under under <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(e)(4)</a>.</p>',
                (value_at_exercise - strike_price)
                * number_of_shares: f'<p>Remember: this option had a readily ascertainable fair market value at grant. Consider <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(e)(4)</a>.</p>',
                value_at_exercise
                * number_of_shares: f'<p>This option had a readily ascertainable fair market value at grant. Consider <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(e)(4)</a>. (Plus, what about the amount paid for the stock?)</p>',
            }

        if question_lang == question_include_sale:
            correct = (
                value_at_sale - strike_price
            ) * number_of_shares - value_of_option
            judgements = {
                correct: f"That is correct. The amount included in the sale is the gain from the sale of the stock, that is, the difference between the amount received ({fm.ac(value_at_sale)}) times the number of shares) and the basis of the stock. The basis of the stock equals the amount paid for the stock (in this case, {fm.ac(strike_price)} times the number of shares) plus the the amount previously included in gross income with respect to the option (in this case, {fm.ac(value_of_option)}.",
                (value_at_sale - strike_price)
                * number_of_shares: "This assumes the basis at sale was equal to the amount paid for the stock. What about the amount included in income when the option was received?",
            }

    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


# third type of property as comp problem--unrestricted property
def unrestricted_property():

    person = fm.create_person()

    value_at_grant = random.randint(5, 25)
    number_of_shares = 5 * random.randint(2, 10)
    hiring_date = fm.month_day(fm.pick_random_date())
    employer = random.choice(abc.animals_by_country_dict["English"])

    # does the person pay for the stock?
    while True:
        amount_paid_at_grant = round(random.random() * value_at_grant)
        if amount_paid_at_grant != value_at_grant and amount_paid_at_grant != 0:
            break

    # sale
    value_at_sale = value_at_grant + random.randint(1, 10)
    years_until_sale = random.randint(2, 8)
    year_sale = fm.current_year + years_until_sale

    problem_facts = f"{person.name} begins work at {employer}, Inc., on {hiring_date}, {str(fm.current_year)}. On {person.poss} first day of work, when the stock trades at {fm.ac(value_at_grant)} per share, {person.name} receives {str(number_of_shares)} shares of {employer} stock from {employer} and pays {fm.ac(amount_paid_at_grant)} per share, as contemplated by the employment agreement. In {str(year_sale)}, {person.name} sells the stock for {fm.ac(value_at_sale)} a share."

    # possible questions
    question_corp_deduct_grant = f"  How much may {employer} deduct per share in {str(fm.current_year)} due to the grant of the shares?\n"
    question_include_grant = f"  How much income must {person.name} include per share in {str(fm.current_year)} due to the grant of the shares?\n"
    question_include_sale = f"  How much income must {person.name} include per share in {str(year_sale)} due to the sale of the shares?\n"

    possible_questions = [
        question_corp_deduct_grant,
        question_include_grant,
        question_include_sale,
    ]

    question_lang = random.choice(possible_questions)

    possibleanswers = [
        0,
        value_at_grant,
        value_at_sale,
        value_at_grant - amount_paid_at_grant,
        amount_paid_at_grant,
        value_at_sale - amount_paid_at_grant,
        value_at_sale - value_at_grant,
    ]

    if (
        question_lang == question_corp_deduct_grant
        or question_lang == question_include_grant
    ):
        correct = value_at_grant - amount_paid_at_grant
        judgements = {
            correct: "That is correct. Because the stock is unrestricted, the employee includes, and the employer deducts, the difference between the value at grant and the amount paid at grant.",
            value_at_grant: "What about the amount paid for the property?",
            0: "Remember: this is unrestricted stock.",
        }

    if question_lang == question_include_sale:
        correct = value_at_sale - value_at_grant

        judgements = {
            correct: f'<p>That is correct. The amount included due to the sale is the gain from the sale of the stock, that is, the difference between the amount received, {fm.ac(value_at_sale)}, and the basis of the stock, as required by <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(a)</a>. The basis of the stock equals the amount paid for the stock, in this case, {fm.ac(amount_paid_at_grant)}, plus the amount previously included in gross income with respect to the stock, in this case, {fm.ac(value_at_grant-amount_paid_at_grant)}.</p>',
            value_at_sale: "What about the basis of the stock?",
            value_at_sale
            - amount_paid_at_grant: "What about the amount included in income when the stock was granted?",
        }

    problem = problem_facts + question_lang

    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


def principal_res():

    # basic facts
    [person1, person2] = fm.create_group()

    class PrincResChoices:
        def __init__(
            self,
            maritalstatus,
            introlang,
            nompro,
            genpro,
            verbbuyname,
            verbbuypron,
            verbmovename,
            verbmovepron,
            threshold,
            verbsellname,
            verbsellpron,
            verbrent,
        ):
            self.maritalstatus = maritalstatus
            self.introlang = introlang
            self.nompro = nompro
            self.genpro = genpro
            self.verbbuyname = verbbuyname
            self.verbbuypron = verbbuypron
            self.verbmovename = verbmovename
            self.verbmovepron = verbmovepron
            self.threshold = threshold
            self.verbsellname = verbsellname
            self.verbsellpron = verbsellpron
            self.verbrent = verbrent

    type_of_problem = random.choices(
        ["move_standard", "use_own_issue", "nonqualified_use"], weights=[2, 2, 1]
    )[0]

    married = PrincResChoices(
        "married",
        f"{person1.name} and {person2.name} are married and file jointly.",
        "they",
        "their",
        "buy",
        "buy",
        "move",
        "move",
        fm.married.section_121_threshold,
        "sell",
        "sell",
        "rent",
    )

    if person1.gender == "nonbinary":
        single = PrincResChoices(
            "single",
            f"{person1.name} is single and files as a single person.",
            person1.nom,
            person1.poss,
            "buys",
            "buy",
            "moves",
            "move",
            fm.single.section_121_threshold,
            "sells",
            "sell",
            "rent",
        )
    else:
        single = PrincResChoices(
            "single",
            f"{person1.name} is single and files as a single person.",
            person1.nom,
            person1.poss,
            "buys",
            "buys",
            "moves",
            "moves",
            fm.single.section_121_threshold,
            "sells",
            "sells",
            "rents",
        )

    if type_of_problem == "move_standard":
        status = random.choice([married, single])
    else:
        status = single

    residence = random.choice(["house", "apartment"])

    purchase_price = 50000 * random.randint(4, 20)

    if status == single:
        gain_on_sale = 25000 * random.randint(11, 20)
    else:
        gain_on_sale = 25000 * random.randint(20, 30)

    sale_price = purchase_price + gain_on_sale

    # problem_date_number = fm.pick_random_date_this_year()
    # purchase_date = fm.full_date(problem_date_number)
    purchase_date = fm.pick_random_date_this_year()

    move_valid = [
        "to a new city because of a new job",
        "to a new residence due to health reasons",
    ]
    move_invalid = ["to a new residence that is preferable", "to a smaller residence"]

    move_reason = random.choice(random.choice([move_valid, move_invalid]))

    right_threshold = status.threshold
    if status == married:
        wrong_threshold = fm.single.section_121_threshold
    else:
        wrong_threshold = fm.married.section_121_threshold

    no_gain = 0
    full_gain = sale_price - purchase_price

    no_basis_recovery = sale_price
    exclude_right_threshold = max(0, full_gain - right_threshold)
    exclude_wrong_threshold = max(0, full_gain - wrong_threshold)

    #    define the three types of questions you could ask

    if type_of_problem == "move_standard":
        move_date = fm.date_after(purchase_date, soonest=800, latest=1500)

    else:
        move_date = fm.date_after(purchase_date, soonest=300, latest=(365 * 2) - 25)

    length_time = (move_date - purchase_date).days

    # first type
    # standard question - testing threshold only

    if type_of_problem == "move_standard":

        problem = f"{status.introlang} On {fm.full_date(purchase_date)}, {status.nompro} {status.verbbuypron} {fm.pick_a_an(residence)} {residence} for {fm.ac(purchase_price)} and {status.verbmovepron} in that same day. The {residence} serves as {status.genpro} principal residence until {fm.full_date(move_date)}, at which point {status.nompro} {status.verbmovepron} {move_reason} and {status.verbsellpron} the {residence} for {fm.ac(sale_price)}. That is, {status.nompro} lived in the {residence} for {length_time} days, at which time {status.nompro} sold the {residence}. How much gain is included in gross income due to the sale?"

        possibleanswers = [
            full_gain,
            no_basis_recovery,
            exclude_wrong_threshold,
            exclude_right_threshold,
            no_gain,
        ]

        excluded_amount = right_threshold

        correct = exclude_right_threshold

        judgements = {
            exclude_right_threshold: f'<p>Correct. The amount of gain is {fm.ac(full_gain)}, but some of that gain is excluded from gross income by the exclusion permitted under <a href="https://www.law.cornell.edu/uscode/text/26/121" target="_new" rel="noreferrer">Section 121</a>--in this case, because the relevant marital status is {status.maritalstatus}, {fm.ac(right_threshold)}. Therefore the taxpayer includes {fm.ac(full_gain)} less {fm.ac(right_threshold)}, which equals {fm.ac(exclude_right_threshold)}.</p>',
            no_basis_recovery: "What about the basis? Also, can any of the gain be excluded for any reason?",
            full_gain: "That is the amount of gain, but can any of the gain be excluded for any reason?",
        }

        if exclude_right_threshold != exclude_wrong_threshold:

            judgements[exclude_wrong_threshold] = (
                '<p>What is the correct limitation for the exclusion under <a href="https://www.law.cornell.edu/uscode/text/26/121" target="_new" rel="noreferrer">Section 121(b)</a>? Consider the taxpayer status.</p>'
            )

    # second type
    # some period of unqualified use in the previous five years - testing two-year requirement and reason for move
    elif type_of_problem == "use_own_issue":

        problem = f"{status.introlang} On {fm.full_date(purchase_date)}, {status.nompro} {status.verbbuypron} {fm.pick_a_an(residence)} {residence} for {fm.ac(purchase_price)} and {status.verbmovepron} in that same day. The {residence} serves as {status.genpro} principal residence until {fm.full_date(move_date)}, at which point {status.nompro} {status.verbmovepron} {move_reason} and {status.verbsellpron} the {residence} for {fm.ac(sale_price)}. That is, {status.nompro} lived in the {residence} for {length_time} days, at which time {status.nompro} sold the {residence}. How much gain is included in gross income due to the sale?"

        possibleanswers = [
            full_gain,
            no_basis_recovery,
            exclude_wrong_threshold,
            exclude_right_threshold,
            no_gain,
        ]

        excluded_amount = int(right_threshold * length_time / (365 * 2))
        wrong_excluded_amount = int(wrong_threshold * length_time / (365 * 2))
        proportionate_exclude = int(max(0, full_gain - excluded_amount))
        proportionate_exclude_wrong_threshold = int(
            max(0, full_gain - wrong_excluded_amount)
        )

        possibleanswers.append(proportionate_exclude)

        if proportionate_exclude != proportionate_exclude_wrong_threshold:

            possibleanswers.append(proportionate_exclude_wrong_threshold)

        if move_reason in move_valid:

            correct = proportionate_exclude

            judgements = {
                proportionate_exclude: f'<p>Correct. The taxpayer did not live in the residence for the full two years required by <a href="https://www.law.cornell.edu/uscode/text/26/121" target="_new" rel="noreferrer">Section 121(a)</a>, but the reason for the move is contemplated in <a href="https://www.law.cornell.edu/uscode/text/26/121" target="_new" rel="noreferrer">Section 121(c)</a>. The taxpayer lived in the property for {length_time} days, so the taxpayer can exclude a proportionate amount, {length_time}/730, of {fm.ac(right_threshold)}, as described in <a href="https://www.law.cornell.edu/cfr/text/26/1.121-3" target="_new" rel="noreferrer">Treas Reg. 1.121-3(g)</a>. Therefore the taxpayer includes {fm.ac(full_gain)} less {fm.ac(excluded_amount)}, which equals {fm.ac(proportionate_exclude)}.</p>',
                proportionate_exclude_wrong_threshold: "This is the right idea, given the reason for the move, but what is the correct full amount to reduce proportionately?",
                exclude_right_threshold: '<p>Is the full <a href="https://www.law.cornell.edu/uscode/text/26/121" target="_new" rel="noreferrer">Section 121(b)</a> amount permitted to be excluded here?</p>',
                no_basis_recovery: "What about the basis? Also, can any of the gain be excluded for any reason?",
                exclude_wrong_threshold: '<p>What is the correct limitation for the exclusion under <a href="https://www.law.cornell.edu/uscode/text/26/121" target="_new" rel="noreferrer">Section 121(b)</a>? Consider the taxpayer status. Also, is that full correct amount excluded?</p>',
                full_gain: "That is the amount of gain, but can any of the gain be excluded for any reason?",
            }

        else:

            correct = full_gain

            judgements = {
                proportionate_exclude: '<p>What was the cause of the move? Is it contemplated in <a href="https://www.law.cornell.edu/uscode/text/26/121" target="_new" rel="noreferrer">Section 121(c)</a>?</p>',
                proportionate_exclude_wrong_threshold: '<p>What was the cause of the move? Is it contemplated in <a href="https://www.law.cornell.edu/uscode/text/26/121" target="_new" rel="noreferrer">Section 121(c)</a>? Also, even if it were contemplated in Section 121(c), what would be the right amount to reduce proportionately?</p>',
                exclude_right_threshold: '<p>Are all the requirements of <a href="https://www.law.cornell.edu/uscode/text/26/121" target="_new" rel="noreferrer">Section 121</a> met?</p>',
                no_basis_recovery: "What about the basis?",
                exclude_wrong_threshold: '<p>Are all the requirements of <a href="https://www.law.cornell.edu/uscode/text/26/121" target="_new" rel="noreferrer">Section 121</a> met? Also, if they are, what is the correct limitation for the exclusion under Section <a href="https://www.law.cornell.edu/uscode/text/26/121" target="_new" rel="noreferrer">Section 121(b)</a>? Consider the taxpayer status.</p>',
                full_gain: f'<p>Correct. The taxpayer did not live in the residence for sufficient time, and the reason for the move was not a reason contemplated by <a href="https://www.law.cornell.edu/uscode/text/26/121" target="_new" rel="noreferrer">Section 121(c)</a>. Therefore the taxpayer must include the full gain of {fm.ac(full_gain)}.</p>',
            }

    # third type - some period of unqualified use - testing apportioning gain from sale between qualified and unqualified use
    elif type_of_problem == "nonqualified_use":

        total_years_unqualified = random.randint(6, fm.current_year - 2010)
        time_live_in_house = random.randint(2, total_years_unqualified - 1)
        unqualified_years = total_years_unqualified - time_live_in_house
        purchase_year_unqualified = fm.current_year - total_years_unqualified
        move_in_year = purchase_year_unqualified + unqualified_years

        percent_unqualified = unqualified_years / total_years_unqualified
        percent_qualified = (
            total_years_unqualified - unqualified_years
        ) / total_years_unqualified

        must_include_gain = int(full_gain * percent_unqualified)
        potential_exclude = int(full_gain * percent_qualified)
        actually_exclude = min(potential_exclude, right_threshold)

        not_excluded = potential_exclude - actually_exclude
        include_total = must_include_gain + not_excluded

        no_unqualified_use_wrong_answer = max(0, full_gain - right_threshold)
        possibleanswers = [include_total, no_gain, full_gain]

        correct = include_total

        problem = f"{status.introlang} On {fm.month_day(purchase_date)}, {purchase_year_unqualified}, {status.nompro} {status.verbbuypron} {fm.pick_a_an(residence)} {residence}. Until {fm.month_day(purchase_date)}, {move_in_year}, {status.nompro} {status.verbrent} out the {residence}. On {fm.month_day(purchase_date)}, {move_in_year}, {status.nompro} {status.verbmovepron} into the {residence}, and the {residence} serves as {status.genpro} principal residence until {fm.month_day(purchase_date)}, {fm.current_year}, at which point {status.nompro} {status.verbsellpron} the {residence} for {fm.ac(sale_price)}. The basis at the time of the sale was {fm.ac(purchase_price)}. How much gain is included in gross income due to the sale?"

        if unqualified_years == 1:
            year_word = "year"
        else:
            year_word = "years"

        correct_explanation = f'<p>Correct. The total time {status.nompro} owned the house is {total_years_unqualified} years. The {unqualified_years} {year_word} for which {status.nompro} {status.verbrent} out the house is a period of nonqualified use, because a period of nonqualified use means any period, other than any portion preceding January 1, 2009, during which the property is not used as the principal residence of the taxpayer or the taxpayer’s spouse or former spouse. <a href="https://www.law.cornell.edu/uscode/text/26/121" target="_new" rel="noreferrer">Section 121(b)(5)(C)(i)</a>. Therefore, {unqualified_years}/{total_years_unqualified} of the gain cannot be excluded under Section 121(a). The total gain on sale is {fm.ac(sale_price)} - {fm.ac(purchase_price)} = {fm.ac(full_gain)}. {unqualified_years}/{total_years_unqualified} x {fm.ac(full_gain)} = {fm.ac(must_include_gain)} is attributable to the unqualified use and must be included. Of the remaining {fm.ac(potential_exclude)}, {fm.ac(actually_exclude)} can be excluded, because the relevant limitation under Section 121(b) is {fm.ac(right_threshold)}. Therefore, {fm.ac(potential_exclude)} - {fm.ac(actually_exclude)} = {fm.ac(not_excluded)} of the portion allocated to qualified use must be included, and the total included is {fm.ac(include_total)}.</p>'

        judgements = {
            include_total: correct_explanation,
            no_gain: '<p>Consider <a href="https://www.law.cornell.edu/uscode/text/26/121" target="_new" rel="noreferrer">Section 121(b)</a>. Was the property always used as a principal residence?</p>',
            full_gain: "Was the property ever used as a principal residence?",
        }

        if include_total != no_unqualified_use_wrong_answer:
            possibleanswers.append(no_unqualified_use_wrong_answer)
            judgements[no_unqualified_use_wrong_answer] = (
                '<p>Consider <a href="https://www.law.cornell.edu/uscode/text/26/121" target="_new" rel="noreferrer">Section 121(b)</a>. Was the property always used as a principal residence?</p>',
            )

        if include_total != must_include_gain:
            possibleanswers.append(must_include_gain)
            judgements[must_include_gain] = (
                "It is correct that all of the gain from nonqualified use must be included. Is there any other gain that must be included? Consider the general limitation on exclusion in Section 121(b)."
            )

    while len(possibleanswers) < 6:
        (possibleanswers, judgements) = fm.random_answer(possibleanswers, judgements)

    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


def exclusion_COD():

    person = fm.create_person()

    forgive_date = fm.month_day(fm.pick_random_date())

    addsub = random.choices([0, 1], weights=[0.2, 0.8])

    loan = 1000 * random.randint(10, 50)
    additional_liabilities = 1000 * random.randint(10, 50)
    total_liabilities = loan + additional_liabilities

    while True:
        end_year_excess = fm.nearestthousand(loan * random.random())
        if end_year_excess != loan:
            break

    while True:
        total_assets = total_liabilities + ((-1) ** addsub[0]) * fm.nearestthousand(
            random.random() * total_liabilities
        )
        if (
            total_assets != total_liabilities
            and total_liabilities - total_assets != 0.5 * loan
            and loan != total_liabilities - total_assets
        ):
            break

    problem = f"{person.name} has a loan of {fm.ac(loan)}. The loan is cancelled on {forgive_date}. {person.name} has {fm.ac(total_liabilities)} of liabilities and {fm.ac(total_assets)} of assets immediately prior to the cancellation of the loan. At the end of the year, due to fluctuations in the value of {person.poss} assets and variability in lending, {person.poss} liabilities exceed {person.poss} assets by {fm.ac(end_year_excess)}. How much is included in {person.poss} gross income due to the cancellation of the loan?"

    judgements = {
        end_year_excess: '<p>What is the relevant time to measure liabilities and assets to determine the amount of the <a href="https://www.law.cornell.edu/uscode/text/26/108" target="_new" rel="noreferrer">Section 108</a> insolvency exception?</p>'
    }

    # add answer where you the additional liabilities in excess give you the wrong answer. maybe have to change amount of additional liabilities in excess.

    possibleanswers = [0, end_year_excess, loan]

    if total_liabilities > total_assets:
        possibleanswers.append(total_liabilities - total_assets)

    if loan - (total_liabilities - total_assets) > 0:
        possibleanswers.append(loan - (total_liabilities - total_assets))

    # not insolvent
    if total_assets > total_liabilities:
        correct = loan
        judgements[correct] = (
            f'<p>That is correct. Cancellation of indebtedness is income. <a href="https://www.law.cornell.edu/uscode/text/26/108" target="_new" rel="noreferrer">Section 108</a> provides an exception to the extent liabilities are in excess of assets, but here, assets are in excess of liabilities.</p>'
        )
        judgements[0] = (
            '<p>Under <a href="https://www.law.cornell.edu/uscode/text/26/61" target="_new" rel="noreferrer">Section 61(a)(11)</a>, COD is income unless an explicit statutory exclusion applies. Given that assets exceed liabilities here, does an exclusion apply?</p>'
        )

    # insolvent, and to more than the extent of the loan
    elif total_liabilities - total_assets > loan:
        correct = 0
        judgements[correct] = (
            '<p>That is correct. Cancellation of indebtedness is generally income, but <a href="https://www.law.cornell.edu/uscode/text/26/108" target="_new" rel="noreferrer">Section 108</a> provides an exception to the extent liabilities are in excess of assets immediately prior to the loan cancellation.</p>'
        )
        judgements[loan] = (
            '<p>Generally COD is included in gross income, but <a href="https://www.law.cornell.edu/uscode/text/26/108" target="_new" rel="noreferrer">Section 108</a> provides exceptions. What exception applies here?</p>'
        )

    # insolvent, and less than the amount of the loan
    else:
        correct = loan - (total_liabilities - total_assets)
        judgements[correct] = (
            f'<p>That is correct. <a href="https://www.law.cornell.edu/uscode/text/26/108" target="_new" rel="noreferrer">Section 108</a> provides an exception to the general rule of inclusion, but only to the extent that the liabilities exceed the assets immediately prior to the loan cancellation. Here, liabilities exceed assets immediately prior to the loan cancellation by {fm.ac(total_liabilities)} - {fm.ac(total_assets)} = {fm.ac(total_liabilities-total_assets)}, so that amount is excluded from gross income, and {fm.ac(correct)} is included.</p>'
        )
        judgements[0] = (
            '<p><a href="https://www.law.cornell.edu/uscode/text/26/108" target="_new" rel="noreferrer">Section 108</a> provides an exception to the general rule of inclusion, but only to the extent that the liabilities exceed the assets.</p>'
        )
        judgements[loan] = (
            '<p>The general rule is that COD is included in income, but consider the exceptions in <a href="https://www.law.cornell.edu/uscode/text/26/108" target="_new" rel="noreferrer">Section 108</a>.</p>'
        )
        judgements[total_liabilities - total_assets] = (
            "This is the amount that is *excluded*, but what amount is included?"
        )

    (possibleanswers, judgements) = fm.random_answer_pot(possibleanswers, judgements, 3)

    while True:
        if len(possibleanswers) < 7:
            (possibleanswers, judgements) = fm.random_answer_pot(
                possibleanswers, judgements, 3
            )
        else:
            break

    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


def qual_empl_disc():

    person = fm.create_person()
    employer = random.choice(abc.animals_by_country_dict["English"])

    benefit_dict = {
        "property": ["books", "clothing", "hardware"],
        "services": ["house cleaning", "website design", "haircuts"],
    }

    benefit = random.choice(["property", "services"])

    type_store = random.choice(benefit_dict[benefit])

    type_job = random.choice(
        ["provide marketing and publicity with respect to", "sell"]
    )

    purchase_fmv = random.randint(5, 30) * 50
    while True:
        purchase_cost = fm.generate_random_item_hund(purchase_fmv, 40, 90)
        if purchase_cost != 0.5 * purchase_fmv and purchase_cost < purchase_fmv:
            break
    gross_income_no_exclude = purchase_fmv - purchase_cost

    while True:
        gross_profit_percentage = random.randint(2, 7) * 5

        if benefit == "services":
            gpp_lang = ""
            relevant_percent = 20
            relevant_percent_lang = "20 percent"
        else:
            gpp_lang = f"The gross profit percentage of the {type_store} that {person.name} purchased, as defined in Section 132(c)(2), is {gross_profit_percentage} percent."
            relevant_percent = gross_profit_percentage
            relevant_percent_lang = (
                f"the gross profit percentage, which equals {relevant_percent} percent"
            )
        statutory_cap = int(relevant_percent * purchase_fmv / 100)
        exclude_amount = min(statutory_cap, gross_income_no_exclude)
        total_include = gross_income_no_exclude - exclude_amount
        if exclude_amount != total_include:
            break

    if gross_income_no_exclude > statutory_cap:
        exclude_amount = statutory_cap
        exclude_lang = "in excess of"
        limit_lang = f"limited to {fm.ac(statutory_cap)}"
    else:
        exclude_amount = gross_income_no_exclude
        exclude_lang = "not in excess of"
        limit_lang = "the full amount that would otherwise be included"

    problem = f"{person.name} is an employee of {employer}, Inc. {employer} sells {type_store} to customers in the ordinary course of the line of business, and {person.name}'s job is to {type_job} {type_store}. As part of {person.poss} compensation, {person.name} is permitted to buy {type_store} at a discount. In {fm.current_year}, {person.name} buys {fm.ac(purchase_fmv)} of {type_store} for {fm.ac(purchase_cost)}. {gpp_lang} How much must {person.name} include in {person.poss} gross income due to these purchases?"

    correct_explain = f"Correct! Absent any exception, {person.name} would include {fm.ac(purchase_fmv)} - {fm.ac(purchase_cost)} = {fm.ac(gross_income_no_exclude)}. Under Section 132(c), {person.name} can exclude that value to the extent that it does not exceed {relevant_percent_lang} of the price at which the {type_store} is offered to customers. {relevant_percent} percent of {fm.ac(purchase_fmv)} is {fm.ac(statutory_cap)}. The amount that would be included in gross income is {exclude_lang} this statutory limit, so the amount excluded is {limit_lang}. The amount included is therefore {fm.ac(gross_income_no_exclude)} - {fm.ac(exclude_amount)} = {fm.ac(total_include)}."

    correct = total_include

    possibleanswers = [
        total_include,
        gross_income_no_exclude,
        purchase_fmv,
        exclude_amount,
        0,
    ]

    if correct == 0:
        zero_explain = correct_explain
    else:
        zero_explain = '<p>Consider the limitation in <a href="https://www.law.cornell.edu/uscode/text/26/132" target="_new" rel="noreferrer">Section 132(c)(1)</a>.</p>'

    judgements = {
        correct: correct_explain,
        gross_income_no_exclude: '<p>This would be the amount of gross income if there were no statutory exclusion. But consider <a href="https://www.law.cornell.edu/uscode/text/26/132" target="_new" rel="noreferrer">Section 132(c)</a>.</p>',
        purchase_fmv: f'<p>Consider <a href="https://www.law.cornell.edu/uscode/text/26/83" target="_new" rel="noreferrer">Section 83(a)</a>. How much did {person.name} pay for the {type_store}? Additionally, are there any provisions that would permit any exclusion? Consider <a href="https://www.law.cornell.edu/uscode/text/26/132" target="_new" rel="noreferrer">Section 132(c)</a>.</p>',
        exclude_amount: "This is the amount excluded. The problem asks about the amount included.",
        0: zero_explain,
    }

    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


def gift():
    [person1, person2] = fm.create_group()

    value_at_gift = 1000 * random.randint(5, 30)

    numbers_list = [value_at_gift]

    def add_unique():
        while True:
            x = fm.generate_random_item(value_at_gift, 55, 150)
            if x not in numbers_list:
                numbers_list.append(x)
                return x

    basis_at_gift = add_unique()

    gain_loss = value_at_gift - basis_at_gift

    property_list = [
        "car",
        "luxury watch",
        "rare book",
        "rare coin",
        "fancy item of clothing",
    ]

    relationship = random.choice(["close friend", "family member"])

    property_1 = random.choice(property_list)

    deduction_question = f"How much of a deduction is {person1.name} permitted to take due to this transaction?"

    income_question = f"How much must {person2.name} include in gross income under Section 61 due to this transaction?"

    question = random.choice([income_question, deduction_question])

    facts = f"{person1.name} gives {person2.name} a {property_1} worth {fm.ac(value_at_gift)}. {person1.name} chooses to do this because {person1.name} is {person2.name}'s {relationship}, and {person1.name} feels generous toward {person2.name}. {person1.name} expects nothing in return."

    possibleanswers = [value_at_gift, basis_at_gift, 0, gain_loss]

    problem = f"{facts} {question}"

    correct = 0

    income_dict = {
        correct: f"Correct. {person2.name} includes nothing in gross income from this transaction. {person1.name} gave the {property_1} out of detached and disinterested generosity. It was therefore a gift, and gifts are excluded from gross income under Section 102."
    }

    deduction_dict = {
        correct: f"Correct. {person1.name} is not allowed a deduction for this transfer. {person1.name} gave the {property_1} out of detached and disinterested generosity, and it was therefore a gift, but no deduction is allowed for gifts to individuals."
    }

    if question == deduction_question:
        judgements = deduction_dict
    elif question == income_question:
        judgements = income_dict

    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


def charitable_donation(type_problem="random"):
    person1 = fm.create_person()

    if type_problem == "random":

        type_donation_list = random.choices(["services", "property"], weights=(1, 2))
        type_donation = type_donation_list[0]

    else:
        type_donation = type_problem

    type_gain = random.choice(
        ["long-term capital gain", "short-term capital gain", "ordinary income"]
    )

    itemizes = random.choice([True, False])

    if itemizes:
        itemizes_word = "itemizes"
        value_property = 100 * random.randint(50, 300)
    else:
        itemizes_word = "does not itemize"
        stded = fm.single.standard_deduction
        value_property = fm.generate_random_item_hund(stded, 30, 80)

    numbers_list = [value_property]

    def add_unique():
        while True:
            x = fm.generate_random_item_hund(value_property, 30, 80)
            if x not in numbers_list:
                numbers_list.append(x)
                return x

    basis_property = add_unique()

    gain = value_property - basis_property

    if gain < 0:
        gainword = "loss"
    else:
        gainword = "gain"

    gain_sentence_true = "It is accurate that contribution of property to a charity is not a realization event."

    gain_question = "Is contribution of property to a charity a realization event?"

    if type_donation == "services":

        problem = f"{person1.name} donates services to a 501(c)(3) organization. If {person1.name} had charged market price for the services, {person1.nom} would have charged {fm.ac(value_property)}, but instead the organization pays {person1.acc} nothing. {person1.name} {itemizes_word} {person1.poss} deductions. How much income, if any, must {person1.name} include in {person1.poss} gross income due to the donation of services, and how much of a deduction, if any, may {person1.name} take due to the donation? (Disregard any limitations that may apply under Section 170(b).)"

        income_question = "Is it necessary to include income when donating services in return for no compensation?"

        correct = "No income, no deduction"
        income_sentence_true = "It is accurate that no income need be included when services are donated in exchange for no compensation."
        services_sentence = 'It is accurate that no deduction is available for the donation of services, under <a href="https://www.law.cornell.edu/cfr/text/26/1.170A-1" target="_new" rel="noreferrer">Treas Reg. 1.170A-1(g)</a>.'
        services_question = 'Is any deduction available for the donation of services? Consider <a href="https://www.law.cornell.edu/cfr/text/26/1.170A-1" target="_new" rel="noreferrer">Treas Reg. 1.170A-1(g)</a>.'

        correct_explanation = (
            f"<p>Correct. {income_sentence_true} {services_sentence}</p>"
        )

        judgements = {
            correct: correct_explanation,
            f"No income, {fm.ac(value_property)} deduction": f"<p>{income_sentence_true} {services_question}</p>",
            f"{fm.ac(value_property)} income, no deduction": f"<p>{income_question} {services_sentence}</p>",
            f"{fm.ac(value_property)} income, {fm.ac(value_property)} deduction": f"<p>{income_question} {services_question}</p>",
        }

    else:

        problem = f"{person1.name} donates a piece of property worth {fm.ac(value_property)} to a 501(c)(3) organization. The basis of the property is {fm.ac(basis_property)}. If {person1.name} had sold the property, {person1.nom} would have recognized {type_gain}. {person1.name} {itemizes_word} {person1.poss} deductions. How much gain, if any, must {person1.name} recognize due to the donation, and how much of a deduction, if any, may {person1.name} take due to the donation? (Disregard any limitations that may apply under Section 170(b).)"

        if not itemizes:
            correct = "No gain, no deduction"

            itemize_question = "Is the deduction for charitable donations an above-the-line or below-the-line deduction?"

            itemize_sentence = "It is accurate that the deduction for charitable donations is available only to itemizers."

            correct_explanation = f"Correct. {gain_sentence_true} {itemize_sentence}"

            judgements = {
                "No gain, no deduction": correct_explanation,
                f"No gain, {fm.ac(basis_property)} deduction": f"{gain_sentence_true} {itemize_question}",
                f"No gain, {fm.ac(value_property)} deduction": f"{gain_sentence_true} {itemize_question}",
                f"{fm.ac(abs(gain))} {gainword}, no deduction": f"{gain_question} {itemize_sentence}",
                f"{fm.ac(abs(gain))} {gainword}, {fm.ac(basis_property)} deduction": f"{gain_question} {itemize_question}",
                f"{fm.ac(abs(gain))} {gainword}, {fm.ac(value_property)} deduction": f"{gain_question} {itemize_question}",
            }

        else:

            # amount_question = 'Consider the amount of the deduction for the donation of property that generates {type_gain} under <a href="https://www.law.cornell.edu/cfr/text/26/1.170A-1" target="_new" rel="noreferrer">Treas Reg. 1.170A-1(c)</a>.'

            no_deduction_question = 'With respect to the availability of a deduction, consider <a href="https://www.law.cornell.edu/uscode/text/26/170" target="_new" rel="noreferrer">Section 170(a)</a>.'

            # deduction_accurate = 'That is the correct amount of deduction under <a href="https://www.law.cornell.edu/cfr/text/26/1.170A-1" target="_new" rel="noreferrer">Treas Reg. 1.170A-1(c)</a>.'

            if type_gain == "long-term capital gain":
                correct_filler = f"{fm.ac(value_property)}"
                wrong_filler = f"{fm.ac(basis_property)}"
                cite = '<a href="https://www.law.cornell.edu/cfr/text/26/1.170A-1" target="_new" rel="noreferrer">Treas Reg. 1.170A-1(c)</a>'
                correct_amount_sentence_amount = "fair market value"

            else:
                wrong_filler = f"{fm.ac(value_property)}"
                correct_filler = f"{fm.ac(basis_property)}"
                cite = '<a href="https://www.law.cornell.edu/uscode/text/26/170" target="_new" rel="noreferrer">Section 170(e)</a>'
                correct_amount_sentence_amount = "basis"

            type_property_question = f"What is the amount of deduction available for property that generates {type_gain} when sold? Consider {cite}."
            correct = f"No gain, {correct_filler} deduction"
            correct_amount_sentence = f"It is accurate for property that would generate {type_gain} if sold, the deduction is the {correct_amount_sentence_amount} of the property, under {cite}."
            correct_explanation = (
                f"<p>Correct. {gain_sentence_true} {correct_amount_sentence}</p>"
            )

            judgements = {
                correct: correct_explanation,
                "No gain, no deduction": f"<p>{gain_sentence_true} {no_deduction_question}</p>",
                f"No gain, {wrong_filler} deduction": f"<p>{gain_sentence_true} {type_property_question}</p>",
                f"{fm.ac(abs(gain))} {gainword}, no deduction": f"<p>{gain_question} {no_deduction_question}</p>",
                f"{fm.ac(abs(gain))} {gainword}, {correct_filler} deduction": f"<p>{gain_question} {correct_amount_sentence}</p>",
                f"{fm.ac(abs(gain))} {gainword}, {wrong_filler} deduction": f"<p>{gain_question} {type_property_question}</p>",
            }

    possibleanswers = list(judgements.keys())

    formattedjudgements = fm.format_dict(judgements, formatting="words")
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers, kindofformatting="words")
    return [problem, cleananswers, judgements_json, correct]


def qri():
    [person1, person2] = fm.create_group()

    class QRIChoices:
        def __init__(
            self,
            introlang,
            nompro,
            genpro,
            buyproper,
            buypronoun,
            financeproper,
            financepronoun,
            itemizeproper,
            itemizepronoun,
        ):
            self.introlang = introlang
            self.nompro = nompro
            self.genpro = genpro
            self.buyproper = buyproper
            self.buypronoun = buypronoun
            self.financeproper = financeproper
            self.financepronoun = financepronoun
            self.itemizeproper = itemizeproper
            self.itemizepronoun = itemizepronoun

    married = QRIChoices(
        f"{person1.name} and {person2.name} are married and file jointly.",
        "they",
        "their",
        "buy",
        "buy",
        "finance",
        "finance",
        "itemize",
        "itemize",
    )

    if person1.gender == "nonbinary":
        single = QRIChoices(
            f"{person1.name} is single and files as a single person.",
            person1.nom,
            person1.poss,
            "buys",
            "buy",
            "finances",
            "finance",
            "itemizes",
            "itemize",
        )
    else:
        single = QRIChoices(
            f"{person1.name} is single and files as a single person.",
            person1.nom,
            person1.poss,
            "buys",
            "buy",
            "finances",
            "finances",
            "itemizes",
            "itemizes",
        )

    status = random.choice([married, single])

    while True:
        purchase_price = 10000 * random.randint(80, 190)
        if purchase_price != 750000:
            break

    while True:
        mortgage_amount = int(
            fm.nearestthousand((random.randint(50, 90) / 100) * purchase_price)
        )
        if mortgage_amount != 750000 and mortgage_amount != 1000000:
            break

    down_payment = purchase_price - mortgage_amount
    interest_rate = random.randint(3, 10)

    annual_interest = int((interest_rate / 100) * mortgage_amount)
    annual_interest_limit = int((interest_rate / 100) * fm.qri_limit)
    annual_interest_old_limit = int((interest_rate / 100) * fm.old_qri_limit)

    annual_interest_full_amount = int((interest_rate / 100) * purchase_price)

    problem = f"{status.introlang} {status.nompro.capitalize()} {status.buypronoun} a house which is used as {status.genpro} principal residence for {fm.ac(purchase_price)}, which {status.nompro} {status.financepronoun} with a mortgage of {fm.ac(mortgage_amount)}, secured by the house, and a cash down payment of {fm.ac(down_payment)}. The mortgage has an interest rate of {interest_rate} percent annually, with a balloon payment at the end (not how mortgages are structured, but play along). {status.nompro.capitalize()} {status.itemizepronoun} {status.genpro} deductions. How much interest, if any, is permitted to be deducted each year due to the interest payments?"

    judgements = {
        mortgage_amount: "The interest is what is deductible, not the principal amount.",
        fm.qri_limit: "The interest is what is deductible, not the amount of acquisition indebtedness.",
        annual_interest_old_limit: "What is the current limitation for the amount that can be considered acquisition indebtedness?",
    }

    if mortgage_amount > fm.qri_limit:
        judgements[annual_interest] = (
            "That is the annual interest, but what about the limitation on acquisition indebtedness?"
        )
        judgements[annual_interest_limit] = (
            f"Correct! Only the interest with respect to {fm.ac(fm.qri_limit)} is permitted to be deducted."
        )

        correct = annual_interest_limit

    else:
        judgements[annual_interest] = (
            f"Correct! The interest with respect to up to {fm.ac(fm.qri_limit)} of acquisition indebtedness is permitted to be deducted, and the amount of the mortgage does not exceed {fm.ac(fm.qri_limit)}."
        )
        judgements[annual_interest_limit] = (
            "That is the interest amount times the annual limit for acquisition indebtedness, but what is the actual principal of the loan?"
        )

        correct = annual_interest

    possibleanswers = [
        fm.qri_limit,
        purchase_price,
        mortgage_amount,
        down_payment,
        annual_interest,
        annual_interest_limit,
        annual_interest_old_limit,
        annual_interest_full_amount,
    ]

    (possibleanswers, judgements) = fm.random_answer_pot(possibleanswers, judgements, 1)

    number_of_small_random = random.randint(0, 3)

    small_random_list = []
    for n in range(number_of_small_random):
        next_answer = fm.generate_random_item(correct, start=10, end=90)
        small_random_list.append(next_answer)

    for item in small_random_list:
        if item not in possibleanswers:
            possibleanswers.append(item)
            judgements[item] = "This answer was randomly generated."

    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


def property_exchange():
    [person1, person2] = fm.create_group()

    value_on_trade = 1000 * random.randint(5, 30)

    numbers_list = [value_on_trade]

    def add_unique():
        while True:
            x = fm.generate_random_item(value_on_trade, 50, 150)
            if x not in numbers_list:
                numbers_list.append(x)
                return x

    property_2_purchase_price = add_unique()
    property_1_purchase_price = add_unique()

    property_list = [
        "car",
        "luxury watch",
        "rare book",
        "rare coin",
        "fancy item of clothing",
    ]

    property_1 = random.choice(property_list)

    while True:
        property_2 = random.choice(property_list)
        if property_2 != property_1:
            break

    class ExchangePerson:
        def __init__(
            self,
            name,
            property_exchanged,
            property_received,
            basis_exchanged_property,
            gain_loss,
        ):
            self.name = name
            self.property_exchanged = property_exchanged
            self.property_received = property_received
            self.basis_exchanged_property = basis_exchanged_property
            self.gain_loss = gain_loss

    person_1_gain = value_on_trade - property_1_purchase_price
    person_2_gain = value_on_trade - property_2_purchase_price

    first_person = ExchangePerson(
        person1.name, property_1, property_2, property_1_purchase_price, person_1_gain
    )
    second_person = ExchangePerson(
        person2.name, property_2, property_1, property_2_purchase_price, person_2_gain
    )

    picked = random.choice([first_person, second_person])

    possibleanswers = numbers_list
    gain_list = [person_1_gain, person_2_gain]

    for x in gain_list:
        if x not in numbers_list:
            numbers_list.append(x)

    if picked.gain_loss > 0:
        gainword = "gain"
    else:
        gainword = "loss"

    correct = value_on_trade

    problem = f"{person1.name} gives {person2.name} a {property_1} worth {fm.ac(value_on_trade)}. {person1.name} paid {fm.ac(property_1_purchase_price)} for the {property_1}, and the basis in the {property_1} has not changed since this purchase. In exchange, {person2.name} gives {person1.name} a {property_2}. The fair market value of the {property_2} is also {fm.ac(value_on_trade)}. {person2.name} bought the {property_2} for {fm.ac(property_2_purchase_price)}, and the basis in the {property_2} has not changed since this purchase. What is {picked.name}'s basis in the {picked.property_received} immediately after the exchange?"

    judgements = {
        correct: f"Correct. {picked.name} has a fair market value basis in the {picked.property_received}. Another way to see the same answer: {picked.name} had a {fm.ac(picked.basis_exchanged_property)} basis in the {picked.property_exchanged}, and recognized a {fm.ac(abs(picked.gain_loss))} {gainword} on the exchange for the {picked.property_received}, so the basis in the {picked.property_received} is {fm.ac(picked.basis_exchanged_property)} + {fm.ac(picked.gain_loss)} = {fm.ac(value_on_trade)}."
    }

    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


def gift_basis(asset_value, transferor_basis, later_sale_price, transferor, transferee):

    transferor_gain = 0
    relationship = random.choice(["family members, but not spouses", "good friends"])

    if transferor_basis > asset_value and later_sale_price < asset_value:
        recipient_basis = asset_value

    else:
        recipient_basis = transferor_basis

    if (
        transferor_basis > asset_value
        and later_sale_price > asset_value
        and later_sale_price < transferor_basis
    ):
        recipient_gain = 0

    else:
        recipient_gain = later_sale_price - recipient_basis

    specific_prob = f" {transferor} gives the property to {transferee}. {transferor} and {transferee} are {relationship}."

    return (transferor_gain, recipient_basis, recipient_gain, specific_prob)


def part_gift(
    asset_value,
    transferor_basis,
    transferor_sale_price,
    later_sale_price,
    transferor,
    transferee,
):

    transferor_gain = max(0, transferor_sale_price - transferor_basis)

    relationship = random.choice(["family members, but not spouses", "good friends"])

    if asset_value > transferor_basis:
        recipient_basis = max(transferor_basis, transferor_sale_price)
        recipient_gain = later_sale_price - recipient_basis

    # 1.1015-4(a) here -- “For determining loss, the unadjusted basis of the property in the hands of the transferee shall not be greater than the fair market value of the property at the time of such transfer." This is relevant only when amount paid < fair market value < adjusted basis.

    elif asset_value < transferor_basis:

        # and now do the regular dual basis analysis.
        if later_sale_price > transferor_basis:
            recipient_basis = transferor_basis
            recipient_gain = later_sale_price - recipient_basis

        elif later_sale_price < asset_value:
            recipient_basis = asset_value
            recipient_gain = later_sale_price - recipient_basis

        elif later_sale_price < transferor_basis and later_sale_price > asset_value:
            recipient_basis = transferor_basis
            recipient_gain = 0

    specific_prob = f" {transferor} sells the property to {transferee} for {fm.ac(transferor_sale_price)}. {transferor} and {transferee} are {relationship}."

    return (transferor_gain, recipient_basis, recipient_gain, specific_prob)


def part_donation(
    asset_value,
    transferor_basis,
    transferor_sale_price,
    later_sale_price,
    transferor,
    transferee,
):

    transferor_sale_basis = int(
        round(transferor_basis * (transferor_sale_price / asset_value))
    )

    transferor_gain = transferor_sale_price - transferor_sale_basis

    recipient_basis = transferor_sale_price + (transferor_basis - transferor_sale_basis)

    recipient_gain = later_sale_price - recipient_basis

    specific_prob = f" {transferor} sells the property to an organization that is tax-exempt under Section 501(c)(3) for {fm.ac(transferor_sale_price)}."

    return (transferor_gain, recipient_basis, recipient_gain, specific_prob)


def death_basis(asset_value, later_sale_price, transferor, transferee):

    transferor_gain = 0
    recipient_basis = asset_value

    recipient_gain = later_sale_price - recipient_basis

    specific_prob = f" {transferor} dies and leaves the property to {transferee}."

    return (transferor_gain, recipient_basis, recipient_gain, specific_prob)


def spouse_basis(
    asset_value, transferor_basis, later_sale_price, transferor, transferee
):

    transferor_gain = 0
    recipient_basis = transferor_basis

    recipient_gain = later_sale_price - recipient_basis

    specific_prob = f" {transferor} and {transferee} are divorcing each other. {transferor} gives the property to {transferee} incident to that divorce."

    return (transferor_gain, recipient_basis, recipient_gain, specific_prob)


def basis_problems(type_problem="random"):
    [person1, person2] = fm.create_group()

    asset_value = 1000 * random.randint(20, 50)

    numbers_list = [asset_value]

    while True:
        transferor_basis = fm.generate_random_item(asset_value, 70, 110)
        if abs(transferor_basis - asset_value) > 1000:
            numbers_list.append(transferor_basis)
            break

    while True:
        transferor_sale_price = fm.generate_random_item(asset_value, 50, 90)
        if transferor_sale_price not in numbers_list:
            numbers_list.append(transferor_sale_price)
            break

    while True:
        later_sale_price = fm.generate_random_item(asset_value)
        if later_sale_price not in numbers_list:
            numbers_list.append(later_sale_price)
            break

    gain_to_transferor_proportionate_basis = transferor_sale_price - int(
        round(transferor_basis * (transferor_sale_price / asset_value))
    )
    gain_to_transferor_basis_first = max(0, transferor_sale_price - transferor_basis)
    no_gain_to_transferor = 0

    # possble basis to transferor
    recipient_basis_fmv = asset_value
    recipient_basis_transferred = transferor_basis
    recipient_basis_first = max(transferor_sale_price, transferor_basis)
    recipient_proportionate_basis = transferor_sale_price + (
        transferor_basis
        - int(round(transferor_basis * (transferor_sale_price / asset_value)))
    )
    random_recipient_proportionate_basis = fm.generate_random_item(
        recipient_proportionate_basis
    )

    no_gain_to_recipient = 0
    fully_taxable_transfer = asset_value - transferor_basis

    possible_answers_gain_to_transferor = [
        gain_to_transferor_proportionate_basis,
        gain_to_transferor_basis_first,
        no_gain_to_transferor,
        fully_taxable_transfer,
    ]

    possible_answers_later_gain_to_recipient = [
        no_gain_to_recipient,
        later_sale_price - recipient_basis_fmv,
        later_sale_price - recipient_basis_transferred,
        later_sale_price - recipient_basis_first,
        later_sale_price - recipient_proportionate_basis,
        later_sale_price - random_recipient_proportionate_basis,
        later_sale_price - transferor_sale_price,
    ]

    transferor_gain_q = f" How much gain or loss does {person1.name} recognize due to {person1.poss} transfer of the property to {person2.name}?"
    recipient_gain_q = f" How much gain or loss does {person2.name} recognize due to {person2.poss} sale of the property for {fm.ac(later_sale_price)}?"

    possible_questions = [transferor_gain_q, recipient_gain_q]

    prob_part_one = f"{person1.name} owns property that is worth {fm.ac(asset_value)}, with a basis of {fm.ac(transferor_basis)}."

    judgements = {
        later_sale_price
        - random_recipient_proportionate_basis: "This number was randomly generated.",
        fully_taxable_transfer: "Was this a sale for full fair market value?",
    }

    if type_problem == "random":
        if transferor_basis > asset_value:
            type_problem = random.choice(["part gift", "gift", "death", "spouse"])
        else:
            type_problem = random.choice(
                ["part donation", "part gift", "gift", "death", "spouse"]
            )

    # set question: if part donation, ask only about the initial transferor. Otherwise, ask about either first or second transfer.
    if type_problem == "part donation":
        prob_part_two = ""
        question_lang = f" How much gain or loss does {person1.name} recognize due to {person1.poss} transfer of the property to the 501(c)(3) organization?"

    else:
        prob_part_two = f" Several years later, {person2.name} sells the property for {fm.ac(later_sale_price)}."
        if type_problem == "deathquiz":
            question_lang = recipient_gain_q
        else:
            question_lang = random.choice(possible_questions)

    # set up questions and judgements
    if type_problem == "gift":
        [transferor_gain, recipient_basis, recipient_gain, specific_prob] = gift_basis(
            asset_value, transferor_basis, later_sale_price, person1.name, person2.name
        )

        if question_lang == transferor_gain_q:

            judgements[transferor_gain] = (
                "Correct! The donor recognizes no gain in a pure gift situation."
            )
            judgements[fully_taxable_transfer] = (
                "Does a donor recognize gain in a pure gift situation?"
            )

        if question_lang == recipient_gain_q:

            if transferor_basis > asset_value:

                if later_sale_price > transferor_basis:

                    judgements[recipient_gain] = (
                        f'<p>Correct! Because the value at the initial transfer was less than the basis, the dual basis rule applies as described in <a href="https://www.law.cornell.edu/uscode/text/26/1015" target="_new" rel="noreferrer">Section 1015(a)</a>. Here, however, the ultimate sale price was greater than the basis in the hands of the transferor, so the recipient uses the transferred basis. {person2.name} therefore recognizes {fm.ac(later_sale_price)} - {fm.ac(recipient_basis)} = {fm.ac(recipient_gain)}.</p>'
                    )

                elif later_sale_price < asset_value:

                    judgements[recipient_gain] = (
                        f'<p>Correct! Because the value at the initial transfer was less than the basis, the dual basis rule applies as described in <a href="https://www.law.cornell.edu/uscode/text/26/1015" target="_new" rel="noreferrer">Section 1015(a)</a>. Because the ultimate sale price was less than the value of the asset at the time of transfer, the recipient must use that value as the basis for determining loss. {person2.name} therefore recognizes {fm.ac(later_sale_price)} - {fm.ac(recipient_basis)} = {fm.ac(recipient_gain)}.</p>'
                    )

                else:

                    judgements[recipient_gain] = (
                        '<p>Correct! Because the value at the initial transfer was less than the basis, the dual basis rule applies as described in <a href="https://www.law.cornell.edu/uscode/text/26/1015" target="_new" rel="noreferrer">Section 1015(a)</a>. Here, the ultimate sale price was greater than the value of the asset at the time of transfer, but less than the basis to the transferor, so the recipient has neither gain nor loss on the subsequent sale.</p>'
                    )

            else:

                judgements[recipient_gain] = (
                    f"Correct! Because the basis at the initial transfer was not greater than the fair market value at the time of transfer, the recipient takes a transferred basis from the donor. {person2.name} therefore recognizes {fm.ac(later_sale_price)} - {fm.ac(recipient_basis)} = {fm.ac(recipient_gain)}."
                )

    elif type_problem == "part gift":
        [transferor_gain, recipient_basis, recipient_gain, specific_prob] = part_gift(
            asset_value,
            transferor_basis,
            transferor_sale_price,
            later_sale_price,
            person1.name,
            person2.name,
        )

        if question_lang == transferor_gain_q:

            if transferor_gain == 0:

                judgements[transferor_gain] = (
                    '<p>Correct! The donor recognizes gain only to the extent the value of the sold portion exceeds the basis of the property under <a href="https://www.law.cornell.edu/cfr/text/26/1.1001-1" target="_new" rel="noreferrer">Section 1.1001-1(e)</a> and does not recognize loss. Essentially, the donor recovers basis first. Here, the basis exceeds the sale price, so the transferor recognizes no gain.</p>'
                )
                judgements[gain_to_transferor_proportionate_basis] = (
                    '<p>How is basis recovered on a part gift / part sale? Compare the basis recovery for property that is transferred through part donation / part sale, as described in <a href="https://www.law.cornell.edu/uscode/text/26/1011" target="_new" rel="noreferrer">Section 1011(b)</a>.</p>'
                )

            else:

                judgements[transferor_gain] = (
                    '<p>Correct! The donor recognizes gain only to the extent the value of the sold portion exceeds the basis of the property under <a href="https://www.law.cornell.edu/cfr/text/26/1.1001-1" target="_new" rel="noreferrer">Section 1.1001-1(e)</a>. Essentially, the donor recovers basis first.</p>'
                )

                judgements[gain_to_transferor_proportionate_basis] = (
                    '<p>How is basis recovered on a part gift / part sale? Compare the basis recovery for property that is transferred through part donation / part sale, as described in <a href="https://www.law.cornell.edu/uscode/text/26/1011" target="_new" rel="noreferrer">Section 1011(b)</a>.</p>'
                )
                judgements[no_gain_to_transferor] = (
                    "If this were a pure gift, there would be no gain to the transferor. But there is some compensation transferred here."
                )

        if question_lang == recipient_gain_q:

            judgements[later_sale_price - recipient_proportionate_basis] = (
                "How is basis recovered for the original transferor--basis first, or basis proportionate? And how does that affect the basis to the recipient?"
            )

            # if dual basis rule is implicated
            if asset_value < transferor_basis and transferor_sale_price < asset_value:

                if (
                    later_sale_price < transferor_basis
                    and later_sale_price > asset_value
                ):

                    judgements[recipient_gain] = (
                        '<p>Correct! Under <a href="https://www.law.cornell.edu/cfr/text/26/1.1015-4" target="_new" rel="noreferrer">Section 1.1015-4(a)</a>, in a part gift/part sale transaction the basis to the recipient is usually the greater of (a) the amount the recipient paid for the property, or (b) the basis of the transferor in the property, but for determining loss, the basis of the property in the recipient cannot exceed the fair market value of the property at the time the property was transferred to the recipient. Here, the later sale price was less than the basis of the transferor and greater than the fair market value at transfer, so {person2.name} recognizes neither gain nor loss.</p>'
                    )

                elif later_sale_price > recipient_basis:

                    judgements[recipient_gain] = (
                        f'<p>Correct! Under <a href="https://www.law.cornell.edu/cfr/text/26/1.1015-4" target="_new" rel="noreferrer">Section 1.1015-4(a)</a>, in a part gift/part sale transaction the basis to the recipient is the greater of (a) the amount the recipient paid for the property, or (b) the basis of the transferor in the property. The dual basis rule could have been relevant, because the fair market value at the part gift/part sale was less than the basis, but because the recipient ultimately sold the property for more than its basis to the recipient at the time of the part gift/part sale,the dual basis rule had no effect. {person2.name} therefore recognizes {fm.ac(later_sale_price)} - {fm.ac(recipient_basis)} = {fm.ac(recipient_gain)}.</p>'
                    )

                else:

                    judgements[recipient_gain] = (
                        f'<p>Correct! Under <a href="https://www.law.cornell.edu/cfr/text/26/1.1015-4" target="_new" rel="noreferrer">Section 1.1015-4(a)</a>, in a part gift/part sale transaction the basis to the recipient is usually the greater of (a) the amount the recipient paid for the property, or (b) the basis of the transferor in the property, but for determining loss, the basis of the property in the recipient cannot exceed the fair market value of the property at the time the property was transferred to the recipient. {person2.name} therefore recognizes {fm.ac(later_sale_price)} - {fm.ac(recipient_basis)} = {fm.ac(recipient_gain)}.</p>'
                    )

            else:  # if dual basis rule is not triggered
                judgements[recipient_gain] = (
                    f'<p>Correct! Under <a href="https://www.law.cornell.edu/cfr/text/26/1.1015-4" target="_new" rel="noreferrer">Section 1.1015-4(a)</a>, the basis to the recipient is the greater of (a) the amount the recipient paid for the property, or (b) the basis of the transferor in the property. {person2.name} therefore recognizes {fm.ac(later_sale_price)} - {fm.ac(recipient_basis)} = {fm.ac(recipient_gain)}.</p>'
                )

    elif type_problem == "part donation":
        [transferor_gain, recipient_basis, recipient_gain, specific_prob] = (
            part_donation(
                asset_value,
                transferor_basis,
                transferor_sale_price,
                later_sale_price,
                person1.name,
                person2.name,
            )
        )

        judgements[transferor_gain] = (
            '<p>Correct! Under <a href="https://www.law.cornell.edu/uscode/text/26/1011" target="_new" rel="noreferrer">Section 1011(b)</a> the donor recovers basis proportionately.</p>'
        )
        judgements[gain_to_transferor_basis_first] = (
            '<p>How is basis recovered on a part donation / part sale? Consider <a href="https://www.law.cornell.edu/uscode/text/26/1011" target="_new" rel="noreferrer">Section 1011(b)</a>. Compare the basis recovery for property that is transferred through part gift / part sale.</p>'
        )

        if gain_to_transferor_basis_first == 0:

            judgements[no_gain_to_transferor] = (
                '<p>If this were a pure donation, the transferor would recognize no gain or loss. But the tax-exempt organization does transfer some compensation. Also, is basis recovered on a part donation / part sale? Consider <a href="https://www.law.cornell.edu/uscode/text/26/1011" target="_new" rel="noreferrer">Section 1011(b)</a>. Compare the basis recovery for property that is transferred through part gift / part sale.</p>'
            )

        else:

            judgements[no_gain_to_transferor] = (
                "If this were a pure donation, the transferor would recognize no gain or loss. But the tax-exempt organization does transfer some compensation."
            )

    elif type_problem == "death" or type_problem == "deathquiz":
        [transferor_gain, recipient_basis, recipient_gain, specific_prob] = death_basis(
            asset_value, later_sale_price, person1.name, person2.name
        )

        if question_lang == transferor_gain_q:
            judgements[transferor_gain] = (
                "Correct! The transferor recognizes no gain in a transfer at death."
            )

        if question_lang == recipient_gain_q:
            judgements[recipient_gain] = (
                f'<p>Correct! Under <a href="https://www.law.cornell.edu/uscode/text/26/1014" target="_new" rel="noreferrer">Section 1014(a)</a>, the basis of the asset is set to the fair market value at the time of death. Therefore {person2.name} recognizes {fm.ac(later_sale_price)} - {fm.ac(asset_value)} = {fm.ac(recipient_gain)} on the subsequent sale.</p>'
            )
            judgements[later_sale_price - recipient_basis_transferred] = (
                '<p>What happens to the basis of an asset that is transferred due to death? Consider <a href="https://www.law.cornell.edu/uscode/text/26/1014" target="_new" rel="noreferrer">Section 1014(a)</a>.</p>'
            )

    elif type_problem == "spouse":
        [transferor_gain, recipient_basis, recipient_gain, specific_prob] = (
            spouse_basis(
                asset_value,
                transferor_basis,
                later_sale_price,
                person1.name,
                person2.name,
            )
        )

        if question_lang == transferor_gain_q:
            judgements[transferor_gain] = (
                "Correct! There is no gain or loss on the gift of property between spouses."
            )

        if question_lang == recipient_gain_q:
            if asset_value < transferor_basis and later_sale_price < transferor_basis:
                judgements[recipient_gain] = (
                    f"Correct! The basis of the property is always transferred between spouses, even if the fair market value of the asset at transfer is less than the basis and thus the dual basis rule would apply in a gift situation between people who are not spouses. {person2.name} therefore recognizes {fm.ac(later_sale_price)} - {fm.ac(recipient_basis)} = {fm.ac(recipient_gain)}."
                )
            else:
                judgements[recipient_gain] = (
                    f"Correct! The basis of the property is always transferred between spouses. {person2.name} therefore recognizes {fm.ac(later_sale_price)} - {fm.ac(recipient_basis)} = {fm.ac(recipient_gain)}."
                )

    if question_lang == recipient_gain_q:
        correct = recipient_gain
        possibleanswers = possible_answers_later_gain_to_recipient

    else:
        correct = transferor_gain
        possibleanswers = possible_answers_gain_to_transferor

    problem_facts = prob_part_one + specific_prob + prob_part_two

    problem = problem_facts + question_lang

    while len(possibleanswers) < 5:
        (possibleanswers, judgements) = fm.random_answer_pot(
            possibleanswers, judgements, 3, 40, 140
        )

    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


def liabilities():

    while True:
        person1 = fm.create_person()
        n = len(person1.name)
        if n < 5:
            break

    while True:
        person2 = fm.create_person()
        n = len(person2.name)
        if n < 5:
            break

    debt_type = random.choice(
        [
            ["nonrecourse", "takes the building subject to the debt"],
            ["recourse", "assumes the debt"],
        ]
    )

    building_fmv = int(10000 * random.randint(20, 200))
    debt = int(fm.fraction_of_thou(building_fmv, 80, 120))
    cash_paid = max(0, building_fmv - debt)
    if cash_paid == 0:
        cash_paid_lang = ""
    else:
        cash_paid_lang = (
            f" {person2.name} also pays {person1.name} {fm.ac(cash_paid)} in cash."
        )

    while True:
        building_basis = fm.fraction_of_thou(building_fmv, 80, 120)
        if building_basis != debt:
            break

    gain_realized_recourse_numb = int(building_fmv - building_basis)

    gain_realized_nonrecourse_numb = int((debt + cash_paid) - building_basis)

    problem_part_1 = f"{person1.name} owns a building with a fair market value of {fm.ac(building_fmv)} and a basis of {fm.ac(building_basis)}. The building is encumbered with {fm.ac(debt)} of {debt_type[0]} debt. {person1.name} sells the building to {person2.name}, who {debt_type[1]}. The debt is legitimate debt, and both parties enter into the transaction for legitimate business reasons."

    question_lang = " Which of the following statements is the most accurate?"

    gain_realized_nonrecourse = f"{person1.name} realizes {fm.ac(abs(gain_realized_nonrecourse_numb))} of {fm.gainword(gain_realized_nonrecourse_numb)} from the building sale."
    gain_realized_recourse = f"{person1.name} realizes {fm.ac(abs(gain_realized_recourse_numb))} of {fm.gainword(gain_realized_recourse_numb)} from the building sale and has {fm.ac(debt - building_fmv)} cancellation of indebtedness income."
    gain_realized_cash_only = f"{person1.name} realizes {fm.ac(abs(cash_paid - building_basis))} of {fm.gainword(cash_paid-building_basis)} from the building sale."
    all_cod = f"{person2.name} {debt_type[1]}, so {person1.name} has {fm.ac(debt)} cancellation of indebtedness income."

    possibleanswers_uni = [gain_realized_nonrecourse, gain_realized_cash_only, all_cod]
    judgements = {
        gain_realized_cash_only: "What is included in amount realized?",
        all_cod: '<p>Consider <a href="https://www.law.cornell.edu/cfr/text/26/1.1001-2" target="_new" rel="noreferrer">Treas. Reg. 1.1001-2(a)(1)</a>.</p>',
    }

    if debt > building_fmv:  # debt is in excess of fair market value

        possibleanswers_addl = [gain_realized_recourse]

        if debt_type[0] == "recourse":

            correct = gain_realized_recourse

            judgements[gain_realized_nonrecourse] = (
                "This would be correct for nonrecourse debt. But debt relief in excess of the fair market value of the property has a different treatment for recourse debt."
            )
            judgements[gain_realized_recourse] = (
                f"Correct. Because this is recourse debt, debt relief up to fair market value is included in amount realized; debt relief in excess of fair market value is treated as cancellation of indebtedness income. In this problem, {fm.ac(building_fmv)} is included in amount realized, for a total of {fm.ac(abs(gain_realized_recourse_numb))} of {fm.gainword(gain_realized_recourse_numb)}. The excess of the debt over the fair market value, that is, {fm.ac(debt)} minus {fm.ac(building_fmv)}, is cancellation of indebtedness income."
            )

        if debt_type[0] == "nonrecourse":

            correct = gain_realized_nonrecourse

            judgements[gain_realized_nonrecourse] = (
                "Correct. Because this is nonrecourse debt, all of the debt relief is included in amount realized."
            )
            judgements[gain_realized_recourse] = (
                "This would be correct for recourse debt. But this is nonrecourse debt."
            )

    else:  # debt is less than fair market value

        possibleanswers_addl = []

        correct = gain_realized_nonrecourse

        if debt_type[0] == "recourse":

            judgements[gain_realized_nonrecourse] = (
                "Correct. Because the amount of debt relief is less than the fair market value of the building, all of the debt relief is included in amount realized."
            )

        if debt_type[0] == "nonrecourse":

            judgements[gain_realized_nonrecourse] = (
                "Correct. Because this is nonrecourse debt, all of the debt relief is included in amount realized."
            )

    problem = problem_part_1 + cash_paid_lang + question_lang
    possibleanswers = possibleanswers_uni + possibleanswers_addl

    judgements_json = json.dumps(judgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


def like_kind():
    [person1, person2] = fm.create_group()
    judgements = {}

    choose_debt = random.choice([1, 0])

    # one person gives up a building and a machine and gets land. The other person gives up land and gets a building and a machine. The person who gives up land might be in a

    building_fmv = fm.nearestthousand(100000 * (1 + random.random()))
    building_basis = fm.fraction_of_thou(building_fmv, 30, 80)
    machine_fmv = 500 * random.randint(10, 60)

    machine_basis = fm.generate_random_item(machine_fmv, 40, 115)

    if choose_debt == 0:
        building_debt = land_debt = 0
        land_fmv = building_fmv + machine_fmv
        land_basis = fm.fraction_of_thou(land_fmv, 30, 80)

    elif choose_debt == 1:
        while True:
            building_debt = fm.generate_random_item(building_fmv, 20, 70)
            land_basis = fm.nearestthousand(100000 * random.random())
            land_debt = fm.generate_random_item(land_basis, 20, 70)
            land_fmv = building_fmv + machine_fmv - building_debt + land_debt
            if land_debt != building_debt and land_fmv > land_basis:
                break

    personal_use_lang = "personal use"
    business_use_lang = "use in a trade or business"

    use_lang_choice = random.choices(
        [personal_use_lang, business_use_lang], weights=(1, 4)
    )[0]

    # let's do the land person first

    # first, gain recognized
    # this will be the correct gain recognized if this person used the land for personal use.
    land_gain_realized = land_fmv - land_basis

    land_boot_debt_swap = max(
        0, land_debt - building_debt
    )  # this is just the debt netted, because the person who gives up land doesn't give up any other boot
    total_boot = machine_fmv + land_boot_debt_swap

    # if this is a like-kind exchange, this person will recognize gain realized, to the extent of boot received, which will be the machine plus net debt relief
    if land_gain_realized < 0:
        land_gain_recognized_like_kind = 0
    else:
        land_gain_recognized_like_kind = min(total_boot, land_gain_realized)

    land_gain_recognized_like_kind_no_netting = machine_fmv + land_debt

    # now, basis

    basis_total_building_recip_like_kind = (
        land_basis + building_debt - land_debt + land_gain_recognized_like_kind
    )  # in a like-kind exchange, total basis equals the land basis plus the net debt relief plus the gain recognized

    basis_machine_recip = machine_fmv  # allocate basis first to the boot
    basis_building_recip_like_kind = (
        basis_total_building_recip_like_kind - basis_machine_recip
    )
    basis_building_recip_personal_use = building_fmv
    basis_building_recip_like_kind_no_debt = (
        basis_building_recip_like_kind + land_debt - building_debt
    )

    # now let's do the person who starts with the building

    building_gain_realized = building_fmv - building_basis
    machine_gain_realized = machine_fmv - machine_basis
    all_gain_realized = building_gain_realized + machine_gain_realized
    building_boot_debt_swap = max(0, building_debt - land_debt - machine_fmv)

    building_gain_recognized_like_kind = min(
        building_gain_realized, building_boot_debt_swap
    )
    total_building_gain_recognized = (
        machine_gain_realized + building_gain_recognized_like_kind
    )

    # here are some wrong answers:
    building_gain_recognized_like_kind_no_netting = min(
        building_gain_realized, building_debt
    )

    building_boot_debt_swap_netting_no_mach = max(0, building_debt - land_debt)
    building_gain_recognized_like_kind_netting_no_mach = min(
        building_gain_realized, building_boot_debt_swap_netting_no_mach
    )

    # now, basis

    basis_land_recip_in_land = (
        building_basis
        + machine_basis
        + total_building_gain_recognized
        + land_debt
        - building_debt
    )

    # some wrong answers for basis

    cost_basis = machine_fmv + building_fmv
    disregard_gain_basis_building_person = basis_land_recip_in_land - machine_fmv
    disregard_debt_basis_building_person = (
        building_basis + machine_basis + total_building_gain_recognized
    )

    problem_part_1 = f"In {fm.current_year}, {person1.name} and {person2.name} enter into a transaction. {person1.name} provides {person2.name} with a building. The building is worth {fm.ac(building_fmv)} and {person1.name}'s basis in the building is {fm.ac(building_basis)}. {person1.name} has held the building for a number of years and has always used it in {person1.poss} business. {person2.name} plans to use the building in {person2.poss} business as well."

    problem_part_2 = f"<br><br>{person1.name} also provides {person2.name} with a machine that {person1.name} uses in {person1.poss} business. The machine has a fair market value of {fm.ac(machine_fmv)}, and {person1.name}'s basis in the machine is {fm.ac(machine_basis)}. {person2.name} plans to use the machine in {person2.poss} business. <br><br>In exchange, {person2.name} provides {person1.name} with undeveloped land. The land is worth {fm.ac(land_fmv)} and has a basis of {fm.ac(land_basis)} to {person2.name}. {person2.name} has always held the land for {use_lang_choice}. {person1.name} plans to use the land in {person1.poss} business."

    if choose_debt == 1:
        debt_lang_building = f" The building is encumbered with debt of {fm.ac(building_debt)}. {person2.name} takes the building subject to the debt."
        debt_lang_land = f" The land is encumbered with debt of {fm.ac(land_debt)}. {person1.name} takes the land subject to the debt."
    else:
        debt_lang_building = ""
        debt_lang_land = ""

    building_person_gain_q = f"<br><br>How much total gain or loss, if any, does {person1.name} recognize in {fm.current_year} due to this transaction?"
    land_person_gain_q = f"<br><br>How much total gain or loss, if any, does {person2.name} recognize in {fm.current_year} due to this transaction? (Disregard any events subsequent to the transaction, such as depreciation deductions on the building.)"
    building_person_basis_q = f"<br><br>What is {person1.name}'s basis in the land immediately after the transaction?"
    land_person_basis_q = f"<br><br>What is {person2.name}'s basis in the building immediately after the transaction?"

    possible_questions = [
        building_person_gain_q,
        land_person_gain_q,
        building_person_basis_q,
        land_person_basis_q,
    ]

    question_lang = random.choice(possible_questions)

    if question_lang == building_person_gain_q:

        correct = building_person_gain = total_building_gain_recognized

        possibleanswers = [building_person_gain, building_gain_recognized_like_kind]

        judgements = {building_gain_recognized_like_kind: "What about the machine?"}

        if building_gain_realized not in possibleanswers:
            possibleanswers.append(building_gain_realized)
            judgements[building_gain_realized] = (
                '<p>What about the machine? Also, consider the effect of <a href="https://www.law.cornell.edu/uscode/text/26/1031" target="_new" rel="noreferrer">Section 1031(b)</a>.</p>'
            )

        if all_gain_realized not in possibleanswers:
            possibleanswers.append(all_gain_realized)
            judgements[all_gain_realized] = (
                '<p>Consider the effect of <a href="https://www.law.cornell.edu/uscode/text/26/1031" target="_new" rel="noreferrer">Section 1031(b)</a>.</p>'
            )

        if choose_debt == 1:

            if building_boot_debt_swap > 0:

                possibleanswers = possibleanswers + [
                    building_gain_recognized_like_kind_netting_no_mach,
                    building_gain_recognized_like_kind_no_netting,
                ]
                judgements[building_gain_recognized_like_kind_no_netting] = (
                    "Remember: only *net* debt relief is boot."
                )

                if building_debt - land_debt - machine_fmv <= building_gain_realized:
                    total_net_debt = building_debt - land_debt - machine_fmv

                    judgements[building_gain_recognized_like_kind_netting_no_mach] = (
                        "Don't forget to reduce the net debt relief by the other boot provided."
                    )
                    judgements[building_person_gain] = (
                        f"Correct! The disposition of the machine is a recognition transaction, and {person1.name} recognizes {fm.ac(machine_gain_realized)} due to providing the machine as partial compensation for the land. With respect to the building, {person1.name} realizes {fm.ac(building_gain_realized)}, which will be recognized to the extent of boot received. Here, {person1.name} receives boot equal to the net debt relief (that is, the excess of {fm.ac(building_debt)} over {fm.ac(land_debt)}), reduced by the fair market value of non-like-kind property provided by {person1.name} (in this case, the fair market value of the machine, {fm.ac(machine_fmv)}). {fm.ac(building_debt)} - {fm.ac(land_debt)} - {fm.ac(machine_fmv)} = {fm.ac(total_net_debt)}. The total gain recognized is thus {fm.ac(machine_gain_realized)} plus {fm.ac(total_net_debt)}."
                    )

                else:
                    total_net_debt = building_debt - land_debt - machine_fmv
                    possibleanswers.append(building_boot_debt_swap)
                    judgements[building_boot_debt_swap] = (
                        "Can the amount recognized be greater than the amount realized?"
                    )
                    judgements[building_gain_recognized_like_kind_netting_no_mach] = (
                        "Don't forget to reduce the net debt relief by the other boot provided."
                    )
                    judgements[building_person_gain] = (
                        f'<p>Correct! The disposition of the machine is a recognition transaction, and {person1.name} recognizes {fm.ac(machine_gain_realized)} due to providing the machine as partial compensation for the land. With respect to the building, {person1.name} realizes gain of {fm.ac(building_gain_realized)}, which will be recognized to the extent of boot received. Here, {person1.name} receives boot equal to the net debt relief (that is, the excess of {fm.ac(building_debt)} over {fm.ac(land_debt)}), reduced by the fair market value of non-like-kind property provided by {person1.name} (in this case, the fair market value of the machine, {fm.ac(machine_fmv)}). The net debt relief reduced by the value of the machine, that is, ({fm.ac(building_debt - land_debt)} reduced by {fm.ac(machine_fmv)}), equals {fm.ac(total_net_debt)}, which is greater than the gain realized. But <a href="https://www.law.cornell.edu/uscode/text/26/1031" target="_new" rel="noreferrer">Section 1031(b)</a> is not a punitive provision--the gain recognized will not be greater than the gain realized. Thus the gain recognized with respect to the building is the same as the gain realized with respect to the building: {fm.ac(building_gain_realized)}. The total gain recognized is therefore the gain recognized due to the machine, {fm.ac(machine_gain_realized)}, plus the gain recognized due to the building, {fm.ac(building_gain_realized)}, which totals {fm.ac(building_person_gain)}.</p>'
                    )

            else:

                possibleanswers.append(building_gain_recognized_like_kind_no_netting)

                judgements[building_gain_recognized_like_kind_no_netting] = (
                    "Remember: only *net* debt relief is boot."
                )
                judgements[building_person_gain] = (
                    f"Correct! The disposition of the machine is a recognition transaction, and {person1.name} recognizes {fm.ac(machine_gain_realized)} due to providing the machine as partial compensation for the land. With respect to the building, {person1.name} realizes {fm.ac(building_gain_realized)}, which will be recognized to the extent of boot received. But only *net* debt relief is boot, where net debt relief equals the excess of {fm.ac(building_debt)} over {fm.ac(land_debt)}, reduced by the fair market value of non-like-kind property provided by {person1.name} (in this case, the fair market value of the machine, {fm.ac(machine_fmv)}). Because {person1.name} has no net debt relief, {person1.name} is treated as receiving no boot and thus recognizes no gain with respect to the like-kind portion of the transaction."
                )

        elif choose_debt == 0:

            judgements[building_person_gain] = (
                f"Correct! The disposition of the machine is a recognition transaction, and {person1.name} recognizes {fm.ac(machine_gain_realized)} due to providing the machine as partial compensation for the land. With respect to the building, {person1.name} realizes {fm.ac(building_gain_realized)}, which will be recognized to the extent of boot received. Here, {person1.name} receives no boot and thus recognizes no gain with respect to the like-kind portion of the transaction."
            )

        if 0 not in possibleanswers:
            possibleanswers.append(0)
            judgements[0] = "Is any boot received?"

    if question_lang == land_person_gain_q:

        possibleanswers = [land_gain_recognized_like_kind, 0]

        judgements = {0: "Is any boot received?"}

        if (
            use_lang_choice == "personal use"
        ):  # personal use--does not matter what the options are

            possibleanswers.append(land_gain_realized)
            land_person_gain = land_gain_realized
            correct = land_person_gain

            judgements[land_person_gain] = (
                f"Correct. This is not a like-kind exchange, because {person2.name} did not use the land in a trade or business."
            )
            if land_gain_recognized_like_kind != land_person_gain:
                judgements[land_gain_recognized_like_kind] = (
                    f"What are the requirements for a like-kind exchange? Are those requirements met here?",
                )
            judgements[0] = (
                f"Is this a like-kind exchange? Also, even if it were a like-kind exchange, is any boot received?"
            )

        elif choose_debt == 0:  # like kind exchange, no debt

            land_person_gain = land_gain_recognized_like_kind
            correct = land_person_gain

            if land_person_gain != land_gain_realized:
                possibleanswers.append(land_gain_realized)
                judgements[land_gain_realized] = (
                    "Is all the gain recognized on this transaction? Why not?"
                )
                judgements[land_person_gain] = (
                    f"Correct! This is a like-kind exchange. With respect to the land, {person2.name} realizes {fm.ac(land_gain_realized)}, which will be recognized to the extent of boot received--here, the fair market value of the machine, {fm.ac(machine_fmv)}."
                )

            elif land_person_gain == land_gain_realized:
                judgements[land_person_gain] = (
                    f"Correct! This is a like-kind exchange. With respect to the land, {person2.name} realizes {fm.ac(land_gain_realized)}, which will be recognized to the extent of boot received. Here, the fair market value of the machine, {fm.ac(machine_fmv)}, exceeds the gain realized, so the full amount of gain is recognized, notwithstanding that this is a like-kind exchange."
                )

        elif (
            land_boot_debt_swap == 0
        ):  # like kind exchange with debt but no net debt relief

            land_person_gain = land_gain_recognized_like_kind
            correct = land_person_gain

            possibleanswers = possibleanswers + [
                land_gain_recognized_like_kind_no_netting
            ]

            if land_person_gain != land_gain_realized:
                possibleanswers.append(land_gain_realized)
                judgements[land_gain_realized] = (
                    "Is all the gain recognized on this transaction? Why not?"
                )
                judgements[land_person_gain] = (
                    f"Correct! This is a like-kind exchange, so gain realized, {fm.ac(land_gain_realized)}, is recognized to the extent of boot received. Here, the only boot received is the machine, because only *net* debt relief is boot."
                )

            elif land_person_gain == land_gain_realized:
                judgements[land_person_gain] = (
                    f"Correct! This is a like-kind exchange. With respect to the land, {person2.name} realizes {fm.ac(land_gain_realized)}, which will be recognized to the extent of boot received. Here, the only boot received is the machine, because only *net* debt relief is boot. The fair market value of the machine, {fm.ac(machine_fmv)}, exceeds the gain realized, so the full amount of gain is recognized, notwithstanding that this is a like-kind exchange."
                )

            judgements[land_gain_recognized_like_kind_no_netting] = (
                "Remember: only *net* debt relief is boot."
            )

        else:  # like kind exchange, debt, net debt relief

            land_person_gain = land_gain_recognized_like_kind
            correct = land_person_gain

            possibleanswers.append(land_gain_recognized_like_kind_no_netting)

            if land_person_gain != land_gain_realized:
                possibleanswers.append(land_gain_realized)
                judgements[land_gain_realized] = (
                    "Is all the gain recognized on this transaction? Why not?"
                )
                judgements[land_person_gain] = (
                    f"Correct! This is a like-kind exchange, so gain realized, {fm.ac(land_gain_realized)}, is recognized to the extent of boot received. Here, {person2.name} receives boot equal to the fair market value of the machine, {fm.ac(machine_fmv)}, plus the net debt relief, that is, the excess of {fm.ac(land_debt)} over {fm.ac(building_debt)}."
                )

            elif land_person_gain == land_gain_realized:
                judgements[land_person_gain] = (
                    f"Correct! This is a like-kind exchange. With respect to the land, {person2.name} realizes {fm.ac(land_gain_realized)}, which will be recognized to the extent of boot received. Here, {person2.name} receives boot equal to the fair market value of the machine, {fm.ac(machine_fmv)}, plus the net debt relief, that is, the excess of {fm.ac(land_debt)} over {fm.ac(building_debt)}. The boot received thus exceeds the gain realized, so the full amount of gain is recognized, notwithstanding that this is a like-kind exchange."
                )

            judgements[land_gain_recognized_like_kind_no_netting] = (
                "Remember: only *net* debt relief is boot."
            )

    if question_lang == building_person_basis_q:

        building_person_basis = basis_land_recip_in_land
        correct = building_person_basis

        possibleanswers = [building_person_basis, disregard_gain_basis_building_person]
        judgements = {disregard_gain_basis_building_person: "What about the machine?"}

        if choose_debt == 1:

            possibleanswers.append(disregard_debt_basis_building_person)

            judgements[building_person_basis] = (
                f"Correct. The basis in the land equals {person1.name}'s basis in the building, {fm.ac(building_basis)}, plus {person1.poss} basis in the machine, {fm.ac(machine_basis)}, plus total gain or loss recognized, {fm.ac(total_building_gain_recognized)}, less the debt relief from giving up the debt on the building, so minus {fm.ac(building_debt)}, plus the consideration provided by taking on the debt on the land, {fm.ac(land_debt)}."
            )
            judgements[disregard_debt_basis_building_person] = "What about the debt?"

        if choose_debt == 0:

            judgements[building_person_basis] = (
                f"Correct. The basis in the land equals {person1.name}'s basis in the building, {fm.ac(building_basis)}, plus {person1.poss} basis in the machine, {fm.ac(machine_basis)}, plus total gain or loss recognized, {fm.ac(total_building_gain_recognized)}."
            )

        if cost_basis not in possibleanswers:

            possibleanswers.append(cost_basis)
            judgements[cost_basis] = f"This is a like-kind exchange for {person1.name}."

    if question_lang == land_person_basis_q:

        possibleanswers = [
            basis_total_building_recip_like_kind,
            basis_building_recip_like_kind,
            basis_building_recip_personal_use,
        ]

        if (
            use_lang_choice == "personal use"
        ):  # personal use--does not matter what the options are

            correct = basis_building_recip_personal_use

            judgements[basis_building_recip_personal_use] = (
                f"Correct. This is not a like-kind exchange, so {person2.name} recognizes all realized gain and has a cost basis in the building."
            )
            judgements[basis_building_recip_like_kind] = "Is this a like-kind exchange?"

        elif choose_debt == 0:  # like kind exchange, no debt

            correct = basis_building_recip_like_kind

            judgements[basis_building_recip_personal_use] = (
                f"Does {person2.name} recognize all realized gain?"
            )
            judgements[basis_building_recip_like_kind] = (
                f"Correct. This is a like-kind exchange, so {person2.name} has a total basis in all the property received of {person2.poss} basis in the land, {fm.ac(land_basis)}, plus the gain {person2.nom} realized due to the receipt of boot, {fm.ac(land_gain_recognized_like_kind)}. That total basis is allocated first to the machine, up to its fair market value of {fm.ac(machine_fmv)}, leaving {fm.ac(basis_building_recip_like_kind)} of basis for the building."
            )

        else:  # like kind exchange, debt, net debt relief

            correct = basis_building_recip_like_kind

            possibleanswers.append(basis_building_recip_like_kind_no_debt)

            judgements[basis_building_recip_personal_use] = (
                f"Does {person2.name} recognize all realized gain?"
            )
            judgements[basis_building_recip_like_kind] = (
                f"Correct. This is a like-kind exchange, so {person2.name} has a total basis in all the property received of {person2.poss} basis in the land, {fm.ac(land_basis)}, plus the gain {person2.nom} recognized due to the receipt of boot (no loss can be recognized, but gain can be), {fm.ac(land_gain_recognized_like_kind)}, less the debt relief from giving up the debt on the land, so minus {fm.ac(land_debt)}, plus the consideration provided by taking on the debt on the building, {fm.ac(building_debt)}. That total basis is allocated first to the machine, up to its fair market value of {fm.ac(machine_fmv)}, leaving {fm.ac(basis_building_recip_like_kind)} of basis for the building."
            )
            judgements[basis_building_recip_like_kind_no_debt] = "What about the debt?"

    problem = (
        problem_part_1
        + debt_lang_building
        + problem_part_2
        + debt_lang_land
        + question_lang
    )

    [possibleanswers, judgements] = fm.random_answer(possibleanswers, judgements)
    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


def installment_sale_plain():

    [person1, person2] = fm.create_group()

    problem_date_number = fm.pick_random_date_this_year()
    problem_date = fm.full_date(problem_date_number)

    property_fmv = 1000 * random.randint(10, 1500)
    property_basis = fm.fraction_of_thou(property_fmv)

    realized_gain = property_fmv - property_basis

    years_until_second_payment = random.randint(4, 10)
    second_payment_year = fm.current_year + years_until_second_payment
    second_payment_date = (
        fm.month_day(problem_date_number) + ", " + str(second_payment_year)
    )

    initial_payment = fm.nearestthousand(property_fmv * random.randint(30, 80) / 100)
    second_payment = property_fmv - initial_payment

    gain_first_payment_prorata = int(realized_gain * (initial_payment / property_fmv))
    gain_second_payment_prorata = int(realized_gain * (second_payment / property_fmv))

    problem_lang_intro = f"On {problem_date}, {person1.name} sells {person2.name} a piece of real estate that is worth {fm.ac(property_fmv)} and has a basis of {fm.ac(property_basis)}."

    problem_lang_other_comp = f" {person2.name} pays cash of {fm.ac(initial_payment)}."

    problem_lang_provides_note = f" {person2.name} also provides a note for {fm.ac(second_payment)} that pays adequate stated interest and provides for a balloon payment of all the principal in {years_until_second_payment} years."

    # other answers
    gain_first_payment_basis_first = max(0, initial_payment - property_basis)
    gain_first_payment_basis_last = initial_payment - max(
        0, property_basis - second_payment
    )
    gain_first_payment_full_note_as_payment = realized_gain
    # random_payment = fm.nearestthousand(realized_gain*random.randint(40,90)/100)

    gain_second_payment_basis_first = realized_gain - gain_first_payment_basis_first
    gain_second_payment_basis_last = realized_gain - gain_first_payment_basis_last
    gain_second_payment_full_note_as_payment = (
        realized_gain - gain_first_payment_full_note_as_payment
    )

    first_payment_gain_q = f" How much gain or loss, if any, does {person1.name} recognize in {str(fm.current_year)} due to the transaction?"

    second_payment_gain_q = f" How much gain or loss, if any, does {person1.name} recognize in {str(second_payment_year)} due to the transaction?"

    question_lang = random.choice([first_payment_gain_q, second_payment_gain_q])

    if question_lang == first_payment_gain_q:
        correct = gain_first_payment_prorata

        possibleanswers = [
            gain_first_payment_basis_first,
            gain_first_payment_basis_last,
            gain_first_payment_full_note_as_payment,
            gain_first_payment_prorata,
        ]

        judgements = {
            correct: f"Correct! The note itself is not considered a payment, so the only payment in the year of the sale is {fm.ac(initial_payment)}. A proportionate amount of each payment is treated as amount recognized, specifically the fraction equal to the total gain divided by the contract price--that is, {fm.ac(realized_gain)} divided by {fm.ac(property_fmv)}, or {fm.as_percent(realized_gain/property_fmv)}.<br><br>Equivalently, you can think of this as basis being recovered proportionate to the payment. That is, because {fm.ac(initial_payment)} divided by {fm.ac(property_fmv)}, or {fm.as_percent(initial_payment/property_fmv)}, of the payments are received, the same percentage of gain realized is recognized.",
            gain_first_payment_basis_first: "This would be correct if all of the basis could be put toward the initial payment--that is, if basis were recovered first. But that is not the approach in installment sales.",
            gain_first_payment_basis_last: "This would be correct if basis were allocated first to the payments on the note--that is, if basis were recovered last. But that is not the approach in installment sales.",
            gain_first_payment_full_note_as_payment: "This would be correct if the note were treated as payment in the year it is received. But that is not the approach in installment sales.",
        }

    if question_lang == second_payment_gain_q:
        correct = gain_second_payment_prorata

        possibleanswers = [
            gain_second_payment_basis_first,
            gain_second_payment_basis_last,
            gain_second_payment_full_note_as_payment,
            gain_second_payment_prorata,
        ]

        judgements = {
            correct: f"Correct! The note itself is not considered a payment; gain on the amount of the note is not recognized until the note is paid. Thus the payment in {str(second_payment_year)} is {fm.ac(second_payment)}. A proportionate amount of each payment is treated as amount recognized, specifically the fraction equal to the total gain divided by the contract price--that is, {fm.ac(realized_gain)} divided by {fm.ac(property_fmv)}, or {fm.as_percent(realized_gain/property_fmv)}.<br><br>Equivalently, you can think of this as basis being recovered proportionate to the payment. That is, because {fm.ac(second_payment)} divided by {fm.ac(property_fmv)}, or {fm.as_percent(second_payment/property_fmv)}, of the payments are received, the same percentage of gain realized is recognized.",
            gain_second_payment_basis_first: "This would be correct if all of the basis had been put toward the initial payment--that is, if basis were recovered first. But that is not the approach in installment sales.",
            gain_second_payment_basis_last: "This would be correct if basis were allocated first to the payments on the note--that is, if basis were recovered last. But that is not the approach in installment sales.",
            gain_second_payment_full_note_as_payment: "This would be correct if the note were treated as payment in the year it is received. But that is not the approach in installment sales.",
        }

    problem = (
        problem_lang_intro
        + problem_lang_other_comp
        + problem_lang_provides_note
        + question_lang
    )

    [possibleanswers, judgements] = fm.random_answer_pot(possibleanswers, judgements, 0)

    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


def installment_sale_debt():

    [person1, person2] = fm.create_group()

    property_fmv = 1000 * random.randint(10, 1500)
    property_basis = fm.fraction_of_thou(property_fmv)

    realized_gain = property_fmv - property_basis

    problem_date_number = fm.pick_random_date_this_year()
    problem_date = fm.full_date(problem_date_number)

    years_until_second_payment = random.randint(4, 10)
    second_payment_year = fm.current_year + years_until_second_payment
    second_payment_date = (
        fm.month_day(problem_date_number) + ", " + str(second_payment_year)
    )

    initial_payment = fm.nearestthousand(property_fmv * random.randint(30, 80) / 100)
    second_payment = property_fmv - initial_payment
    gain_first_payment_prorata = int(realized_gain * (initial_payment / property_fmv))
    gain_second_payment_prorata = int(realized_gain * (second_payment / property_fmv))

    problem_lang_intro = f"On {problem_date}, {person1.name} sells {person2.name} a piece of real estate that is worth {fm.ac(property_fmv)} and has a basis of {fm.ac(property_basis)}."

    choose_qualifying = random.choice(["qualified debt", "nonqualified debt"])

    if choose_qualifying == "qualified debt":
        problem_lang_addl = f" {person1.name} acquired the debt many years previously."
    else:
        problem_lang_addl = f" {person1.name} acquired the debt six months ago, after {person1.nom} had put the property on the market."

    problem_lang_other_comp = f" The property is encumbered with debt of {fm.ac(initial_payment)}. {person2.name} takes the property subject to the debt."

    problem_lang_provides_note = f" {person2.name} provides a note for {fm.ac(second_payment)} that pays adequate stated interest and provides for a balloon payment of all the principal in {years_until_second_payment} years."

    excluded_debt = min(property_basis, initial_payment)
    initial_payment_qual_debt = initial_payment - excluded_debt
    contract_price_excluded_debt = property_fmv - excluded_debt
    gain_first_payment_qual_debt = int(
        initial_payment_qual_debt * (realized_gain / contract_price_excluded_debt)
    )
    gain_second_payment_qual_debt = realized_gain - gain_first_payment_qual_debt

    # if you exclude all debt
    initial_payment_exclude_all_debt = int(0)
    contract_price_exclude_all_debt = property_fmv - initial_payment
    gain_first_payment_exclude_all_debt = int(
        initial_payment_exclude_all_debt
        * (realized_gain / contract_price_exclude_all_debt)
    )
    gain_second_payment_exclude_all_debt = (
        realized_gain - gain_first_payment_exclude_all_debt
    )

    # other answers
    gain_first_payment_basis_first = int(max(0, initial_payment - property_basis))
    gain_first_payment_basis_last = initial_payment - max(
        0, property_basis - second_payment
    )
    gain_first_payment_full_note_as_payment = realized_gain
    random_payment = int(realized_gain * random.randint(40, 90) / 100)

    gain_second_payment_basis_first = int(
        realized_gain - gain_first_payment_basis_first
    )
    gain_second_payment_basis_last = realized_gain - gain_first_payment_basis_last
    gain_second_payment_full_note_as_payment = (
        realized_gain - gain_first_payment_full_note_as_payment
    )

    first_payment_gain_q = f" How much gain or loss, if any, does {person1.name} recognize in {str(fm.current_year)} due to the transaction?"

    second_payment_gain_q = f" How much gain or loss, if any, does {person1.name} recognize in {str(second_payment_year)} due to the transaction?"

    question_lang = random.choice([first_payment_gain_q, second_payment_gain_q])

    if choose_qualifying == "qualified debt":

        if question_lang == first_payment_gain_q:

            correct = gain_first_payment_qual_debt

            possibleanswers = [
                gain_first_payment_qual_debt,
                gain_first_payment_basis_last,
                gain_first_payment_full_note_as_payment,
                gain_first_payment_prorata,
                random_payment,
            ]

            judgements = {
                correct: f"Correct! Because the debt was not acquired in contemplation of the disposition of the property, this is qualifying indebtedness. Therefore the amount of the debt relief is excluded from payment received and from contract price to the extent of basis.",
                gain_first_payment_prorata: "This would be correct if this were not qualifying indebtedness.",
                gain_first_payment_basis_last: "This would be correct if this were not qualifying indebtedness and if basis were allocated first to the payments on the note--that is, if basis were recovered last. But that is not the approach in installment sales.",
                gain_first_payment_full_note_as_payment: "This would be correct if this were not qualifying indebtedness and the note were treated as payment in the year it is received. But that is not the approach in installment sales.",
                random_payment: "This number was randomly generated.",
            }

            if initial_payment > property_basis:
                possibleanswers.append(gain_first_payment_exclude_all_debt)

                judgements[gain_first_payment_exclude_all_debt] = (
                    "It is true this is qualifying indebtedness, but debt can be excluded only up to basis."
                )

        if question_lang == second_payment_gain_q:

            correct = gain_second_payment_qual_debt

            possibleanswers = [
                gain_second_payment_qual_debt,
                gain_second_payment_basis_last,
                gain_second_payment_full_note_as_payment,
                gain_second_payment_prorata,
                random_payment,
            ]

            judgements = {
                correct: f"Correct! Because the debt was not acquired in contemplation of the disposition of the property, this is qualifying indebtedness. Therefore the amount of the debt relief is excluded from payment received and from contract price to the extent of basis.",
                gain_second_payment_prorata: "This would be correct if this were not qualifying indebtedness.",
                gain_second_payment_basis_last: "This would be correct if this were not qualifying indebtedness and if basis were allocated first to the payments on the note--that is, if basis were recovered last. But that is not the approach in installment sales.",
                gain_second_payment_full_note_as_payment: "This would be correct if this were not qualifying indebtedness and the note were treated as payment in the year it is received. But that is not the approach in installment sales.",
                random_payment: "This number was randomly generated.",
            }

            if initial_payment > property_basis:

                possibleanswers.append(gain_second_payment_exclude_all_debt)

                judgements[gain_second_payment_exclude_all_debt] = (
                    "It is true this is qualifying indebtedness, but debt can be excluded only up to basis."
                )

    elif choose_qualifying == "nonqualified debt":

        if question_lang == first_payment_gain_q:

            correct = gain_first_payment_prorata

            possibleanswers = [
                gain_first_payment_qual_debt,
                gain_first_payment_basis_last,
                gain_first_payment_full_note_as_payment,
                gain_first_payment_prorata,
                random_payment,
            ]

            judgements = {
                correct: f"Correct! This is not qualifying indebtedness, and so debt relief is not excluded from payment received or from contract price. The note itself is not considered a payment, so the only payment in the year of the sale is {fm.ac(initial_payment)}. Basis is recovered proportionate to the payment. That is, because {fm.ac(initial_payment)} divided by {fm.ac(property_fmv)}, or {fm.as_percent(initial_payment/property_fmv)}, of the payments are received, the same percentage of gain realized is recognized.",
                gain_first_payment_qual_debt: "This would be correct if this were qualifying indebtedness.",
                gain_first_payment_basis_last: "It is true this is not qualifying indebtedness, and this would be correct if basis were allocated first to the payments on the note--that is, if basis were recovered last. But that is not the approach in installment sales.",
                gain_first_payment_full_note_as_payment: "It is true this is not qualifying indebtedness, and this would be correct if the note were treated as payment in the year it is received. But that is not the approach in installment sales.",
                random_payment: "This number was randomly generated.",
            }

        if question_lang == second_payment_gain_q:

            correct = gain_second_payment_prorata

            possibleanswers = [
                gain_second_payment_qual_debt,
                gain_second_payment_basis_last,
                gain_second_payment_full_note_as_payment,
                gain_second_payment_prorata,
                random_payment,
            ]

            judgements = {
                correct: f"Correct! This is not qualifying indebtedness, and so debt relief is not excluded from payment received or from contract price. The note itself is not considered a payment; gain on the amount of the note is not recognized until the note is paid. Thus the payment in {str(second_payment_year)} is {fm.ac(second_payment)}. Basis is recovered proportionate to the payment. That is, because {fm.ac(second_payment)} divided by {fm.ac(property_fmv)}, or {fm.as_percent(second_payment/property_fmv)}, of the payments are received, the same percentage of gain realized is recognized.",
                gain_second_payment_qual_debt: "This would be correct if this were qualifying indebtedness.",
                gain_second_payment_basis_last: "This would be correct if basis were allocated first to the payments on the note--that is, if basis were recovered last. But that is not the approach in installment sales.",
                gain_second_payment_full_note_as_payment: "This would be correct if the note were treated as payment in the year it is received. But that is not the approach in installment sales.",
                random_payment: "This number was randomly generated.",
            }

    problem = (
        problem_lang_intro
        + problem_lang_other_comp
        + problem_lang_addl
        + problem_lang_provides_note
        + question_lang
    )

    [possibleanswers, judgements] = fm.random_answer_pot(possibleanswers, judgements, 0)

    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


def installment_sale_related_party():

    [person1, person2, person3] = fm.create_group(3)

    if person2.name in names.malenames:
        relatives_267 = [
            "brother",
            "husband",
            "father",
            "grandfather",
            "great-grandfather",
            "son",
            "grandson",
        ]
        relatives_other = ["cousin", "uncle", "nephew"]

    else:
        relatives_267 = [
            "sister",
            "wife",
            "mother",
            "grandmother",
            "great-grandmother",
            "daughter",
            "granddaughter",
        ]
        relatives_other = ["cousin", "aunt", "niece"]

    relatives = relatives_267 + relatives_other

    property_fmv = 1000 * random.randint(10, 1500)
    property_basis = fm.fraction_of_thou(property_fmv)

    realized_gain = property_fmv - property_basis

    years_until_second_payment = random.randint(4, 10)
    second_payment_year = fm.current_year + years_until_second_payment
    # the soonest and latest are picked so that there is a 70% chance that the sale will be before two years

    while True:
        how_far_after = random.randint(400, 870)
        if how_far_after != 730:
            break

    problem_date_number = fm.pick_random_date_this_year()
    problem_date = fm.full_date(problem_date_number)

    third_party_sale_date = fm.full_date(
        fm.date_after(problem_date_number, soonest=how_far_after, latest=how_far_after)
    )

    initial_payment = fm.nearestthousand(property_fmv * random.randint(30, 80) / 100)
    second_payment = property_fmv - initial_payment
    gain_first_payment_prorata = int(realized_gain * (initial_payment / property_fmv))
    gain_second_payment_prorata = int(realized_gain * (second_payment / property_fmv))
    included_second_payment = min(second_payment, property_fmv) - initial_payment
    gain_second_payment = int(included_second_payment * (realized_gain / property_fmv))

    resale_price = fm.generate_random_item(property_fmv, 90, 130)

    resale_price_as_payment = max(
        0, (min(property_fmv, resale_price) - initial_payment)
    )
    gain_resale_prorata = int(realized_gain * (resale_price_as_payment / property_fmv))
    full_resale_as_payment = int(realized_gain * resale_price / property_fmv)

    amt_included_second_payment_with_453 = max(
        0, second_payment - resale_price_as_payment
    )
    gain_second_payment_pro_rata_with_453 = int(
        realized_gain * amt_included_second_payment_with_453 / property_fmv
    )

    problem_lang_intro = f"On {problem_date}, {person1.name} sells {person2.name} a piece of real estate that is worth {fm.ac(property_fmv)} and has a basis of {fm.ac(property_basis)}."

    relationship = random.choice(relatives)
    # testing
    # relationship = random.choice(relatives_267)

    problem_lang_relative = f" {person2.name} is {person1.name}'s {relationship}."

    problem_lang_other_comp = f" {person2.name} pays cash of {fm.ac(initial_payment)}."

    problem_lang_provides_note = f" {person2.name} also provides a note for {fm.ac(second_payment)} that pays adequate stated interest and provides for a balloon payment of all the principal in {years_until_second_payment} years."

    problem_lang_sale_third_party = f" On {third_party_sale_date}, {person2.name} sells the property to {person3.name} for {fm.ac(resale_price)}."

    # other answers
    gain_first_payment_basis_first = int(max(0, initial_payment - property_basis))
    gain_first_payment_basis_last = initial_payment - max(
        0, property_basis - second_payment
    )
    gain_first_payment_full_note_as_payment = realized_gain
    random_payment = int(realized_gain * random.randint(40, 90) / 100)

    gain_second_payment_basis_first = int(
        realized_gain - gain_first_payment_basis_first
    )
    gain_second_payment_basis_last = realized_gain - gain_first_payment_basis_last
    gain_second_payment_full_note_as_payment = (
        realized_gain - gain_first_payment_full_note_as_payment
    )

    first_payment_gain_q = f" How much gain or loss, if any, does {person1.name} recognize in {str(fm.current_year)} due to the sale to {person2.name}?"

    resale_gain_q = f" How much gain or loss, if any, does {person1.name} recognize due to the sale to {person3.name}?"

    second_payment_gain_q = f" How much gain or loss, if any, does {person1.name} recognize due to the payment of the note in {str(second_payment_year)}?"

    # testing
    # question_lang = resale_gain_q
    question_lang = random.choice(
        [first_payment_gain_q, second_payment_gain_q, resale_gain_q]
    )

    if question_lang == first_payment_gain_q:
        correct = gain_first_payment_prorata

        possibleanswers = [
            gain_first_payment_basis_first,
            gain_first_payment_basis_last,
            gain_first_payment_full_note_as_payment,
            gain_first_payment_prorata,
            random_payment,
        ]

        judgements = {
            correct: f"Correct! The note itself is not considered a payment, so the only payment in the year of the sale is {fm.ac(initial_payment)}. A proportionate amount of each payment is treated as amount recognized, specifically the fraction equal to the total gain divided by the contract price--that is, {fm.ac(realized_gain)} divided by {fm.ac(property_fmv)}, or {fm.as_percent(realized_gain/property_fmv)}.<br><br>Equivalently, you can think of this as basis being recovered proportionate to the payment. That is, because {fm.ac(initial_payment)} divided by {fm.ac(property_fmv)}, or {fm.as_percent(initial_payment/property_fmv)}, of the payments are received, the same percentage of gain realized is recognized.",
            gain_first_payment_basis_first: "This would be correct if all of the basis could be put toward the initial payment--that is, if basis were recovered first. But that is not the approach in installment sales.",
            gain_first_payment_basis_last: "This would be correct if basis were allocated first to the payments on the note--that is, if basis were recovered last. But that is not the approach in installment sales.",
            gain_first_payment_full_note_as_payment: "This would be correct if the note were treated as payment in the year it is received. But that is not the approach in installment sales.",
            random_payment: "This number was randomly generated.",
        }

    if question_lang == resale_gain_q:

        if relationship in relatives_267:

            possibleanswers = [
                gain_resale_prorata,
                0,
                random_payment,
                gain_first_payment_basis_first,
                gain_first_payment_basis_last,
                gain_first_payment_full_note_as_payment,
            ]

            if how_far_after < 730:

                correct = gain_resale_prorata

                judgements = {
                    correct: f'<p>Correct! This is a relationship described in <a href="https://www.law.cornell.edu/uscode/text/26/267" target="_new" rel="noreferrer">Section 267</a>, and the sale to {person3.name} happened not more than two years after the initial sale from {person1.name} to {person2.name}, so <a href="https://www.law.cornell.edu/uscode/text/26/453" target="_new" rel="noreferrer">Section 453(e)</a> applies. The payment included is {fm.ac(resale_price_as_payment)}, and a proportionate amount of that payment, {fm.ac(gain_resale_prorata)}, is income.</p>',
                    0: f'<p>This is a relationship described in <a href="https://www.law.cornell.edu/uscode/text/26/267" target="_new" rel="noreferrer">Section 267</a>, and the the sale to {person3.name} happened less not more than two years after the initial sale from {person1.name} to {person2.name}. Consider <a href="https://www.law.cornell.edu/uscode/text/26/453" target="_new" rel="noreferrer">Section 453(e)</a>.</p>',
                    random_payment: "This number was randomly generated.",
                }

                if resale_price > second_payment:

                    possibleanswers.append(full_resale_as_payment)

                    judgements[full_resale_as_payment] = (
                        f"How much of the sale price to {person3.name} is considered a payment on the note? Consider 453(e)(3)."
                    )

            if how_far_after > 730:

                correct = 0

                judgements = {
                    correct: f'<p>Correct! This is a relationship described in <a href="https://www.law.cornell.edu/uscode/text/26/267" target="_new" rel="noreferrer">Section 267</a>, so <a href="https://www.law.cornell.edu/uscode/text/26/453" target="_new" rel="noreferrer">Section 453(e)</a> could apply. But because the sale to {person3.name} happened more than two years after the initial sale from {person1.name} to {person2.name}, it exceeds the two-year cutoff described in 453(e)(2), so there is no deemed payment.</p>',
                    gain_resale_prorata: f'<p>This is a relationship described in <a href="https://www.law.cornell.edu/uscode/text/26/267" target="_new" rel="noreferrer">Section 267</a>, so <a href="https://www.law.cornell.edu/uscode/text/26/453" target="_new" rel="noreferrer">Section 453(e)</a> could apply. But how long did after the sale from {person1.name} to {person2.name} did the sale to {person3.name} occur? Consider 453(e)(2).</p>',
                    random_payment: "This number was randomly generated.",
                }

                if resale_price > second_payment:

                    possibleanswers.append(full_resale_as_payment)

                    judgements[full_resale_as_payment] = (
                        f'<p>Does <a href="https://www.law.cornell.edu/uscode/text/26/453" target="_new" rel="noreferrer">Section 453(e)</a> apply? How long after the initial sale did the sale to {person3.name} take place? Moreover, even if it did apply, how much of the sale price to {person3.name} would be considered a payment on the note? Consider 453(e)(3).</p>'
                    )

        else:

            correct = 0

            possibleanswers = [
                gain_resale_prorata,
                0,
                random_payment,
                full_resale_as_payment,
            ]

            judgements = {
                correct: '<p>Correct! This is not a relationship described in <a href="https://www.law.cornell.edu/uscode/text/26/267" target="_new" rel="noreferrer">Section 267</a>.</p>',
                gain_resale_prorata: '<p>Is this a relationship described in <a href="https://www.law.cornell.edu/uscode/text/26/267" target="_new" rel="noreferrer">Section 267</a>?</p>',
                full_resale_as_payment: '<p>Is this a relationship described in <a href="https://www.law.cornell.edu/uscode/text/26/267" target="_new" rel="noreferrer">Section 267</a>?</p>',
                random_payment: "This number was randomly generated.",
            }

    if question_lang == second_payment_gain_q:

        if relationship not in relatives_267:

            correct = gain_second_payment_prorata

            possibleanswers = [
                gain_second_payment_pro_rata_with_453,
                gain_second_payment_prorata,
                random_payment,
            ]

            judgements = {random_payment: "This number was randomly generated."}

            if how_far_after < 730:

                judgements[correct] = (
                    f'<p>Correct! <a href="https://www.law.cornell.edu/uscode/text/26/453" target="_new" rel="noreferrer">Section 453(e)</a> does not apply, because "{relationship}" does not count as a related party under <a href="https://www.law.cornell.edu/uscode/text/26/267" target="_new" rel="noreferrer">Section 267</a>. Therefore the regular rules apply. The note itself is not considered a payment; gain on the amount of the note is not recognized until the note is paid. Thus the payment in {str(second_payment_year)} is {fm.ac(second_payment)}. Basis is recovered proportionate to the payment. That is, because {fm.ac(second_payment)} divided by {fm.ac(property_fmv)}, or {fm.as_percent(second_payment/property_fmv)}, of the payments are received, the same percentage of gain realized is recognized.</p>'
                )
                judgements[gain_second_payment_pro_rata_with_453] = (
                    f'<p>This would be correct if <a href="https://www.law.cornell.edu/uscode/text/26/453" target="_new" rel="noreferrer">Section 453(e)</a> applied. But it does not, because "{relationship}" does not count as a related party under <a href="https://www.law.cornell.edu/uscode/text/26/267" target="_new" rel="noreferrer">Section 267</a>.</p>'
                )

            if how_far_after > 730:

                judgements[correct] = (
                    f'<p>Correct! <a href="https://www.law.cornell.edu/uscode/text/26/453" target="_new" rel="noreferrer">Section 453(e)</a> does not apply, because {relationship} is not described in <a href="https://www.law.cornell.edu/uscode/text/26/267" target="_new" rel="noreferrer">Section 267</a>. (In addition, the sale to {person3.name} happened more than two years after the initial sale from {person1.name} to {person2.name} and thus exceeds the two-year cutoff described in 453(e)(2).) Therefore the regular rules apply. the note itself is not considered a payment; gain on the amount of the note is not recognized until the note is paid. Thus the payment in {str(second_payment_year)} is {fm.ac(second_payment)}. Basis is recovered proportionate to the payment. That is, because {fm.ac(second_payment)} divided by {fm.ac(property_fmv)}, or {fm.as_percent(second_payment/property_fmv)}, of the payments are received, the same percentage of gain realized is recognized.</p>'
                )
                judgements[gain_second_payment_pro_rata_with_453] = (
                    f'<p>This would be correct if <a href="https://www.law.cornell.edu/uscode/text/26/453" target="_new" rel="noreferrer">Section 453(e)</a> applied. But it does not, because "{relationship}" does not count as a related party under <a href="https://www.law.cornell.edu/uscode/text/26/267" target="_new" rel="noreferrer">Section 267</a>. In addition, the sale to {person3.name} happened more than two years after the initial sale from {person1.name} to {person2.name} and thus exceeds the two-year cutoff described in 453(e)(2).</p>'
                )

        elif how_far_after > 730:

            correct = gain_second_payment_prorata

            possibleanswers = [
                gain_second_payment_basis_first,
                gain_second_payment_basis_last,
                gain_second_payment_full_note_as_payment,
                gain_second_payment_prorata,
                random_payment,
            ]

            judgements = {
                correct: f'<p>Correct! <a href="https://www.law.cornell.edu/uscode/text/26/453" target="_new" rel="noreferrer">Section 453(e)</a> does not apply, because the sale to {person3.name} happened more than two years after the initial sale from {person1.name} to {person2.name}. Therefore the regular installment sale rules apply. The note itself is not considered a payment; gain on the amount of the note is not recognized until the note is paid. Thus the payment in {str(second_payment_year)} is {fm.ac(second_payment)}. Basis is recovered proportionate to the payment. That is, because {fm.ac(second_payment)} divided by {fm.ac(property_fmv)}, or {fm.as_percent(second_payment/property_fmv)}, of the payments are received, the same percentage of gain realized is recognized.</p>',
                gain_second_payment_pro_rata_with_453: f'<p>This would be correct if <a href="https://www.law.cornell.edu/uscode/text/26/453" target="_new" rel="noreferrer">Section 453(e)</a> applied. But it does not, because the sale to {person3.name} happened more than two years after the initial sale from {person1.name} to {person2.name}.</p>',
                random_payment: "This number was randomly generated.",
            }

        else:

            correct = gain_second_payment_pro_rata_with_453

            possibleanswers = [
                0,
                gain_second_payment_pro_rata_with_453,
                gain_second_payment_prorata,
                random_payment,
            ]

            judgements = {
                gain_second_payment_prorata: '<p><a href="https://www.law.cornell.edu/uscode/text/26/453" target="_new" rel="noreferrer">Section 453</a> is not a punitive provision. Including the full payment means recognizing more gain than was realized. What about the amount included on the resale, due to <a href="https://www.law.cornell.edu/uscode/text/26/453" target="_new" rel="noreferrer">Section 453</a>?</p>'
            }

            if resale_price_as_payment < second_payment:

                judgements[0] = "Has all of the realized gain been recognized?"
                judgements[gain_second_payment_pro_rata_with_453] = (
                    f'<p>Correct! The gain on the second payment is {fm.ac(gain_second_payment_pro_rata_with_453)}. The amount remaining to be included after the inclusion on the resale due to <a href="https://www.law.cornell.edu/uscode/text/26/453" target="_new" rel="noreferrer">Section 453(e)</a> is considered paid, and basis is recovered pro rata. (The effect, of course, is that all of the gain remaining is recognized.)</p>'
                )

            else:

                judgements[0] = (
                    '<p>Correct. All of the gain was recognized due to the resale. No gain is left to be recognized. <a href="https://www.law.cornell.edu/uscode/text/26/453" target="_new" rel="noreferrer">Section 453(e)</a> is not a punitive provision.</p>'
                )

    problem = (
        problem_lang_intro
        + problem_lang_relative
        + problem_lang_other_comp
        + problem_lang_provides_note
        + problem_lang_sale_third_party
        + question_lang
    )

    [possibleanswers, judgements] = fm.random_answer_pot(possibleanswers, judgements, 0)

    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


def installment_sale_like_kind():

    [person1, person2] = fm.create_group()

    land_fmv = fm.nearestthousand(100000 * (1 + random.random()))

    cash_amt = 10000 * random.randint(1, 20)

    while True:
        note_amt = 10000 * random.randint(1, 20)
        if cash_amt != note_amt:
            break

    building_fmv = land_fmv + cash_amt + note_amt

    while True:
        building_basis = fm.generate_random_item(land_fmv)
        if building_basis < building_fmv:
            break

    building_gain_realized = building_fmv - building_basis

    years_until_second_payment = random.randint(4, 10)
    second_payment_year = fm.current_year + years_until_second_payment

    initial_payment_no_like_kind = land_fmv + cash_amt
    second_payment = building_fmv - initial_payment_no_like_kind

    gain_first_payment_prorata_no_like_kind = int(
        building_gain_realized * (initial_payment_no_like_kind / building_fmv)
    )

    # if like kind
    basis_remaining_for_boot = max(0, building_basis - land_fmv)
    total_boot = cash_amt + note_amt
    total_gain_recognized_like_kind = total_boot - basis_remaining_for_boot
    gain_first_year_prorata_like_kind = int(
        cash_amt * total_gain_recognized_like_kind / total_boot
    )
    cash_percent = cash_amt / total_boot

    problem_lang_intro = f"On {fm.date_for_problem()}, {person1.name} exchanges property with {person2.name}. {person1.name} provides a building that is worth {fm.ac(building_fmv)} and has a basis of {fm.ac(building_basis)}. {person1.name} used the building in {person1.poss} business. In exchange, {person2.name} provides a piece of land that is worth {fm.ac(land_fmv)} as well as cash of {fm.ac(cash_amt)} and a note with adequate stated interest in the amount of {fm.ac(note_amt)} on which all the principal is due in {str(second_payment_year)}. "

    business_use_lang_1 = " plans to use the land for business use. "
    personal_use_lang_1 = " plans to use the land for personal use. "

    business_use_lang_2 = " plans to use the building for business use. "
    personal_use_lang_2 = " plans to use the building for personal use. "

    use_lang_choice_person1 = random.choices(
        [personal_use_lang_1, business_use_lang_1], weights=(1, 4), k=1
    )[0]
    use_lang_choice_person2 = random.choice([personal_use_lang_2, business_use_lang_2])

    problem_lang_person1_use = person1.name + use_lang_choice_person1

    problem_lang_person2_use = person2.name + use_lang_choice_person2

    # possible answers
    random_payment = int(building_gain_realized * random.randint(40, 90) / 100)

    first_payment_gain_q = f"How much gain or loss, if any, does {person1.name} recognize in {str(fm.current_year)} due to the transaction?"

    question_lang = first_payment_gain_q

    problem = (
        problem_lang_intro
        + problem_lang_person1_use
        + problem_lang_person2_use
        + question_lang
    )

    possibleanswers = [
        gain_first_year_prorata_like_kind,
        building_gain_realized,
        random_payment,
        gain_first_payment_prorata_no_like_kind,
    ]

    judgements = {
        random_payment: "This number was randomly generated.",
        building_gain_realized: 'What is the signficance of the note? Consider <a href="https://www.law.cornell.edu/uscode/text/26/453" target="_new" rel="noreferrer">Section 453</a>.',
    }

    if use_lang_choice_person1 == business_use_lang_1:

        correct = gain_first_year_prorata_like_kind

        if basis_remaining_for_boot == 0:

            amt_lang = f"{person1.name}'s basis in the building is less the value of the land, so there is no basis left to offset the non-like-kind property. Thus the full cash payment in the first year is gain."

        else:

            amt_lang = f"There is {fm.ac(basis_remaining_for_boot)} left of basis for the non-like-kind portion of the transaction. The total gain recognized is therefore the total amount of the boot, {fm.ac(total_boot)}, less the basis remaining to be allocated to the non-like-kind-portion of the transaction, {fm.ac(basis_remaining_for_boot)}. This gain will be recognized proportionately as each payment is received. In the first year, {fm.ac(cash_amt)}/{fm.ac(total_boot)} = {fm.as_percent(cash_percent)} of the payment is received, so that is the percentage of the gain recognized: {fm.as_percent(cash_percent)} x {fm.ac(total_gain_recognized_like_kind)} = {fm.ac(gain_first_year_prorata_like_kind)}."

        if building_gain_realized < total_boot:

            boot_recognized_lang = f"Here, because the amount of the boot is greater than the amount of gain, the full amount of gain is recognized: {fm.ac(total_gain_recognized_like_kind)}."

        else:

            boot_recognized_lang = f"The gain recognized is therefore {fm.ac(total_gain_recognized_like_kind)} (the total amount of the boot, that is, the value of the cash plus the note)."

        judgements[gain_first_year_prorata_like_kind] = (
            f'<p>Correct! This is a like-kind exchange. {person1.name} realizes {fm.ac(building_gain_realized)} on the transaction. Because this is a like-kind exchange, {person1.name} recognizes that gain to the extent of boot received. {boot_recognized_lang} The installment method controls when that amount will be recognized, as described in <a href="https://www.law.cornell.edu/uscode/text/26/453" target="_new" rel="noreferrer">Section 453(f)(6)</a>. Conceptually, the basis in the building of {fm.ac(building_basis)} goes first to the like-kind portion. {amt_lang}</p>'
        )

        if use_lang_choice_person2 == personal_use_lang_2:

            judgements[gain_first_payment_prorata_no_like_kind] = (
                f'<p>How do the like-kind rules of <a href="https://www.law.cornell.edu/uscode/text/26/1031" target="_new" rel="noreferrer">Section 1031</a> interact with the installment sale rules? For example, is {person2.name}\'s planned use of the property relevant to your analysis?</p>'
            )

        else:

            judgements[gain_first_payment_prorata_no_like_kind] = (
                f'<p>How do the like-kind rules of <a href="https://www.law.cornell.edu/uscode/text/26/1031" target="_new" rel="noreferrer">Section 1031</a> interact with the installment sale rules?</p>'
            )

    else:
        correct = gain_first_payment_prorata_no_like_kind

        judgements[gain_first_payment_prorata_no_like_kind] = (
            f"Correct! Because {person1.name} will use the land for personal use, this is not a like-kind exchange. Therefore the regular installment sale rules apply, and the basis is recovered pro rata."
        )
        judgements[gain_first_year_prorata_like_kind] = (
            "Is this a like-kind exchange? How will the received property be used?"
        )

    [possibleanswers, judgements] = fm.random_answer_pot(possibleanswers, judgements, 0)
    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


def installment_sales():
    rn = random.randint(1, 4)

    if rn == 1:
        return installment_sale_plain()
    elif rn == 2:
        return installment_sale_related_party()
    elif rn == 3:
        return installment_sale_debt()
    elif rn == 4:
        return installment_sale_like_kind()


def depreciation_question(type_problem="random"):

    person1 = fm.create_person()

    asset = random.choice(dp.full_asset_list)

    if type_problem == "sold":
        sold = True
    elif type_problem == "not sold":
        sold = False
    else:
        sold = random.choice([True, False])

    initial_basis = 1000 * random.randint(10, 40)

    while True:
        years_passed = round(random.random() * asset.recovery_period)
        if years_passed > 0 and years_passed < asset.recovery_period:
            break

    question_year = fm.current_year + years_passed

    sale_date = fm.month_day(fm.pick_random_date()) + ", " + str(question_year)

    if person1.gender == "nonbinary":
        usepronoun = "use"
    else:
        usepronoun = "uses"

    problem_lang = f"{person1.name} has a {asset.name} that {person1.nom} {usepronoun} in {person1.poss} business."

    if asset.listed == False:
        period_lang = (
            f" The class life of the {asset.name} is {asset.class_life} years."
        )

    else:
        period_lang = f" Refer to the statute for the relevant recovery period for the {asset.name}."

    acq_lang = f" {person1.name} acquired the {asset.name} on {fm.date_for_problem()}, for {fm.ac(initial_basis)} and put it into use on that same date."

    if sold == True:
        sale_lang = f" On {sale_date}, {person1.name} sells the {asset.name}."

    else:
        sale_lang = ""

    question_lang = f" How much depreciation may {person1.name} take in {str(question_year)} with respect to the {asset.name}? (Assume that Section 168(k) does not apply, and also assume that many other depreciable assets were put into use throughout the year.)"

    problem = problem_lang + period_lang + acq_lang + sale_lang + question_lang

    # possible answers

    year_depreciation = int(
        round(fm.depreciate_asset(asset, years_passed, initial_basis, sold)[1])
    )
    no_disposal = year_depreciation * 2
    straight_line_no_disposal = int(round(initial_basis / asset.recovery_period))
    class_life_straight_line = int(round(initial_basis / asset.class_life))

    possibleanswers_real = [
        year_depreciation,
        no_disposal,
        straight_line_no_disposal,
        class_life_straight_line,
    ]
    random_answer = random.randint(min(possibleanswers_real), max(possibleanswers_real))

    possibleanswers = [
        year_depreciation,
        straight_line_no_disposal,
        class_life_straight_line,
        random_answer,
    ]

    judgements = {
        straight_line_no_disposal: '<p>What is the method of depreciation that applies to this asset? Consider <a href="https://www.law.cornell.edu/uscode/text/26/168" target="_new" rel="noreferrer">Section 168(b)</a>.</p>',
        random_answer: "This number was randomly generated.",
        class_life_straight_line: '<p>Is the class life the same as the recovery period? Also, what is the method of depreciation that applies to this asset? Consider <a href="https://www.law.cornell.edu/uscode/text/26/168" target="_new" rel="noreferrer">Section 168(b)</a>.</p>',
    }

    correct = year_depreciation

    if sold == True:
        possibleanswers.append(no_disposal)
        possibleanswers.append(straight_line_no_disposal)

        judgements[year_depreciation] = (
            f'<p>Correct! To obtain this answer, apply the correct schedule from <a href="/assets/RevProc87-57.pdf" target="_new">Rev. Proc. 87-57</a> to the initial basis. Specifically, this property has a recovery period of {asset.recovery_period} years, starting and ending with a half year of depreciation, and this is year {years_passed+1} of that time. Moreover, the {asset.name} was sold, and there is deemed to be half a year of depreciation available in the year sold.</p>'
        )
        judgements[no_disposal] = (
            f'<p>This would be correct if the {asset.name} had not been sold. But what about the convention, as described in <a href="https://www.law.cornell.edu/uscode/text/26/168" target="_new" rel="noreferrer">Section 168(d)</a>?</p>'
        )
        judgements[straight_line_no_disposal] = (
            '<p>What is the method of depreciation that applies to this asset? Consider <a href="https://www.law.cornell.edu/uscode/text/26/168" target="_new" rel="noreferrer">Section 168(b)</a>. Also consider the relevant convention, as in Section 168(d).</p>'
        )

    else:

        judgements[year_depreciation] = (
            f'<p>Correct! To obtain this answer, apply the correct schedule from <a href="/assets/RevProc87-57.pdf" target="_new">Rev. Proc. 87-57</a> to the initial basis. Specifically, this property has a recovery period of {asset.recovery_period} years, starting and ending with a half year of depreciation, and this is year {years_passed+1} of that time.</p>'
        )
        judgements[straight_line_no_disposal] = (
            '<p>What is the method of depreciation that applies to this asset? Consider <a href="https://www.law.cornell.edu/uscode/text/26/168" target="_new" rel="noreferrer">Section 168(b)</a>.</p>'
        )

    possibleanswers = list(set(possibleanswers))
    while len(possibleanswers) < 5:
        (possibleanswers, judgements) = fm.random_answer_ones(
            possibleanswers, judgements
        )

    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


def cap_gain_netting():

    def excess_of(x, y):
        return max(0, x - y)

    def create_stock_facts(loss_gain, long_or_short, name_list=[]):
        year = fm.current_year
        while True:
            corp_name = fm.pick_entity_name()
            if corp_name not in name_list:
                break

        loss_dictionary = {"start": 60, "end": 90}
        gain_dictionary = {"start": 110, "end": 140}

        loss_gain_dict = {"loss": loss_dictionary, "gain": gain_dictionary}

        relevant_dict = loss_gain_dict[loss_gain]

        start = relevant_dict["start"]
        end = relevant_dict["end"]

        purchase_price = 500 * random.randint(20, 80)
        sale_price = int(fm.generate_random_item(purchase_price, start, end))

        gain_or_loss_amount = sale_price - purchase_price

        while True:
            date_sold = fm.pick_random_date_given_year(year)
            if date_sold.month > 2:
                break

        if long_or_short == "long":
            date_purchased = fm.date_before(date_sold, soonest=366, latest=15 * 365)
        elif long_or_short == "short":
            while True:
                date_purchased = fm.date_before(date_sold, soonest=90, latest=360)
                if date_purchased.year != date_sold.year:
                    break

        problem_facts = f"On {fm.full_date(date_sold)}, they sell {corp_name}, stock for {fm.ac(sale_price)}. They bought the {corp_name}, stock for {fm.ac(purchase_price)} on {fm.full_date(date_purchased)}."

        answer_facts = f"The sale of the {corp_name}, stock generates {fm.ac(abs(gain_or_loss_amount))} of {long_or_short}-term capital {loss_gain}. "

        stock_dict = {
            "corp_name": corp_name,
            "problem_facts": problem_facts,
            "answer_facts": answer_facts,
            "date_purchased": date_purchased,
            "date_sold": date_sold,
            "sale_price": sale_price,
            "gain_loss_amount": gain_or_loss_amount,
            "length": long_or_short,
            "loss_gain": loss_gain,
        }

        return stock_dict

    person1 = fm.create_person()

    number_of_assets = random.randint(2, 4)
    selected_assets = []

    pair_list = []
    stock_dict_list = []

    random_spread = random.choice(["random", "spread"])

    def create_pairing():
        loss_gain = random.choice(["loss", "gain"])
        length = random.choice(["long", "short"])
        return [loss_gain, length]

    if random_spread == "random":
        for n in range(number_of_assets):
            pair_list.append(create_pairing())

    else:
        for n in range(number_of_assets):
            while True:
                pairing = create_pairing()
                if pairing not in pair_list:
                    pair_list.append(pairing)
                    break

    for pair in pair_list:
        stock_dict = create_stock_facts(pair[0], pair[1], name_list=selected_assets)
        stock_dict_list.append(stock_dict)
        selected_assets.append(stock_dict["corp_name"])

    asset_purchase_lang = answer_lang = ""
    STCL = STCG = LTCL = LTCG = net_all_gains_losses = net_all_gains = 0
    list_of_prices = []

    for stock_dict in stock_dict_list:

        asset_purchase_lang += f"\n- {stock_dict['problem_facts']}"

        answer_lang += f" {stock_dict['answer_facts']}"

        net_all_gains_losses += stock_dict["gain_loss_amount"]

        identifier_pair = [stock_dict["loss_gain"], stock_dict["length"]]

        if identifier_pair == ["gain", "long"]:

            LTCG = LTCG + stock_dict["gain_loss_amount"]
            net_all_gains = stock_dict["gain_loss_amount"]

        elif identifier_pair == ["loss", "long"]:
            LTCL = LTCL - stock_dict["gain_loss_amount"]
            print(
                f'The new long term loss is {stock_dict["gain_loss_amount"]} and long term capital loss is now {LTCL}'
            )

        elif identifier_pair == ["gain", "short"]:
            STCG = STCG + stock_dict["gain_loss_amount"]
            net_all_gains = net_all_gains + stock_dict["gain_loss_amount"]

        else:
            STCL = STCL - stock_dict["gain_loss_amount"]
            print(
                f'The new loss is {stock_dict["gain_loss_amount"]} and short term capital loss is now {STCL}'
            )

    net_STCL = excess_of(STCL, STCG)
    net_LTCG = excess_of(LTCG, LTCL)

    net_CG = excess_of(net_LTCG, net_STCL)

    ordinary_income = 500 * random.randint(10, 60)

    total_gains = LTCG + STCG
    total_losses = STCL + LTCL

    if total_losses > total_gains:
        type_question = "loss_carryforward"
    else:
        type_question = "capital_gains"

    net_CG = excess_of(net_LTCG, net_STCL)

    if type_question == "capital_gains":

        problem_lang = f"In {fm.current_year}, {person1.name} engages in the following transactions. {person1.name} sells no other capital or quasi-capital assets in {fm.current_year} and holds all stock for investment.\n{asset_purchase_lang}"

        question_lang = f"\n\nHow much is taxed at the preferential capital gains rate for {person1.name} in {fm.current_year}?"

        number_list = [net_CG, net_all_gains_losses, net_all_gains]

        while True:

            if net_CG != 0:
                random_answer = fm.generate_random_item(net_CG, 70, 120) + 500
            elif net_all_gains_losses != 0:
                random_answer = (
                    fm.generate_random_item(net_all_gains_losses, 70, 120) + 500
                )
            else:
                random_answer = 500 * random.randrange(51, 151, 2)

            if random_answer != 0 and random_answer not in number_list:
                break

        possibleanswers = [net_CG, net_all_gains_losses, net_all_gains, random_answer]
        correct = net_CG

        judgements = {
            correct: f"That is correct! The amount taxed at the preferential rate is the net capital gain. The net capital gain is the excess of net long term capital gain, which is {fm.ac(net_LTCG)}, over net short term capital loss, which is {fm.ac(net_STCL)}. More specifically: {answer_lang}",
            random_answer: "This answer was randomly generated.",
        }

        if net_CG != net_all_gains:

            judgements = fm.merge(
                judgements,
                {
                    net_all_gains: '<p>You netted all the capital gains. How do the capital losses figure in? Consider <a href="https://www.law.cornell.edu/uscode/text/26/1222" target="_new" rel="noreferrer">Section 1222(11)(b)</a>, and work back through the definitions of the various terms.</p>'
                },
            )

        if net_all_gains_losses not in [net_CG, net_all_gains]:

            judgements = fm.merge(
                judgements,
                {
                    net_all_gains_losses: '<p>You netted all the gains and losses. But netting all the capital gains and losses does not result in net capital gain, which is a defined term. In particular, consider <a href="https://www.law.cornell.edu/uscode/text/26/1222" target="_new" rel="noreferrer">Section 1222(11)(b)</a>, and work back through the definitions of the various terms.</p>'
                },
            )

    else:
        question_lang = f"Assume there are no capital loss carryforwards from previous years. How much capital loss, if any, does {person1.name} carry to {fm.current_year+1}?"
        problem_lang = f"In {fm.current_year}, {person1.name} engages in the following transactions. {person1.name} sells no other capital or quasi-capital assets in {fm.current_year} and holds all stock for investment.{asset_purchase_lang}\n\n{person1.name} also has {fm.ac(ordinary_income)} of ordinary income in {fm.current_year}."
        usable_loss = min(total_gains + 3000, total_losses)
        loss_carryforward = total_losses - usable_loss
        soak_up_all_OI_usable = min(total_gains + ordinary_income, total_losses)
        loss_carryforward_soak_up_all_OI = total_losses - soak_up_all_OI_usable
        usable_loss_no_3000 = min(total_gains, total_losses)
        loss_carryforward_no_3000 = total_losses - usable_loss_no_3000

        number_list = [
            loss_carryforward,
            loss_carryforward_soak_up_all_OI,
            loss_carryforward_no_3000,
            usable_loss,
            0,
        ]
        while True:

            if loss_carryforward != 0:
                random_answer = (
                    fm.generate_random_item(loss_carryforward, 80, 120) + 500
                )

            else:
                random_answer = 500 * random.randrange(11, 61, 2)

            if random_answer not in number_list:
                break

        possibleanswers = [
            loss_carryforward,
            loss_carryforward_soak_up_all_OI,
            loss_carryforward_no_3000,
            usable_loss,
            random_answer,
            0,
        ]

        correct = loss_carryforward

        if correct == 0:

            judgements = {
                correct: f'<p>That is correct! {person1.name} is an individual, so the losses that may be used in {fm.current_year} equal the total amount of capital gains plus up to $3,000 of ordinary income. <a href="https://www.law.cornell.edu/uscode/text/26/1211" target="_new" rel="noreferrer">Section 1211(b)</a>. Put another way, once the losses soak up all the capital gains, up to $3,000 of the losses may be used to absorb up to $3,000 of ordinary income. Here, because the total losses, {fm.ac(total_losses)}, do not exceed the total gains, {fm.ac(total_gains)}, plus $3,000, there were no losses left to carry forward. More specifically: {answer_lang}</p>',
                usable_loss: f"That is the correct amount of loss that can be used in {fm.current_year}. But the question asks how much loss can be carried forward.",
                random_answer: "This answer was randomly generated.",
            }

        if correct > 0:

            judgements = {
                correct: f'<p>That is correct! {person1.name} is an individual, so the losses that may be used in {fm.current_year} equal the total amount of capital gains, {fm.ac(total_gains)}, plus up to $3,000 of ordinary income. <a href="https://www.law.cornell.edu/uscode/text/26/1211" target="_new" rel="noreferrer">Section 1211(b)</a>. Here, because the total losses, {fm.ac(total_losses)}, exceed the total gains, {fm.ac(total_gains)}, plus $3,000 by {fm.ac(loss_carryforward)}, that amount can be carried forward. More specifically: {answer_lang} </p>',
                loss_carryforward_soak_up_all_OI: f'<p>What about the limitations in <a href="https://www.law.cornell.edu/uscode/text/26/1211" target="_new" rel="noreferrer">Section 1211(b)(1)</a>?</p>',
                loss_carryforward_no_3000: f'<p>What about the $3000 referred to in <a href="https://www.law.cornell.edu/uscode/text/26/1211" target="_new" rel="noreferrer">Section 1211(b)(1)</a>?</p>',
                0: f"{person1.name} is an individual, so the losses that may be used in {fm.current_year} equal the total amount of capital gains, {fm.ac(total_gains)}, plus up to $3,000. But the total losses are greater than {fm.ac(total_gains+3000)}. What happens to the rest of the losses?",
                random_answer: "This answer was randomly generated.",
            }

    problem = f"{problem_lang}\n\n{question_lang}"

    possibleanswers = list(set(possibleanswers))
    while len(possibleanswers) < 5:
        (possibleanswers, judgements) = fm.random_answer_pot(
            possibleanswers, judgements, 3, start=60, end=110
        )

    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


def section_1231_netting():
    person1 = fm.create_person()

    if person1.gender == "nonbinary":
        usepronoun = "use"
    else:
        usepronoun = "uses"

    number_of_assets = random.randint(3, 5)
    selected_assets = []
    assets_for_problem = []

    for n in range(number_of_assets):
        while True:
            listasset = dp.create_asset_facts()
            if listasset.asset not in selected_assets:
                selected_assets.append(listasset.asset)
                assets_for_problem.append(listasset)
                break

    # initialize variables
    asset_purchase_lang = ""
    answer_lang = ""
    loss_OI = gain_OI = loss_1231 = gain_1231 = net_all_gains_losses = (
        net_all_gains_losses
    ) = 0

    for item in assets_for_problem:
        asset_purchase_lang += f"\n- {item.problem_facts}"
        answer_lang += " " + item.answer_facts_1231

        gainloss = item.sale_price - item.purchase_price
        net_all_gains_losses = net_all_gains_losses + gainloss

        if item.long_or_short == "long":

            if gainloss > 0:
                gain_1231 = gain_1231 + gainloss

            else:
                loss_1231 = loss_1231 - gainloss

        elif item.long_or_short == "short":

            if gainloss > 0:
                gain_OI = gain_OI + gainloss

            else:
                loss_OI = loss_OI - gainloss

    net_1231 = gain_1231 - loss_1231
    net_OI = gain_OI - loss_OI

    if net_1231 <= 0:
        compare_language = "do not exceed"
        type_of_1231 = "ordinary"

    else:
        type_of_1231 = "long-term capital"
        compare_language = "exceed"

    correct_lang = f"That is correct! The total amount of 1231 gains is {fm.ac(gain_1231)}. The total amount of 1231 losses is {fm.ac(loss_1231)}. Because the 1231 gains {compare_language} the 1231 losses, all 1231 gains and losses are {type_of_1231} gains and losses under Section 1231(a)."

    if net_1231 < 0:
        total_OI = net_OI + net_1231

    else:
        total_OI = net_OI

    problem_lang = f"In {fm.current_year}, {person1.name} sells the following assets, each of which {person1.nom} {usepronoun} in {person1.poss} business. {person1.name} sells no other assets in {fm.current_year} that {person1.nom} used in {person1.poss} business. All assets were put into use on the day purchased. Assume that all the assets are depreciable, but that the basis at sale equals purchase price--that is, there has been no depreciation. This is a wildly unrealistic, indeed, incoherent assumption, but it will help you focus on the specific issue of netting 1231 gains and losses for now.\n\n{asset_purchase_lang}"

    question_lang = f"\n\nHow much net ordinary gain or loss does {person1.name} have in {fm.current_year} due to these transactions?"

    problem = problem_lang + question_lang

    correct = total_OI

    capital_all_gains_losses = 0
    ordinary_all_gains_losses = net_all_gains_losses

    possibleanswers = [total_OI, capital_all_gains_losses, ordinary_all_gains_losses]

    possibleanswers = list(set(possibleanswers))

    while len(possibleanswers) < 5:
        while True:
            if net_1231 != 0:
                random_answer = fm.generate_random_item_hund(net_1231, 80, 120)
            else:
                random_answer = 500 * random.randint(10, 60)
            if random_answer not in possibleanswers:
                possibleanswers.append(random_answer)
                break

    if net_1231 < 0:

        if net_OI != 0:

            judgements = {
                correct: f"{correct_lang} Additionally, there is a net of {fm.ac(net_OI)} from assets that were held for less than one year and thus are not Section 1231 assets. This is a total of {fm.ac(total_OI)} treated as ordinary income. More specifically: {answer_lang}",
                random_answer: "This number was randomly generated.",
            }

        else:

            judgements = {
                correct: f"{correct_lang}. There is no other source of ordinary income or loss from the disposition of these assets. More specifically: {answer_lang}",
                random_answer: "This number was randomly generated.",
            }

    else:

        if net_OI != 0:

            judgements = {
                correct: f"{correct_lang} Additionally, there is a net of {fm.ac(net_OI)} from assets that were held for less than one year and thus are not Section 1231 assets. This is a total of {fm.ac(total_OI)} treated as ordinary. More specifically: {answer_lang}",
                random_answer: "This number was randomly generated.",
            }

        else:

            judgements = {
                correct: f"{correct_lang} There is no other source of ordinary income or loss from the disposition of these assets. More specifically: {answer_lang}",
                random_answer: "This number was randomly generated.",
            }

    if net_OI != capital_all_gains_losses:

        judgements[capital_all_gains_losses] = (
            '<p>You treated all gains and losses as capital. What about <a href="https://www.law.cornell.edu/uscode/text/26/1231" target="_new" rel="noreferrer">Section 1231(a)(2)</a>?</p>'
        )

    if ordinary_all_gains_losses not in [total_OI, capital_all_gains_losses]:

        judgements[ordinary_all_gains_losses] = (
            '<p>You treated all gains and losses as ordinary. What about <a href="https://www.law.cornell.edu/uscode/text/26/1231" target="_new" rel="noreferrer">Section 1231(a)(1)</a>?</p>'
        )

    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


def recapture():
    person1 = fm.create_person()

    asset = random.choice(dp.full_asset_list)

    if person1.gender == "nonbinary":
        usepronoun = "use"
    else:
        usepronoun = "uses"

    initial_basis = 1000 * random.randint(10, 40)

    while True:
        years_passed = round(random.random() * asset.recovery_period)
        if years_passed > 1 and years_passed < asset.recovery_period:
            break

    total_depreciation = int(
        fm.depreciate_asset(asset, years_passed, initial_basis, sold=True)[0]
    )
    basis_with_depreciation = initial_basis - total_depreciation

    possiblelevels = [
        "below basis with depreciation",
        "above original basis",
        "between original basis and basis with depreciation",
    ]

    level_of_sale = random.choice(possiblelevels)

    if level_of_sale == "below basis with depreciation":
        while True:
            sale_price = fm.generate_random_item_ones(basis_with_depreciation, 60, 90)
            if sale_price < basis_with_depreciation:
                break

    elif level_of_sale == "above original basis":
        while True:
            sale_price = fm.generate_random_item(initial_basis, 105, 120)
            if sale_price > initial_basis:
                break

    else:
        while True:
            sale_price = fm.nearestthousand(
                random.randint(basis_with_depreciation, initial_basis)
            )
            if (
                sale_price not in [basis_with_depreciation, initial_basis]
                and basis_with_depreciation < sale_price < initial_basis
            ):
                break

    gainloss = sale_price - basis_with_depreciation
    recomputed_basis = basis_with_depreciation + total_depreciation

    if gainloss > 0:
        recapture = min(recomputed_basis, sale_price) - basis_with_depreciation
    else:
        recapture = 0

    question_year = fm.current_year + years_passed

    sale_date = fm.month_day(fm.pick_random_date()) + ", " + str(question_year)

    problem_lang = f"{person1.name} has a {asset.name} that {person1.nom} {usepronoun} in {person1.poss} business."

    if asset.listed == False:
        period_lang = (
            f" The class life of the {asset.name} is {asset.class_life} years."
        )
    else:
        period_lang = f" Refer to the statute for the relevant recovery period for the {asset.name}."

    acq_lang = f" {person1.name} acquired the {asset.name} on {fm.date_for_problem()}, for {fm.ac(initial_basis)}, and put the {asset.name} into use that same day. On {sale_date}, {person1.name} sells the {asset.name} for {fm.ac(sale_price)}. {person1.name} may or may not have disposed of other assets used in business in {question_year}."

    question_lang_character = f" What is the character of the gain or loss that {person1.name} recognizes due to the sale of the {asset.name}? (Assume that Section 168(k) does not apply.)"

    question_lang_ordinary_income = f" What is the minimum amount of ordinary gain or loss that {person1.name} recognizes due to the sale of the {asset.name}? (Assume that Section 168(k) does not apply.)"

    possible_questions = [question_lang_character, question_lang_ordinary_income]

    question_lang = random.choice(possible_questions)

    problem = problem_lang + period_lang + acq_lang + question_lang

    # question is overall character of the gain or loss
    if question_lang == possible_questions[0]:

        possibleanswers = [
            "Gain, some of which is ordinary, and some of which is 1231 gain, which will be characterized based on other 1231 transactions.",
            "Gain, all of which is ordinary.",
            "Gain, all of which is 1231 gain, which will be characterized based on other 1231 transactions.",
            "Gain, some of which is ordinary, and some of which is capital.",
            "Gain, all of which is capital.",
            "Loss, some of which is ordinary, and some of which is 1231 loss, which will be characterized based on other 1231 transactions.",
            "Loss, all of which is ordinary.",
            "Loss, all of which is 1231 loss, which will be characterized based on other 1231 transactions.",
            "Loss, some of which is ordinary, and some of which is capital.",
            "Loss, all of which is capital.",
        ]

        if level_of_sale == "below basis with depreciation":

            correct = "Loss, all of which is 1231 loss, which will be characterized based on other 1231 transactions."

            judgements_for_gain = {
                "Gain, some of which is ordinary, and some of which is 1231 gain, which will be characterized based on other 1231 transactions.": "This sale generates loss. Consider depreciation.",
                "Gain, all of which is ordinary.": "This sale generates loss. Consider depreciation.",
                "Gain, all of which is 1231 gain, which will be characterized based on other 1231 transactions.": "This sale generates loss. Consider depreciation.",
                "Gain, some of which is ordinary, and some of which is capital.": "This sale generates loss. Consider depreciation.",
                "Gain, all of which is capital.": "This sale generates loss. Consider depreciation.",
            }

            judgements_for_loss = {
                "Loss, some of which is ordinary, and some of which is 1231 loss, which will be characterized based on other 1231 transactions.": "You are correct that loss is generated. But why is some of the loss ordinary?",
                "Loss, all of which is ordinary.": "You are correct that loss is generated. But why is the loss ordinary?",
                "Loss, all of which is 1231 loss, which will be characterized based on other 1231 transactions.": f"Correct. Due to the total depreciation of {fm.ac(total_depreciation)}, the basis at sale was {fm.ac(basis_with_depreciation)}. Because the sale price was below the basis, the sale resulted in loss. Because the {asset.name} was used for business, was held for more than one year, and is depreciable, the {asset.name} is a quasi-capital asset, so any loss will be 1231 loss. We cannot know its character without knowing about {person1.poss} other 1231 gains and losses for the year.",
                "Loss, some of which is ordinary, and some of which is capital.": f'<p>This is not a capital asset. Consider <a href="https://www.law.cornell.edu/uscode/text/26/1221" target="_new" rel="noreferrer">Section 1221(a)(2)</a>. How can you determine the character of the loss?</p>',
                "Loss, all of which is capital.": f'<p>This is not a capital asset. Consider <a href="https://www.law.cornell.edu/uscode/text/26/1221" target="_new" rel="noreferrer">Section 1221(a)(2)</a>. How can you determine the character of the loss?</p>',
            }

        elif level_of_sale == "above original basis":

            correct = "Gain, some of which is ordinary, and some of which is 1231 gain, which will be characterized based on other 1231 transactions."

            judgements_for_gain = {
                "Gain, some of which is ordinary, and some of which is 1231 gain, which will be characterized based on other 1231 transactions.": "Correct! Because the sale price is greater than the original basis, all of the depreciation will be recaptured. The gain due to the excess of the sale price over the original basis will be 1231 gain.",
                "Gain, all of which is ordinary.": "Some of the gain, that due to the recapture of the depreciation, will definitely be ordinary. But how can you determine the character of the gain due to the excess of the sale price over the original basis?",
                "Gain, all of which is 1231 gain, which will be characterized based on other 1231 transactions.": "Consider depreciation and recapture.",
                "Gain, some of which is ordinary, and some of which is capital.": "Some of the gain, that due to the recapture of the depreciation, will definitely be ordinary. But how can you determine the character of the gain due to the excess of the sale price over the original basis.",
                "Gain, all of which is capital.": "What about recapture? Also, how can you determine the character of the gain not due to recapture?",
            }

            judgements_for_loss = {
                "Loss, some of which is ordinary, and some of which is 1231 loss, which will be characterized based on other 1231 transactions.": "This sale generates gain, not loss. Double-check your depreciation calculations",
                "Loss, all of which is ordinary.": "This sale generates gain, not loss. Double-check your depreciation calculations.",
                "Loss, all of which is 1231 loss, which will be characterized based on other 1231 transactions.": "This sale generates gain, not loss. Double-check your depreciation calculations.",
                "Loss, some of which is ordinary, and some of which is capital.": "This sale generates gain, not loss. Double-check your depreciation calculations.",
                "Loss, all of which is capital.": "This sale generates gain, not loss. Double-check your depreciation calculations.",
            }

        elif level_of_sale == "between original basis and basis with depreciation":

            correct = "Gain, all of which is ordinary."

            judgements_for_gain = {
                "Gain, some of which is ordinary, and some of which is 1231 gain, which will be characterized based on other 1231 transactions.": "The gain due to recapture is ordinary. Is there other gain?",
                "Gain, all of which is ordinary.": f'<p>Correct! All of the gain is due to depreciation, so all of the gain is recharacterized as ordinary due to <a href="https://www.law.cornell.edu/uscode/text/26/1245" target="_new" rel="noreferrer">Section 1245</a> recapture.</p>',
                'Gain, all of which is 1231 gain, which will be characterized based on all <a href="https://www.law.cornell.edu/uscode/text/26/1231" target="_new" rel="noreferrer">Section 1231</a> transactions for the year.': "Consider depreciation and recapture.",
                "Gain, some of which is ordinary, and some of which is capital.": "The gain due to recapture is ordinary. Is there other gain?",
                "Gain, all of which is capital.": "What about recapture?",
            }

            judgements_for_loss = {
                "Loss, some of which is ordinary, and some of which is 1231 loss, which will be characterized based on other 1231 transactions.": "This sale generates gain, not loss. Double-check your depreciation calculations",
                "Loss, all of which is ordinary.": "This sale generates gain, not loss. Double-check your depreciation calculations.",
                "Loss, all of which is 1231 loss, which will be characterized based on all Section 1231 transactions for the year.": "This sale generates gain, not loss. Double-check your depreciation calculations.",
                "Loss, some of which is ordinary, and some of which is capital.": "This sale generates gain, not loss. Double-check your depreciation calculations.",
                "Loss, all of which is capital.": "This sale generates gain, not loss. Double-check your depreciation calculations.",
            }

        judgements = fm.merge(judgements_for_gain, judgements_for_loss)

        formattedjudgements = fm.format_dict(judgements, "words")

        cleananswers = possibleanswers

    if question_lang == question_lang_ordinary_income:

        possibleanswersbegin = [recapture, total_depreciation, gainloss, 0]

        while True:
            random_answer = total_depreciation + 500 * random.randint(1, 15)
            if random_answer not in possibleanswersbegin:
                break

        possibleanswers = possibleanswersbegin + [random_answer]

        if level_of_sale == "below basis with depreciation":

            correct = 0

            judgements = {
                correct: f'<p>That is correct. Because the total depreciation, {fm.ac(total_depreciation)}, results in a basis, {fm.ac(basis_with_depreciation)}, that exceeds the sale price, the disposition results in loss. <a href="https://www.law.cornell.edu/uscode/text/26/1245" target="_new" rel="noreferrer">Section 1245</a> does not result in recapture when there is a loss on the sale. The loss is <a href="https://www.law.cornell.edu/uscode/text/26/1231" target="_new" rel="noreferrer">Section 1231</a> loss, and therefore its character is based on all 1231 transactions for the year.</p>',
                gainloss: f'<p>This is the loss generated by the sale. But <a href="https://www.law.cornell.edu/uscode/text/26/1245" target="_new" rel="noreferrer">Section 1245</a> does not result in recapture when there is a loss on the sale. Additionally, the loss is Section 1231 loss, and therefore its character is based on all <a href="https://www.law.cornell.edu/uscode/text/26/1231" target="_new" rel="noreferrer">Section 1231</a> transactions for the year. We thus cannot know its character without additional information.</p>',
                total_depreciation: 'This is the total depreciation for the asset. The sale of this asset results in a loss. Why would the total depreciation be recaptured under <a href="https://www.law.cornell.edu/uscode/text/26/1245" target="_new" rel="noreferrer">Section 1245</a>?',
                random_answer: "This number was randomly generated.",
            }

        elif level_of_sale == "above original basis":

            correct = recapture

            judgements = {
                recapture: f'<p>Correct! The total depreciation, {fm.ac(total_depreciation)}, results in a basis of {fm.ac(basis_with_depreciation)}. The portion of this gain that is due to recapture, {fm.ac(recapture)}, is ordinary income under <a href="https://www.law.cornell.edu/uscode/text/26/1245" target="_new" rel="noreferrer">Section 1245</a>. Because this is a <a href="https://www.law.cornell.edu/uscode/text/26/1231" target="_new" rel="noreferrer">Section 1231</a> asset, the remainder of the gain is 1231 gain, and its character will be determined by taking into account all 1231 gain and loss for the year.</p>',
                0: f'<p>It is true that this is a <a href="https://www.law.cornell.edu/uscode/text/26/1231" target="_new" rel="noreferrer">Section 1231</a> asset, so to the extent that the regular 1231 rules apply, we cannot know whether this gain is ordinary or capital (because that will be determined based on all 1231 transactions for the year). But what about <a href="https://www.law.cornell.edu/uscode/text/26/1245" target="_new" rel="noreferrer">Section 1245</a>?</p>',
                gainloss: "This is the full amount of gain. It is true that some of this is ordinary. But do we know that all of it is ordinary? What type of asset is this asset, given that it is a depreciable asset used in a trade or business and held for more than one year?",
                random_answer: "This number was randomly generated.",
            }

        elif level_of_sale == "between original basis and basis with depreciation":

            correct = recapture

            judgements = {
                recapture: f'<p>Correct! The total depreciation, {fm.ac(total_depreciation)}, results in a basis of {fm.ac(basis_with_depreciation)}. Because the sale price is between the original basis and the basis after depreciation, all {fm.ac(recapture)} of the gain is due to depreciation, so all is recaptured as ordinary income under <a href="https://www.law.cornell.edu/uscode/text/26/1245" target="_new" rel="noreferrer">Section 1245</a>.</p>',
                0: f'<p>It is true that this is a <a href="https://www.law.cornell.edu/uscode/text/26/1231" target="_new" rel="noreferrer">Section 1231</a> asset, so to the extent that the regular 1231 rules apply, we cannot know whether this gain is ordinary or capital (because that will be determined based on all 1231 transactions for the year). But what about <a href="https://www.law.cornell.edu/uscode/text/26/1245" target="_new" rel="noreferrer">Section 1245</a>?</p>',
                random_answer: "This number was randomly generated.",
                total_depreciation: "This is the amount of depreciation. How do you calculate the basis of the property at sale, given this amount of depreciation?",
            }

        formattedjudgements = fm.format_dict(judgements)

    possibleanswers = list(set(possibleanswers))
    while len(possibleanswers) < 5:
        possibleanswers, judgements = fm.random_answer_ones(possibleanswers, judgements)

    cleananswers = fm.create_clean_answers(possibleanswers)
    judgements_json = json.dumps(formattedjudgements)
    return [problem, cleananswers, judgements_json, correct]


def asset_sale_all():
    person1 = fm.create_person()

    number_of_assets = random.randint(1, 3)
    number_of_stock = random.randint(1, 3)
    selected_assets = []
    assets_for_problem = []
    ordinary = 0
    total_1231 = 0
    LTCL = 0
    LTCG = 0
    STCL = 0
    STCG = 0
    gross_income = 0

    asset_purchase_lang = answer_lang = ""
    losses_1231 = 0
    gains_1231 = 0

    for n in range(number_of_stock):
        while True:
            listasset = dp.create_asset_facts(type="stock")
            if listasset.asset not in selected_assets:
                selected_assets.append(listasset.asset)
                assets_for_problem.append(listasset)
                break

    for n in range(number_of_assets):
        while True:
            listasset = dp.create_asset_facts()
            if listasset.asset not in selected_assets:
                selected_assets.append(listasset.asset)
                assets_for_problem.append(listasset)
                break

    for item in assets_for_problem:
        asset_purchase_lang += f"\n- {item.problem_facts} {item.period_lang}"

        answer_lang += f" {item.answer_facts_all_netting}"
        total_1231 = total_1231 + item.amount_1231

        ordinary = ordinary + item.ordinary

        gain_or_loss = item.sale_price - item.depreciated_basis

        if gain_or_loss > 0:
            gross_income += gain_or_loss

        if item.amount_1231 < 0:
            losses_1231 += item.amount_1231
        else:
            gains_1231 += item.amount_1231

        if item.type_of_gain == "capital":
            if item.long_or_short == "long":

                if item.gain_or_loss_no_depreciation == "gain":
                    LTCG = LTCG + gain_or_loss

                elif item.gain_or_loss_no_depreciation == "loss":
                    LTCL = LTCL - gain_or_loss

            elif item.long_or_short == "short":

                if item.gain_or_loss_no_depreciation == "gain":
                    STCG = STCG + gain_or_loss

                elif item.gain_or_loss_no_depreciation == "loss":
                    STCL = STCL - gain_or_loss

    if total_1231 <= 0:
        compare_language = "do not exceed"
        type_of_1231 = "ordinary"
        ordinary = ordinary + total_1231

    else:
        type_of_1231 = "long-term capital"
        compare_language = "exceed"
        LTCG += gains_1231
        LTCL += losses_1231

    net_STCL = max(0, STCL - STCG)
    net_LTCG = max(0, LTCG - LTCL)

    total_losses = STCL + LTCL
    total_gains = STCG + LTCG

    net_CG = max(0, net_LTCG - net_STCL)

    net_CL = max(0, total_losses - total_gains)

    offsetting = max(0, min(net_CL, ordinary, 3000))

    carryforward = max(0, net_CL - offsetting)

    if ordinary < 0:
        offsetting_language = f"There is no additional ordinary gain or income; rather, there is ordinary loss of {fm.ac(-ordinary)}."

    else:
        offsetting_language = f"Before using any offsetting capital losses, there is {fm.ac(ordinary)} of ordinary income. Capital losses can be used to offset {fm.ac(offsetting)} of that, which reduces the capital losses accordingly."

    # if ordinary_total != ordinary_not_STCG:
    #     print("stcg taxable")
    #     stcg_lang = "Additionally, short-term capital gain that is not offset by capital losses is taxed at ordinary rates."
    # else:
    #     stcg_lang = ''

    if gains_1231 != 0 or losses_1231 != 0:
        answer_lang_1231 = f"<br><br>The total amount of 1231 gains is {fm.ac(gains_1231)}. The total amount of 1231 losses is {fm.ac(losses_1231)}. Because the 1231 gains {compare_language} the 1231 losses, all 1231 gains and losses are {type_of_1231} gains and losses under Section 1231(a). Thus there is an additional {fm.ac(gains_1231)} of long-term capital gain and {fm.ac(losses_1231)} of long-term capital loss."
    else:
        answer_lang_1231 = "<br><br>There are no 1231 gains or losses."

    answer_lang_capital = f"Therefore, netting all capital gains and losses, there is {fm.ac(net_LTCG)} of net long-term capital gain and {fm.ac(net_STCL)} of net short-term capital loss, resulting in {fm.ac(net_CG)} of net capital gain."

    summary_answer_lang = f"{answer_lang_1231} {answer_lang_capital}"

    problem_lang = f"In {fm.current_year}, {person1.name} sells the following assets. {person1.name} holds all stock for investment, uses each of the other assets in their business, and put each asset used for business into use the same day it was purchased. {person1.name} sells no other assets in {fm.current_year}.\n\n{asset_purchase_lang}"

    # question=random.choice(['capgain','ordinary','losscarry'])
    question = random.choice(["capgain", "losscarry"])

    if question == "capgain":
        question_lang = f"\n\nHow much net capital gain, taxed at a favorable rate, does {person1.name} have in {fm.current_year} due to these transactions?"
        summary_answer_lang_addl = ""
        correct = net_CG

    # elif question == 'ordinary':
    #     question_lang= f"<br><br>How much net ordinary gain or loss does {person1.name} have in {fm.current_year} due to these transactions?"
    #     summary_answer_lang_addl = f"Before using any offsetting capital losses, there is {fm.ac(ordinary)} of income that is not capital gain. There are {fm.ac(offsetting)} of capital losses available to offset ordinary income. Therefore, netting all ordinary gains and losses, and using the offsetting capital losses available, there is {fm.ac(ordinary_total)} of income taxed at ordinary rates.<br>"
    #     correct = ordinary_total

    elif question == "losscarry":
        question_lang = f"\n\nHow much capital loss does {person1.name} carry into {fm.current_year+1}?"

        if net_CL == 0:
            summary_answer_lang_addl = "There is no excess of capital losses over capital gains, so no losses are carried into the next year."
        else:
            summary_answer_lang_addl = f"There is an excess of {fm.ac(net_CL)} of capital losses over gains. {offsetting_language} Therefore {fm.ac(carryforward)} of losses are carried into the next year.<br>"
        correct = carryforward

    problem = problem_lang + question_lang

    answer_lang = (
        f"Correct!\n\n{answer_lang} {summary_answer_lang}\n\n{summary_answer_lang_addl}"
    )

    judgements = {correct: answer_lang}

    possibleanswers = [correct, 0]

    if correct == 0:
        possibleanswers.append(1000 * random.randint(2, 10))

    [possibleanswers, judgements] = fm.random_answer_pot(possibleanswers, judgements, 1)
    [possibleanswers, judgements] = fm.random_answer_pot(possibleanswers, judgements, 1)
    [possibleanswers, judgements] = fm.random_answer_pot(possibleanswers, judgements, 0)
    [possibleanswers, judgements] = fm.random_answer_pot(possibleanswers, judgements, 0)
    [possibleanswers, judgements] = fm.random_answer_pot(possibleanswers, judgements, 3)

    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


def section_24_credit():
    [taxpayer, spouse] = fm.create_group()

    number_of_children = random.randint(2, 4)

    type_dict = {
        "qualifying child": {
            "male": ["son", "grandson", "brother", "stepbrother", "nephew"],
            "female": ["daughter", "granddaughter", "sister", "stepsister", "niece"],
        },
        "qualifying relative": {
            "male": ["son", "grandson", "uncle"],
            "female": ["daughter", "granddaughter", "aunt"],
        },
    }

    full_credit = fm.section_24_credit_2020
    child_info = []
    child_lang = ""
    credit_amt = number_qual_child = number_qual_rel = 0
    for i in range(0, number_of_children):
        type_of_child = random.choices(["qualifying child", "qualifying relative"])
        gender = random.choice(["male", "female"])
        relationship = random.choice(type_dict[type_of_child[0]][gender])
        if gender == "male":
            child_name = random.choice(names.malenames)
        else:
            child_name = random.choice(names.femalenames)

        if type_of_child == ["qualifying child"]:
            age_child = random.randrange(3, 17)
            individual_age_lang = f", who is {age_child}"
            credit_amt += full_credit
            number_qual_child += 1

        elif type_of_child == ["qualifying relative"]:
            if relationship in type_dict["qualifying child"][gender]:
                age_child = random.choice([18])
                individual_age_lang = f", who is {age_child}"
            else:
                age_child = 0
                individual_age_lang = ""
            credit_amt += 500
            number_qual_rel += 1

        individual = [type_of_child[0], gender, relationship, age_child]
        individual_lang = (
            f" {child_name}, {taxpayer.name}'s {relationship}{individual_age_lang}"
        )

        if i == number_of_children - 2:
            child_lang = child_lang + individual_lang + "; and"
        elif i == number_of_children - 1:
            child_lang = f"{child_lang} {individual_lang}, each of whom earns less than {fm.ac(fm.exemption_amount)} in {fm.current_year}."
        else:
            child_lang = child_lang + individual_lang + ";"

        child_info.append(individual)

    possible_marital_status = ["married", "unmarried"]

    marital_status = random.choice(possible_marital_status)

    if marital_status == "married":
        pronouns = [
            f"{taxpayer.name} is married to {spouse.name}, and they file a joint tax return. They have",
            "they",
            "their",
            "provide",
            f"{taxpayer.name} and {spouse.name}",
        ]
        threshold = fm.section_24_threshold.marriedlimit
    else:
        pronouns = [
            f"{taxpayer.name} is unmarried and files as head of household. {taxpayer.name} has",
            f"{taxpayer.nom}",
            f"{taxpayer.poss}",
            "provides",
            f"{taxpayer.name}",
        ]
        threshold = fm.section_24_threshold.headofhouseholdlimit

    phaseout_type = random.choice(["phaseout full", "phaseout partial", "no phaseout"])

    if phaseout_type == "phaseout full":
        magi = int((20 * credit_amt - 1000 + threshold) * (1 + random.random()))

    elif phaseout_type == "phaseout partial":
        while True:
            magi = int(
                fm.nearesthundred(
                    random.randint(threshold, (20 * credit_amt - 1000 + threshold))
                )
            )
            true_phaseout = 50 * math.ceil((magi - threshold) / 1000)
            if credit_amt - true_phaseout > 0:
                break

    elif phaseout_type == "no phaseout":
        magi = int(fm.generate_random_item(threshold, 70, 99))

    true_phaseout = max(0, 50 * math.ceil((magi - threshold) / 1000))
    final_credit = max(0, credit_amt - true_phaseout)
    fractions_of_thousand_for_phaseout = credit_amt / 50

    no_fraction_thereof_phaseout = max(0, 50 * int((magi - threshold) / 1000))
    final_credit_no_fraction = max(0, credit_amt - no_fraction_thereof_phaseout)

    problem = f"{pronouns[0]} an AGI of {fm.ac(magi)} and {pronouns[3]} more than half the support for each of the following people who live in {pronouns[2]} house: {child_lang} What amount, if any, may {pronouns[4]} credit against {pronouns[2]} tax in {fm.current_year} due to the Section 24 credit?"

    correct = final_credit

    if final_credit != 0:
        random_answer = fm.generate_random_item(final_credit)
    else:
        random_answer = fm.generate_random_item(credit_amt)

    possibleanswers = [
        final_credit,
        0,
        credit_amt,
        final_credit_no_fraction,
        random_answer,
        true_phaseout,
    ]

    if phaseout_type == "phaseout full":

        judgements = {
            correct: f"This is correct. The number of qualifying children is {number_qual_child}. The number of dependents who are not qualifying children for purposes of the child tax credit is {number_qual_rel}. This would initially lead to a credit of {number_qual_child} x {fm.ac(full_credit)} + {number_qual_rel} x $500 = {fm.ac(credit_amt)}. However, adjusted gross income exceeds the threshold amount, {fm.ac(threshold)}, by more than {int(fractions_of_thousand_for_phaseout):,} thousands or fractions thereof, so there is sufficient AGI to phase out the entire credit.",
            credit_amt: f'<p>What about the phaseout in <a href="https://www.law.cornell.edu/uscode/text/26/24" target="_new" rel="noreferrer">24(b)</a>, as modified in Section 24(h)(3)?</p>',
            random_answer: "This number was randomly generated.",
        }

        if final_credit_no_fraction != 0:

            judgements[final_credit_no_fraction] = (
                f'<p>What is the significance of the language "or fraction thereof" in <a href="https://www.law.cornell.edu/uscode/text/26/24" target="_new" rel="noreferrer">24(b)</a>?</p>'
            )

    elif phaseout_type == "phaseout partial":

        judgements = {
            correct: f"This is correct. The number of qualifying children is {number_qual_child}. The number of dependents who are not qualifying children for purposes of the child tax credit is {number_qual_rel}. This would initially lead to a credit of {number_qual_child} x {fm.ac(full_credit)} + {number_qual_rel} x $500 = {fm.ac(credit_amt)}. However, adjusted gross income exceeds the threshold amount, {fm.ac(threshold)}, by {int(math.ceil((magi-threshold)/1000)):,} thousands or fractions thereof, so the credit is reduced by $50 x {int(math.ceil((magi-threshold)/1000)):,}, for a total of {fm.ac(credit_amt)} - {fm.ac(true_phaseout)} = {fm.ac(final_credit)}.",
            credit_amt: f'<p>What about the phaseout in <a href="https://www.law.cornell.edu/uscode/text/26/24" target="_new" rel="noreferrer">24(b)</a>, as modified in Section 24(h)(3)?</p>',
            random_answer: "This number was randomly generated.",
            0: "Is the credit entirely phased out?",
        }

        if final_credit_no_fraction != final_credit:

            judgements[final_credit_no_fraction] = (
                f'<p>What is the significance of the language "or fraction thereof" in <a href="https://www.law.cornell.edu/uscode/text/26/24" target="_new" rel="noreferrer">24(b)</a>?</p>'
            )

        if true_phaseout != final_credit:

            judgements[true_phaseout] = (
                "This is the correct phaseout. But the question is: how much credit is left after the phaseout?"
            )

    elif phaseout_type == "no phaseout":

        judgements = {
            correct: f"This is correct. The number of qualifying children is {number_qual_child}. The number of dependents who are not qualifying children for purposes of the child tax credit is {number_qual_rel}. The adjusted gross income is not above the threshold of {fm.ac(threshold)}, so the total credit is {number_qual_child} x {fm.ac(full_credit)} + {number_qual_rel} x $500 = {fm.ac(credit_amt)}, with no phaseout.",
            random_answer: "This number was randomly generated.",
            0: "Is the credit phased out?",
        }

    possibleanswers = list(set(possibleanswers))
    while len(possibleanswers) < 5:
        (possibleanswers, judgements) = fm.random_answer_hund(
            possibleanswers, judgements
        )

    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


def section_21_credit():
    [taxpayer, spouse] = fm.create_group()

    number_of_children = random.randint(1, 3)
    if number_of_children == 1:
        childword = "child"
    else:
        childword = "children"

    possible_marital_status = ["married", "unmarried"]

    marital_status = random.choice(possible_marital_status)

    if marital_status == "married":
        pronouns = [
            f"{taxpayer.name} is married to {spouse.name}, and they file a joint tax return. They have",
            "they",
            "their",
            "provide",
            "live",
        ]
        threshold = fm.section_24_threshold.marriedlimit
    else:
        pronouns = [
            f"{taxpayer.name} is unmarried and files as head of household. {taxpayer.name} has",
            f"{taxpayer.nom}",
            f"{taxpayer.poss}",
            "provides",
            "lives",
        ]
        threshold = fm.section_24_threshold.singlelimit

    child_lang = ""
    number_qual_child = 0

    for i in range(0, number_of_children):
        gender = random.choice(["male", "female"])
        if gender == "male":
            (child_name, relationship) = (random.choice(names.malenames), "son")
        else:
            (child_name, relationship) = (random.choice(names.femalenames), "daughter")

        if number_of_children == 1:
            young = random.randrange(1, 12)
            old = random.randrange(13, 18)
            age_child = random.choice([young, old])
        else:
            age_child = random.randrange(1, 12)

        individual_age_lang = f", who is {age_child}"
        if marital_status == "married":
            individual_lang = (
                f" {child_name}, {pronouns[2]} {relationship}" + individual_age_lang
            )
        else:
            individual_lang = (
                f" {child_name}, {taxpayer.name}'s {relationship}" + individual_age_lang
            )

        if age_child < 13:
            number_qual_child += 1

        if i == number_of_children - 2:
            child_lang = child_lang + individual_lang + "; and"
        elif i == number_of_children - 1:
            child_lang = child_lang + individual_lang + "."
        else:
            child_lang = child_lang + individual_lang + ";"

    threshold = 15000
    app_percent_init = 35

    max_creditable_amt = int(min(2, number_qual_child) * 3000)

    DCAP_choices = [
        [
            f"{taxpayer.name} elects the maximum amount of contribution to {taxpayer.poss} employer's dependent care assistance program ('DCAP') under Section 129.",
            5000,
        ],
        ["", 0],
    ]

    if number_qual_child > 0:
        amt_spent = int(
            fm.generate_random_item(max_creditable_amt, 70, 130)
            + random.randint(1, 9) * 100
        )
        DCAP_choice = random.choices(DCAP_choices, weights=[30, 70])[0]

    else:
        amt_spent = int(fm.generate_random_item(3000, 70, 130))
        DCAP_choice = DCAP_choices[1]

    DCAP_lang = DCAP_choice[0]
    DCAP_max = DCAP_choice[1]

    creditable_expenses_no_DCAP = min(max_creditable_amt, amt_spent)
    creditable_expenses = max(0, creditable_expenses_no_DCAP - DCAP_max)

    possible_phaseout = ["phaseout full", "phaseout partial", "no phaseout"]
    phaseout_type = random.choices(possible_phaseout, weights=[30, 40, 30])[0]

    if phaseout_type == "phaseout full":
        magi = random.randint(44000, 80000)

    elif phaseout_type == "phaseout partial":
        magi = random.randint(15000, 43000)

    elif phaseout_type == "no phaseout":
        magi = int(fm.generate_random_item(threshold, 70, 99))

    # right answer
    true_phaseout = max(0, math.ceil((magi - threshold) / 2000))
    app_percent = max(20, app_percent_init - true_phaseout)
    final_credit = int(creditable_expenses * app_percent / 100)

    # no phaseout
    final_credit_no_phaseout = int(creditable_expenses * app_percent_init / 100)

    # phaseout, no limit
    no_limit_phaseout = max(0, app_percent_init - true_phaseout)
    final_credit_no_limit_phaseout = int(creditable_expenses * no_limit_phaseout / 100)

    # phaseout, no 'fraction thereof'
    no_fraction_thereof_phaseout = max(0, int((magi - threshold) / 2000))
    final_credit_no_fraction = int(
        creditable_expenses
        * max(20, app_percent_init - no_fraction_thereof_phaseout)
        / 100
    )

    # no DCAP
    final_credit_no_DCAP = int(creditable_expenses_no_DCAP * app_percent / 100)

    if DCAP_lang == "":
        DCAP_answer_lang = ""
    else:
        DCAP_answer_lang = f'<br><br>Under the flush language of <a href="https://www.law.cornell.edu/uscode/text/26/21" target="_new" rel="noreferrer">Section 21(c)</a>, the amount of creditable expenses is reduced by the $5000 contributed to the DCAP, leaving total creditable expenses of {fm.ac(creditable_expenses)}. '

    # make some fake answers if kid isn't qualifying individual
    pretend_q_max_creditable_amt = 3000
    pretend_q_creditable_expenses = min(pretend_q_max_creditable_amt, amt_spent)
    pretend_q_final_credit_no_phaseout = int(
        pretend_q_creditable_expenses * app_percent_init / 100
    )

    pretend_q_final_credit = int(pretend_q_creditable_expenses * app_percent / 100)
    pretend_q_final_credit_no_limit_phaseout = int(
        pretend_q_creditable_expenses * no_limit_phaseout / 100
    )
    pretend_q_final_credit_no_fraction = int(
        pretend_q_creditable_expenses
        * max(20, app_percent_init - no_fraction_thereof_phaseout)
        / 100
    )

    problem = f"{pronouns[0]} an AGI of {fm.ac(magi)} and {pronouns[4]} with {pronouns[2]} {childword}: {child_lang} {fm.to_capital(pronouns[1])} spent {fm.ac(amt_spent)} on care for {pronouns[2]} {childword} in {fm.current_year}. {DCAP_lang} What amount, if any, may {pronouns[1]} credit against {pronouns[2]} {fm.current_year} tax due to the Section 21 credit?"

    correct = final_credit

    possibleanswers = [final_credit, final_credit_no_limit_phaseout, amt_spent]

    if number_of_children == 1 and age_child == old:

        possibleanswers = possibleanswers + [
            pretend_q_final_credit_no_phaseout,
            pretend_q_final_credit_no_fraction,
        ]

        judgements = {
            correct: f'<p>Correct. {taxpayer.name} has no qualifying individuals under <a href="https://www.law.cornell.edu/uscode/text/26/21" target="_new" rel="noreferrer">21(b)(1)(A)</a>, because {child_name} is older than 12.</p>',
            pretend_q_final_credit: f'<p>How old is {child_name}? Consider <a href="https://www.law.cornell.edu/uscode/text/26/21" target="_new" rel="noreferrer">21(b)(1)(A)</a></p>',
            pretend_q_final_credit_no_phaseout: f'<p>How old is {child_name}? Consider <a href="https://www.law.cornell.edu/uscode/text/26/21" target="_new" rel="noreferrer">21(b)(1)(A)</a>.</p>',
            pretend_q_final_credit_no_fraction: f'<p>How old is {child_name}? Consider <a href="https://www.law.cornell.edu/uscode/text/26/21" target="_new" rel="noreferrer">21(b)(1)(A)</a></p>',
            amt_spent: f"This is the amount that {taxpayer.name} spent, but the question is what credit is available due to those expenses.",
            pretend_q_final_credit_no_limit_phaseout: f'<p>How old is {child_name}? Consider <a href="https://www.law.cornell.edu/uscode/text/26/21" target="_new" rel="noreferrer">21(b)(1)(A)</a>.</p>',
        }

    else:

        possibleanswers = possibleanswers + [final_credit, max_creditable_amt]

        judgements = {
            amt_spent: f"This is the amount that {taxpayer.name} spent, but the question is what credit is available due to those expenses.",
            max_creditable_amt: '<p>This is the maximum amount of employment expenses eligible for the credit, but is the full amount of these expenses creditable? Consider <a href="https://www.law.cornell.edu/uscode/text/26/21" target="_new" rel="noreferrer">21(a)(1)</a>.</p>',
        }

        if DCAP_lang != "":

            possibleanswers.append(final_credit_no_DCAP)

            judgements[final_credit_no_DCAP] = (
                '<p>What about the interaction of the DCAP and Section 21 described in <a href="https://www.law.cornell.edu/uscode/text/26/21" target="_new" rel="noreferrer">21(c)</a>?</p>'
            )

        if phaseout_type == "no phaseout":

            judgements[correct] = (
                f"This is correct. The number of qualifying children is {number_qual_child}, which means that the maximum amount of employment-related expenses eligible for the credit is {fm.ac(max_creditable_amt)}. {taxpayer.name} spent {fm.ac(amt_spent)}, so the creditable amount is {fm.ac(creditable_expenses_no_DCAP)}. {DCAP_answer_lang} The credit percentage is not phased out, because AGI is not greater than $15,000. Therefore the final credit is {app_percent} percent times  {fm.ac(creditable_expenses)} = {fm.ac(final_credit)}."
            )

        else:

            possibleanswers += [final_credit_no_phaseout, final_credit_no_fraction]

            judgements[final_credit_no_phaseout] = (
                f'<p>What about the phaseout in <a href="https://www.law.cornell.edu/uscode/text/26/21" target="_new" rel="noreferrer">21(a)(2)</a>?</p>'
            )
            judgements[final_credit_no_fraction] = (
                f'<p>What is the significance of the language "or fraction thereof" in <a href="https://www.law.cornell.edu/uscode/text/26/21" target="_new" rel="noreferrer">21(a)(2)</a>?</p>'
            )

            if phaseout_type == "phaseout full":

                possibleanswers.append(final_credit_no_limit_phaseout)

                judgements[correct] = (
                    f"This is correct. The number of qualifying individuals is {number_qual_child}, which means that the maximum amount of employment-related expenses eligible for the credit is {fm.ac(max_creditable_amt)}. {taxpayer.name} spent {fm.ac(amt_spent)}, so the creditable amount is {fm.ac(creditable_expenses_no_DCAP)}. {DCAP_answer_lang} The credit percentage is phased down to 20 percent, because AGI is greater than $43,000. Therefore the final credit is 20 percent x {fm.ac(creditable_expenses)} = {fm.ac(final_credit)}."
                )

                judgements[final_credit_no_limit_phaseout] = (
                    f'<p>What is the significance of the parenthetical "(but not below 20 percent)" in <a href="https://www.law.cornell.edu/uscode/text/26/21" target="_new" rel="noreferrer">21(a)(2)</a>?</p>'
                )

            elif phaseout_type == "phaseout partial":

                judgements[correct] = (
                    f"This is correct. The number of qualifying individuals is {number_qual_child}, which means that the maximum amount of employment-related expenses eligible for the credit is {fm.ac(max_creditable_amt)}. {taxpayer.name} spent {fm.ac(amt_spent)}, so the creditable amount is {fm.ac(creditable_expenses_no_DCAP)}. {DCAP_answer_lang} The credit percentage is phased out, because AGI is greater than $15,000. Therefore the final credit is {app_percent} percent times  {fm.ac(creditable_expenses)} = {fm.ac(final_credit)}."
                )

    [possibleanswers, judgements] = fm.random_answer_pot(possibleanswers, judgements, 3)

    possibleanswers.append(0)

    formattedjudgements = fm.format_dict(judgements)
    judgements_json = json.dumps(formattedjudgements)
    cleananswers = fm.create_clean_answers(possibleanswers)
    return [problem, cleananswers, judgements_json, correct]


# Implementation

functions_dict = {
    "rates": rates_problems,
    "gross-ups": gross_up,
    "time value of money": tvm,
    "unrestricted property as compensation": unrestricted_property,
    "restricted property as compensation": restricted_property,
    "options as compensation": options_as_comp,
    "different ways of satisfying a debt": satisfy_debt,
    "bonds, shifting interest rates, and COD": bonds_COD,
    "gain from sale of principal residence": principal_res,
    "COD exclusion": exclusion_COD,
    "qualified employee discount": qual_empl_disc,
    "charitable donation deduction": charitable_donation,
    "home mortgage interest deduction": qri,
    "taxable property exchange": property_exchange,
    "basis": basis_problems,
    "like-kind exchanges": like_kind,
    "transactions with liabilities": liabilities,
    "installment sales": installment_sales,
    "depreciation": depreciation_question,
    "capital gains and losses": cap_gain_netting,
    "section 1231 netting": section_1231_netting,
    "recapture": recapture,
    "section 24 credit": section_24_credit,
    "section 21 credit": section_21_credit,
    "capital gain + section 1231 + recapture": asset_sale_all,
}

functions_list = ["a random type of problem"] + list(functions_dict.keys())


def function_picker(fn):
    if fn == "a random type of problem":
        fn_pick = random.choice(list(functions_dict.values()))
    else:
        fn_pick = functions_dict[fn]

    return fn_pick()


# Rates page


def rates_facts(type_of_taxpayer, taxable_income):
    type_of_taxpayer = fm.rates_dict[type_of_taxpayer]
    max_key = max(list(type_of_taxpayer.brackets["TopOfBracket"].keys()))
    max_value = type_of_taxpayer.brackets["TopOfBracket"][max_key]
    if taxable_income > max_value:
        response = (
            f"Please enter taxable income less than {max_value} for this taxpayer."
        )
    else:
        average_rate_answer = fm.rates_facts_average(type_of_taxpayer, taxable_income)
        tax_owed_answer = int(average_rate_answer * taxable_income)
        marginal_rate_answer = fm.rates_facts_marginal(type_of_taxpayer, taxable_income)

        response = f"The tax owed is {fm.ac(tax_owed_answer)}.\nThe average tax rate is {fm.as_percent(average_rate_answer)}.\nThe marginal tax rate is {fm.as_percent(marginal_rate_answer)}."

    return response
