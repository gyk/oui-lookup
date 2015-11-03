import urllib2

oui_list_uri = r'https://code.wireshark.org/review/gitweb?p=wireshark.git;a=blob_plain;f=manuf'

def download_oui():
    # Downloads OUI list from Wireshark manufacturer database
    response = urllib2.urlopen(oui_list_uri)
    txt = response.read()

    with open(r'oui.txt', 'w') as f:
        f.write(txt)

if __name__ == '__main__':
    download_oui()
