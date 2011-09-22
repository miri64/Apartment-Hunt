#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Copyright (c) 2011 Martin Lenders

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import simplejson as json
from htmlentitydefs import name2codepoint
import lxml.html
import codecs
import os, sys
import re
import locale
from shutil import rmtree
from urllib import urlopen, urlencode
from getpass import getpass
import urllib2
import ConfigParser
import datetime
from urlparse import urlparse,parse_qs,urlunparse

from pyquery import PyQuery

boroughs = {
        '10115': u'Mitte',
        '10117': u'Mitte',
        '10119': u'Mitte',
        '10178': u'Mitte',
        '10179': u'Mitte',
        '10243': u'Friedrichshain',
        '10245': u'Friedrichshain',
        '10247': u'Friedrichshain/Prenzlauer Berg',
        '10249': u'Friedrichshain/Prenzlauer Berg',
        '10315': u'Friedrichfelde',
        '10317': u'Friedrichfelde/Lichtenberg/Rummelsburg',
        '10318': u'Friedrichfelde/Karlshorst',
        '10319': u'Friedrichfelde/Karlshorst',
        '10365': u'Lichtenberg',
        '10367': u'Lichtenberg',
        '10405': u'Prenzlauer Berg',
        '10407': u'Prenzlauer Berg',
        '10409': u'Prenzlauer Berg',
        '10435': u'Mitte/Prenzlauer Berg',
        '10437': u'Prenzlauer Berg',
        '10439': u'Pankow/Prenzlauer Berg',
        '10551': u'Tiergarten',
        '10553': u'Tiergarten',
        '10555': u'Tiergarten',
        '10557': u'Tiergarten',
        '10559': u'Tiergarten',
        '10585': u'Charlottenburg',
        '10587': u'Charlottenburg',
        '10589': u'Charlottenburg',
        '10623': u'Charlottenburg (City)',
        '10625': u'Charlottenburg (City)',
        '10627': u'Charlottenburg (City)',
        '10629': u'Charlottenburg (City)',
        '10707': u'Charlottenburg/Wilmersdorf',
        '10709': u'Charlottenburg/Wilmersdorf',
        '10711': u'Charlottenburg/Grunewald/Wilmersdorf',
        '10713': u'Wilmersdorf',
        '10715': u'Wilmersdorf',
        '10717': u'Wilmersdorf',
        '10719': u'Wilmersdorf/Charlottenburg',
        '10777': u'Wilmersdorf/Schöneberg',
        '10779': u'Schöneberg/Wilmersdorf',
        '10781': u'Schöneberg',
        '10783': u'Schöneberg',
        '10785': u'Kreuzberg/Schöneberg/Tiergarten',
        '10787': u'Charlottenburg/Schöneberg/Tiergarten',
        '10789': u'Charlottenburg/Schöneberg/Wilmersdorf',
        '10823': u'Schöneberg',
        '10825': u'Schöneberg/Wilmersdorf',
        '10827': u'Friedenau/Schöneberg',
        '10829': u'Schöneberg',
        '10961': u'Kreuzberg',
        '10963': u'Kreuzberg/Tiergarten',
        '10965': u'Kreuzberg/Schöneberg/Tempelhof/Neukölln',
        '10967': u'Kreuzberg/Neukölln',
        '10969': u'Kreuzberg',
        '10997': u'Kreuzberg',
        '10999': u'Kreuzberg',
        '12043': u'Neukölln',
        '12045': u'Neukölln',
        '12047': u'Neukölln',
        '12049': u'Neukölln',
        '12051': u'Neukölln',
        '12053': u'Neukölln',
        '12055': u'Neukölln',
        '12057': u'Neukölln',
        '12059': u'Neukölln',
        '12099': u'Britz/Mariendorf/Neukölln/Tempelhof',
        '12101': u'Tempelhof',
        '12103': u'Mariendorf/Schöneberg/Tempelhof',
        '12105': u'Schöneberg/Tempelhof/Mariendorf',
        '12107': u'Lichtenrade/Mariendorf/Marienfelde/Tempelhof/Buckow',
        '12109': u'Tempelhof/Mariendorf',
        '12157': u'Friedenau/Schöneberg/Steglitz',
        '12159': u'Friedenau/Schöneberg',
        '12161': u'Friedenau/Steglitz',
        '12163': u'Friedenau/Steglitz',
        '12165': u'Steglitz',
        '12167': u'Steglitz',
        '12169': u'Steglitz',
        '12203': u'Lichterfelde',
        '12205': u'Lichterfelde',
        '12207': u'Lichterfelde',
        '12209': u'Lichterfelde',
        '12247': u'Steglitz',
        '12249': u'Lankwitz',
        '12277': u'Mariendorf/Marienfelde',
        '12279': u'Lichterfelde/Marienfelde',
        '12305': u'Buckow/Lichtenrade',
        '12307': u'Lichtenrade/Marienfelde',
        '12309': u'Lichtenrade',
        '12347': u'Britz',
        '12349': u'Britz/Buckow',
        '12351': u'Britz/Buckow/Rudow',
        '12353': u'Buckow/Rudow',
        '12355': u'Rudow',
        '12357': u'Buckow/Rudow',
        '12359': u'Britz/Buckow/Rudow',
        '12435': u'Alt-Treptow/Neukölln/Plänterwald',
        '12437': u'Baumschulenweg/Plänterwald',
        '12439': u'Niederschöneweide/Oberschöneweide',
        '12459': u'Oberschöneweide',
        '12487': u'Adlershof/Johannisthal',
        '12489': u'Adlershof/Johannisthal',
        '12524': u'Altglienicke',
        '12526': u'Bohnsdorf',
        '12527': u'Flughafen Schönefeld/Grünau/Karolinenhof/Schmöckwitz',
        '12555': u'Köpenick',
        '12557': u'Köpenick',
        '12559': u'Köpenick/Müggelheim',
        '12587': u'Friedrichshagen',
        '12589': u'Hessenwinkel/Rahnsdorf/Wilhelmshagen',
        '12619': u'Hellersdorf/Kaulsdorf',
        '12621': u'Hellersdorf/Kaulsdorf',
        '12623': u'Kaulsdorf/Mahlsdorf',
        '12627': u'Hellersdorf',
        '12629': u'Hellersdorf',
        '12679': u'Marzahn',
        '12681': u'Marzahn',
        '12683': u'Biesdorf',
        '12685': u'Marzahn',
        '12687': u'Marzahn',
        '12689': u'Marzahn',
        '13051': u'Hohenschönhausen/Malchow/Margaretenhöhe/Wartenberg',
        '13053': u'Hohenschönhausen',
        '13055': u'Hohenschönhausen',
        '13057': u'Falkenberg/Hohenschönhausen',
        '13059': u'Hohenschönhausen/Wartenberg',
        '13086': u'Weissensee',
        '13088': u'Stadtrandsiedlung Malchow/Weissensee',
        '13089': u'Heinersdorf',
        '13125': u'Buch/Karow',
        '13127': u'Buchholz/Französisch Buchholz',
        '13129': u'Blankenburg',
        '13156': u'Niederschönhausen/Rosenthal',
        '13158': u'Französisch Buchholz/Niederschönhausen/Rosenthal',
        '13159': u'Blankenfelde',
        '13187': u'Pankow',
        '13189': u'Pankow',
        '13347': u'Wedding',
        '13349': u'Wedding',
        '13351': u'Wedding',
        '13353': u'Charlottenburg/Tiergarten/Wedding',
        '13355': u'Wedding',
        '13357': u'Wedding',
        '13359': u'Wedding',
        '13403': u'Reinickendorf/Tegel/Wittenau',
        '13405': u'Reinickendorf/Tegel/Wedding',
        '13407': u'Reinickendorf/Wedding/Wittenau',
        '13409': u'Reinickendorf/Wedding',
        '13435': u'Wittenau',
        '13437': u'Reinickendorf/Wittenau',
        '13439': u'Wittenau',
        '13465': u'Frohnau/Hermsdorf',
        '13467': u'Hermsdorf',
        '13469': u'Lübars/Reinickendorf/Waidmannslust/Wittenau',
        '13503': u'Heiligensee/Tegel',
        '13505': u'Heiligensee/Konradshöhe/Tegel',
        '13507': u'Tegel',
        '13509': u'Reinickendorf/Tegel/Wittenau (mit Borsigwalde)',
        '13581': u'Spandau/Staaken',
        '13583': u'Spandau',
        '13585': u'Spandau',
        '13587': u'Hakenfelde/Spandau',
        '13589': u'Spandau',
        '13591': u'Spandau/Staaken',
        '13593': u'Spandau/Staaken',
        '13595': u'Pichelsdorf/Spandau',
        '13597': u'Charlottenburg/Pichelsdorf/Spandau',
        '13597': u'Charlottenburg/Pichelsdorf/Spandau',
        '13599': u'Haselhorst/Siemensstadt/Spandau/Tegel',
        '13627': u'Charlottenburg (Nord)/Siemensstadt',
        '13629': u'Charlottenburg/Siemensstadt/Tegel',
        '14050': u'Charlottenburg (Westend)',
        '14052': u'Charlottenburg',
        '14053': u'Charlottenburg',
        '14055': u'Charlottenburg/Grunewald/Wilmersdorf',
        '14057': u'Charlottenburg',
        '14059': u'Charlottenburg',
        '14089': u'Gatow (Kladow)',
        '14109': u'Nikolassee/Wannsee',
        '14129': u'Nikolassee/Zehlendorf',
        '14163': u'Nikolassee/Zehlendorf',
        '14165': u'Zehlendorf',
        '14167': u'Lichterfelde/Zehlendorf',
        '14169': u'Dahlem/Lichterfelde/Zehlendorf',
        '14193': u'Dahlem/Grunewald/Nikolassee/Schmargendorf',
        '14195': u'Dahlem/Lichterfelde/Schmargendorf/Steglitz/Wilmersdorf',
        '14197': u'Friedenau/Wilmersdorf (Rheingau)',
        '14199': u'Grunewald/Schmargendorf/Wilmersdorf',
    }

