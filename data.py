import pandas as pd
import urllib.request
import json
from datetime import date, datetime
import time
import os


def get_data(stk_name):
    try:
        list_of_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                          'August', 'September', 'October', 'November', 'December']

        data = urllib.request.urlopen(
            "https://query1.finance.yahoo.com/v8/finance/chart/"+stk_name+".NS?region=IN&lang=en-US&interval=1mo&useYfid=true&range=max").read()
        output = json.loads(data.decode('utf-8'))

        # Geting Month and year from API...
        f_year = []
        res = []
        year_obj_main = [i for i in output['chart']
                         ['result'][0]['timestamp']]
        for t in year_obj_main:
            if len(f_year) == 0:
                res.append(str(datetime.fromtimestamp(t).year))
                # Frst Year from API
                f_year.append(int(datetime.fromtimestamp(t).year))
                # res.append(str(datetime.fromtimestamp(t).month) +
                #            '.' + str(datetime.fromtimestamp(t).year))
            else:
                res.append(str(datetime.fromtimestamp(t).year))
                # res.append(str(datetime.fromtimestamp(t).month) +
                #            '.' + str(datetime.fromtimestamp(t).year))

        #  Getting Close Values
        close = [j for j in output['chart']['result']
                 [0]['indicators']["adjclose"][0]["adjclose"]]

        #  Removing Un completed year/month Values...
        todays_date = date.today()
        year = [i for i in range((f_year[0]), todays_date.year + 1, 1)]

        ct = 0
        for i in range(0, len(res), 1):
            if int(res[i]) == int(f_year[0]):
                ct = ct + 1
            else:
                break

        if ct != 12:
            del close[:ct]
            del year[:1]
        else:
            pass

        # Change Close to  percenage...
        close_pt = [0]
        for i in range(0, len(close)-1, 1):
            pt = round((((close[i+1]/close[i])-1)*100), 2)
            close_pt.append(pt)

        #  Mapping Year to respecive month wise close value and Creating Dictionary....
        fdic = {}
        count = 0
        maxi = 12
        for i in year:
            for j in range(count, maxi, 1):

                if i not in fdic:
                    fdic[i] = []
                try:
                    fdic[i].append(close_pt[j])
                except:
                    continue
            count = maxi
            maxi = maxi + 12

        del fdic[todays_date.year][todays_date.month]
        # Creating Marix...

        dp = pd.DataFrame.from_dict(
            fdic, orient='index', columns=list_of_months)

        mydir = "Stocks"
        CHECK_FOLDER = os.path.isdir(mydir)
        if not CHECK_FOLDER:
            os.mkdir(mydir)

        os.chdir(mydir)
        f = open(os.path.join(os.getcwd(), stk_name + '.csv'),
                 'w+', newline='')
        dp.to_csv(f)
        print(stk_name + ".CSV Generated")
        os.chdir('..')
        f.close()
        return dp

    except:
        print("No Stock Data Available....")
