import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

#2011~2019 & 2021 10 years 5/1~9/25
begin_month = 5
end_month = 5
begin_day = 1
end_day = 1
begin_year = 2022
end_year = 2022
def getWinPer(month,day,year):
    response = requests.get(
        "https://www.baseball-reference.com/boxes/?month="+ str(month) +"&day="+str(day)+"&year="+str(year))
    soup = BeautifulSoup(response.text, "html.parser")
    t_list = []    #30 teams order
    p_list = []    #win per 30 teams order
    count = 0
    # per = soup.find_all("table",id = "standings-upto-AL-overall")
    tdd = soup.find_all("td",class_ = "right")
    te = soup.find_all("th",class_ = "left")
    for e in te:
        if count == 30:
            break
        if e.getText() == 'FLA':
            t_list.append('MIA')
        else:
            t_list.append(e.getText())
        count+=1
    count = 0
    reverse = True
    for t in tdd:
        if t.getText()[0] == '.':
            if reverse:
                p_list.append(t.getText())
                count += 1
            reverse = reverse^1
        if count == 30:
            break
    return t_list,p_list
def getbox(month,day,year):
    response = requests.get(
        "https://www.baseball-reference.com/boxes/?month="+ str(month) +"&day="+str(day)+"&year="+str(year))
    soup = BeautifulSoup(response.text, "html.parser")
    loser_list = []
    l_list = []
    winner_list = []
    w_list = []
    losers = soup.find_all("tr",class_ = "loser")
    for loser in losers:
        loser_list.append(loser.select_one("a").getText())
        # print(loser.select_one("a").getText())
    for l in loser_list:
        for team in full_team_list:
            if team in l:
                l_list.append(teamlist[full_team_list.index(team)])
    winners = soup.find_all("tr",class_ = "winner")
    for winner in winners:
        winner_list.append(winner.select_one("a").getText())
    for w in winner_list:
        for team in full_team_list:
            if team in w:
                w_list.append(teamlist[full_team_list.index(team)])
    L1 = []
    W1 = []
    for i in l_list:
        if i not in L1:
            L1.append(i)
    for i in w_list:
        if i not in W1:
            W1.append(i)
    a = [x for x in L1 if x in W1] #列表中相同元素
    for i in a:
        if i in L1:
            L1.remove(i)
        if i in W1:
            W1.remove(i)
    return L1,W1
def getNextDay(month,day):
    if day == 31 and month in [5,7,8,10]:
        day = 1
        month+=1
    elif day == 30 and month in [4,6,9]:
        day = 1
        month += 1
    else:
        day += 1
    return month,day
def getLastNDay(month,day,n):
    if day > n-1:
        day -= n-1
    elif month in [4,6,8,9,11]:
        day += 32-n
        month -= 1
    else:
        day += 31-n
        month -= 1
    return month,day

def changeDateType(begin_month,end_month,begin_day,end_day):
    if begin_month < 10:
        begin_month = "0" + str(begin_month)
    else:
        begin_month = str(begin_month)
    if begin_day < 10:
        begin_day = "0" + str(begin_day)
    else:
        begin_day = str(begin_day)
    if end_month < 10:
        end_month = "0" + str(end_month)
    else:
        end_month = str(end_month)
    if end_day < 10:
        end_day = "0" + str(end_day)
    else:
        end_day = str(end_day)
    return begin_month,end_month,begin_day,end_day
