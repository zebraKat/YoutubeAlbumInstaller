from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common import alert
from selenium.common.exceptions import NoAlertPresentException
from pytube import Playlist
import time
from selenium import webdriver

PlaylistURL = "https://www.youtube.com/playlist?list=OLAK5uy_l2Xm9yuNUyMI33pZDmWAD88IdXWeHiKkM"

options = webdriver.FirefoxOptions()
driver = webdriver.Firefox(options=options)

driver.get("https://www.cnvmp3.com")



def is_alert_open(driver):

    try:
        driver.switch_to.alert  # Try switching to an alert
        return True
    except NoAlertPresentException:
        return False



def DownloadVideo(url):
    time.sleep(5)
    WebDriverWait(driver,10).until(
    EC.presence_of_element_located((By.ID,"video-url"))
    )

    textbox = driver.find_element(By.ID, "video-url")
    convertButton = driver.find_element(By.ID,"convert-button-1")
    textbox.clear()

    textbox.send_keys(url + Keys.ENTER)
    convertButton.click()

    if is_alert_open(driver):
        driver.refresh();
        DownloadVideo(url)
    
    try:
        WebDriverWait(driver,50).until(
          EC.element_to_be_clickable((By.ID, "convert-again-btn"))
        ) 
    except Exception as e:
        driver.refresh()
        return DownloadVideo(url)

    time.sleep(5)

    convertAgain = driver.find_element(By.ID, "convert-again-btn")

    convertAgain.click()

def get_youtube_playlist_links(playlist_url):
   # """Fetches all video links from a YouTube playlist."""
    try:
        playlist = Playlist(playlist_url)
        return [video_url for video_url in playlist.video_urls]
    except Exception as e:
        print(f"Error: {e}")
        return []

def DownloadPlaylist(playlistURL):
    videos = get_youtube_playlist_links(playlistURL)
    for link in videos:
        DownloadVideo(link)
    time.sleep(25)
    driver.quit()



DownloadPlaylist(PlaylistURL)
#DownloadVideo(videoURL)
