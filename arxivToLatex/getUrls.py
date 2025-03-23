import requests
from bs4 import BeautifulSoup
import time

def get_arxiv_paper_urls(base_url, query, max_results=100):
    paper_links = set()  # Use a set to avoid duplicate URLs
    start = 0  # Start parameter for pagination
    
    while len(paper_links) < max_results:
        # Construct the search URL with pagination
        search_url = f"{base_url}/search/?query={query}&searchtype=all&source=header&start={start}&max_results=50"
        print(f"Fetching results from: {search_url}")
        
        # Send a GET request to the arXiv search page
        response = requests.get(search_url)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve data: {response.status_code}")
            break
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all the paper links on the current page
        for link in soup.find_all('a', href=True):
            href = link['href']
            if '/abs/' in href:
                full_url = f"https://arxiv.org{href}"
                paper_links.add(full_url)
                print(f"Found paper: {full_url}")
        
        # Check if there is a "Next" button for pagination
        next_button = soup.find('a', class_='pagination-next')
        if not next_button:
            print("No more pages found.")
            break
        
        # Move to the next page
        start += 50  # arXiv shows 50 results per page
        
        # Add a small delay to avoid overwhelming the server
        time.sleep(1)
    
    # Convert the set to a list and limit to max_results
    paper_links = list(paper_links)[:max_results]
    
    return paper_links

if __name__ == "__main__":
    # Base URL for arXiv
    base_url = "https://arxiv.org"
    
    # Search query (you can modify this to search for specific topics)
    query = "machine+learning"
    
    # Maximum number of results to fetch
    max_results = 200  # Change this to the desired number of papers
    
    # Get the paper URLs
    paper_urls = get_arxiv_paper_urls(base_url, query, max_results)
    
    # Print the extracted URLs
    for url in paper_urls:
        print(url)
    
    # Optionally, save the URLs to a file
    with open("arxiv_paper_urls.txt", "w") as file:
        for url in paper_urls:
            file.write(url + "\n")
    
    print(f"Extracted {len(paper_urls)} paper URLs.")