def _get_json_object(filename):
    if os.path.exists(filename):
        fp = open(filename)
        try:
            obj = json.load(fp)
            date = datetime.datetime.strptime(obj['date'],"%Y-%M-%d")
            age = date - datetime.datetime.today()
            if age <= datetime.timedelta(days=3):
                return obj
        except json.decoder.JSONDecodeError:
            pass
        except KeyError,e:
            if e.args[0] == 'date': pass
            else:
                print 'KeyError:',e
    return dict()

def _set_json_object(filename,obj):
    fp = open(filename,"w")
    return json.dump(obj,fp,ensure_ascii=False)

old_exposes = _get_json_object(os.path.join(os.path.dirname(__file__),'old_exposes.json'))
new_exposes = {'date':datetime.date.today().isoformat()}

def ensure_dir(dirname):
    try:
        os.makedirs(dirname)
    except OSError:
        pass

def unescape(s):
    s = re.sub('&#([0-9]+);', lambda m: unichr(int(m.group(1))), s)
    return re.sub('&(%s);' % '|'.join(name2codepoint), 
            lambda m: unichr(name2codepoint[m.group(1)]), s)

class AbstractExpose:
    def get_title(self):
        if self.title == None:
            self.title = self.pyquery('title').text()
        return self.title
    
    def get_borough(self):
        if self.borough == None:
            address = self.get_address()
            zip = re.search('[0-9]{5}',address)
            self.borough = None
            if zip != None:
                self.borough = boroughs.get(zip.group())
            if self.borough == None:
                title = self.get_title()
                link = self.get_expose_link()
                the_boroughs = set(boroughs.values())
                self.borough = 'k. A.'
                for borough in the_boroughs:
                    for sub in borough.split('/'):
                        if title.find(sub) >= 0:
                            self.borough = sub
                        if link.lower().find(sub.lower()) >= 0:
                            self.borough = sub
        return self.borough
    
    def get_address(self):
        raise NotImplementedError()
        
    def get_expose_link(self):
        return self.expose_link
    
    def get_contact(self):
        raise NotImplementedError()
    
    def get_cold_rent(self):
        raise NotImplementedError()
    
    def get_additional_charges(self):
        raise NotImplementedError()
    
    def get_operation_expenses(self):
        raise NotImplementedError()
    
    def get_heating_cost(self):
        raise NotImplementedError()
    
    def get_heating_type(self):
        raise NotImplementedError()
    
    def get_total_rent(self):
        raise NotImplementedError()
    
    def get_object_state(self):
        raise NotImplementedError()
    
    def get_security(self):
        raise NotImplementedError()
    
    def get_commission(self):
        raise NotImplementedError()
    
    def get_space(self):
        raise NotImplementedError()
    
    def get_floor(self):
        raise NotImplementedError()
    
    def get_flat_type(self):
        raise NotImplementedError()
    
    def get_rooms(self):
        raise NotImplementedError()
    
    def get_year(self):
        raise NotImplementedError()
    
    def get_availability(self):
        raise NotImplementedError()
    
    def __str__(self):
        return '<Expose: '+self.expose_link+'>'
    
    def __repr__(self):
        return str(self)
    
    def as_dict(self):
        return {
                'title': self.title,
                'borough': self.borough,
                'address': self.address,
                'expose_link': self.expose_link,
                'contact': self.contact,
                'cold_rent': self.cold_rent,
                'additional_charges': self.additional_charges,
                'operation_expenses': self.operation_expenses,
                'heating_cost': self.heating_cost,
                'heating_type': self.heating_type,
                'total_rent': self.total_rent,
                'object_state': self.object_state,
                'security': self.security,
                'commission': self.commission,
                'space': self.space,
                'floor': self.floor,
                'flat_type': self.flat_type,
                'rooms': self.rooms,
                'year': self.year,
                'availability': self.availability,
            }
    
    def __init__(self,expose_link):
        self.pyquery = PyQuery(lxml.html.parse(expose_link).getroot())
        self.title = None
        self.borough = None
        self.address = None
        self.expose_link = expose_link
        self.contact = None
        self.cold_rent = None
        self.additional_charges = None
        self.operation_expenses = None
        self.heating_cost = None
        self.heating_type = None
        self.total_rent = None
        self.object_state = None
        self.security = None
        self.commission = None
        self.space = None
        self.floor = None
        self.flat_type = None
        self.rooms = None
        self.year = None
        self.availability = None

