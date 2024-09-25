import requests
import os
import re
from bs4 import BeautifulSoup
from datetime import datetime
import os
import sys


source_id = 'US_Courts_VCLR_Rules'
location_id = 'Rules of Admission and Practice'

def ret_file_name_full(source_id, location_id, rule_name, extention):
    exe_folder = os.path.dirname(str(os.path.abspath(sys.argv[0])))
    date_prefix = datetime.today().strftime("%Y%m%d")
    out_path = os.path.join(exe_folder, 'out', remove_invalid_paths(source_id), remove_invalid_paths(location_id),
                            (date_prefix))
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    index = 1
    outFileName = os.path.join(out_path, remove_invalid_paths(rule_name) + extention)
    retFileName = outFileName
    while os.path.isfile(retFileName):
        retFileName = os.path.join(out_path, remove_invalid_paths(rule_name) + "_" + str(index) + extention)
    index += 1
    return retFileName


def ret_out_folder(source_id, location_id):
    exe_folder = os.path.dirname(str(os.path.abspath(sys.argv[0])))
    date_prefix = datetime.today().strftime("%Y%m%d")
    out_path = os.path.join(exe_folder, 'out', remove_invalid_paths(source_id), 'Skip Rules',
                            remove_invalid_paths(location_id), date_prefix)
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    return out_path

def remove_invalid_paths(path_val):
    return re.sub(r'[\\/*?:"<>|]', "", path_val)


sheet_links = {
         'Rules of Admission and Practice ': 'http://www.uscourts.cavc.gov/rules_of_admission_and_practice.php'

}

for rule_name, url in sheet_links.items():
    resource = requests.get(url)
    soup = BeautifulSoup(resource.text, "html.parser")

    table = soup.find('table')
    table = table.findAll('tr')
    for item in table:
        td_element = item.findAll('td')
        name=''
        for i in td_element:
            try:
                name+=str(i.text)
                if i.find('a'):
                    rule_url = 'http://www.uscourts.cavc.gov/' + i.find('a').get('href')
                    rule_response = requests.get(rule_url, allow_redirects=False)
                    if rule_response.status_code == 200:
                        rule_html = rule_response.text
                        resource = requests.get(rule_url)
                        soup = BeautifulSoup(resource.text, "html.parser")

                        content = soup.find('div', {'id': 'content_subpage'})
                        rule_name = content.find('h1').text

                        output_fileName = ret_file_name_full(source_id, location_id, rule_name,  '.html')
                        with open(output_fileName, 'w', encoding='utf-8') as f:
                            f.write(str(content))

            except Exception as e:
                pass
            else:
                print(f"Downloaded HTML for rule '{rule_name}' at URL: {rule_url}")




