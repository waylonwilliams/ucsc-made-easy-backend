from flask import Blueprint, request, jsonify, session, make_response
from info import *
from functions import prereq_check, major_check, ge_check
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="hahahddd%55^jjd9", # NHI UPDATE YOUR PASSWORD
  database = "4y"
)
mycursor = mydb.cursor(buffered=True)
plan = Blueprint(__name__, "plan")

@plan.route("/", methods = ["POST", "OPTIONS"])
def setup():
    # cleanly handle OPTIONS request
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
    
    # when I change raw strings into good json, use values > 50
    # they just need to not conflict with front end list, and backend only cares about label

    # check for client id
    # front only fetches when client id is present
    data = request.get_json()
    client_id = data["client_id"]
    mycursor.execute("""
        SELECT position, course
        FROM planner
        WHERE client_id = %s
        ORDER BY position""", (client_id,))
    temp_courses = mycursor.fetchall()
    # if it wasn't in db, add it
    ap_courses = []
    courses = [[] for i in range(16)]
    for course in temp_courses:
        if course[0] == -1: # should be position value
            ap_courses.append(course[1]) # update to {"value": arbitrary_value, "label": course[1]} later
        else:
            courses[course[0]].append(course[1])
    
    # basic prereq checks
    ret, satisfied_courses, satisfied_ge = prereq_check(courses, ap_courses)
    ret = major_check(ret, satisfied_courses)
    ret = ge_check(ret, satisfied_ge)
    ret.append(["Course info here", "Info here", ""])

    ap_courses_formatted = []
    arbitrary_value = 100
    for i in ap_courses:
        ap_courses_formatted.append({"value": arbitrary_value, "label": i})
        arbitrary_value += 1

    return jsonify({"schedule": courses, "ap_courses": ap_courses_formatted, "prereq": ret})
    # return list of courses, list of ap courses, and usual prereq data

@plan.route("/add", methods = ["POST", "OPTIONS"])
def add():
    # handle OPTIONS cleanly
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.status_code = 200
        return response
    # access db using client id
    data = request.get_json()
    client_id = data["client_id"]
    slot = data["slot"]
    course = data["course"]
    ap_courses = data["ap_courses"]
    schedule = data["schedule"]
    mycursor.execute("""INSERT INTO planner (client_id, position, course)
                     VALUES (%s, %s, %s)""", (client_id, slot, course,))
    mydb.commit()
    
    # ap_courses is an array of the satisfactions
    # schedule is a nested list of courses in each quarter
    ret, satisfied_courses, satisfied_ge = prereq_check(schedule, ap_courses)
    ret = major_check(ret, satisfied_courses)
    ret = ge_check(ret, satisfied_ge)
    ret.append([])
    ret[19].append(course_links_ges[course]["Title"])
    if course in prereq_info:
        prereq_string = "[ "
        for index, req_block in enumerate(prereq_info[course]): # right order?
            prereq_string += prereq_info[course][index][0]
            for local_index, course_req in enumerate(req_block):
                if local_index == 0:
                    continue
                prereq_string += " or "
                prereq_string += prereq_info[course][index][local_index]
            if index < len(prereq_info[course]) - 1:
                prereq_string += " ]  and  [ "
        prereq_string += " ]"
        ret[19].append(prereq_string)
    else:
        ret[19].append("None")
    ret[19].append(course_links_ges[course]["Link"])
    return jsonify(ret) # could also include info to be displayed for newly added course

