import re
import csv

# Example: '00:00:01    XeroxCor    # XEROX CORPORATION'
P_LINE = r'(?P<mac_prefix>[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2})\s+(?P<corp>[^\s]+)' \
    r'(?:\s+#\s(?P<comment>.+)){0,1}$'
p_line = re.compile(P_LINE)

oui_list = []

with open(r'./oui.txt', 'r') as f:
    for line in f:
        ma = p_line.match(line)
        if not ma:
            continue

        result = [None, None, None]
        result[0] = ma.group('mac_prefix').replace(':', '')
        result[1] = ma.group('corp')
        result[2] = ma.group('comment') if ma.group('comment') else ''

        oui_list.append(result)

def purge_comment(comment):
    """
    "SANYO Electric Co., Ltd" -> ['SANYO', 'Electric']
    """
    if comment == '':
        return ['']

    STOP_WORDS = set(['LTD', 'INC', 'CO', 'LLC', 'LIMITED', 'CORPORATION'])
    words = comment.replace('.', ' ').replace(',', ' ').split()
    words = [w for w in words if w.upper() not in STOP_WORDS]
    return words


all_corps = set(x[1] for x in oui_list)
exclusive_corps = set(all_corps)
corp_dict = {}

for [mac_prefix, corp, comment] in oui_list:
    if corp not in exclusive_corps:
        continue

    comment = ' '.join(purge_comment(comment)).lower()
    if not comment:
        continue
    if corp_dict.has_key(corp):
        if corp_dict[corp] != comment:
            exclusive_corps.remove(corp)
    else:
        corp_dict[corp] = comment

def to_title_case(w):
    return w[0].upper() + w[1:].lower()

for i in range(len(oui_list)):
    corp = oui_list[i][1]
    if corp not in exclusive_corps:
        comment = oui_list[i][2]
        if not comment:
            continue
        
        words = purge_comment(comment)
        description = to_title_case(words[0])

        if len(words) > 1:
            description += to_title_case(words[1])

        oui_list[i][1] = description

with open(r'./oui.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for l in oui_list:
        writer.writerow(l)
