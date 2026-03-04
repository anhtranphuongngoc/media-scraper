import requests
import urllib.request
import pandas as pd
from bs4 import BeautifulSoup
from pytubefix import YouTube
import os
from playwright.sync_api import sync_playwright


def fetch_artical_numbers(dataset):
	# Fetch all article numbers
	df = pd.read_excel(dataset)
	
	artical_numbers = df['Article Number']
	return artical_numbers


def create_subfolder(folder_name):
	if not os.path.exists(folder_name):
		os.mkdir(folder_name)
		print(f"Folder '{folder_name}' created.")
	else:
		print(f"Folder '{folder_name}' already exists.")	


def download_media_item():
	artical_numbers = fetch_artical_numbers('zalora_product_dataset.xlsx')

	with sync_playwright() as p:
		browser = p.chromium.launch(headless=False)
		context = browser.new_context(
			user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 SHOPQAAutomation/"
		)

		page = context.new_page()

		for number in artical_numbers:
			file_path = f"./{number}"

			create_subfolder(number)

			# Open the product page using SKU
			page.goto(f"https://www.zalora.com.my/p/{number}")

			# Get product media element
			images = page.locator("[data-test-id='mediaItem'] img")

			for i in range(images.count()):
				# The media locator
				img = images.nth(i)
				src = img.get_attribute("src")
				
				# If the media has 'svg' element, which is the play button
				# then it indicates that the media is a video
				if img.evaluate("""
					(node) => {
						return node.previousElementSibling?.tagName.toLowerCase() === 'svg';
					}
					"""):
					# Click on that media to open to video and get the video id
					img.click()

					# Extract the video id
					video_id = page.locator("iframe[id^='video']").first.get_attribute("id").split("video_")[1]
					print("The video id is:", video_id)

					download_youtube_video_by_id(video_id, file_path)
					continue
				urllib.request.urlretrieve(src, f"{file_path}/new_image_{i}.jpg") # Save the image
				print(f"Image {i} is saved")

			print(f"Media saved at: {file_path}\n")

		browser.close()


def download_youtube_video_by_id(video_id, output_path):
    """
    Downloads a YouTube video to a specified output path using its video ID.
    """
    try:
        # Construct the full URL from the video ID
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        
        # Create a YouTube object
        yt = YouTube(video_url)

        # Filter for the highest resolution progressive stream
        video_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        
        if not video_stream:
            print("Could not find a suitable progressive stream")
            return
        
        # Download the video
        video_stream.download(output_path)
        
        print("Download completed successfully!")
        
    except Exception as e:
        print(f"An error occurred: {e}")				


if __name__=="__main__":
    download_media_item()