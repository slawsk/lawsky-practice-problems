# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 08:13:00 2020

@author: carso
"""
import functionmodules as fm
import random
import profile


class CapGainsFacts:
    def __init__(
        self,
        problem_lang,
        answer_lang,
        LTCG,
        LTCL,
        STCG,
        STCL,
        ordinary,
        carryforward,
        long_term_carryforward,
        short_term_carryforward,
        total_losses,
        total_gains,
        offset,
        offset_from_short_term,
        offset_from_long_term,
    ):
        self.problem_lang = problem_lang
        self.answer_lang = answer_lang
        self.LTCG = LTCG
        self.LTCL = LTCL
        self.STCG = STCG
        self.STCL = STCL
        self.ordinary = ordinary
        self.carryforward = carryforward
        self.long_term_carryforward = long_term_carryforward
        self.short_term_carryforward = short_term_carryforward
        self.total_losses = total_losses
        self.total_gains = total_gains
        self.offset = offset
        self.offset_from_short_term = offset_from_short_term
        self.offset_from_long_term = offset_from_long_term


class Asset:
    def __init__(self, name, class_life, recovery_period, listed):
        self.name = name
        self.class_life = class_life
        self.recovery_period = recovery_period
        self.listed = listed


computer = Asset("computer", 6, 5, False)
copier = Asset("copier", 6, 5, False)
helicopter = Asset("helicopter", 6, 5, False)
car = Asset("car", 3, 5, True)
taxi = Asset("taxi", 3, 5, True)
bus = Asset("bus", 9, 5, False)
light_truck = Asset("light general purpose truck", 4, 5, True)
heavy_truck = Asset("heavy general purpose truck", 6, 5, False)
locomotive = Asset("locomotive", 15, 7, False)
tractor = Asset("tractor unit for over-the-road use", 4, 3, False)
trailer = Asset("trailer", 6, 5, False)
barge = Asset("barge", 18, 10, False)
furniture = Asset("collection of office furniture", 10, 7, False)


full_asset_list = [
    computer,
    copier,
    helicopter,
    car,
    taxi,
    bus,
    light_truck,
    heavy_truck,
    locomotive,
    tractor,
    trailer,
    barge,
    furniture,
]


class AssetFacts:
    def __init__(
        self,
        asset,
        date_purchased,
        purchase_price,
        date_sold,
        sale_price,
        long_or_short,
        gain_or_loss_no_depreciation,
        problem_facts,
        period_lang,
        answer_facts_cap_gain,
        answer_facts_1231,
        answer_facts_all_netting,
        depreciated_basis,
        recapture,
        amount_1231,
        ordinary,
        type_of_gain,
    ):
        self.asset = asset
        self.date_purchased = date_purchased
        self.purchase_price = purchase_price
        self.date_sold = date_sold
        self.sale_price = sale_price
        self.long_or_short = long_or_short
        self.gain_or_loss_no_depreciation = gain_or_loss_no_depreciation
        self.problem_facts = problem_facts
        self.answer_facts_cap_gain = answer_facts_cap_gain
        self.answer_facts_1231 = answer_facts_1231
        self.answer_facts_all_netting = answer_facts_all_netting
        self.depreciated_basis = depreciated_basis
        self.recapture = recapture
        self.amount_1231 = amount_1231
        self.ordinary = ordinary
        self.type_of_gain = type_of_gain
        self.period_lang = period_lang


def create_asset_facts(type="asset", year=fm.current_year):

    corp_name = fm.pick_entity_name()
    stock = Asset(f"shares of stock issued by {corp_name}", 50, 50, False)

    if type == "asset":
        asset = random.choice(full_asset_list)
        preset = "a "
        post = "."
        if asset.listed == False:
            period_lang = (
                f" The class life of the {asset.name} is {asset.class_life} years."
            )
        else:
            period_lang = f" Refer to the statute for the relevant recovery period for the {asset.name}."

    elif type == "stock":
        asset = stock
        preset = ""
        post = ""
        period_lang = ""

    purchase_price = 500 * random.randint(20, 80)

    sale_price = int(fm.generate_random_item(purchase_price, 70, 130))

    if sale_price - purchase_price < 0:
        gain_or_loss = "loss"
    else:
        gain_or_loss = "gain"

    gain_or_loss_amount = abs(sale_price - purchase_price)

    date_sold = fm.pick_random_date_given_year(year)
    while date_sold.month in (1, 12):
        date_sold = fm.pick_random_date_given_year(year)

    long_or_short = random.choice(["long", "short"])

    if long_or_short == "long":
        date_purchased = fm.date_before(
            date_sold, soonest=366, latest=(asset.recovery_period - 1) * 365
        )
        type_of_gain = "1231"
    elif long_or_short == "short":
        date_purchased = fm.date_before(date_sold, soonest=90, latest=360)
        while date_purchased.year == date_sold.year:
            date_purchased = fm.date_before(date_sold, soonest=90, latest=360)
        type_of_gain = "ordinary"

    if type == "stock":
        type_of_gain = "capital"
        depreciation = years_depreciation = 0

    else:
        years_depreciation = year - date_purchased.year

        [total_depreciation, annual_depreciation] = fm.depreciate_asset(
            asset, years_depreciation, purchase_price, True
        )

        depreciation = int(total_depreciation)

    depreciated_basis = purchase_price - depreciation

    truegainloss = sale_price - depreciated_basis
    if truegainloss < 0:
        typegainloss = "loss"
    else:
        typegainloss = "gain"

    recomputed_basis = depreciated_basis + depreciation
    if truegainloss > 0:
        recapture = min(recomputed_basis, sale_price) - depreciated_basis
    else:
        recapture = 0

    if type_of_gain == "1231":
        if truegainloss < 0:
            amount_1231 = truegainloss
        else:
            amount_1231 = max(0, truegainloss - recapture)
    else:
        amount_1231 = 0

    if type_of_gain == "ordinary":
        ordinary = truegainloss
        remaining_after_recapture = ordinary - recapture
        if truegainloss > 0 and truegainloss > recapture:
            ordinary_lang = f"Of this, {fm.ac(recapture)} is recapture and thus ordinary income, and the remaining {fm.ac(remaining_after_recapture)} is also ordinary, because the asset was held for less than one year and is therefore not a Section 1231 asset."
        elif truegainloss > 0:
            ordinary_lang = f"This entire amount is recapture and thus ordinary income."
        else:
            ordinary_lang = f"This is entirely ordinary, because the asset was held for less than one year and is therefore not a Section 1231 asset."

    else:
        ordinary = recapture
        if amount_1231 > 0:
            ordinary_lang = f"Of this, {fm.ac(recapture)} is recapture and thus ordinary income, and the remaining {fm.ac(amount_1231)} is 1231 {typegainloss}, because this is a depreciable asset used in a trade or business and held for more than one year."
        elif amount_1231 < 0:
            ordinary_lang = f"None of this is ordinary, because the property was sold for a loss. This is entirely Section 1231 loss, because this is a depreciable asset use in a trade or business and held for more than one year."
        else:
            ordinary_lang = f"All of this is recapture and thus ordinary income."

    problem_facts = f"On {fm.full_date(date_sold)}, they sell {preset}{asset.name} for {fm.ac(sale_price)}. They bought the {asset.name} for {fm.ac(purchase_price)} on {fm.full_date(date_purchased)}."

    answer_facts_cap_gain = f"The sale of the {asset.name} generates {fm.ac(gain_or_loss_amount)} of {long_or_short}-term capital {gain_or_loss}. "

    answer_facts_1231 = f"The sale of the {asset.name} generates {fm.ac(gain_or_loss_amount)} of {type_of_gain} {gain_or_loss}. "

    if type == "stock":
        answer_facts_all_netting = answer_facts_cap_gain
    else:
        answer_facts_all_netting = f"With respect to the {asset.name}, there is {fm.ac(depreciation)} of depreciation, which results in a final basis of {fm.ac(depreciated_basis)}. Upon sale, there is {fm.ac(sale_price)} - {fm.ac(depreciated_basis)} = {fm.ac(truegainloss)} of {typegainloss}. {ordinary_lang}"

    assetforlist = AssetFacts(
        asset,
        date_purchased,
        purchase_price,
        date_sold,
        sale_price,
        long_or_short,
        gain_or_loss,
        problem_facts,
        period_lang,
        answer_facts_cap_gain,
        answer_facts_1231,
        answer_facts_all_netting,
        depreciated_basis,
        recapture,
        amount_1231,
        ordinary,
        type_of_gain,
    )

    return assetforlist
    # print(assetforlist.problem_facts)


def create_cap_gain_year(year=fm.current_year):

    # while True:

    number_of_assets = random.randint(2, 3)
    selected_assets = []
    assets_for_problem = []

    for n in range(number_of_assets):
        while True:
            listasset = create_asset_facts(type="stock", year=year)
            if listasset.asset not in selected_assets:
                selected_assets.append(listasset.asset)
                assets_for_problem.append(listasset)
                break

    # initialize variables
    asset_purchase_lang = "<br>"
    answer_lang = ""
    STCL = STCG = LTCL = LTCG = net_all_gains_losses = net_all_gains = 0
    list_of_prices = []

    for item in assets_for_problem:

        asset_purchase_lang = asset_purchase_lang + f"<br>{item.problem_facts}"
        answer_lang = answer_lang + f"<br>{item.answer_facts_cap_gain}"

        gainloss = item.sale_price - item.purchase_price
        net_all_gains_losses = net_all_gains_losses + gainloss

        if item.long_or_short == "long":

            if item.gain_or_loss_no_depreciation == "gain":
                LTCG = LTCG + gainloss
                net_all_gains = net_all_gains + gainloss

            elif item.gain_or_loss_no_depreciation == "loss":
                LTCL = LTCL - gainloss

        elif item.long_or_short == "short":

            if item.gain_or_loss_no_depreciation == "gain":
                STCG = STCG + gainloss
                net_all_gains = net_all_gains + gainloss

            elif item.gain_or_loss_no_depreciation == "loss":
                STCL = STCL - gainloss

        list_of_prices.append(item.purchase_price)
        list_of_prices.append(item.sale_price)

    print(answer_lang)
    print(asset_purchase_lang)

    net_STCL = max(0, STCL - STCG)
    net_LTCG = max(0, LTCG - LTCL)

    total_losses = STCL + LTCL
    total_gains = STCG + LTCG

    net_CG = max(0, net_LTCG - net_STCL)

    net_CL = min(0, total_losses - total_gains)

    ordinary = 500 * random.randint(10, 60)

    ordinary_income_lang = (
        f"<br><br>They also have {fm.ac(ordinary)} of ordinary income in {year}."
    )

    offset = min(total_losses - total_gains, 3000, ordinary)
    usable_loss = total_gains + offset
    carryforward = total_losses - usable_loss

    # offset_from_short_term = min(net_STCL-net_LTCG,offset)
    # offset_from_long_term = min(LTCL-LTCG,offset-offset_from_short_term)

    # long_term_carryforward = max(0,LTCL-LTCG-offset_from_long_term)
    # short_term_carryforward = max(0,STCL-net_LTCG-offset_from_short_term)

    offset_from_long_term = offset_from_short_term = long_term_carryforward = (
        short_term_carryforward
    ) = 0
    problem_lang = f"{asset_purchase_lang} {ordinary_income_lang}"

    # if carryforward > 0:
    #     break

    year_facts = CapGainsFacts(
        problem_lang,
        answer_lang,
        LTCG,
        LTCL,
        STCG,
        STCL,
        ordinary,
        carryforward,
        long_term_carryforward,
        short_term_carryforward,
        total_losses,
        total_gains,
        offset,
        offset_from_short_term,
        offset_from_long_term,
    )

    return year_facts