customRange = []
pitcher = []
scoreBoard = []
row  = 0
col = 0
teamlist = ["NYY","BAL","LAA","CLE","CHC","SFG","ATL","PIT","SEA","PHI","HOU","MIL","DET","WSN","CIN","COL","BOS","KCR","MIN","TOR","LAD","STL","CHW","OAK","TBR","MIA","SDP","NYM","TEX","ARI","FLA"]
full_team_list = ["Yankees","Orioles","Angels","Cleveland","Cubs","Giants","Braves","Pirates","Mariners","Phillies","Astros","Brewers","Tigers","Nationals","Reds","Rockies","Boston","Royals","Twins","Jays","Dodgers","Cardinals","White","Athletics","Rays","Marlins","Padres","Mets","Rangers","Diamondbacks"]
# b_month,e_month,b_day,e_day=changeDateType(begin_month,end_month,begin_day,end_day)
#    https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2022&month=1000&season1=2022&ind=0&team=0%2Cts&rost=0&age=0&filter=&players=0&startdate=2022-05-01&enddate=2022-05-14
# response = requests.get(
#     "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2022&month=1000&season1=2022&ind=0&team=0%2Cts&rost=0&age=0&filter=&players=0&startdate="+str(begin_year)+"-"+b_month+"-"+b_day+"&enddate="+str(end_year)+"-"+e_month+"-"+e_day)
# soup = BeautifulSoup(response.text, "html.parser")
# print(soup.prettify())
# stats = soup.find_all("td",class_ = ["grid_line_regular","grid_line_break"])
df = pd.DataFrame([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]], columns=['TEAM','HR','BB%','K%','ISO','BABIP','AVG','OBP','SLG','WOBA','WRC+','BSR','DEF','K/9','BB/9','HR/9','FIP','ERA','GS','PBABIP','YEAR','MONTH','DAY','WPER','WPERN','OPP','TARGET'])
count = 0
count2 = 0
month = begin_month
day = begin_day
year = begin_year
num_days = 7
thisyear = 0
# while year < 2022:
while thisyear < 45:
    thisyear+=1
    t,p = getWinPer(month,day,year)
    month,day = getNextDay(month,day)
    monthnext,daynext = getNextDay(month,day)
    month7, day7 = getLastNDay(month,day,num_days)
    tn,pn = getWinPer(month7,day7,year)
    b_month,e_month,b_day,e_day=changeDateType(month7,month,day7,day)
    count = 0
    count2 += 1
    l,w = getbox(monthnext,daynext,year)
    response2 = requests.get(
        # https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2011&month=1000&season1=2011&ind=0&team=0%2Cts&rost=0&age=0&filter=&players=0&startdate=2011-05-01&enddate=2011-05-07
        "https://www.fangraphs.com/leaders.aspx?pos=all&stats=pit&lg=all&qual=0&type=8&season="+str(year)+"&month=1000&season1="+str(year)+"&ind=0&team=0%2Cts&rost=0&age=0&filter=&players=0&startdate="+str(year)+"-"+b_month+"-"+b_day+"&enddate="+str(year)+"-"+e_month+"-"+e_day
        )
    soup2 = BeautifulSoup(response2.text, "html.parser")
    response = requests.get(
        # https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season=2011&month=1000&season1=2011&ind=0&team=0%2Cts&rost=0&age=0&filter=&players=0&startdate=2011-05-01&enddate=2011-05-07
        "https://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg=all&qual=0&type=8&season="+str(year)+"&month=1000&season1="+str(year)+"&ind=0&team=0%2Cts&rost=0&age=0&filter=&players=0&startdate="+str(year)+"-"+b_month+"-"+b_day+"&enddate="+str(year)+"-"+e_month+"-"+e_day)
    soup = BeautifulSoup(response.text, "html.parser")
    stats = soup.find_all("td",class_ = ["grid_line_regular","grid_line_break"])
    stats_pitcher = soup2.find_all("td",class_ = ["grid_line_regular","grid_line_break"])
    for pit in stats_pitcher:
        if count%21 != 17:
            if pit.getText() == 'FLA':
                pitcher.append('MIA')
            else:
                pitcher.append(pit.getText())
        count += 1
    count = 0
    current_team = 0
    for stat in stats:
        # print(count2)
        new  = pd.DataFrame
        if count%22 != 16: 
            # customRange.append(stat.getText())
            customRange.append(stat.getText())
        count+=1
        if count%22==0 and count > 0:
            if customRange[1] == 'FLA':
                customRange[1] = 'MIA'
            opponent = 'NYY'
            nextgame = -1
            if customRange[1] in l:
                opponent = w[l.index(customRange[1])] 
                nextgame = 0
            elif customRange[1] in w:
                opponent = l[w.index(customRange[1])] 
                nextgame = 1
            else:
                opponent = 'NONE'
            wper = p[t.index(customRange[1])]
            wpern = pn[tn.index(customRange[1])]
            temp = teamlist.index(customRange[1])
            temp2 = pitcher.index(teamlist[temp])//20
            new  = pd.DataFrame({
                'TEAM':customRange[1],
                # 'PA':customRange[3],
                'HR':customRange[4],
                # 'R':customRange[5],
                'RBI':customRange[6],
                # 'SB':customRange[7],
                'BB%':customRange[8],
                'K%':customRange[9],
                'ISO':customRange[10],
                'BABIP':customRange[11],
                'AVG':customRange[12],
                'OBP':customRange[13],
                'SLG':customRange[14],
                'WOBA':customRange[15],
                'WRC+':customRange[16],
                'BSR':customRange[17],
                'DEF':customRange[19],
                'K/9':pitcher[temp2*20+8],
                'BB/9':pitcher[temp2*20+9],
                'HR/9':pitcher[temp2*20+10],
                'FIP':pitcher[temp2*20+17],
                'PBABIP':pitcher[temp2*20+11],
                'GS':pitcher[temp2*20+6],
                'ERA':pitcher[temp2*20+16],
                'YEAR':year,
                'MONTH':month,
                'DAY':day,
                'OPP':opponent,
                'WPERN':wpern,
                'TARGET':nextgame,
                'WPER':wper,   #wper
                # 'TARGET':customRange[20],   #target
                },
                index=[1]   
            )
            current_team += 1
            df=df.append(new,ignore_index=True)
            customRange = []
            
        #print(stat.getText())
        # customRange.append(stats.select_one("a").getText())
    print(str(month) + "day: "+ str(day))
    if month == 9 and day == 25:
        print(year)
        month = 5
        day = 1
        if year < 2019:
            year += 1
        elif year == 2019:
            year = 2021
        elif year == 2021:
            break
    pitcher = []
df =df.drop(df.index[0])
print(count2)
df.to_csv('data_test.csv',index=False)

