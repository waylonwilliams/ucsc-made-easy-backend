import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re

url = "https://iq2prod1.smartcatalogiq.com/Catalogs/University-of-California-Santa-Cruz/current/General-Catalog/Courses"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
web_byte = urlopen(req).read()
webpage = web_byte.decode("utf-8")
soup = BeautifulSoup(webpage, "html.parser")
links = []

if soup:
    l = soup.find("ul", class_="sc-child-item-links")
    for elem in l.find_all("li"):
        link = elem.find("a")
        if link:
            links.append(link["href"])

class_links = {}
graduate_pattern = r'\b[A-Z]{2,4}\s2[0-9]{2}[A-Z]?\b'
url = "https://iq2prod1.smartcatalogiq.com{}"
print("Got links")
print(links)

for i in links:
    try:
        req = Request(url.format(i), headers={'User-Agent': 'Mozilla/5.0'})
        web_byte = urlopen(req).read()
        webpage = web_byte.decode("utf-8")
        soup = BeautifulSoup(webpage, "html.parser")
        if soup:
            courses = soup.find_all('h2', class_='course-name')
            for course in courses:
                course_name = course.find("span").text
                if re.match(graduate_pattern, course_name):
                    continue
                course_link = course.find("a")["href"]
                if course_name not in class_links:
                    print(course_name)
                    class_links[course_name] = course_link
    except:
        pass

print("Course names scraped, now course info\n\n\n")

with open("courses.py", "w") as fh:
    fh.write("course_links_ges = {\n")
    counter = 0
    for course in class_links:
        link = class_links[course]
        req = Request(url.format(link), headers={'User-Agent': 'Mozilla/5.0'})
        web_byte = urlopen(req).read()
        webpage = web_byte.decode("utf-8")
        soup = BeautifulSoup(webpage, "html.parser")
        if soup:
            gen_ed_text = None
            credits = 0
            title = ""

            # title
            tt = soup.find("h1")
            if tt:
                title = tt.get_text().strip()

            # gen ed
            gen_ed = soup.find("div", class_="genEd")
            if gen_ed:
                gen_ed_tag = gen_ed.find('p')
                if gen_ed_tag:
                    gen_ed_text = gen_ed_tag.get_text()
                    cleaned_gen_ed_text = gen_ed_text.strip()
                else:
                    cleaned_gen_ed_text = None
            else:
                cleaned_gen_ed_text = None
            
            # credits 
            cred = soup.find_all("div", class_="extraFields")
            for c in cred:
                meow = c.find("h4")
                if meow:
                    if "Credits" in meow.get_text().strip():
                        cmeow = c.find("p")
                        if cmeow:
                            credits = int(cmeow.get_text().strip())

            print(course, title, gen_ed, cred)

        else:
            print("error opening catalog page")
        if cleaned_gen_ed_text == None:
            print(course, "GE:", str(cleaned_gen_ed_text), "Credits:", credits, "Title:", title, "Link:", links[counter], "Value:", counter)
            fh.write("\t'" + course + "': {'GE': None, 'Credits': " + str(credits) + ", 'Title': '''" + title + "''', 'Link': '" + links[counter] + "''', 'value': '" + str(counter) + "'},\n")
        else:
            # Need to handle PE and PR gen eds, also this next write is not perfected
            print(course, "GE:", str(cleaned_gen_ed_text), "Credits:", credits, "Title:", title, "Link:", links[counter], "Value:", counter)
            fh.write("\t'" + course + "': {'GE': '" + str(cleaned_gen_ed_text) + "', 'Credits': " + str(credits) + ", 'Title': '" + title + "', 'Link': '" + links[counter] + "'},\n")
        counter += 1
    fh.write("}\n")