class GeneralExpose(AbstractExpose):
    def get_title(self):
        return self.title
    
    def get_borough(self):
        return self.borough
    
    def get_address(self):
        return self.address
        
    def get_expose_link(self):
        return self.expose_link
    
    def get_contact(self):
        return self.contact
    
    def get_cold_rent(self):
        return self.cold_rent
    
    def get_additional_charges(self):
        return self.additional_charges
    
    def get_operation_expenses(self):
        return self.operation_expenses
    
    def get_heating_cost(self):
        return self.heating_cost
    
    def get_heating_type(self):
        return self.heating_type
    
    def get_total_rent(self):
        return self.total_rent
    
    def get_object_state(self):
        return self.object_state
    
    def get_security(self):
        return self.security
    
    def get_commission(self):
        return self.commission
    
    def get_space(self):
        return self.space
    
    def get_floor(self):
        return self.floor
    
    def get_flat_type(self):
        return self.flat_type
    
    def get_rooms(self):
        return self.rooms
    
    def get_year(self):
        return self.year
    
    def get_availability(self):
        return self.availability
    
    def __get_delegate(self):
        if self.expose_link != None:
            if self.expose_link.find('immobilienscout24.de') >= 0:
                return ImmoscoutExpose(self.expose_link)
            elif self.expose_link.find('immonet.de') >= 0:
                return ImmonetExpose(self.expose_link)
            elif self.expose_link.find('immowelt.de') >= 0:
                return ImmoweltExpose(self.expose_link)
        raise Exception("Illegal Link: "+self.expose_link)
    
    def __getattr__(self,attr):
        if isinstance(self.delegate, dict):
            value = eval('self.delegate.get("%s")' % attr)
            if value != None:
                return value
            self.delegate = self.__get_delegate()
        return eval('self.delegate.get_%s()' % attr)
    
    def __str__(self):
        return str(self.delegate)
    
    def __repr__(self):
        return repr(self.delegate)
    
    def as_dict(self):
        if isinstance(self.delegate, dict):
            return self.delegate
        else:
            return self.delegate.as_dict()
    
    def __init__(self,expose_link):
        self.expose_link = expose_link
        if self.expose_link in old_exposes.keys():
            self.delegate = old_exposes[self.expose_link]
        else:
            self.delegate = self.__get_delegate()

