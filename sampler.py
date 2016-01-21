import requests
import argparse
import xml.dom.minidom as minidom
import collections as col
import itertools


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', metavar='URL', help="input url")
    parser.add_argument('expected_result', type=int, nargs="*", help="IAB categories in correct format")
    args = parser.parse_args()
    return args

#xml parsing, created dictionary of 2 attributes, pass id return iab
def xml_map(xml_file, expected_input):
    xmlParsedFile = minidom.parse(xml_file)
    xml_list = xmlParsedFile.getElementsByTagName('Category')
    IDAdvertCategory = [row.attributes['IDAdvertCategory'].value for row in xml_list]
    ClientIAB = [row.attributes['ClientIAB'].value for row in xml_list]
    IDAdvertCategory = list(map(int, IDAdvertCategory))
    IDtoIABtuple=list(zip(IDAdvertCategory, ClientIAB))
    IDtoIABdict = col.defaultdict(list)
    for id,ib in IDtoIABtuple:
        IDtoIABdict[id].append(ib)
    getvalue=[IDtoIABdict.get(id, 'Not found') for id in expected_input if id in IDtoIABdict]
    mergedIABs=list(itertools.chain.from_iterable(getvalue))
    parent=[i.split('-')[0] for i in mergedIABs]
    combined_lists=mergedIABs+parent
    final_list=list(col.OrderedDict.fromkeys(combined_lists))
    return final_list



#get response from rest call, compare to expected result
def rawbody_response(url, setIABs):
    r = requests.get(url)
    body_response=r.text
    true_response=body_response.split()
    expected_iab=xml_map(xml_file, setIABs)
    counter_one=0
    counter_two=0
    counter_three=0
    if set(expected_iab)==set(true_response):
        counter_one = counter_one +1
        return url + " Test result = [PASS]" + " \t Counter: " +str(counter_one)
    elif len(true_response)==0:
        counter_two = counter_two +1
        return url + " Test result = [EMPTY]" + "\t Counter: " +str(counter_two)
    else:
        counter_three = counter_three + 1
        return url + " Test result = [FAIL]"+ "\t Counter: " + str(counter_three)




def main():
    args = get_args()
    input_url ="".join((stage_adress,args.url))

    b=xml_map(xml_file, args.expected_result)
    print(b)
    a=rawbody_response(input_url, args.expected_result)
    print(a)


stage_adress="http://lax4.wesee.com:8080/?loc="
xml_file="/home/emma/Python/Files/xmlclient"

#example input for argparse
#.20minutos.es/noticia/2030681/0/pobreza/vida-sexual/menos-satisfactoria 508 305 582
#http://beautyheart.org/pull-out-braid/4/ 10157 303 10014 10054 372

if __name__ == '__main__':
    main()
