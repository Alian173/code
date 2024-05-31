from pytube import YouTube 
from pytube.exceptions import LiveStreamError 
import os 
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

currentUser = os.getlogin()
path = 'C:\\Users\\' + currentUser + '\\AppData\\Local\\VotV\\Assets\\tv'

query = input("SEARCH QUERY: ")
amount = int(input("VIDEO AMOUNT: "))
options = webdriver.ChromeOptions() 
options.add_argument("--headless")
options.add_argument("--mute-audio")
driver = webdriver.Chrome(options=options)
driver.get('https://www.youtube.com/results?search_query='+query)

# SELECT FILTER
rejectPath = "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[1]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]"
videoClickPath = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/h3/a/yt-formatted-string"
WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, rejectPath)))
driver.find_element(By.XPATH, rejectPath).click()    
time.sleep(1)
driver.find_element(By.XPATH, videoClickPath).click()    

#CHOOSE VIDEO
toDownloadNext = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[28]/div[2]/div[1]/a[2]"




for i in range(0, amount):
    f = open("votv_dloaded.txt", "r")
    currentUrl = driver.current_url

    if currentUrl not in f:
        yt = YouTube(currentUrl)
        try:
            video = yt.streams.filter(progressive=True, file_extension='mp4').first() 
        except LiveStreamError:
            driver.find_element(By.CLASS_NAME, "ytp-next-button").click()    
            break
        out_file = video.download(output_path=path) 

        base, ext = os.path.splitext(out_file) 
        new_file = base + '.mp4'
        os.rename(out_file, new_file) 
        print("DOWNLOADED " + str(i + 1) + "/ " + str(amount))
        f.close()
        f = open("votv_dloaded.txt", "a")
        f.write(currentUrl + ";")
        f.close()
        driver.find_element(By.CLASS_NAME, "ytp-next-button").click()  