@plan.route("/remove", methods = ["POST", "OPTIONS"])
def remove():
    # handle OPTIONS cleanly
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.status_code = 200
        return response
    # access db using client id
    data = request.get_json()
    client_id = data["client_id"]
    slot = data["slot"]
    course = data["course"]
    ap_courses = data["ap_courses"]
    schedule = data["schedule"]
    mycursor.execute("""DELETE FROM planner
                     WHERE client_id = %s AND position = %s AND course = %s""", (client_id, slot, course,))
    mydb.commit()
    
    # ap_courses is an array of the satisfactions
    # schedule is a nested list of courses in each quarter
    ret, satisfied_courses, satisfied_ge = prereq_check(schedule, ap_courses)
    ret = major_check(ret, satisfied_courses)
    ret = ge_check(ret, satisfied_ge)
    ret.append([])
    ret[19].append(course_links_ges[course]["Title"])
    if course in prereq_info:
        prereq_string = "[ "
        for index, req_block in enumerate(prereq_info[course]): # right order?
            prereq_string += prereq_info[course][index][0]
            for local_index, course_req in enumerate(req_block):
                if local_index == 0:
                    continue
                prereq_string += " or "
                prereq_string += prereq_info[course][index][local_index]
            if index < len(prereq_info[course]) - 1:
                prereq_string += " ]  and  [ "
        prereq_string += " ]"
        ret[19].append(prereq_string)
    else:
        ret[19].append("None")
    ret[19].append(course_links_ges[course]["Link"])
    return jsonify(ret) # could also include info to be displayed for newly added course

@plan.route("/prereqadd", methods = ["POST", "OPTIONS"])
def prereqadd():
    # handle OPTIONS cleanly
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.status_code = 200
        return response
    # access db using client id
    data = request.get_json()
    client_id = data["client_id"]
    slot = data["slot"] # should be -1
    course = data["course"]
    ap_courses = data["ap_courses"]
    schedule = data["schedule"]
    mycursor.execute("""INSERT INTO planner (client_id, position, course)
                     VALUES (%s, %s, %s)""", (client_id, slot, course,))
    mydb.commit()
    
    # ap_courses is an array of the satisfactions
    # schedule is a nested list of courses in each quarter
    ret, satisfied_courses, satisfied_ge = prereq_check(schedule, ap_courses)
    ret = major_check(ret, satisfied_courses)
    ret = ge_check(ret, satisfied_ge)
    ret.append([course, "None", ""])
    # what to do for these
    return jsonify(ret) # could also include info to be displayed for newly added course

@plan.route("/prereqremove", methods = ["POST", "OPTIONS"])
def prereqremove():
    # handle OPTIONS cleanly
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.status_code = 200
        return response
    # access db using client id
    data = request.get_json()
    client_id = data["client_id"]
    slot = data["slot"] # should be -1
    course = data["course"]
    ap_courses = data["ap_courses"]
    schedule = data["schedule"]
    mycursor.execute("""DELETE FROM planner
                     WHERE client_id = %s AND position = %s AND course = %s""", (client_id, slot, course,))
    mydb.commit()
    
    # ap_courses is an array of the satisfactions
    # schedule is a nested list of courses in each quarter
    ret, satisfied_courses, satisfied_ge = prereq_check(schedule, ap_courses)
    ret = major_check(ret, satisfied_courses)
    ret = ge_check(ret, satisfied_ge)
    ret.append([course, "None", ""])
    return jsonify(ret) # could also include info to be displayed for newly added course

@plan.route("/getinfo", methods = ["POST", "OPTIONS"])
def getinfo():
    # handle OPTIONS cleanly
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.status_code = 200
        return response
    # access db using client id
    data = request.get_json()
    course = data["course"]
    ap_courses = data["ap_courses"]
    schedule = data["schedule"]
    # ap_courses is an array of the satisfactions
    # schedule is a nested list of courses in each quarter
    ret, satisfied_courses, satisfied_ge = prereq_check(schedule, ap_courses)
    ret = major_check(ret, satisfied_courses)
    ret = ge_check(ret, satisfied_ge)
    ret.append([])
    ret[19].append(course_links_ges[course]["Title"])
    if course in prereq_info:
        prereq_string = "[ "
        for index, req_block in enumerate(prereq_info[course]): # right order?
            prereq_string += prereq_info[course][index][0]
            for local_index, course_req in enumerate(req_block):
                if local_index == 0:
                    continue
                prereq_string += " or "
                prereq_string += prereq_info[course][index][local_index]
            if index < len(prereq_info[course]) - 1:
                prereq_string += " ]  and  [ "
        prereq_string += " ]"
        ret[19].append(prereq_string)
    else:
        ret[19].append("None")
    ret[19].append(course_links_ges[course]["Link"])
    # what to do for these
    return jsonify(ret) # could also include info to be displayed for newly added course

@plan.after_request
def middleware(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response
