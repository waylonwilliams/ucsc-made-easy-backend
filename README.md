# [UCSC Made Easy](https://ucscmadeeasy.vercel.app/)

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

Visit the app on the web [here](https://ucscmadeeasy.vercel.app/)

To run locally,

Clone both the front-end and back-end repos

```
git clone https://github.com/waylonwilliams/ucsc-made-easy-backend.git
git clone https://github.com/nhi1e/ucsc-made-easy-frontend.git
```

In one terminal, navigate to the front-end repo and run

```
npm i
npm run dev
```

In a new terminal, navigate to the back-end repo and run

```
docker build -t course-planner .
docker run -it -p 5000:8080 course-planner
```

Or, if you don't have Docker
```
pip install -r requirements.txt
flask run
```
