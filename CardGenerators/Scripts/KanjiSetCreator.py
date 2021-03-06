import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



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



class Vocab :


    def __init__(self, symbol, meaning, reading_one, reading_two) :
        self.symbol = symbol
        self.meaning = meaning
        self.reading_one = reading_one
        self.reading_two = reading_two


    def DuplCheck(self, vocab) :
        if vocab.reading_one == vocab.reading_two :
            vocab.reading_two = ''



class WaniKani : 

    
    Info_Collection = []
    Section = ['kanji', 'vocabulary']
    Realms = ['pleasant', 'painful', 'death', 'hell', 'paradise', 'reality' ]
    
    

    #Starting Webdriver and going to WaniKani / Section and Level
    @classmethod
    def ENoTabi_WaniKani(self, section, realm, level) :
        global driver
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(executable_path='/Users/frederick/Documents/Repositories/VocabCreatorStudy/CardGenerators/chromedriver', chrome_options=options) 
        #initializing driver and driver options so it can run without opening chrome window 

        driver.get(f"https://www.wanikani.com/{section}?difficulty={realm}")
        driver.find_element_by_css_selector(f'#level-{level} a[href]').click()
        #Going to Wanikani.com section and clicking on first element under level


    # Grabbing Kanji/Vocab Information and returning it 
    def Tsukamu(self, section) : 
        symbol =  driver.find_element_by_css_selector(f'.{section}-icon').text

        meaning = driver.find_element_by_css_selector('header > h1').text
        meaning = meaning[:0] + meaning[3 + len(symbol):]
        #Did this to rid of extra text that also comes from h1 element holding meaning text

        if section == 'kanji' : 
            readings = driver.find_elements_by_css_selector('.span4 > p')
            kanji = Kanji(symbol, meaning.lstrip(), readings[0].text, readings[1].text, readings[2].text)
            return kanji 
        else :
            readings = driver.find_elements_by_css_selector('.pronunciation-variant')
            vocab = Vocab(symbol, meaning.lstrip(), readings[0].text, readings[-1].text)
            return vocab


    # Going to next Kanji/Vocab in level
    def Tsugi(self) :
        # Has to wait for element to be clickable - method will fail for vocab if you don't
        nextButton = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".next a")))
        nextButton.click()
        


    # Grabbing all Kanji/Vocab in the level
    def Atsumeru(self, section, realm, level) :
        self.ENoTabi_WaniKani(section, realm, level)
        while True :
            try:
                Site.Info_Collection.append(Site.Tsukamu(section))
                print(self.Info_Collection[-1].symbol, self.Info_Collection[-1].meaning)
                Site.Tsugi()
            except:
                print('No More Info In Current Level') 
                driver.quit()
                break


    # Creating document in certain format for Quizlet
    def Create_Cards(self, section, realm, level, info_Collection) :
        # For Quizlet Cards
        #cards = open(os.getcwd() + '/Quizlet_Cards/' + f"{section}_{realm}_{level}.rtf", "w+")
        cards = open('/Users/frederick/Documents/Repositories/VocabCreatorStudy/Databases/ExcelSheets/' + "WaniKani_Kanji.txt", "a")
        if section == 'kanji' : 
            for kanji in info_Collection : 
                kanji.NoneCheck(kanji)
                cards.write(
                    f"{kanji.symbol}\t{kanji.meaning}\n")

        cards.close() 
    


        








#Script Run 
Site = WaniKani()

section = Site.Section[0]
realm = Site.Realms[5]
level = 0


#Choose options here 
for i in range(51,60) :
    Site.Atsumeru(section, realm, i)
    Site.Create_Cards(section, realm, i, Site.Info_Collection)
    Site.Info_Collection.clear()



# -------------Key------------- #

# Sections 
    # 0 : kanji
    # 1 : vocabulary

# Levels Relative to Realms
    # 0 : pleasant : 1 - 10
    # 1 : painful : 11 - 20
    # 2 : death : 21 - 30 
    # 3 : hell : 31 - 40
    # 4 : paradise : 41 - 50 
    # 5 : reality : 51 - 60 

#------Regex to get rid of empty lines : ^\W+?\(.+\)\s+\n------#
