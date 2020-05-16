import pandas as pd
import time
import requests
import json
import datetime
from tqdm import tqdm
from datetime import datetime

def get_date_ranges():
    dates_list = []

    # Making list of dates; Each January 1st and June 1st from 2015 until January 1st 2020
    for i in range(11, 21):
        dates_list.append('01/01/20'+str(i))
        dates_list.append('01/02/20'+str(i))
        dates_list.append('01/03/20'+str(i))
        dates_list.append('01/04/20'+str(i))
        dates_list.append('01/05/20'+str(i))
        dates_list.append('01/06/20'+str(i))
        dates_list.append('01/07/20'+str(i))
        dates_list.append('01/08/20'+str(i))
        dates_list.append('01/09/20'+str(i))
        dates_list.append('01/10/20'+str(i))
        dates_list.append('01/11/20'+str(i))
        dates_list.append('01/12/20'+str(i))

    dates_list = dates_list[:-11]
    return dates_list


def get_user_comments(user, size, after, before):
    url = (f'https://api.pushshift.io/reddit/search/comment/?author={user}&sort=asc&size={size}&after={after}&before={before}')
    r = requests.get(url)
    try:
        raw_json = json.loads(r.text)
        data = raw_json['data']
        comments = [[post['body'], post['link_id'], post['id'], datetime.utcfromtimestamp(post['created_utc'])] for post in data]
    except json.decoder.JSONDecodeError:
        return []
    return comments


def getTimeStamp(date_input):
    return time.mktime(datetime.strptime(date_input, "%d/%m/%Y").timetuple())


# comments = get_user_comments('awalker88', 10, int(getTimeStamp('1/4/2020')), int(getTimeStamp('27/4/2020')))


dates = [int(getTimeStamp(date)) for date in get_date_ranges()]

cmmts = []
for i in tqdm(range(len(dates)-1)):
    # Setting up dates
    after = dates[i]
    before = dates[i+1]

    cmmts.append(get_user_comments('mindofmetalandwheels', 500, after=after, before=before))
    time.sleep(0.5)

unrolled_cmmts = []
for cmmt in cmmts:
    for c in cmmt:
        unrolled_cmmts.append(c)

cmmts = pd.DataFrame(unrolled_cmmts, columns=['comment', 'link_id', 'id', 'time'])
cmmts['permalink'] = 'www.reddit.com/comments/' + cmmts['link_id'].str[3:] + '/_/' + cmmts['id']
cmmts.to_csv('cgp_grey_comments.csv', index=False)