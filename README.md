***Ecommerce Product Media Scraper***

This project automates the process of extracting and downloading product media (images and videos) from an e-commerce product page using an article number provided in an Excel file.


**📌 Overview**

The workflow performs the following steps:

1. Read the article number from an Excel file.

2. Create a folder named after the article number.

3. Generate and open the product URL using the article number.

4. Extract image and video sources.

5. Download videos using `pytube`.
   
6. Download images using `urlretrieve`.

7. Save all media into the corresponding folder.



**⚙️ Tech Stack**

- Python 3

- pandas (read Excel file)

- Playwright (browser automation & scraping)

- urllib.request (download images)

- pytube (download videos)


**📂 Project Structure**
```
media-scraper/
├── zalora_product_dataset.xlsx
├── scrape_product_media.py
└── README.md
```