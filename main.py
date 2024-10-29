from bs4 import BeautifulSoup
import requests
import time

n = int(input("How many unfamiliar skills do you want to input? "))
unfamiliar_skills = []

for i in range(n):
    s = input(f"Enter unfamiliar skills {i+1}: ")
    unfamiliar_skills.append(s)

print(f"Filtering out {unfamiliar_skills}")


def find_jobs():
    html_text = requests.get(
        "https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=&searchTextText=&txtKeywords=python&txtLocation="
    ).text
    soup = BeautifulSoup(html_text, "lxml")
    jobs = soup.find_all("li", class_="clearfix job-bx wht-shd-bx")
    for index, job in enumerate(jobs):
        published_date = job.find("span", class_="sim-posted").span.text
        if "few" in published_date or "1 day ago" in published_date:
            company_name = job.find("h3", class_="joblist-comp-name").text.strip()
            skills_section = job.find("div", class_="more-skills-sections")
            skills = [span.text.strip() for span in skills_section.find_all("span")]
            formatted_skills = ", ".join(skills)

            more_info = job.header.a["href"]
            if not any(skill in skills for skill in unfamiliar_skills):
                with open(f"posts/{index}.txt", "w") as f:
                    f.write(f"Company Name: {company_name.strip()}\n")
                    f.write(f"Required Skills: {formatted_skills.strip()}\n")
                    f.write(f"More Info: {more_info}")
                print(f"File saved: {index}")


if __name__ == "__main__":
    while True:
        find_jobs()
        time_wait = 10
        print(f"Waiting {time_wait} minutes...")
        time.sleep(time_wait * 60)
