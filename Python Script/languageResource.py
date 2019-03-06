# -*- coding: utf-8 -*-
import os
import sys
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from xml.etree.ElementTree import ElementTree, Element, SubElement, dump


class MyError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

def get_gdoc_information_android():
    GDOC_ID = sys.argv[1]
    JSON_KEY_PATH = sys.argv[2]
    VALUES_PATH = sys.argv[3]
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_PATH, scope)

    #구글 로그인
    gc = gspread.authorize(credentials)
    #시트오픈
    sh = gc.open_by_key(GDOC_ID)
    print ":::::::::::::spreadsheets open:::::::::::::"
    # Select worksheet by index. Worksheet indexes start from zero
    worksheet = sh.sheet1
    print ":::::::::::::Select worksheet:::::::::::::"

    all_values = worksheet.get_all_values()

    for idx, locale in enumerate(all_values[0][1:]):
        generate_xml(all_values, VALUES_PATH, locale, idx)

def generate_xml(datas, values_dir, locale, idx):
    print "::::::::::::: %s parse start!:::::::::::::" % locale

    if locale == 'en':
        values_path = os.path.join(values_dir, "values")
    else:
        values_path = os.path.join(values_dir, "values-" + locale)

    resources = Element("resources")

    for value in datas[1:]:
        data = value[idx]
        key = value[0]
        SubElement(resources, "string", name=key).text = data

    if not os.path.exists(values_path):
        os.makedirs(values_path)

    resource_tree = ElementTree(resources)
    resource_tree.write(os.path.join(values_path, "strings.xml"), encoding='utf-8', xml_declaration=True)


if __name__=='__main__':
    get_gdoc_information_android()