class ImmoscoutExpose(AbstractExpose):
    def get_address(self):
        if self.address == None:
            self.address = lxml.html.tostring(self.pyquery("div.is24-ex-address p")[1],
                        method="text",
                        encoding="iso-8859-1"
                    )
            if not self.address:
                self.address = u'k. A.'
            else:
                self.address = self.address.replace(',','')
                self.address = self.address.replace('\r','')
                self.address = re.sub('Karte ansehenStreet View','', self.address)
                self.address = self.address.strip()
                self.address = unicode(re.sub('\n\s+', ', ', self.address),encoding='iso-8859-1')
        return self.address
    
    def get_contact(self):
        if self.contact == None:
            self.contact = self.pyquery("div.is24-ex-realtor-s").html()
            if not self.contact:
                self.contact = 'k. A.'
            else:
                self.contact = re.sub('<[^>]*>','',self.contact)
                self.contact = re.sub('[\t\n]','',self.contact)
                self.contact = re.sub(' (&#13;)+',', ',self.contact)
                self.contact = re.sub('(&#13;)+ ',', ',self.contact)
                self.contact = re.sub('(&#13;)+',', ',self.contact)
                self.contact = re.sub(', +(, +)*',', ',self.contact)
                self.contact = re.sub(':[^ ]',': ',self.contact)
                self.contact = re.sub('[ ]+',' ',self.contact)
                self.contact = re.sub(', $','',self.contact).strip()
        return self.contact
        
        
    def get_cold_rent(self):
        if self.cold_rent == None:
            self.cold_rent = self.pyquery("strong.is24qa-kaltmiete").text()
            if not self.cold_rent:
                self.cold_rent = 'k. A.'
        return self.cold_rent
    
    def get_additional_charges(self):
        if self.additional_charges == None:
            self.pyquery(".is24-operator").remove()
            self.additional_charges = self.pyquery("td.is24qa-nebenkosten").text()
            if not self.additional_charges:
                self.additional_charges = 'k. A.'
        return self.additional_charges
    
    def get_operation_expenses(self):
        return 'k. A.'
    
    def get_heating_cost(self):
        if self.heating_cost == None:
            self.pyquery(".is24-operator").remove()
            self.heating_cost = self.pyquery("td.is24qa-heizkosten").text()
            if not self.heating_cost:
                self.heating_cost = 'k. A.'
            else:
                self.heating_cost = re.sub(r'\n\s*',' ',self.heating_cost.replace('\r',''))
        return self.heating_cost
    
    def get_heating_type(self):
        if self.heating_type == None:
            self.heating_type = self.pyquery("td.is24qa-heizungsart").text()
            if not self.heating_type:
                self.heating_type = 'k. A.'
        return self.heating_type
    
    def get_total_rent(self):
        if self.total_rent == None:
            self.pyquery(".is24-operator").remove()
            self.total_rent = self.pyquery("strong.is24qa-gesamtmiete").text()
            if not self.total_rent:
                self.total_rent = 'k. A.'
        return self.total_rent
    
    def get_object_state(self):
        if self.object_state == None:
            self.object_state = self.pyquery("td.is24qa-objektzustand").text()
            if not self.object_state:
                self.object_state = 'k. A.'
        return self.object_state
    
    def get_security(self):
        if self.security == None:
            self.security = self.pyquery("td.is24-mortgage").text()
            if not self.security:
                self.security = 'k. A.'
        return self.security
    
    def get_commission(self):
        if self.commission == None:
            self.commission = self.pyquery("td.is24qa-provision").text()
            if not self.commission:
                self.commission = 'k. A.'
        return self.commission
    
    def get_space(self):
        if self.space == None:
            self.space = self.pyquery("td.is24qa-wohnflaeche-ca").text()
            if self.space:
                self.space = 'ca. '+self.space
            else:
                self.space = 'k. A.'
        return self.space
    
    def get_floor(self):
        if self.floor == None:
            self.floor = self.pyquery("td.is24qa-etage").text()
            if not self.floor:
                self.floor = 'k. A.'
        return self.floor
    
    def get_flat_type(self):
        if self.flat_type == None:
            self.flat_type = self.pyquery("td.is24qa-wohnungstyp").text()
            if not self.flat_type:
                self.flat_type = 'k. A.'
        return self.flat_type
    
    def get_rooms(self):
        if self.rooms == None:
            self.rooms = self.pyquery("td.is24qa-zimmer").text()
            if not self.rooms:
                self.rooms = 'k. A.'
        return self.rooms
    
    def get_year(self):
        if self.year == None:
            self.year = self.pyquery("td.is24qa-baujahr").text()
            if not self.year:
                self.year = 'k. A.'
        return self.year
    
    def get_availability(self):
        if self.availability == None:
            self.availability = self.pyquery("td.is24qa-bezugsfrei-ab").text()
            if not self.availability:
                self.availability = 'k. A.'
        return self.availability

class ImmonetExpose(AbstractExpose):
    def find_in_table(self,sub):
        try:
            return [n for n in self.pyquery("td.label") \
                    if unicode(n.text).find(sub) != -1
                ][0].getparent()[1]
        except IndexError:
            return None
    
    def evaluate_table_value(self,key):
        value = self.find_in_table(key)
        tostring = lambda tag: lxml.html.tostring(tag, encoding='utf8', method='text')
        if value != None:
            if len(tostring(value).strip()) > 0:
                return tostring(value).strip()
        return 'k. A.'
    
    def get_address(self):
        if self.address == None:
            address_html = self.pyquery('div#objektAdresse div').html()
            find_links = re.search("\w*<a",address_html)
            if find_links != None:
                self.address = re.sub(r'<br\s*/>\n\s*', ', ', address_html[0:find_links.start()]).strip()
            else:
                self.address = re.sub(r'<br\s*/>\n\s*', ', ', address_html).strip()
            self.address = unicode(re.sub(r'<br\s*/>', '', self.address).strip())
            if not self.address:
                self.address = u'k. A.'
        return self.address
    
    def get_contact(self):
        if self.contact == None:
            contact_name = self.pyquery('a#firmName').text()
            if contact_name:
                contact_name = contact_name.strip()
            else:
                contact_wrap = self.pyquery('div#anbieter p.wrap')
                if len(contact_wrap) > 0:
                    contact_name = contact_wrap[0].text.strip()
                else:
                    contact_name = 'k. A.'
            contact_phone = self.pyquery('#boxPhone2').text()
            if contact_phone:
                contact_phone = ' ('+re.sub('([0-9]+) ([^0-9]+)',r'\1, \2',contact_phone).strip()+')'
            else:
                contact_phone = self.pyquery('#boxPhone1').text()
                if contact_phone:
                    contact_phone = ' ('+re.sub('([0-9]+) ([^0-9]+)',r'\1, \2',contact_phone).strip()+')'
                else:
                    contact_phone = ''
            self.contact = contact_name + contact_phone
        return self.contact
    
    def get_cold_rent(self):
        if self.cold_rent == None:
            self.cold_rent = self.evaluate_table_value('Miete zzgl. NK')
        return self.cold_rent
    
    def get_additional_charges(self):
        if self.additional_charges == None:
            self.additional_charges = self.evaluate_table_value('Nebenkosten')
        return self.additional_charges
    
    def get_operation_expenses(self):
        if self.operation_expenses == None:
            self.operation_expenses = self.evaluate_table_value('Betriebskosten')
        return self.operation_expenses
    
    def get_heating_cost(self):
        if self.heating_cost == None:
            self.heating_cost = self.evaluate_table_value('Heizkosten')
        return self.heating_cost
    
    def get_heating_type(self):
        if self.heating_type == None:
            self.heating_type = self.evaluate_table_value('Heizung')
        return self.heating_type
    
    def get_total_rent(self):
        if self.total_rent == None:
            rent = 0
            try:
                rent = float(re.search(r'[0-9]*\.*[0-9]*,*[0-9]+',self.get_cold_rent()).group().replace('.','').replace(',','.'))
            except AttributeError:
                pass
            try:
                rent += float(re.search(r'[0-9]*\.*[0-9]*,*[0-9]+',self.get_additional_charges()).group().replace('.','').replace(',','.'))
            except AttributeError:
                pass
            try:
                rent += float(re.search(r'[0-9]*\.*[0-9]*,*[0-9]+',self.get_operation_expenses()).group().replace('.','').replace(',','.'))
            except AttributeError:
                pass
            try:
                rent += float(re.search(r'[0-9]*\.*[0-9]*,*[0-9]+',self.get_heating_cost()).group().replace('.','').replace(',','.'))
            except AttributeError:
                pass
            try:
                total_rent = self.find_in_table('Miete inkl. NK')
                if total_rent == 'k. A.':
                    total_rent = self.find_in_table('Monatsmiete')
                total_rent = float(re.search(r'[0-9]*[.,][0-9]*[,.]*[0-9]+',total_rent.text.strip()).group().replace('.','').replace(',','.'))
                if total_rent > rent:
                    rent = total_rent
            except AttributeError:
                pass
            
            self.total_rent = locale.str(rent)+u' €'
        return self.total_rent
    
    def get_object_state(self):
        if self.object_state == None:
            self.object_state = self.evaluate_table_value("Zustand")
        return self.object_state
    
    def get_security(self):
        if self.security == None:
            self.security = self.evaluate_table_value('Kaution')
            if self.security == 'k. A.':
                self.security = re.sub(u'[0-9,.] €','\0',self.evaluate_table_value('Genossenschaftsanteil'))
        return self.security
    
    def get_commission(self):
        if self.commission == None:
            self.commission = self.evaluate_table_value("Courtage")
        return self.commission
    
    def get_space(self):
        if self.space == None:
            self.space = self.find_in_table(u'Wohnfläche')
            if self.space != None:
                self.space = re.sub('.sup2;*',u'²',self.space.text.strip())
            else:
                self.space = 'k. A.'
        return self.space
    
    def get_floor(self):
        if self.floor == None:
            self.floor = self.evaluate_table_value("Etage")
        return self.floor
    
    def get_flat_type(self):
        if self.flat_type == None:
            metas = self.pyquery("meta")
            self.flat_type = 'k. A.'
            for meta in metas:
                if meta.get("name") == "description":
                    self.flat_type = meta.get("content")
        return self.flat_type
    
    def get_rooms(self):
        if self.rooms == None:
            self.rooms = self.evaluate_table_value("Zimmer")
        return self.rooms
    
    def get_year(self):
        if self.year == None:
            self.year = self.evaluate_table_value("Baujahr")
        return self.year
    
    def get_availability(self):
        if self.availability == None:
            self.availability = self.evaluate_table_value(u"Verfügbar ab")
        return self.availability

