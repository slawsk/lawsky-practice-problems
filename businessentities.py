# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 09:33:07 2019

@author: Lawsky
"""
import random
import animalsbycountry as abc
import functionmodules as fm

class BusinessEntity:
  def __init__(self, location,entity_type,entity_suffix,entity_name,default_choice,elect_choice,member_language,liability_language,type_triple,foreign_US):
    self.location = location
    self.entity_type = entity_type
    self.entity_suffix = entity_suffix
    self.entity_name = entity_name
    self.default_choice = default_choice 
    self.elect_choice = elect_choice
    self.member_language = member_language
    self.liability_language = liability_language
    self.type_triple = type_triple
    self.foreign_US = foreign_US



per_se_ed = ['Argentina, Sociedad Anonima', 'Australia, Public Limited Company', 'Austria, Aktiengesellschaft', 'Belgium, Societe Anonyme', 'Brazil, Sociedade Anonima', 'Canada, Corporation & Company', 'Chile, Sociedad Anonima', 'Colombia, Sociedad Anonima', 'Ecuador, Sociedad Anonima', 'Ecuador, Compania Anonima', 'France, Societe Anonyme', 'Germany, Aktiengesellschaft', 'Guatemala, Sociedad Anonima', 'India, Public Limited Company', 'Luxembourg, Societe Anonyme', 'Mexico, Sociedad Anonima', 'Netherlands, Naamloze Vennootschap', 'New Zealand, Limited Company', 'Nigeria, Public Limited Company', 'Portugal, Sociedade Anonima', 'Spain, Sociedad Anonima', 'Switzerland, Aktiengesellschaft', 'United Kingdom, Public Limited Company']

state = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]



terms_by_country_ed_dict = {'Argentina': {'Sociedad Anonima': 'sa', 'Sociedad de Responsabilidad Limitada': 'srl', 'Sociedad en Comandita por Acciones': 'scpa'}, 
                            'Australia': {'Limited Liability Partnership': 'LLP', 'Unlimited Proprietary Company': 'pty','Public Limited Company':'plc'}, 
                            'Austria': {'eingetragenes Einzelunternehmen': 'eu', 'Aktiengesellschaft': 'ag', 'offene Gesellschaft': 'og', 'Kommanditgesellschaft': 'kg'}, 
                            'Belgium': {'vereniging zonder winstoogmerk': 'vzw', 'vennootschap onder firma': 'vof', 'eenpersoons besloten vennootschap met beperkte aansprakelijkheid': 'ebvba', 'gewone commanditaire vennootschap': 'comm.v','Societe Anonyme':'sa'}, 
                            'Brazil': {'Sociedade limitada': 'ltda', 'Sociedade Anonima': 'sa'}, 
                            'Canada': {'Limited Partnership': 'lp', 'Corporation':'inc','Company':'co.'}, 
                            'Chile': {'Empresa Individual de Responsabilidad Limitada': 'eirl', 'Sociedad Anonima': 'sa', 'Sociedad de responsabilidad limitada': 'ltda'}, 
                            'Colombia': {'Sociedad Anonima': 'sa', 'Empresa Unipersonal': 'e.u.', 'Sociedad de Responsabilidad Limitada': 'ltda'}, 
                            'Dominican Republic': {'Sociedad Anonima': 'sa', 'Sociedad de Resposabilidad Limitada': 'srl', 'Empresa Individual de Responsabilidad Limitada': 'eirl.'}, 
                            'Ecuador': {'Sociedad Anonima': 'sa', 'Compania Limitada': 'Cia. Ltda.','Compania Anonima':'ca'}, 
                            'France': {'Societe en nom collectif': 'snc', 'Societe en commandite simple': 'scs', 'Societe Anonyme': 'SA'}, 
                            'Germany': {'Kommanditgesellschaft': 'kg', 'Gesellschaft burgerlichen Rechts': 'gbr', 'Offene Handelsgesellschaft': 'ohg', 'Gesellschaft mit beschrankter Haftung': 'gmbh', 'Aktiengesellschaft': 'ag'}, 
                            'Guatemala': {'Sociedad Anonima': 'sa'}, 
                            'Haiti': {'Sociedad Anonima': 'sa'}, 
                            'India': {'Public Limited Company': 'ltd.'}, 
                            'Luxembourg': {'Societe Anonyme': 'sa', 'Societe a responsabilite limitee': 'sarl'}, 
                            'Mexico': {'Sociedad Anonima': 'sa', 'Sociedad de Responsabilidad Limitada': 's. de. r.l.', 'Sociedad en Comandita Simple': 's. en c.'}, 
                            'Netherlands': {'Vennootschap onder firma': 'vof', 'Commanditaire vennootschap': 'nv','Naamloze Vennootschap':'nv'}, 
                            'New Zealand': {'limited liability company': 'limited','Limited Company':''}, 
                            'Nigeria': {'Public Limited Company': 'plc', 'Private Limited Company': 'ltd.'}, 
                            'Portugal': {'Limitada': 'lda.', 'Sociedade Anonima': 'sa'}, 
                            'Spain': {'Sociedad Anonima': 'sa', 'Sociedad Limitada': 'sl', 'Sociedad Limitada Nueva Empresa': 's.l.n.e.', 'Sociedad Colectiva': 's.c.', 'Sociedad Comanditaria': 's.cra'}, 
                            'Switzerland': {'Societe Anonyme': 'sa', 'Gesellschaft mit beschrankter Haftung': 'gmbh', 'Societe a responsabilite limitee': 'sarl','Aktiengesellschaft':'ag'}, 
                            'United Kingdom': {'Public Limited Company': 'plc', 'Limited Liability Partnership': 'llp', 'Limited Partnership': 'lp'}, 
                            'United States': {'Limited Liability Company': 'llc', 'corporation': 'inc', 'Limited Liability Partnership': 'llp', 'limited partnership': 'lp'}}

languages = {'English':['Australia','Canada','India','United Kingdom','United States','New Zealand','Nigeria'],'Spanish':['Argentina','Chile','Colombia','Dominican Republic','Ecuador','Guatemala','Mexico','Spain','Peru'],'German':['Austria','Germany','Switzerland'],'Dutch':['Belgium','Netherlands'],'French':['France','Haiti','Luxembourg'],'Portugese':['Brazil','Portugal']}

language_by_country = {'Australia': 'English', 'Canada': 'English', 'India': 'English', 'United Kingdom': 'English', 'United States': 'English', 'New Zealand': 'English', 'Nigeria': 'English', 'Argentina': 'Spanish', 'Chile': 'Spanish', 'Colombia': 'Spanish', 'Dominican Republic': 'Spanish', 'Ecuador': 'Spanish', 'Guatemala': 'Spanish', 'Mexico': 'Spanish', 'Spain': 'Spanish', 'Peru': 'Spanish', 'Austria': 'German', 'Germany': 'German', 'Switzerland': 'German', 'Belgium': 'Dutch', 'Netherlands': 'Dutch', 'France': 'French', 'Haiti': 'French', 'Luxembourg': 'French', 'Brazil': 'Portugese', 'Portugal': 'Portugese'}


in_use_dict = {'Corporation': ['corp.', 'inc.', 'ag'], 'General Partnership': ['ltda', 'og', 'snc'], 'Joint Venture': [], 'Limited': ['ltd', 'ltda', 'gmbh', 'tapui', 'srl', 'scs', 'limited', 'lda.'], 'Limited Liability Company': ['llc', 'plc', 'srl', 'sarl', 'nv', 'sa'], 'Limited Liability Limited Partnership': ['lllp'], 'Limited Liability Partnership': ['llp'], 'Limited Partnership': ['lp', 'scpa', 'comm.v', 's. en c.', 's. en c.', 'scs', 'kg'], 'Private Company': []}

dictionary_by_general_type = {
    'Limited Liability Company': [['Argentina', 'Sociedad Anonima', 'sa'], ['Argentina', 'Sociedad de Responsabilidad Limitada', 'srl'], ['Australia', 'Public Limited Company', 'plc'], ['Belgium', 'Societe Anonyme', 'sa'], ['Brazil', 'Sociedade Anonima', 'sa'], ['Chile', 'Sociedad Anonima', 'sa'], ['Colombia', 'Sociedad Anonima', 'sa'], ['Dominican Republic', 'Sociedad Anonima', 'sa'], ['Dominican Republic', 'Sociedad de Resposabilidad Limitada', 'srl'], ['Ecuador', 'Sociedad Anonima', 'sa'], ['Guatemala', 'Sociedad Anonima', 'sa'], ['Haiti', 'Sociedad Anonima', 'sa'], ['Luxembourg', 'Societe Anonyme', 'sa'], ['Luxembourg', 'Societe a responsabilite limitee', 'sarl'], ['Mexico', 'Sociedad Anonima', 'sa'], ['Netherlands', 'Commanditaire vennootschap', 'nv'], ['Netherlands', 'Naamloze Vennootschap', 'nv'], ['Nigeria', 'Public Limited Company', 'plc'], ['Portugal', 'Sociedade Anonima', 'sa'], ['Spain', 'Sociedad Anonima', 'sa'], ['Switzerland', 'Societe Anonyme', 'sa'], ['Switzerland', 'Societe a responsabilite limitee', 'sarl'], ['United Kingdom', 'Public Limited Company', 'plc'], ['United States', 'Limited Liability Company', 'llc']], 
    'Limited Partnership': [['Argentina', 'Sociedad en Comandita por Acciones', 'scpa'], ['Austria', 'Kommanditgesellschaft', 'kg'], ['Belgium', 'gewone commanditaire vennootschap', 'comm.v'], ['Canada', 'Limited Partnership', 'lp'], ['France', 'Societe en commandite simple', 'scs'], ['Germany', 'Kommanditgesellschaft', 'kg'], ['Mexico', 'Sociedad en Comandita Simple', 's. en c.'], ['Spain', 'Sociedad Comanditaria', 's.cra'], ['United Kingdom', 'Limited Partnership', 'lp'], ['United States', 'limited partnership', 'lp']], 'Limited Liability Partnership': [['Australia', 'Limited Liability Partnership', 'llp'], ['United Kingdom', 'Limited Liability Partnership', 'llp'], ['United States', 'Limited Liability Partnership', 'llp']], 
    'Corporation': [['Austria', 'Aktiengesellschaft', 'ag'], ['Canada', 'Corporation', 'inc'], ['Canada', 'Company', 'co'], ['Ecuador', 'Compania Anonima', 'ca'], ['France', 'Societe Anonyme', 'SA'], ['Germany', 'Aktiengesellschaft', 'ag'], ['Switzerland', 'Aktiengesellschaft', 'ag'], ['United States', 'corporation', 'inc']], 
    'General Partnership': [['Austria', 'offene Gesellschaft', 'og'], ['Belgium', 'vennootschap onder firma', 'vof'], ['France', 'Societe en nom collectif', 'snc'], ['Germany', 'Offene Handelsgesellschaft', 'ohg'], ['Netherlands', 'Vennootschap onder firma', 'vof']], 'Limited': [['Brazil', 'Sociedade limitada', 'ltda'], ['Chile', 'Sociedad de responsabilidad limitada', 'ltda'], ['Colombia', 'Sociedad de Responsabilidad Limitada', 'ltda'], ['Germany', 'Gesellschaft mit beschrankter Haftung', 'gmbh'], ['India', 'Public Limited Company', 'ltd'], ['New Zealand', 'limited liability company', 'limited'], ['Nigeria', 'Private Limited Company', 'ltd'], ['Portugal', 'Limitada', 'lda.'], ['Switzerland', 'Gesellschaft mit beschrankter Haftung', 'gmbh']],
    'Private Company':[['United Kingdom','Private Company','']]}

dictionary_by_general_type_no_US = {
    'Limited Liability Company': [['Argentina', 'Sociedad Anonima', 'sa'], ['Argentina', 'Sociedad de Responsabilidad Limitada', 'srl'], ['Australia', 'Public Limited Company', 'plc'], ['Belgium', 'Societe Anonyme', 'sa'], ['Brazil', 'Sociedade Anonima', 'sa'], ['Chile', 'Sociedad Anonima', 'sa'], ['Colombia', 'Sociedad Anonima', 'sa'], ['Dominican Republic', 'Sociedad Anonima', 'sa'], ['Dominican Republic', 'Sociedad de Resposabilidad Limitada', 'srl'], ['Ecuador', 'Sociedad Anonima', 'sa'], ['Guatemala', 'Sociedad Anonima', 'sa'], ['Haiti', 'Sociedad Anonima', 'sa'], ['Luxembourg', 'Societe Anonyme', 'sa'], ['Luxembourg', 'Societe a responsabilite limitee', 'sarl'], ['Mexico', 'Sociedad Anonima', 'sa'], ['Netherlands', 'Commanditaire vennootschap', 'nv'], ['Netherlands', 'Naamloze Vennootschap', 'nv'], ['Nigeria', 'Public Limited Company', 'plc'], ['Portugal', 'Sociedade Anonima', 'sa'], ['Spain', 'Sociedad Anonima', 'sa'], ['Switzerland', 'Societe Anonyme', 'sa'], ['Switzerland', 'Societe a responsabilite limitee', 'sarl'], ['United Kingdom', 'Public Limited Company', 'plc']], 
    'Limited Partnership': [['Argentina', 'Sociedad en Comandita por Acciones', 'scpa'], ['Austria', 'Kommanditgesellschaft', 'kg'], ['Belgium', 'gewone commanditaire vennootschap', 'comm.v'], ['Canada', 'Limited Partnership', 'lp'], ['France', 'Societe en commandite simple', 'scs'], ['Germany', 'Kommanditgesellschaft', 'kg'], ['Mexico', 'Sociedad en Comandita Simple', 's. en c.'], ['Spain', 'Sociedad Comanditaria', 's.cra'], ['United Kingdom', 'Limited Partnership', 'lp'], ['United States', 'limited partnership', 'lp']], 'Limited Liability Partnership': [['Australia', 'Limited Liability Partnership', 'llp'], ['United Kingdom', 'Limited Liability Partnership', 'llp']], 
    'Corporation': [['Austria', 'Aktiengesellschaft', 'ag'], ['Canada', 'Corporation', 'inc'], ['Canada', 'Company', 'co'], ['Ecuador', 'Compania Anonima', 'ca'], ['France', 'Societe Anonyme', 'SA'], ['Germany', 'Aktiengesellschaft', 'ag'], ['Switzerland', 'Aktiengesellschaft', 'ag']], 
    'General Partnership': [['Austria', 'offene Gesellschaft', 'og'], ['Belgium', 'vennootschap onder firma', 'vof'], ['France', 'Societe en nom collectif', 'snc'], ['Germany', 'Offene Handelsgesellschaft', 'ohg'], ['Netherlands', 'Vennootschap onder firma', 'vof']], 'Limited': [['Brazil', 'Sociedade limitada', 'ltda'], ['Chile', 'Sociedad de responsabilidad limitada', 'ltda'], ['Colombia', 'Sociedad de Responsabilidad Limitada', 'ltda'], ['Germany', 'Gesellschaft mit beschrankter Haftung', 'gmbh'], ['India', 'Public Limited Company', 'ltd'], ['New Zealand', 'limited liability company', 'limited'], ['Nigeria', 'Private Limited Company', 'ltd'], ['Portugal', 'Limitada', 'lda.'], ['Switzerland', 'Gesellschaft mit beschrankter Haftung', 'gmbh']],
    'Private Company':[['United Kingdom','Private Company','']]}

suffix_US = {'Limited Liability Company':'llc','Limited Partnership':'lp','General Partnership':'gp','Limited Liability Partnership':'llp'}

triple_entity_type_dict= {
'[1, 1, 0]':['General Partnership'],
'[0, 1, 0]':['General Partnership'],
'[1, 1, 1]':['Limited','Limited Liability Company','Limited Liability Partnership'],
'[0, 1, 1]':['Limited Liability Company','Limited Liability Partnership'],
'[1, 0, 1]':['Private Company'],
'[0, 0, 1]':['Limited Liability Company']}

triple_default_elect_dict = {'[0, 0, 1]':{'default':'disregarded entity','elect':'corporation'},
'[0, 0, 0]':{'default':'disregarded entity','elect':'corporation'}, 
'[0, 1, 0]':{'default':'partnership','elect':'corporation'}, 
'[0, 1, 1]':{'default':'partnership','elect':'corporation'},
#if foreign entity
'[1, 0, 0]':{'default':'disregarded entity','elect':'corporation'},
'[1, 1, 0]':{'default':'partnership','elect':'corporation'}, 
'[1, 0, 1]':{'elect':'disregarded entity','default':'corporation'}, 
'[1, 1, 1]':{'elect':'partnership','default':'corporation'}} 

def pick_per_se_entity():
    foreign_US = random.choice(['foreign','United States'])
    
    if foreign_US == 'foreign':
        entity_type_location = random.choice(per_se_ed)
        country = entity_type_location.split(', ')[0]
        entity_type = entity_type_location.split(', ')[1]
        entity_suffix = terms_by_country_ed_dict[country][entity_type]
        country_language = language_by_country[country]    
        
    else:
        country = random.choice(state)
        entity_type = "corporation"
        entity_suffix = random.choice(['inc.','co.'])
        country_language = 'English'
    
    entity_name = random.choice(abc.animals_by_country_dict[country_language])
    member_language = random.choice(['has only one member.','has more than one member.'])
    liability_language = f'All members of {entity_name} have limited liability.' 
    default_choice = ''
    elect_choice = ''
    type_triple = ''
    per_se_entity = BusinessEntity(country,entity_type,entity_suffix,entity_name,default_choice,elect_choice,member_language,liability_language,type_triple,foreign_US)
    return(per_se_entity)

def pick_other_entity():
    type_triple = []
    
    while True:
        for n in range(0,3):
            type_triple.append(random.choice([1,0]))
        if not(type_triple[1] == type_triple[2] == 0):
            break

    if type_triple[0]==0:
        foreign_US = 'U.S.'
    elif type_triple[0]==1:
        foreign_US = 'foreign'
    triple_string = str(type_triple)
    list_to_check = triple_entity_type_dict[triple_string] 
    classification = random.choice(list_to_check)

    if type_triple[0]==0:
        country = random.choice(state)
        entity_name = random.choice(abc.animals_by_country_dict['English'])
        entity_type = classification
        entity_suffix = suffix_US[classification]
        
    else:
        while True:
            entity_partial = random.choice(dictionary_by_general_type_no_US[classification])
            if entity_partial[0]+", "+entity_partial[1] not in per_se_ed:
                break
        country = entity_partial[0]
        entity_type = entity_partial[1]
        entity_suffix = entity_partial[2]
        country_language = language_by_country[country]
        entity_name = random.choice(abc.animals_by_country_dict[country_language])
    
    if type_triple[1] == 0:
        member_language = 'has only one member.'
    elif type_triple[1] == 1:
        member_language = 'has more than one member.' 
        
    if type_triple[2] == 0:
        liability_language = 'At least one member of the entity has unlimited liability.'
    elif type_triple[2] == 1:
        liability_language = 'All members of the entity have limited liability.'
    
    default_choice = triple_default_elect_dict[triple_string]['default']
    
    elect_choice =  triple_default_elect_dict[triple_string]['elect']

    other_entity = BusinessEntity(country,entity_type,entity_suffix,entity_name,default_choice,elect_choice,member_language,liability_language,type_triple,foreign_US)
    
    return(other_entity)
    
# problem = f"{entity_name} {entity_suffix} is organized in {country} as {fm.pick_a_an(entity_type)} {entity_type}. Is {entity_name} eligible to check the box?" 
# print(problem)
# def create_entity():
# country = random.choice[terms_by_country.keys()]
# business_suffix =  random.choice[terms_by_country[country]]
#print(per_se_corp_ed)