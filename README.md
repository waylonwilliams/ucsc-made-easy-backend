[Link to the front end repo](https://github.com/nhi1e/ucsc-made-easy-frontend)


https://github.com/waylonwilliams/ucsc-made-easy-backend/assets/145303505/8d3b7c52-2688-4d69-af73-1961a857f5dd


## Motivation
UCSC's provided course planning tools are unhelpful and leave many students without the knowledge needed for successful course planning. This app brings all necessary information into one place to make the process of course planning fast and intuitive for students unfamiliar with their requirements. 

## Features
- Accurate course info for all 4000+ courses (ge fulfillment, credits, prerequisites, link, etc)
- Other credits accounted for such as AP exams, test outs, etc
- Major requirements for all majors across different catalog years
- Real-time requirement and prerequisite satisfaction check
- Downloading your plan as a pdf
- Store user plans in database to be reloaded upon return


## How to run
Clone both the front-end and back-end repos
```
git clone https://github.com/waylonwilliams/ucsc-made-easy-backend.git
git clone https://github.com/nhi1e/ucsc-made-easy-frontend.git
```
Navigate to the front-end repo in one terminal and run
```
npm i
npm run dev
```
In a new terminal, navigate to the back-end repo and run
```
flask run
```

## What's next for UCSC Made Easy
Refining the application to be good enough for serious use. More web scraping and ensuring that data is accurate, polishing the UI to be as smooth as possible, and hopefully getting in touch with the school to share this platform and help students.