class ImmoweltExpose(AbstractExpose):
    def get_basic_value(self,k):
        try:
            try:
                return self.basic_values[k]
            except AttributeError:
                keys = self.pyquery('span.eckdatenbezeichner')
                values = self.pyquery('span.eckdatencontent')
                self.basic_values = dict()
                for l,v in zip(keys,values):
                    key = lxml.html.tostring(l,encoding=unicode,method='text').strip().strip(':')
                    value = lxml.html.tostring(v,encoding=unicode,method='text').strip()
                    self.basic_values[key] = value
                return self.basic_values[k]
        except KeyError:
            return None
    
    def get_from_read(self,k):
        try:
            try:
                return self.read[k]
            except AttributeError:
                keys = self.pyquery('div.read h6')
                values = self.pyquery('div.read p')
                self.read = dict()
                for l,v in zip(keys,values):
                    key = lxml.html.tostring(l,encoding=unicode,method='text').strip()
                    value = lxml.html.tostring(v,encoding=unicode,method='text').strip()
                    self.read[key] = value
                return self.read[k]
        except KeyError:
            return None
    
    def get_address(self):
        if self.address == None:
            self.address = ''
            street = self.pyquery('#ctl00_MainContent_ExposeAnschrift1_lblStrasse')
            if street != None:
                self.address += street.text().strip() + ', '
            zip_town = self.pyquery('#ctl00_MainContent_ExposeAnschrift1_lblPlzOrt')
            if zip_town != None:
                self.address += zip_town.text().strip()
            borough = self.pyquery('#ctl00_MainContent_ExposeAnschrift1_lblStadtteil')
            if borough != None:
                self.address += ' '+borough.text().strip()
            self.address = self.address.strip()
        return self.address
    
    def get_contact(self):
        if self.contact == None:
            address_json = re.findall('{eo:.*};',str(self.pyquery('script')))[0]
            address_json = address_json.replace('eo','"eo"')
            address_json = address_json.replace('v','"v"')
            address_json = address_json.replace('i','"i"').strip(';')
            address_scramble = eval(address_json)['eo']
            address = {
                    'exposeOffererName': dict(),
                    'exposeOffererAddress': dict(),
                    'exposeOffererContact': dict(),
                }
            for a in address_scramble:
                parent = self.pyquery('#'+a['i'])[0].getparent().getparent()
                address_part_id = parent.get('id')
                address_part = unescape(unescape(a['v']))
                address_order = [lxml.html.tostring(e).find(a['i']) >= 0 for e in parent].index(True)
                if address_part_id == 'exposeOffererContact':
                    address_part = self.pyquery('#'+a['i'])[0].getparent()[0].text + ' ' + address_part
                address[address_part_id][address_order] = address_part
            self.contact = ''
            for id in address:
                for part in address[id]:
                    self.contact += address[id][part].strip()+', '
                self.contact = self.contact.strip().strip(',')+'; '
            self.contact = self.contact.strip().strip(';')
            if len(self.contact) == 0:
                self.contact = 'k. A.'
        return self.contact
    
    def get_cold_rent(self):
        if self.cold_rent == None:
            self.cold_rent = self.get_basic_value(u'Kaltmiete')
            if self.cold_rent == None:
                self.cold_rent = 'k. A.'
        return self.cold_rent
    
    def get_additional_charges(self):
        if self.additional_charges == None:
            self.additional_charges = self.get_basic_value(u'Nebenkosten')
            if self.additional_charges == None:
                self.additional_charges = 'k. A.'
        return self.additional_charges
    
    def get_operation_expenses(self):
        if self.operation_expenses == None:
            self.operation_expenses = self.get_basic_value(u'Betriebskosten')
            if self.operation_expenses == None:
                self.operation_expenses = 'k. A.'
        return self.operation_expenses
    
    def get_heating_cost(self):
        if self.heating_cost == None:
            self.heating_cost = self.get_basic_value(u'Heizkosten')
            if self.heating_cost == None:
                self.heating_cost = 'k. A.'
        return self.heating_cost
    
    def get_heating_type(self):
        if self.heating_type == None:
            facilities = self.pyquery('.linklist_icon_04 li')
            self.heating_type = 'k. A.'
            tostring = lambda x: lxml.html.tostring(x, encoding=unicode, method='text')
            for f in facilities:
                if tostring(f).lower().find('heizung'):
                    self.heating_type = tostring(f).strip()
                    break
        return self.heating_type
    
    def get_total_rent(self):
        if self.total_rent == None:
            rent = 0
            try:
                rent = float(re.search(r'[0-9]*\.*[0-9]*,*[0-9]+',self.get_cold_rent()).group().replace('.','').replace(',','.'))
            except AttributeError:
                pass
            try:
                rent += float(re.search(r'[0-9]*\.*[0-9]*,*[0-9]+',self.get_additional_charges()).group().replace('.','').replace(',','.'))
            except AttributeError:
                pass
            try:
                rent += float(re.search(r'[0-9]*\.*[0-9]*,*[0-9]+',self.get_operation_expenses()).group().replace('.','').replace(',','.'))
            except AttributeError:
                pass
            try:
                rent += float(re.search(r'[0-9]*\.*[0-9]*,*[0-9]+',self.get_heating_cost()).group().replace('.','').replace(',','.'))
            except AttributeError:
                pass
            try:
                total_rent = self.get_basic_value(u'Warmmiete')
                if total_rent != None:
                    total_rent = float(re.search(r'[0-9]*\.*[0-9]*,*[0-9]+',total_rent).group().replace('.','').replace(',','.'))
                    if total_rent > rent:
                        rent = total_rent
                else:
                    return 'k. A.'
            except AttributeError:
                pass
            
            self.total_rent = str(rent)+u' €'
        return self.total_rent
    
    def get_object_state(self):
        if self.object_state == None:
            self.object_state = 'k. A.'
        return self.object_state
    
    def get_security(self):
        if self.security == None:
            self.security = self.get_basic_value(u'Kaution')
            if self.security == None:
                self.security = 'k. A.'
        return self.security
    
    def get_commission(self):
        if self.commission == None:
            self.commission = self.get_from_read(u'Provision')
            if self.commission == None or self.commission == 'Die Mieterprovision beträgt':
                self.commission = 'k. A.'
        return self.commission
    
    def get_space(self):
        if self.space == None:
            self.space = self.get_basic_value(u'Wohnfläche')
            if self.space == None:
                self.space = 'k. A.'
        return self.space
    
    def get_floor(self):
        if self.floor == None:
            self.floor = self.get_basic_value(u'Stockwerk')
            if self.floor != None:
                if self.floor == 'Erdgeschoss':
                    return '0'
                self.floor = re.sub('([0-9]+)\. Etage',r'\1',self.floor)
            else:
                self.floor = 'k. A.'
        return self.floor
    
    def get_flat_type(self):
        if self.flat_type == None:
            self.flat_type = self.get_basic_value(u'Immobilienart')
            if self.flat_type == None:
                self.flat_type = 'k. A.'
        return self.flat_type
    
    def get_rooms(self):
        if self.rooms == None:
            self.rooms = self.get_basic_value(u'Zimmer')
            if self.rooms == None:
                self.rooms = 'k. A.'
        return self.rooms
    
    def get_year(self):
        if self.year == None:
            self.year = self.get_basic_value(u'Baujahr')
            if self.year == None:
                self.year = 'k. A.'
        return self.year
    
    def get_availability(self):
        if self.object_state == None:
            self.object_state = 'k. A.'
        return self.object_state

