#------Psuedo Code----------#
    #---Selenium Side---#
        # Open Wani Kani
        # Go to desired Kanji Level  
        # Grab Kanji 
        # Grab Onyomi - Unless it's None 
        # Grab Kunyomi - Unless it's None 
        # Grab Nanori - Unless it's None 
        # Go To next Kanji 
        # repeat from step 3 - Unless it's the last kanji in Level

    #---Text Editor Side ---#
        # Receive kanji collection
        # Create New Document  
        # Print in this format : 

            #上 (Meaning)	Above
            #上 (Onyomi)		じよう
            #上（Kunyomi）	 うえ、 あ、 のぼ、 うわ、 かみ
        #
        # Save Document 
        # Don't Profit 



import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



class Kanji :


    def __init__(self, symbol, meaning, onyomi='', kunyomi='', nanori='') :
        self.symbol = symbol
        self.meaning = meaning
        self.onyomi = onyomi
        self.kunyomi = kunyomi
        self.nanori = nanori


    def NoneCheck(self, kanji) :
        if kanji.onyomi == 'None' :
            setattr(kanji, 'onyomi', '')
        if kanji.kunyomi == 'None' :
            setattr(kanji, 'kunyomi', '')
        if kanji.nanori == 'None' :
            setattr(kanji, 'nanori', '')



class WaniKani : 

    
    Kanji_Collection = []
    Section = ['kanji', 'vocabulary']
    Realms = ['pleasant', 'painful', 'death', 'hell', 'paradise', 'reality' ]
    # Levels Relative to Realms
    # 0 : pleasant : 1 - 10
    # 1 : painful : 11 - 20
    # 2 : death : 21 - 30 
    # 3 : hell : 31 - 40
    # 4 : paradise : 41 - 50 
    # 5 : reality : 51 - 60 
    

    @classmethod
    def ENoTabi_WaniKani(self, section, realm, level) :
        global driver
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(executable_path='/Users/frederick/Documents/REPOS/WaniKani_Card_Generator/WaniKani_CardSet_Creator/chromedriver', chrome_options=options) 

        driver.get(f"https://www.wanikani.com/{section}?difficulty={realm}")
        #^ Chooses between Kanji or Vocab
        driver.find_element_by_css_selector(f'#level-{level} .single-character-grid a[href]').click()
        #^ Chooses starting lesson (Need one for vocab)


    def Tsukamu_Kanji(self) : 
        symbol =  "".join(set(driver.find_element_by_css_selector('.kanji-icon').text.lstrip()))

        meaning = driver.find_element_by_css_selector('header > h1').text
        meaning = meaning[:0] + meaning[4:]

        readings = driver.find_elements_by_css_selector('.span4 > p')

        kanji = Kanji(symbol, meaning.lstrip(), readings[0].text, readings[1].text, readings[2].text)
        return kanji 


    def Tsugi_Kanji(self) :
        driver.implicitly_wait(3)
        driver.find_element_by_css_selector('.next a').click()


    def Atsumeru_Kanji(self, section, kanji_realm, kanji_level) :
        self.ENoTabi_WaniKani(section, kanji_realm, kanji_level)
        while True :
            try:
                Site.Kanji_Collection.append(Site.Tsukamu_Kanji())
                print(self.Kanji_Collection[-1].symbol, self.Kanji_Collection[-1].meaning)
                Site.Tsugi_Kanji()
            except:
                print('No More Kanji In Current Level') 
                driver.quit()
                break


    def Create_Cards(self, Kanji_Collection) :
        cards = open("test.rtf", "w+")
        for kanji in Kanji_Collection: 
            kanji.NoneCheck(kanji)
            cards.write(
                f"{kanji.symbol} (Meaning)      {kanji.meaning}\n"+
                f"{kanji.symbol} (Onyomi)       {kanji.onyomi}\n" + 
                f"{kanji.symbol} (Kunyomi)      {kanji.kunyomi}\n"+
                f"{kanji.symbol} (Nanori)       {kanji.nanori}\n"  
                )
        cards.close() 
    

#------Regex to get rid of empty lines : \W\s\(\w+\)\s+\n------#
        








#Script Run 
Site = WaniKani()
Site.Atsumeru_Kanji(Site.Section[0], Site.Realms[0], 1)
Site.Create_Cards(Site.Kanji_Collection)