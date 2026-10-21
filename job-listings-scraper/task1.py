import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://realpython.github.io/fake-jobs/"
response = requests.get(url)
print("Status Code:", response.status_code) # Should print 200

soup = BeautifulSoup(response.text, "html.parser")
job_cards = soup.find_all("div", class_="card-content")
print(f"Total jobs found: {len(job_cards)}") # Should print 100

jobs_data = []

for card in job_cards:
    title_el = card.find("h2", class_="title")
    company_el = card.find("h3", class_="subtitle")
    location_el = card.find("p", class_="location")
    
    # Find all <a> links in the footer; the "Apply" link has the job detail URL
    links = card.find_all("a", class_="card-footer-item")
    apply_url = links[1]["href"] if len(links) > 1 else None

    jobs_data.append({
        "job_title": title_el.text.strip() if title_el else "N/A",
        "company_name": company_el.text.strip() if company_el else "N/A",
        "location": location_el.text.strip() if location_el else "N/A",
        "job_url": apply_url
    })

df = pd.DataFrame(jobs_data)

# Split location into City and State!
df[['city', 'state']] = df['location'].str.split(', ', expand=True)

# Save to CSV
df.to_csv("fake_python_jobs.csv", index=False)

# Preview the top 5 rows
df.head()
