from asyncio.base_tasks import _task_print_stack
import requests
from bs4 import BeautifulSoup
import pandas as pd
teamlist = ["NYY","BAL","LAA","CLE","CHC","SFG","ATL","PIT","SEA","PHI","HOU","MIL","DET","WSN","CIN","COL","BOS","KCR","MIN","TOR","LAD","STL","CHW","OAK","TBR","MIA","SDP","NYM","TEX","ARI"]
full_team_list = ["Yankees","Orioles","Angels","Cleveland","Cubs","Giants","Braves","Pirates","Mariners","Phillies","Astros","Brewers","Tigers","Nationals","Reds","Rockies","Boston","Royals","Twins","Jays","Dodgers","Cardinals","White","Athletics","Rays","Marlins","Padres","Mets","Rangers","Diamondbacks"]
def getbox(month,day,year):
    response = requests.get(
        "https://www.baseball-reference.com/boxes/?month="+ str(month) +"&day="+str(day)+"&year="+str(year))
    soup = BeautifulSoup(response.text, "html.parser")

    loser_list = []
    l_list = []
    winner_list = []
    w_list = []
    t_list = []
    p_list = []
    count = 0
    # per = soup.find_all("table",id = "standings-upto-AL-overall")
    tdd = soup.find_all("td",class_ = "right")
    te = soup.find_all("th",class_ = "left")
    for e in te:
        if count == 30:
            break
        t_list.append(e.getText())
        count+=1
    # print(t_list)
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
    # print(p_list)
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
    print(L1)
    print(W1)
    a = [x for x in L1 if x in W1] #列表中相同元素
    print(a)
    for i in a:
        if i in L1:
            L1.remove(i)
        if i in W1:
            W1.remove(i)
    print("12132123132")
    print(L1)
    print(W1)
    # lnew = list((set(l_list) ^ set(w_list))&set(l_list))
    # wnew = list((set(l_list) ^ set(w_list))&set(w_list))
    # print(lnew)
    # print(wnew)
    return L1,W1
l,w=getbox(5,28,2022)
# print(l)
# print(w)



