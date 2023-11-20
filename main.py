import requests
from bs4 import BeautifulSoup
import csv

# Function to extract data from a single page
def extract_data_from_page(url):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Initialize lists to store data
        blog_titles = []
        blog_dates = []
        blog_image_urls = []
        blog_likes_counts = []

        # Extract information from each blog post
        blog_posts = soup.find_all('article', class_='blog-item')
        for post in blog_posts:
            # Extract blog title
            title = post.find('h6').text.strip()
            blog_titles.append(title)

            # Extract blog date
            date = post.find('div', class_='bd-item').find('span').text.strip()
            blog_dates.append(date)

            # Extract blog image URL
            image_url = post.find('a', class_='rocket-lazyload')['data-bg']
            blog_image_urls.append(image_url)

            # Extract blog likes count
            likes_count = post.find('a', class_='zilla-likes').find('span').text.strip()
            blog_likes_counts.append(likes_count)

        return blog_titles, blog_dates, blog_image_urls, blog_likes_counts
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return [], [], [], []

# Send a GET request to the initial page
url = "https://rategain.com/blog"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the total number of pages
    last_page = int(soup.find('span', class_='page-numbers dots').find_previous('a').text)

    # Initialize lists to store data
    all_blog_titles = []
    all_blog_dates = []
    all_blog_image_urls = []
    all_blog_likes_counts = []

    # Iterate through all pages
    for page_number in range(1, last_page + 1):
        page_url = f"https://rategain.com/blog/page/{page_number}/"
        titles, dates, image_urls, likes_counts = extract_data_from_page(page_url)

        # Append data from the current page to the lists
        all_blog_titles.extend(titles)
        all_blog_dates.extend(dates)
        all_blog_image_urls.extend(image_urls)
        all_blog_likes_counts.extend(likes_counts)

    # Save the data to a CSV file
    with open('blog_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Blog Title', 'Blog Date', 'Blog Image URL', 'Likes Count'])

        for title, date, image_url, likes_count in zip(all_blog_titles, all_blog_dates, all_blog_image_urls, all_blog_likes_counts):
            writer.writerow([title, date, image_url, likes_count])

    print("Scraping and data extraction successful. Data saved to 'blog_data.csv'.")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")