class ExposeFilter:
    def in_borough(self,expose,boroughs):
        the_borough = expose.get_borough()
        for borough in boroughs:
            if the_borough.lower().find(borough.lower()) >= 0:
                return True
    
    def in_floors(self,expose,floors):
        floor = expose.get_floor()
        try:
            if int(floor) in floors:
                return True
        except TypeError:
            if int(floor) == floors:
                return True
        except ValueError:
            return False
        return False
    
    def is_one_of_types(self,expose,patterns):
        flat_type = expose.get_flat_type()
        for pattern in patterns:
            if re.search(pattern,flat_type):
                return True
        return False
    
    def is_commissioned(self,expose):
        commission = expose.get_commission()
        found = re.search(r'[0-9]+',commission) != None
        if not found:
            return commission.lower().find('miete') >= 0 or commission.lower() == 'ja'
        return found
        
    def has_min_rooms(self,expose,room_number):
        rooms = expose.get_rooms()
        if rooms != 'k. A.':
            return float(rooms.replace(',','.')) >= room_number
        else:
            return True
    
    @staticmethod
    def parse_total_rent(rent_str):
        rent = re.search('[0-9]+[,.]*[0-9]*',rent_str)
        if rent == None:
            return 0
        else:
            rent = rent.group()
            return float(rent.replace(',','.'))
    
    def has_max_total_rent(self,expose,total_rent):
        rent = ExposeFilter.parse_total_rent(expose.get_total_rent())
        if rent == 0:
            return False
        else:
            return rent <= total_rent
    
    def has_one_of_heating_types(self,expose,patterns):
        heating_type = expose.get_heating_type()
        if heating_type != 'k. A.':
            for pattern in patterns:
                if re.search(pattern,heating_type):
                    return True
        return False
    
    def has_one_of_object_states(self,expose,patterns):
        object_state = expose.get_object_state()
        if object_state != 'k. A.':
            for pattern in patterns:
                if re.search(pattern,object_state):
                    return True
        return False
    
    def realtor_company_name_contains(self,expose,patterns):
        contact = expose.get_contact()
        for pattern in patterns:
            if re.search(pattern,contact):
                return True
    
    def categorize(self,expose):
        total_rent = ExposeFilter.parse_total_rent(expose.get_total_rent())
        category = (int(total_rent)/10)*10
        if self.categories.has_key(category):
            self.categories[category].append(expose)
        else:
            self.categories[category] = [expose]
    
    def __init__(self, expose_links):
        self.categories = dict()
        print "Filtering..."
        prog = ProgressBar(len(expose_links))
        for num,expose_link in enumerate(expose_links):
            sys.stdout.write(str(prog.update(num))+' \r') 
            expose = GeneralExpose(expose_link)
            if (not self.in_floors(expose,0) and 
                not self.is_commissioned(expose) and
                self.has_min_rooms(expose,2) and
                not self.has_one_of_heating_types(expose,[r'Ofenheizung']) and
                not self.has_one_of_object_states(expose,[r'[Rr]enovierungsbed.*rftig','[Uu]nrenoviert']) and
                not self.is_one_of_types(expose,[r'[Ee]rdgeschoss',r'[Pp]arterre',r'[Ff]erien']) and
                self.has_max_total_rent(expose,500) and
                not self.realtor_company_name_contains(expose,[r'GMRE','GAGFAH']) and
                not self.in_borough(expose,[
                        'Adlershof',
                        'Biesdorf',
                        'Britz',
                        'Buckow',
                        'Französisch Buchholz',
                        'Friedrichsfelde',
                        'Heiligensee',
                        'Hellersdorf',
                        'Karlshorst',
                        'Konradshöhe',
                        'Köpenick',
                        'Lichtenberg',
                        'Lichtenrade',
                        'Lichterfelde',
                        'Mariendorf',
                        'Marienfelde',
                        'Marzahn',
                        'Pankow',
                        'Plänterwald',
                        'Reinickendorf',
                        'schönhausen',
                        'schöneweide',
                        'Spandau',
                        'Tegel',
                        'Wannsee',
                        'Wartenberg',
                        'Wittenau'
                    ])):
                self.categorize(expose)
            new_exposes[expose_link] = expose.as_dict()
        print prog.update(num+1), '\r' 

