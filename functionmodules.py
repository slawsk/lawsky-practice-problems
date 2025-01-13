# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 22:31:19 2019

@author: carso
"""
import random
import math
from datetime import datetime
from datetime import date
from datetime import time
import names
import numpy as np
import statistics
import animalsbycountry as abc
import pandas as pd
import re
import pypandoc
import os
from dash.exceptions import PreventUpdate
import json
import base64


class Section724Asset:
    def __init__(
        self,
        assettype,
        subsection,
        partnertypegain,
        partnershiptypegain,
        lossprobability,
    ):
        self.assettype = assettype
        self.subsection = subsection
        self.partnershiptypegain = partnershiptypegain
        self.lossprobability = lossprobability
        self.partnertypegain = partnertypegain


class Problem:
    def __init__(self, fact_pattern, questions_list):
        self.fact_pattern = fact_pattern
        self.questions = questions_list


class Question:
    def __init__(self, question, answers, explanation, topic):
        self.question = question
        self.answers = answers
        self.explanation = explanation
        self.topic = topic


class AnswerExpl:
    def __init__(self, answers, explanation):
        self.answers = answers
        self.explanation = explanation


class Person:
    def __init__(self, name, gender, nom, acc, poss):
        self.name = name
        self.gender = gender
        self.nom = nom
        self.acc = acc
        self.poss = poss


class SingleMarriedLimit:
    def __init__(self, singlelimit, headofhouseholdlimit, marriedlimit):
        self.singlelimit = singlelimit
        self.headofhouseholdlimit = headofhouseholdlimit
        self.marriedlimit = marriedlimit


class FilingStatus:
    def __init__(
        self,
        status,
        brackets,
        standard_deduction,
        section_24_threshold,
        section_121_threshold,
    ):
        self.status = status
        self.brackets = brackets
        self.standard_deduction = standard_deduction
        self.section_24_threshold = section_24_threshold
        self.section_121_threshold = section_121_threshold


class RatesProb:
    def __init__(self, factsentence, pronouns, type_taxpayer):
        self.factsentence = factsentence
        self.pronouns = pronouns
        self.type_taxpayer = type_taxpayer


class CorrectVerb:
    def __init__(self, nbv, bv):
        self.nbv = nbv
        self.bv = bv


current_year = date.today().year
# current_year = 2025
current_year_for_book = 2025
rev_proc_for_book = "Rev. Proc. 2024-40"

code_updated = "December 5, 2024"

regs_updated = "December 5, 2024"

code_updated_bk = "December 5, 2024"

now = datetime.now()
now_stamp = datetime.timestamp(datetime.now())

current_date_for_title = now.strftime("%Y%m%d")

current_date_for_text = now.strftime("%B %d, %Y")

code_and_regs_file_name = "assets\\CodeAndRegSectionsToUse.xlsx"

waiting_list = [
    "Inflating rates...",
    "Standardly deducting...",
    "Extending credits...",
    "Negotiating rate cuts...",
    "Creating deductions...",
    "Imagining a new kind of business entity...",
    "Taking a break to pet the cat...",
    "Adding up numbers...",
    "Imagining formulas...",
    "Itemizing deductions...",
    "Deducting items...",
    "Charitably deducting...",
    "Homing in on the mortgage deduction...",
    "Depreciating assets...",
    "Amortizing intangibles...",
    "Intangibly amortizing...",
    "Exchanging like-kind assets...",
    "Heading a household...",
    "Distributing partnership assets tax-free...",
]

MAX_QUIZ_QUESTIONS = 20

# At the beginning of each calendar year:
# (1) Use createRatesDF.py to create the inflation brackets
# (2) Use the relevant revenue procedure to fill in adjustments_YEAR_dict below
# (3) Upload the new Inflation Revenue Procedure to the assets folder
# (4) Update the code and regulations to keep the code and regs book up to date
# (5) Update current_year_for_book and rev_proc_for_book above,
# so people can make their books before the new year


# 2024 inflation brackets:
married_df_2024 = pd.DataFrame(
    {
        "BottomOfBracket": {
            0: 0,
            1: 23200,
            2: 94300,
            3: 201050,
            4: 383900,
            5: 487450,
            6: 731200,
        },
        "TopOfBracket": {
            0: 23200,
            1: 94300,
            2: 201050,
            3: 383900,
            4: 487450,
            5: 731200,
            6: 10000000,
        },
        "AmountToAdd": {
            0: 0.0,
            1: 2320.0,
            2: 10852.0,
            3: 34337.0,
            4: 78221.0,
            5: 111357.0,
            6: 196669.5,
        },
        "MarginalRate": {0: 0.1, 1: 0.12, 2: 0.22, 3: 0.24, 4: 0.32, 5: 0.35, 6: 0.37},
    }
)

single_df_2024 = pd.DataFrame(
    {
        "BottomOfBracket": {
            0: 0,
            1: 11600,
            2: 47150,
            3: 100525,
            4: 191950,
            5: 243725,
            6: 609350,
        },
        "TopOfBracket": {
            0: 11600,
            1: 47150,
            2: 100525,
            3: 191950,
            4: 243725,
            5: 609350,
            6: 10000000,
        },
        "AmountToAdd": {
            0: 0.0,
            1: 1160.0,
            2: 5426.0,
            3: 17168.5,
            4: 39110.5,
            5: 55678.5,
            6: 183647.25,
        },
        "MarginalRate": {0: 0.1, 1: 0.12, 2: 0.22, 3: 0.24, 4: 0.32, 5: 0.35, 6: 0.37},
    }
)

hoh_df_2024 = pd.DataFrame(
    {
        "BottomOfBracket": {
            0: 0,
            1: 16550,
            2: 63100,
            3: 100500,
            4: 191950,
            5: 243700,
            6: 609350,
        },
        "TopOfBracket": {
            0: 16550,
            1: 63100,
            2: 100500,
            3: 191950,
            4: 243700,
            5: 609350,
            6: 10000000,
        },
        "AmountToAdd": {
            0: 0.0,
            1: 1655.0,
            2: 7241.0,
            3: 15469.0,
            4: 37417.0,
            5: 53977.0,
            6: 181954.5,
        },
        "MarginalRate": {0: 0.1, 1: 0.12, 2: 0.22, 3: 0.24, 4: 0.32, 5: 0.35, 6: 0.37},
    }
)

# 2025 inflation brackets:
married_df_2025 = pd.DataFrame(
    {
        "BottomOfBracket": {
            0: 0,
            1: 23850,
            2: 96950,
            3: 206700,
            4: 394600,
            5: 501050,
            6: 751600,
        },
        "TopOfBracket": {
            0: 23850,
            1: 96950,
            2: 206700,
            3: 394600,
            4: 501050,
            5: 751600,
            6: 1000000,
        },
        "AmountToAdd": {
            0: 0.0,
            1: 2385.0,
            2: 11157.0,
            3: 35302.0,
            4: 80398.0,
            5: 114462.0,
            6: 202154.5,
        },
        "MarginalRate": {0: 0.1, 1: 0.12, 2: 0.22, 3: 0.24, 4: 0.32, 5: 0.35, 6: 0.37},
    }
)

single_df_2025 = pd.DataFrame(
    {
        "BottomOfBracket": {
            0: 0,
            1: 11925,
            2: 48475,
            3: 103350,
            4: 197300,
            5: 250525,
            6: 626350,
        },
        "TopOfBracket": {
            0: 11925,
            1: 48475,
            2: 103350,
            3: 197300,
            4: 250525,
            5: 626350,
            6: 1000000,
        },
        "AmountToAdd": {
            0: 0.0,
            1: 1192.5,
            2: 5578.5,
            3: 17651.0,
            4: 40199.0,
            5: 57231.0,
            6: 188769.75,
        },
        "MarginalRate": {0: 0.1, 1: 0.12, 2: 0.22, 3: 0.24, 4: 0.32, 5: 0.35, 6: 0.37},
    }
)

hoh_df_2025 = pd.DataFrame(
    {
        "BottomOfBracket": {
            0: 0,
            1: 17000,
            2: 64850,
            3: 103350,
            4: 197300,
            5: 250500,
            6: 626350,
        },
        "TopOfBracket": {
            0: 17000,
            1: 64850,
            2: 103350,
            3: 197300,
            4: 250500,
            5: 626350,
            6: 1000000,
        },
        "AmountToAdd": {
            0: 0.0,
            1: 1700.0,
            2: 7442.0,
            3: 15912.0,
            4: 38460.0,
            5: 55484.0,
            6: 187031.5,
        },
        "MarginalRate": {0: 0.1, 1: 0.12, 2: 0.22, 3: 0.24, 4: 0.32, 5: 0.35, 6: 0.37},
    }
)


adjustments_2024_dict = {
    "married_st_ded": 29200,
    "single_st_ded": 14600,
    "hoh_st_ded": 21900,
    "qbi_married_thresh": 383900,
    "qbi_single_thresh": 191950,
    "qbi_hoh_thresh": 191950,
    "exemption_152": 5050,  # this is the exemption amount for 152(d)(1)(B)
    "eitc_earned_income_amount": 17400,  # for unmarried, two children, EITC
    "eitc_threshold_phaseout_amount": 22720,  # for unmarried, two children, EITC
    "eitc_completed_phaseout": 55768,  # for unmarried, two children, EITC
    "eitc_max_credit": 6960,  # for unmarried, two children, EITC
    "eitc_investment_limit": 11600,
    "rev_proc": "Rev. Proc. 2023-34",
    "social security cutoff": 168600,
    "married_df": married_df_2024,
    "single_df": single_df_2024,
    "hoh_df": hoh_df_2024,
}

adjustments_2025_dict = {
    "eitc_earned_income_amount": 17880,  # section 32, for unmarried, two children, EITC
    "eitc_threshold_phaseout_amount": 23350,  # section 32, for unmarried, two children, EITC
    "eitc_completed_phaseout": 57310,  # section 32, for unmarried, two children, EITC
    "eitc_max_credit": 7152,  # section 32, for unmarried, two children, EITC
    "eitc_investment_limit": 11950,  # section 32
    "married_st_ded": 30000,  # section 63
    "single_st_ded": 15000,  # section 63
    "hoh_st_ded": 22500,  # section 63
    "exemption_152": 5200,  # section 152(d)(1)(B) exemption amount
    "qbi_married_thresh": 394600,  # section 199A
    "qbi_single_thresh": 197300,  # section 199A
    "qbi_hoh_thresh": 197300,  # section 199A
    "rev_proc": "Rev. Proc. 2024-40",
    "social security cutoff": 176100,
    "married_df": married_df_2025,
    "single_df": single_df_2025,
    "hoh_df": hoh_df_2025,
}

adjustments_dict_dict = {2024: adjustments_2024_dict, 2025: adjustments_2025_dict}

infl_dict = adjustments_dict_dict[current_year]


rates_list = [0, 0.1, 0.12, 0.22, 0.24, 0.32, 0.35, 0.37]

qri_limit = 750000
old_qri_limit = 1000000


# status, brackets, standard deduction, section 24 threshold, section 121 threshold. Only st ded changes
married = FilingStatus(
    "Married Filing Jointly",
    infl_dict["married_df"],
    infl_dict["married_st_ded"],
    400000,
    500000,
)  ##
single = FilingStatus(
    "Single", infl_dict["single_df"], infl_dict["single_st_ded"], 200000, 250000
)  ##
hoh = FilingStatus(
    "Head of Household", infl_dict["hoh_df"], infl_dict["hoh_st_ded"], 200000, 250000
)  ##

# [threshold amount, amount of phaseout] Only threshold amount changes
qbi_dict = {
    "Married Filing Jointly": [infl_dict["qbi_married_thresh"], 100000],
    "Single": [infl_dict["qbi_single_thresh"], 50000],
    "Head of Household": [infl_dict["qbi_hoh_thresh"], 50000],
}  ##

# this is the exemption amount for 152(d)(1)(B)
exemption_amount = infl_dict["exemption_152"]

# for unmarried, two children, EITC
earned_income_amount = infl_dict["eitc_earned_income_amount"]
threshold_phaseout_amount = infl_dict["eitc_threshold_phaseout_amount"]
completed_phaseout = infl_dict["eitc_completed_phaseout"]

current_rev_proc = infl_dict["rev_proc"]

number_rev_proc = current_rev_proc[-2:]

rates_dict = {
    "Married Filing Jointly": married,
    "Single": single,
    "Head of Household": hoh,
}
section_24_threshold = SingleMarriedLimit(200000, 200000, 400000)
section_24_credit_old = 1000
section_24_credit_2020 = 2000

# years over which depreciated:[depreciation schedule from rev proc]
dep_dict = {
    3: [33.33, 44.45, 14.81, 7.41],
    5: [20.0, 32.0, 19.2, 11.52, 11.52, 5.76],
    7: [14.29, 24.49, 17.49, 12.49, 8.93, 8.92, 8.93, 4.46],
    10: [10.0, 18.0, 14.4, 11.52, 9.22, 7.37, 6.55, 6.55, 6.56, 6.55, 3.28],
    15: [
        5.0,
        9.5,
        8.55,
        7.7,
        6.93,
        6.23,
        5.9,
        5.9,
        5.91,
        5.9,
        5.91,
        5.9,
        5.91,
        5.9,
        5.91,
        2.95,
    ],
}


non_capital_asset = [
    "patent created by {person1.name}",
    "invention created by {person1.name}",
    "design created by {person1.name}",
    " secret formula created by {person1.name}",
    "copyright created by {person1.name}",
    "literary composition created by {person1.name}",
    "musical composition created by {person1.name}",
    "artistic composition created by {person1.name}",
    "accounts receivable from {person1.name}'s business",
    "supplies {person1.name} regularly used in {person1.poss} business",
    "inventory",
]


family_dict = {
    "male": ["father", "uncle", "son", "grandson", "brother", "stepbrother", "nephew"],
    "female": [
        "aunt",
        "mother",
        "daughter",
        "granddaughter",
        "sister",
        "stepsister",
        "niece",
    ],
    "nonbinary": ["parent", "child", "grandchild", "sibling", "stepsibling"],
}


def dict_add_unique(d1, d2, list):
    for item in list:
        if item not in d1.keys():
            d1[item] = d2[item]


ordinals_dictionary = [
    "0th",
    "1st",
    "2nd",
    "3rd",
    "4th",
    "5th",
    "6th",
    "7th",
    "8th",
    "9th",
    "10th",
    "11th",
    "12th",
    "13th",
    "14th",
    "15th",
    "16th",
    "17th",
    "18th",
    "19th",
    "20th",
    "21st",
    "22nd",
    "23rd",
    "24th",
    "25th",
    "26th",
    "27th",
    "28th",
    "29th",
    "30th",
    "31st",
]

color_list = [
    "black",
    "white",
    "gray",
    "silver",
    "maroon",
    "red",
    "purple",
    "green",
    "lime",
    "olive",
    "yellow",
    "mauve",
    "blue",
    "teal",
]

page_style_dict = {
    "max-width": "1200px",
    "margin-left": "auto",
    "margin-right": "auto",
    "background-color": "#fff",
}

# Defining Terms


def nearest_pot(x, power):
    return int(math.ceil(x / 10**power)) * 10**power


def nearest_x(num, x):
    return int(math.ceil(num / x)) * x


def nearesthundred(x):
    return int(math.ceil(x / 100.0)) * 100


def nearestthousand(x):
    return int(math.ceil(x / 1000.0)) * 1000


def nearestmillion(x):
    return int(math.ceil(x / 1000000.0)) * 1000000


def as_curr(amount):
    if amount >= 0:
        return "${:,}".format(amount)
    else:
        return "-${:,}".format(-amount)


def ac(amount):
    return as_curr(amount)


def as_percent(amount):
    return "{:.0%}".format(amount)


def as_percent_for_exam(amount):
    return "{:.1%}".format(amount)


def reformat(l, formatting="cash"):
    newlist = []

    if formatting == "cash":

        for member in l:
            if type(member) is int:
                newlist.append(as_curr(member))
            else:
                newlist.append(member)

    if formatting == "percent":
        for member in l:
            newlist.append(as_percent(member))

    return newlist


def to_capital(input):
    return input.capitalize()


def format_dict(d, formatting="cash"):

    if formatting == "cash":
        formatted_dictionary = {as_curr(key): value for key, value in d.items()}

    if formatting == "percent":
        formatted_dictionary = {as_percent(key): value for key, value in d.items()}

    if formatting == "words":
        formatted_dictionary = d

    return formatted_dictionary


def merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res


def date_after(afterdate, soonest=300, latest=1500):
    afterdate_ordinal = date.toordinal(afterdate)
    difference = random.randint(soonest, latest)
    random_date_ordinal = afterdate_ordinal + difference
    return date.fromordinal(random_date_ordinal)


def date_before(beforedate, soonest=300, latest=1500):
    beforedate_ordinal = date.toordinal(beforedate)
    random_date_ordinal = beforedate_ordinal - random.randint(soonest, latest)
    return date.fromordinal(random_date_ordinal)


def pick_random_date(start=date.today()):
    date_ordinal = date.toordinal(start)
    random_date_ordinal = date_ordinal + random.randint(100, 500)
    return date.fromordinal(random_date_ordinal)


def random_date_before_month(monthbefore, start=date.today()):
    while True:
        datestring = pick_random_date()
        if datestring.month < monthbefore:
            return datestring
            break


def random_date_month_range(monthafter=1, monthbefore=12, start=date.today()):
    while True:
        datestring = pick_random_date()
        if datestring.month >= monthafter and datestring.month < monthbefore:
            return datestring
            break


def pick_random_date_this_year():
    start_date = date.today().replace(day=1, month=1).toordinal()
    random_day_this_year = start_date + random.randint(0, 364)
    return date.fromordinal(random_day_this_year)


def pick_random_date_given_year(year=current_year):
    start_date = date.today().replace(day=1, month=1, year=year).toordinal()
    random_day_given_year = start_date + random.randint(0, 364)
    return date.fromordinal(random_day_given_year)


def month(random_date):
    # random_date needs to be a date from date.
    return random_date.strftime("%B")


def day(random_date):
    # random_date needs to be a date from date.
    return random_date.strftime("%d")


def month_day(random_date):
    return random_date.strftime("%B %d")


def full_date(random_date):
    return random_date.strftime("%B %d, %Y")


def date_for_problem():
    return full_date(pick_random_date_this_year())


def create_person():
    name = random.choice(names.all_names)
    gender_list = ["nonbinary", "binary"]
    picked_pronoun = random.choices(gender_list, weights=[5, 95], k=1)[0]
    if picked_pronoun == "nonbinary":
        return Person(name, "nonbinary", "they", "them", "their")
    elif name in names.malenames:
        return Person(name, "male", "he", "him", "his")
    else:
        return Person(name, "female", "she", "her", "her")


def create_group(size=2):
    firstletterlist = []
    personlist = []
    for i in range(size):
        while True:
            created = create_person()
            if created.name[0] not in firstletterlist:
                firstletterlist.append(created.name[0])
                personlist.append(created)
                break
    return personlist


def create_street_group(size=2):
    firstletterlist = []
    streetlist = []
    for i in range(size):
        while True:
            created = random.choice(names.flower)
            typestreet = random.choice(["Lane", "Street", "Road"])
            if created[0] not in firstletterlist:
                firstletterlist.append(created[0])
                streetlist.append(f"{created} {typestreet}")
                break
    return streetlist


def match_explain(answer, text="Try again!"):
    return [answer, text]


def dict_to_list(d):
    l = []
    for key, value in d.items():
        l.append([key, value])
    return l


def fraction_of_thou(number, start=1, end=99):
    fraction_of_number = random.randint(start, end)
    return nearestthousand(number * fraction_of_number / 100)


def gainword(number):
    if number < 0:
        word = "loss"
    else:
        word = "gain"
    return word


def create_clean_answers(
    possibleanswers, kindofformatting="cash", type_answers="website"
):
    if kindofformatting == "cash":
        setanswers = set(possibleanswers)
        listanswers = list(setanswers)
    else:
        listanswers = possibleanswers

    if type_answers == "website":
        if kindofformatting == "cash" or kindofformatting == "percent":
            listanswers.sort()
            cleananswers = reformat(listanswers, kindofformatting)
        elif kindofformatting == "words":
            random.shuffle(possibleanswers)
            cleananswers = possibleanswers
        elif kindofformatting == "wordsnoshuffle":
            cleananswers = possibleanswers

    elif type_answers == "quiz":
        if kindofformatting == "cash" or kindofformatting == "percent":
            cleananswers = reformat(listanswers, kindofformatting)
        elif kindofformatting == "words":
            cleananswers = possibleanswers

    return cleananswers


def generate_random_pot(comparator, power_of_ten, start=80, end=120):
    while True:
        fraction_of_number = random.randrange(start, end)
        random_answer = nearest_pot(comparator * fraction_of_number / 100, power_of_ten)
        if random_answer != comparator:
            break
    if power_of_ten > -1:
        return int(random_answer)
    else:
        return round(random_answer, 1)


def generate_random_basis(comparator, power_of_ten, lossprobability):

    start = (120 * lossprobability - 20) / lossprobability

    basis = generate_random_pot(comparator, power_of_ten, start=start, end=120)

    return basis


def generate_random_item(comparator, start=80, end=120):
    while True:
        fraction_of_number = random.randrange(start, end)
        random_answer = nearestthousand(comparator * fraction_of_number / 100)
        if random_answer != comparator:
            break

    return int(random_answer)


def generate_random_item_mill(comparator, start=80, end=120):
    while True:
        fraction_of_number = random.randrange(start, end)
        random_answer = nearesthundred(comparator * fraction_of_number / 100)
        if random_answer != comparator:
            break

    return int(random_answer)


def generate_random_item_hund(comparator, start=80, end=120):
    while True:
        fraction_of_number = random.randrange(start, end)
        random_answer = nearesthundred(comparator * fraction_of_number / 100)
        if random_answer != comparator:
            break

    return int(random_answer)


def generate_random_item_ones(comparator, start=80, end=120):
    while True:
        fraction_of_number = random.randrange(start, end)
        random_answer = int(comparator * fraction_of_number / 100)
        if random_answer != comparator:
            break
    return int(random_answer)


def random_answer(possibleanswers, judgements, start=80, end=120):
    while True:
        rand_answer = generate_random_item(statistics.mean(possibleanswers), start, end)
        if rand_answer not in possibleanswers:
            possibleanswers.append(rand_answer)
            judgements[rand_answer] = "This answer was randomly generated."
            break

    return possibleanswers, judgements


def random_answer_ones(possibleanswers, judgements, start=80, end=120):
    while True:
        mean_list = list(set(possibleanswers))
        if 0 in mean_list:
            mean_list.remove(0)
        rand_answer = generate_random_item_ones(statistics.mean(mean_list), start, end)
        if rand_answer not in possibleanswers:
            possibleanswers.append(rand_answer)
            judgements[rand_answer] = "This answer was randomly generated."
            break
    return possibleanswers, judgements


def random_answer_ones_off_target(
    possibleanswers, judgements, target, start=80, end=120
):
    while True:
        rand_answer = generate_random_item_ones(target, start, end)
        if rand_answer not in possibleanswers:
            possibleanswers.append(rand_answer)
            judgements[rand_answer] = "This answer was randomly generated."
            break
    return possibleanswers, judgements


def random_answer_hund(possibleanswers, judgements):
    while True:
        mean_list = list(possibleanswers)
        if 0 in possibleanswers:
            mean_list.remove(0)
        rand_answer = generate_random_item_hund(statistics.mean(mean_list))
        if rand_answer not in possibleanswers:
            possibleanswers.append(rand_answer)
            judgements[rand_answer] = "This answer was randomly generated."
            break

    return possibleanswers, judgements


def random_answer_pot(possibleanswers, judgements, pot, start=80, end=120):
    while True:
        mean_list = list(set(possibleanswers))
        if 0 in mean_list:
            mean_list.remove(0)
        if abs(statistics.mean(mean_list)) < 10**pot:
            comparenum = random.choice(mean_list)
        else:
            comparenum = statistics.mean(mean_list)

        start_nearest = nearest_pot(comparenum * start / 100, pot)
        end_nearest = nearest_pot(comparenum * end / 100, pot)
        if (
            end_nearest - start_nearest <= 10**pot
        ) and start_nearest in possibleanswers:
            comparenum += end_nearest + 10**pot

        rand_answer = generate_random_pot(comparenum, pot, start, end)
        if rand_answer not in possibleanswers:
            possibleanswers.append(rand_answer)
            judgements[rand_answer] = "This answer was randomly generated."
            break

    return possibleanswers, judgements


def pick_entity_name(type="corporation"):
    entity_base = random.choice(abc.animals_by_country_dict["English"])

    if type == "corporation":
        entity_name = f"{entity_base}, Inc."
    elif type == "none":
        entity_name = entity_base
    else:
        entity_name = f"{entity_base}, LLC"

    return entity_name


def pick_a_an(entity):
    if entity[0] in ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U", "8"]:
        return "an"
    else:
        return "a"


def entity_list_generate(number):

    entity_list = []

    for n in range(0, number):
        while True:
            entity_name = random.choice(abc.animals_by_country_dict["English"])
            if entity_name not in entity_list:
                entity_list.append(entity_name)
                break

    return entity_list


def property_name():
    color_name = random.choice(color_list)
    fullname = to_capital(color_name) + "acre"

    return fullname


def depreciate_asset(asset, year, initial_basis, sold=False):

    recovery_period = asset.recovery_period
    dep_schedule = dep_dict[recovery_period]

    year_depreciation = 0
    total_depreciation = 0

    if recovery_period != 50:

        for item in range(0, year + 1):
            annual_depreciation = initial_basis * dep_schedule[item] / 100
            if item == year and sold == True:
                annual_depreciation = 0.5 * annual_depreciation

            if item == year:
                year_depreciation = annual_depreciation

            total_depreciation = total_depreciation + annual_depreciation

    return [total_depreciation, year_depreciation]


def get_integer(question_string):

    while True:
        x = input(question_string)
        try:
            int(x)
            return int(x)
            break
        except ValueError:
            print("Please enter an integer.")


def random_choice_input(type_string, how_to_gen_random):
    random_choice = input("Random " + type_string + "? (y/n): ")
    if random_choice == "y":
        output_number = how_to_gen_random
    else:
        output_number = get_integer(type_string + ": ")

    return output_number


def add_to_file(filename, *args):
    file = open(filename, "a")

    for arg in args:
        file.write("\n")
        file.write("\n")
        file.write("\n")
        file.write(arg)

    file.close()


def tax_owed_answer(type_of_taxpayer, taxable_income):
    df = type_of_taxpayer.brackets
    for n in range(df.index.max() + 1):
        if df.at[n, "BottomOfBracket"] < taxable_income <= df.at[n, "TopOfBracket"]:
            return int(
                round(
                    df.at[n, "AmountToAdd"]
                    + df.at[n, "MarginalRate"]
                    * (taxable_income - df.at[n, "BottomOfBracket"]),
                    0,
                )
            )
            break


def rates_facts_marginal(type_of_taxpayer, taxable_income):
    df = type_of_taxpayer.brackets
    for n in range(df.index.max() + 1):
        if df.at[n, "BottomOfBracket"] < taxable_income <= df.at[n, "TopOfBracket"]:
            return df.at[n, "MarginalRate"]
            break


def rates_facts_average(type_of_taxpayer, taxable_income):
    tax_owed = tax_owed_answer(type_of_taxpayer, taxable_income)
    if taxable_income == 0:
        return 0
    else:
        return tax_owed / taxable_income


def rates_facts(type_of_taxpayer, taxable_income):
    max_key = max(list(type_of_taxpayer.brackets["TopOfBracket"].keys()))
    max_value = type_of_taxpayer.brackets["TopOfBracket"][max_key]
    if taxable_income > max_value:
        response = (
            f"Please enter taxable income less than {max_value} for this taxpayer."
        )
    else:
        average_rate_answer = rates_facts_average(type_of_taxpayer, taxable_income)
        tax_owed = int(tax_owed_answer(type_of_taxpayer, taxable_income))
        marginal_rate_answer = rates_facts_marginal(type_of_taxpayer, taxable_income)

        response = f"The tax owed is {as_curr(tax_owed)}.\nThe average tax rate is {as_percent(average_rate_answer)}.\nThe marginal tax rate is {as_percent(marginal_rate_answer)}."

    return response


def clean_string(x):
    if x[0] == "$":
        x = x.replace("$", "")
        x = x.replace(",", "")
        try:
            return int(x)
        except:
            return x
    elif x[-1] == "%":
        x = x.replace("%", "")
        try:
            return float(x) / 100
        except:
            return x
    else:
        return x


def fancify_string(x, y):
    if x[0] == "$" or x[1] == "$":
        try:
            return ac(y)
        except:
            return y
    elif x[-1] == "%":
        try:
            return as_percent(y)
        except:
            return y
    else:
        return y


def clean_explanation(x):
    no_brackets = re.sub("<.*?>", "", x)
    no_correct_1 = re.sub("This is correct. ", "", no_brackets)
    no_correct = re.sub("Correct. ", "", no_correct_1)
    no_correct_exclam = re.sub("Correct! ", "", no_correct)
    no_ascii = re.sub("\u2022", "<br>", no_correct_exclam)
    return re.sub("That is correct. ", "", no_ascii)


def convert_doc(inputname, outputname):
    pypandoc.convert_file(
        inputname,
        "docx",
        outputfile=outputname,
        extra_args=["--reference-doc=custom-reference.docx"],
    )


def create_answer_key(fullstring, date):

    coursename_string = "## Lawsky Practice Problems\n"
    website_string = "## https://www.lawskypracticeproblems.org/ \n"
    exam_title_string = f"## Practice Quiz {current_date_for_text} \n"

    answer_key_title_base = f"saved_files/taxquiz.{date}"

    answer_key_title = f"{answer_key_title_base}.md"

    file = open(answer_key_title, "w")

    file.write(coursename_string)
    file.write(website_string)
    file.write(exam_title_string)
    file.write(fullstring)
    file.close()

    convert_doc(answer_key_title, f"{answer_key_title_base}.docx")


def extract_date(filetitle):
    first_split = filetitle.split(".", 1)[1]
    second_split = first_split.split(".")[0]
    return int(second_split)


def remove_old_files(directory):
    for filetitle in os.listdir(directory):
        try:
            titlenumber = extract_date(filetitle)
            if now_stamp - titlenumber > 20:
                os.remove(f"{directory}/{filetitle}")
        except:
            pass


def maximum_width(itemlist):
    return max([len(str(x)) for x in itemlist])


def dropdown_width(answerslist):
    return max(6, 0.6 * maximum_width(answerslist))


def create_explanation(n_clicks, hidden1, submit_type_reset, input1, list1):
    if input1 is None:
        raise PreventUpdate

    if n_clicks == 0 or hidden1 == 0 or submit_type_reset == 0:
        explanation = ""

    else:
        judgement_dict = json.loads(list1)
        explanation = judgement_dict.get(input1, "\nTry again.")

    return explanation


def create_problem(n_clicks_submit_types, dropdown_id_value, fn_type):
    if n_clicks_submit_types == 0:
        return ["", "", "", "", 0, {"display": "none"}, {"display": "none"}]

    else:
        if dropdown_id_value not in fn_type.functions_list:
            dropdown_id_value = "a random type of problem"
        outputlist = fn_type.function_picker(dropdown_id_value)
        answerslist = [{"label": i, "value": i} for i in outputlist[1]]
        maxwidth = dropdown_width(outputlist[1])
        judgementlist = outputlist[2]
        problemtext = outputlist[0]
        return [
            problemtext,
            answerslist,
            "",
            judgementlist,
            0,
            {"width": f"{maxwidth}em", "max-width": "90%", "display": "block"},
            {"display": "block"},
        ]


image_filename = "assets/CodeAndRegsPic.png"
encoded_image = base64.b64encode(open(image_filename, "rb").read())

counter_file = "bookdownloads.txt"
