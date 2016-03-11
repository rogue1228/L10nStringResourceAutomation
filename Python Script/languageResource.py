import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import csv;

import gdata.docs.service
import gdata.spreadsheet.service

from xml.etree.ElementTree import ElementTree, Element, SubElement, dump


'''
    get google doc information from the command line argument
    download method
    Create by : YoungChan Lee

'''
def get_gdoc_information_android():
    #email = raw_input('Email address:')
    #password = getpass('Password:')
    #gdoc_id = raw_input('Google Doc Id:')
    gdoc_id = sys.argv[1]
    downloadpath = sys.argv[2]
    try:
        file_path = download(gdoc_id)
        readCSV(downloadpath,file_path)
    except Exception, e:
        print ":::::::::::::ERROR:::::::::::::"
        print(e)
        #raise e

def download(gdoc_id, download_path=None, ):

    print "Downloading the CVS file with id %s" % gdoc_id

    gd_client = gdata.docs.service.DocsService()

    #auth using ClientLogin
    gs_client = gdata.spreadsheet.service.SpreadsheetsService()
    #gs_client.ClientLogin(email, password)

    #getting the key(resource id and tab id from the ID)
    resource    = gdoc_id.split('#')[0]
    tab         = gdoc_id.split('#')[1].split('=')[1]
    resource_id = 'spreadsheet:'+resource

    if download_path is None:
        download_path = os.path.abspath(os.path.dirname(__file__))

    file_name = os.path.join(download_path, '%s.csv' % (gdoc_id))

    print 'download_path : %s' % download_path;
    print 'Downloading spreadsheet to %s' % file_name

    docs_token = gd_client.GetClientLoginToken()
    gd_client.SetClientLoginToken(gs_client.GetClientLoginToken())
    gd_client.Export(resource_id, file_name, gid=tab)
    gd_client.SetClientLoginToken(docs_token)

    print "Download Completed!"

    return file_name

def readCSV(savepath, file_name):
    print "read CSV file : %s" % file_name
    SourceCSV= open(file_name,"r")
    csvReader = csv.reader(SourceCSV)
    header = csvReader.next()
    androidkey_idx = header.index("android_key")
    eng_idx = header.index("eng")
    kor_idx = header.index("kor")
    jap_idx = header.index("jap")

    # Make an empty Element
    resources_eng = Element("resources")
    resources_kor = Element("resources")
    resources_jap = Element("resources")

    # Loop through the lines in the file and get each coordinate
    for row in csvReader:
        androidkey = row[androidkey_idx]
        eng = row[eng_idx]

        kor = row[kor_idx]
        if not row[kor_idx]:
            kor = row[eng_idx]

        jap = row[jap_idx]
        if not row[jap_idx]:
            jap = row[eng_idx]


        #append eng resource
        if row[eng_idx]:
            string_eng = Element("string")
            string_eng.attrib["name"] = androidkey.decode('utf-8')
            string_eng.text = eng.decode('utf-8')
            resources_eng.append(string_eng)

            #append kor resource
            string_kor = Element("string")
            string_kor.attrib["name"] = androidkey.decode('utf-8')
            string_kor.text =  kor.decode('utf-8')
            resources_kor.append(string_kor)

            #append jap resource
            string_jap = Element("string")
            string_jap.attrib["name"] = androidkey.decode('utf-8')
            string_jap.text = jap.decode('utf-8')
            resources_jap.append(string_jap)


    # Print the coordinate list    
    #dump(resources_eng)
    #dump(resources_kor)
    #dump(resources_jap)

    #Make Resource Folder
    newpath_en = savepath+r'\values'
    if not os.path.exists(newpath_en):
        os.makedirs(newpath_en)

    newpath_ko = savepath+r'\values-ko'
    if not os.path.exists(newpath_ko):
        os.makedirs(newpath_ko)


    newpath_ja = savepath+r'\values-ja'
    if not os.path.exists(newpath_ja):
        os.makedirs(newpath_ja)

    #make Xml file
    ElementTree(resources_eng).write(newpath_en+"\\string.xml", "utf-8")
    ElementTree(resources_kor).write(newpath_ko+"\\string.xml", "utf-8")
    ElementTree(resources_jap).write(newpath_ja+"\\string.xml", "utf-8")

    SourceCSV.close()
    os.remove(file_name)


if __name__=='__main__':
    get_gdoc_information_android()