class ProgressBar:
    def update(self, amount = 0):
        if amount < 0:
            amount = 0
        if amount > self.max:
            amount = self.max
        self.amount = amount
        
        fraction = float(self.amount) / self.max
        
        hundred_percent = self.width - 2
        num_symbols = int(round(fraction * hundred_percent))
        
        self.bar = self.start_sym + self.fill_sym*num_symbols + \
                self.empty_sym*(hundred_percent-num_symbols) + self.end_sym
        percent_str = "%3.2f%%" % (fraction*100)
        percent_place = (len(self.bar) / 2) - len(percent_str) / 2 - 1
        self.bar = self.bar[0:percent_place] + percent_str + \
                self.bar[(percent_place+len(percent_str)):]
        return self.bar
    
    def __str__(self):
        return str(self.bar)
    
    def __init__(self,max,width=40,start_sym='[',end_sym=']',fill_sym='=',empty_sym=' '):
        self.bar = ''
        self.max = max
        self.width = width
        self.start_sym = start_sym
        self.end_sym = end_sym
        self.fill_sym = fill_sym
        self.empty_sym = empty_sym
        self.amount = 0
        self.update()

def get_pages(search_url):
    try: 
        search_page = PyQuery(lxml.html.parse(urlopen(search_url)).getroot())
        if (search_url.find('immonet.de') >= 0):
            return int(search_page("div#pager1 a")[-2].text)
        elif (search_url.find('immobilienscout24.de') >= 0):
            pager = search_page(".is24-pager-s").text()
            return int(re.search(r'Seite [0-9]+ von ([0-9]+)',pager).group(1))
    except TypeError, e:
        print e
    except IOError, e:
        print e
    return 0

def get_results_per_page(search_url):
    if (search_url.find('immonet.de') >= 0):
        listsize = parse_qs(urlparse(search_url).query).get('listsize')
        if (listsize):
            return int(listsize[0])
        else:
            return 12

def get_search_links(search_url,max_pages = None):
    search_url = search_url.strip().strip('\n')
    pages = get_pages(search_url)
    if max_pages != None and max_pages < pages:
        pages = max_pages
    links = []
    if (search_url.find('immonet.de') >= 0):
        parsed_url = urlparse(search_url)
        query = parse_qs(parsed_url.query)
        results_per_page = get_results_per_page(search_url)
                
        for i in range(pages):
            query['pageoffset'] = 1 + i * results_per_page
            links.append(urlunparse((
                    parsed_url[0],
                    parsed_url[1],
                    parsed_url[2],
                    parsed_url[3],
                    urlencode(query).replace('%27%5D','').replace('%5B%27',''),
                    parsed_url[5]
                )))
            
    if (search_url.find('immobilienscout24.de') >= 0):
        search_url = re.sub(r'Suche/S-([0-9]*)/Wohnung-Miete',r'Suche/S-\1/P-1/Wohnung-Miete',search_url)
        for i in range(1,pages+1):
            links.append(search_url.replace(r'/P-1/',("/P-%d/"%i)))
    if (search_url.find('immowelt.de') >= 0):
        links.append(search_url)
            
    return links

def generate_wiki_overview(categories):
    wiki = codecs.open(os.path.join(os.path.dirname(__file__),"wiki_page.txt"),encoding='utf-8',mode="w")
    wiki_page = get_wiki_page()
    number = 0
    today = datetime.date.today()
    wiki.write(u"== Kandidaten %s ==\n" % today.strftime("%Y-%M-%d"))
    for i in range(51):
        category = categories.get(i*10)
        if category != None:
            wiki.write(u"=== Preisklasse %d0 - %d9 € ===\n" % (i,i))
            for entry in category:
                if in_wiki(wiki_page,entry):
                    wiki.write(u"[%s-%05d] ''' ''(bereits im Wiki!!!)'' %s '''\n" % (today.strftime("%Y%M%d"), number, entry.get_title()))
                else:
                    wiki.write(u"[%s-%05d] ''' %s '''\n" % (today.strftime("%Y%M%d"), number, entry.get_title()))
                number += 1
                wiki.write(u' * Expose: %s\n' % entry.get_expose_link())
                wiki.write(u' * Bezirk: ' + entry.get_borough() + '\n')
                wiki.write(u'  * Adresse: %s\n' % entry.get_address())
                wiki.write(u' * Gesamtmiete: %s\n' % entry.get_total_rent())
                wiki.write(u'  * Kaltmiete: %s\n' % entry.get_cold_rent())
                wiki.write(u'  * Nebenkosten: %s\n' % entry.get_additional_charges())
                wiki.write(u'  * Heizkosten: %s\n' % entry.get_heating_cost())
                wiki.write(u'  * Betriebskosten: %s\n' % entry.get_operation_expenses())
                wiki.write(u' * Kaution: %s\n' % entry.get_security())
                wiki.write(u' * Provision: %s\n' % entry.get_commission())
                wiki.write(u' * Wohnfläche: %s\n' % entry.get_space())
                wiki.write(u' * Zimmer: %s\n' % entry.get_rooms())
                wiki.write(u' * Etage: %s\n' % entry.get_floor())
                wiki.write(u' * Verfügbar ab: %s\n' % entry.get_availability())
                wiki.write(u' * Kontakt: %s\n' % entry.get_contact())
                wiki.write('\n')
                new_exposes[entry.get_expose_link()] = entry.as_dict()
            wiki.write('\n')
    wiki.close()

