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
    #test 현재경로
    # VALUES_PATH = os.getcwd()
    #구글 로그인
    gc = gspread.authorize(credentials)
    #시트오픈
    sh = gc.open_by_key(GDOC_ID)
    print ":::::::::::::spreadsheets open:::::::::::::"
    # Select worksheet by index. Worksheet indexes start from zero
    worksheet = sh.sheet1
    print ":::::::::::::Select worksheet:::::::::::::"
    # Make an empty Element
    resources_eng = Element("resources")
    resources_kor = Element("resources")
    resources_jap = Element("resources")

    all_records = worksheet.get_all_records(empty2zero=False, head=1, default_blank='')
    for record in all_records:
        try:
        # print("key : %s value : %s"% (record[u'android_key'],record[u'eng']))
            if record[u'eng'] == "" : raise MyError("리소스 만들기 실패 key %s : 기본번역이 없습니다." %record[u'android_key'].encode('utf-8'))
        
            SubElement(resources_eng, "string", name=record[u'android_key']).text = record[u'eng'] 
            SubElement(resources_kor, "string", name=record[u'android_key']).text = record[u'kor'] if record[u'kor'] != "" else record[u'eng']
            SubElement(resources_jap, "string", name=record[u'android_key']).text = record[u'jap'] if record[u'jap'] != "" else record[u'eng']
        except MyError as e:
            print(e)

    KR_PATH = os.path.join(VALUES_PATH, "values-ko")
    EN_PATH = os.path.join(VALUES_PATH, "values")
    JA_PATH = os.path.join(VALUES_PATH, "values-ja")

    # 폴더가 없으면 만들어준다
    if not os.path.exists(VALUES_PATH):
        os.makedirs(VALUES_PATH)

    if not os.path.exists(KR_PATH):
        os.makedirs(KR_PATH)

    if not os.path.exists(EN_PATH):
        os.makedirs(EN_PATH)

    if not os.path.exists(JA_PATH):
        os.makedirs(JA_PATH)

    krTree = ElementTree(resources_eng)
    krTree.write(os.path.join(EN_PATH, "strings.xml"), encoding='utf-8', xml_declaration=True)
    krTree = ElementTree(resources_kor)
    krTree.write(os.path.join(KR_PATH, "strings.xml"), encoding='utf-8', xml_declaration=True)
    krTree = ElementTree(resources_jap)
    krTree.write(os.path.join(JA_PATH, "strings.xml"), encoding='utf-8', xml_declaration=True)


if __name__=='__main__':
    get_gdoc_information_android()