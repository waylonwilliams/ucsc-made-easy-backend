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
    # check for client id
    data = request.get_json()
    client_id = data["client_id"]
    mycursor.execute("""
        SELECT client_id, position, course
        FROM planner
        WHERE client_id = %s
        ORDER BY position""", (client_id,))
    temp_courses = mycursor.fetchall()
    # if it wasn't in db, add it
    if temp_courses == []:   
        mycursor.executemany("INSERT INTO planner (client_id, position, course) values (%s, %s, %s)", [(client_id, i, None) for i in range(48)])
        mydb.commit()
        mycursor.nextset()
        return jsonify({"prev_vals": [], "prereq": [], "prev_aps": []}) # empty list will init the values to nothing
    # if it was already in db, do nothing
    else:
        # init
        setup = []
        setup_aps = []
        ap_courses = []
        courses = [{1: None, 2: None, 3: None} for i in range(16)]
        # get courses on screen and info for prereq check functions
        for i in temp_courses:
            if i[1] == -1: # skip ap classes, not sure what to do with these
                ap_courses.append(i[2]) # this will at least get the values right, not the loading select tho
                setup_aps.append({"title": i[2]})
                continue
            if i[2] != None:
                setup.append({"value": int(course_links_ges[i[2]]["value"]), "label": i[2]})
            else:
                setup.append(None)
            courses[i[1] // 3][i[1] % 3 + 1] = i[2]
        # prereq check functions so colors are also updated on start
        unsatisfied, satisfied, ap_ges, credits = prereq_check(courses, ap_courses)
        major_satisfaction = major_check(satisfied)
        ge_satisfaction = ge_check(ap_ges)
        temp_return = [0 for i in range(48)]
        for i in unsatisfied:
            temp_return[unsatisfied[i][0]] = 1
        temp_return += major_satisfaction + ge_satisfaction
        temp_return.append(credits)
        return jsonify({"prev_vals": setup, "prereq": temp_return, "prev_aps": setup_aps}) # jsonify will format it for me    

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
    print(ret)
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
    print(ret)
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
    print(ret)
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
    print(ret)
    return jsonify(ret) # could also include info to be displayed for newly added course

@plan.route("getinfo", methods = ["POST", "OPTIONS"])
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
    client_id = data["client_id"]
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
    print(ret)
    return jsonify(ret) # could also include info to be displayed for newly added course

@plan.after_request
def middleware(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response