def get_config(config_path):
    config = ConfigParser.ConfigParser()
    try:
        configfile = open(config_path)
        config.readfp(configfile)
        configfile.close()
    except IOError:
        pass
    return config

def set_config(config_path, config):
    configfile = open(config_path,'w')
    config.write(configfile)
    configfile.close()

def prompt_user_passwd():
    username = raw_input('Username: ')
    password = getpass()
    return username, password

def get_wiki_authentication():
    config_path = os.path.join(os.path.dirname(__file__), 'config')
    config = get_config(config_path)
    if not config.has_section('wiki authentication'):
        config.add_section('wiki authentication')
        username, password = prompt_user_passwd()
        config.set('wiki authentication','username',username)
        config.set('wiki authentication','password',password)
        set_config(config_path,config)
    else:
        username = config.get('wiki authentication','username')
        password = config.get('wiki authentication','password')
    return username, password

def get_wiki_page():
    print "Get Wiki-Page for reference"
    username, password = get_wiki_authentication()
    while 1:
        try:
            password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
            top_level_url = "http://yoursiblings.org/trac/wiki/"
            password_mgr.add_password(None, top_level_url, username, password)
            handler = urllib2.HTTPBasicAuthHandler(password_mgr)
            opener = urllib2.build_opener(handler)
            fp = opener.open('http://yoursiblings.org/trac/wiki/Wohnungssuche?format=txt')
            break
        except urllib2.HTTPError, e:
            print e, '... Please repeat your username and password'
            config_path = os.path.join(os.path.dirname(__file__), 'config')
            config = get_config(config_path)
            username, password = prompt_user_passwd()
            config.set('wiki authentication','username',username)
            config.set('wiki authentication','password',password)
            set_config(config_path,config)
    wiki_page = fp.read()
    fp.close()
    print "  ... Done"
    return wiki_page
    
def in_wiki(wiki, expose):
    return wiki.find(expose.get_expose_link()) >= 0

def get_expose_links(search_urls, pages = None):
    print "Collecting expose links:"
    expose_links = set()
    
    for search_url in search_urls:
        search_url = search_url.strip().strip('\n')
        print "* For '" + str(search_url)+"'"
        host = urlparse(search_url).netloc
        if pages != None:
            links = get_search_links(search_url, pages)
        else:
            links = get_search_links(search_url)
        if len(links) > 0:
            prog = ProgressBar(len(links))
            for num,link in enumerate(links):
                file = urlopen(link)
                parsed_url = urlparse(link)
                if parsed_url.netloc.find('immonet.de') >= 0:
                    sys.stdout.write(str(prog.update(num))+' \r') 
                    page = file.read()
                    regex = re.compile(r'<a id="lnkToDetails_[0-9]*" href="([^"]*)"')
                    for a_tag in regex.finditer(page):
                        expose_links = expose_links.union([parsed_url.scheme+'://'+parsed_url.netloc+a_tag.group(1)])
                elif parsed_url.netloc.find('immobilienscout24.de') >= 0:
                    sys.stdout.write(str(prog.update(num))+' \r') 
                    page = file.read()
                    regex = re.compile(r'<a href="(/expose/[0-9]*)')
                    for a_tag in regex.finditer(page):
                        expose_links = expose_links.union([parsed_url.scheme+'://'+parsed_url.netloc+urlparse(a_tag.group(1)).path])
                elif parsed_url.netloc.find('immowelt.de') >= 0:
                    root = lxml.html.parse(file).getroot()
                    pyquery = PyQuery(root)
                    last_first = 1
                    hits_count_span = pyquery(
                            'span#ctl00_MainContent_ListNavigation1_lblHitsCount'
                        ).text()
                    hits = re.search('\(von\s*([0-9]+)\s*Objekten\)',hits_count_span).group(1)
                    prog = ProgressBar(int(hits))
                    page_num = 1
                    while 1:
                        sys.stdout.write(str(prog.update(last_first))+' \r')
                        match = re.search('([0-9]+)\s*-\s*([0-9]+)',hits_count_span)
                        if (last_first > int(match.group(1)) or 
                                int(match.group(1)) > int(match.group(2))):
                            break
                        if pages != None:
                            if page_num > pages:
                                break
                        
                        page = lxml.html.tostring(root)
                        regex = re.compile(r'<a href="(/immobilien/immodetail\.aspx\?id=[0-9]+)')
                        for a_tag in regex.finditer(page):
                            expose_links = expose_links.union([parsed_url.scheme+'://'+parsed_url.netloc+a_tag.group(1)])
                        
                        fields = pyquery('form#aspnetForm input')
                        last_first = int(match.group(1))
                        params = {'__EVENTTARGET':'ctl00$MainContent$ListNavigation1$nlbPlus'}
                        for field in fields:
                            if (field.get('type') == 'text' or 
                                    field.get('type') == 'hidden' or 
                                    field.get('type') == 'password'):
                                params[field.get('name')] = field.get('value')
                        page_num += 1
                        file = urlopen(link, urlencode(params))
                        root = lxml.html.parse(file).getroot()
                        pyquery = PyQuery(root)
                        hits_count_span = pyquery(
                            'span#ctl00_MainContent_ListNavigation1_lblHitsCount'
                        ).text()
                    num = hits
                else:
                    raise Exception('URL of host %s://%s not supported' % (parsed_url.scheme,parsed_url.netloc))
                file.close()
    print prog.update(num)
    return expose_links

def encode_expose(obj):
    return dict(obj)

if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf-8')
    if (len(sys.argv) < 2):
        stderr.write("Usage: %s <Search-URL-File> [<Page number>]\n", argv[0])
    search_urls = open(sys.argv[1])
        
    if len(sys.argv) == 3:
        expose_links = get_expose_links(search_urls, int(sys.argv[2]))
    else:
        expose_links = get_expose_links(search_urls)
    
    if len(expose_links) > 0:
        filter = ExposeFilter(expose_links)
        
        generate_wiki_overview(filter.categories)
    else:
        sys.stderr.write("Error: No expose links found.\n")
    _set_json_object(os.path.join(os.path.dirname(__file__),'old_exposes.json'),new_exposes)

