import json
import requests
from bs4 import BeautifulSoup

class KattisPages:
    def __init__(self):
        self.data = {}
        self.problems = []

    def getProblem(self, ID):
        return self.data[ID]

    def getProblems(self):
        return self.data
        
    def getIDs(self):
        return self.problems
        
    def load(self, file_name): #not workiing as intended
        with open(file_name) as f: 
            data = json.loads(f.read())
    
    def save(self, file_name): #not working as intended
        print('saving as', file_name)
        try: 
            f = open(file_name, 'wt') 
            f.write(str(self.data)) 
            f.close() 
        except: 
            print("Unable to write to file")
        
    def addPages(self, args):
        for i in args:
            self.addPage(i)
    
    def addPage(self, p):
        print("adding page",p)
        page = requests.get('https://open.kattis.com/problems?page=' + str(p))
        soup = BeautifulSoup(page.content, 'html.parser')
        
        names = soup.find_all("td", class_="name_column")
        self.problems = [str(name.find('a')['href']).split('/')[2] for name in names]
        
        numbers = soup.find_all("td", class_="nowrap numeric")
        for i in range(len(numbers)//8):
            VARS = ['SUBM TOTAL', 'SUBM ACC.', \
                    'SUBM RATIO', 'SUBM FASTEST', \
                    'USR TOTAL', 'USR ACC.', \
                    'USR RATIO', 'DIFFICULTY']
            self.data[self.problems[i]] = \
                {var[1] : numbers[8*i + var[0]].text for var in enumerate(VARS)}

        print("added page",p)
    


kp = KattisPages()
kp.addPages(range(31))
kp.save('kattis_archive.txt')
print(kp.getIDs())


#print(kp.getProblems(), sep='\n')
#print(len(kp.getProblems()))
