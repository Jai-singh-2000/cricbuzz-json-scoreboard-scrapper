from bs4 import BeautifulSoup
import requests
import json
import os.path

def battingTable(content,list):
    
    name=""
    status=""
    runs=""
    bowled=""
    fours=""
    sixes=""
    strikeRate=""

    nameContainer=content.find('div',class_='cb-col-27')
    if nameContainer!=None: #Agar div none nahi hua to aage jana
        if nameContainer.a in nameContainer:
            name=nameContainer.a.text
    
    statusContainer=content.find('div',class_="cb-col cb-col-33")
    if statusContainer!=None:
        status=statusContainer.span.text

    runsContainer=content.find('div',class_="cb-col cb-col-8 text-right text-bold")
    if runsContainer!=None:
        runs=runsContainer.text

    scores=content.find_all('div',class_="cb-col cb-col-8 text-right")
    if scores!=[]:

        for idx,score in enumerate(scores):

            if idx==0:
                bowled=score.text
            elif idx==1:
                fours=score.text
            elif idx==2:
                sixes=score.text
            elif idx==3:
                strikeRate=score.text


    if name!="" and status!="" and runs!="" and bowled!="" and fours!="" and sixes!="" and strikeRate!="":
        # line=f'Batter {name} | Status {status} | Runs {runs} | Fours {fours} | Sixes {sixes} | Strike rate {strikeRate}'

        object={
            "name":name,
            "status":status,
            "runs":runs,
            "fours":fours,
            "sixes":sixes,
            "strikeRate":strikeRate
        }

        list.append(object)
       
# ---------------------------------------------

def bowlingTable(content,list):
    
    name=""
    runs=""
    maiden=""
    wickets=""
    noBall=""
    wides=""
    economyRate=""
    over=""

    nameContainer=content.find('div',class_='cb-col cb-col-40')
    if nameContainer!=None: #Agar div none nahi hua to aage jana
        name=nameContainer.a.text

    scores=content.find_all('div',class_="cb-col cb-col-8 text-right")
    if scores!=[]:
        for idx,score in enumerate(scores):
            if idx==0:
                over=score.text
            elif idx==1:
                maiden=score.text
            elif idx==2:
                noBall=score.text   
            elif idx==3:
                wides=score.text
    
    runsContainer=content.find_all('div',class_="cb-col cb-col-10 text-right")
    for idx,element in enumerate(runsContainer):
        if idx==0:
            if element!=None:
                runs=element.text
        elif idx==1:
            if element!=None:
                economyRate=element.text

    wicketsContainer=content.find('div',class_="cb-col cb-col-8 text-right text-bold")
    if wicketsContainer!=None:
        wickets=wicketsContainer.text

    
    if name!="" and over!="" and maiden!="" and noBall!="" and wides!="" and runs!="" and wickets!="" and economyRate!="":
        # print(f'Bowler {name} | Over {over} | Maiden {maiden} | Runs {runs} | Wickets {wickets} |  No-balls {noBall} | Wides {wides} |Economy-rate {economyRate}')

        object={
            "name":name,
            "over":over,
            "maiden":maiden,
            "noBall":noBall,
            "wides":wides,
            "runs":runs,
            "wickets":wickets,
            "economyRate":economyRate,
        }

        list.append(object)

# ---------------------------------------------

def findDirectory():
    i=1
    while i<=50:
        if os.path.exists(f"data{i}"):
            i=i+1
        else:
            directory_name=f"data{i}"
            os.makedirs(directory_name)
            return directory_name


# -----------------------------------------------

html_link = input("Enter cricbuzz scoreboard url : ")

html_text=requests.get(html_link).text

directory_name=findDirectory()

soup=BeautifulSoup(html_text,'lxml')


# Find all 6 tables
tables=soup.find_all('div','cb-col cb-col-100 cb-ltst-wgt-hdr') 

for number,table in enumerate(tables):
    #Iterate all table one by one
    
    
    if number==0 or number==3: #If table is first
        
        #Select all rows from 1st table
        rows=table.find_all('div',class_='cb-col cb-col-100 cb-scrd-itms')     
        batters_list=[]
        
        for idx, row in enumerate(rows):
            battingTable(row,batters_list) # Pass all rows as arguement one by one'
        
        table_no=""
        if number==0:
            table_no=1
        elif number==3:
            table_no=2

        jsonString = json.dumps(batters_list,indent = 6)
        jsonFile = open(f"{directory_name}/team{table_no}_batting.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()      


    if number==1 or number==4: #If table is second
        
        #Select all rows from 1st table
        rows=table.find_all('div',class_='cb-col cb-col-100 cb-scrd-itms') 
        bowlers_list=[]
        for idx, row in enumerate(rows):
            bowlingTable(row,bowlers_list) # Pass all rows as arguement one by one'
        
        table_no=""
        if number==1:
            table_no=1
        elif number==4:
            table_no=2

        jsonString = json.dumps(bowlers_list,indent = 6)
        jsonFile = open(f"{directory_name}/team{table_no}_bowling.json", "w")
        jsonFile.write(jsonString)
        jsonFile.close()       
    
    
    
    
    
    
    
    
    
    
    
    
    
   

  