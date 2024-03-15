from flask import Blueprint, request, jsonify, make_response
from info import *
from functions import prereq_check, major_check, ge_check
from planner import db, Planner
from sqlalchemy import text

bp = Blueprint(__name__, "plan")

@bp.route("/", methods = ["POST", "OPTIONS"])
def setup():
    # cleanly handle OPTIONS request
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response

    # check for client id
    # front only fetches when client id is present
    data = request.get_json()
    client_id = data["client_id"]
    rows = db.session.execute(text("""
        SELECT position, course
        FROM planner
        WHERE client_id = :client_id
        ORDER BY position"""), {"client_id": client_id})
    temp_courses = rows.fetchall()
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
    ret.append(["Course info here", [], ""])

    ap_courses_formatted = []
    arbitrary_value = 100
    for i in ap_courses:
        ap_courses_formatted.append({"value": arbitrary_value, "label": i})
        arbitrary_value += 1

    return jsonify({"schedule": courses, "ap_courses": ap_courses_formatted, "prereq": ret})
    # return list of courses, list of ap courses, and usual prereq data

@bp.route("/add", methods = ["POST", "OPTIONS"])
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
    db.session.execute(text("""INSERT INTO planner (client_id, position, course)
                    VALUES (:client_id , :slot , :course )"""), {"client_id": client_id, "slot" : slot, "course" : course})
    db.session.commit()
    
    # ap_courses is an array of the satisfactions
    # schedule is a nested list of courses in each quarter
    ret, satisfied_courses, satisfied_ge = prereq_check(schedule, ap_courses)
    ret = major_check(ret, satisfied_courses)
    ret = ge_check(ret, satisfied_ge)
    ret.append([])
    ret[19].append(course_links_ges[course]["Title"])
    if course in prereq_info:
        prereq_array = []
        i = -1
        # prereq_string = "[ "
        for index, req_block in enumerate(prereq_info[course]): # right order?
            # prereq_string += prereq_info[course][index][0]
            prereq_array.append([prereq_info[course][index][0]])
            i += 1
            for local_index, course_req in enumerate(req_block):
                if local_index == 0:
                    continue
                # prereq_string += " or "
                prereq_array[i].append(prereq_info[course][index][local_index])
                # prereq_string += prereq_info[course][index][local_index]
        #     if index < len(prereq_info[course]) - 1:
        #         prereq_string += " ]  and  [ "
        # prereq_string += " ]"
        # ret[19].append(prereq_string)
        ret[19].append(prereq_array)
        print(prereq_array)
    else:
        # ret[19].append("None")
        ret[19].append([])
    ret[19].append(course_links_ges[course]["Link"])
    return jsonify(ret) # could also include info to be displayed for newly added course

@bp.route("/remove", methods = ["POST", "OPTIONS"])
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
    db.session.execute(text("""DELETE FROM planner
                    WHERE client_id = :client_id AND position = :slot AND course = :course"""), {"client_id": client_id, "slot" : slot, "course" : course})
    db.session.commit()
    
    # ap_courses is an array of the satisfactions
    # schedule is a nested list of courses in each quarter
    ret, satisfied_courses, satisfied_ge = prereq_check(schedule, ap_courses)
    ret = major_check(ret, satisfied_courses)
    ret = ge_check(ret, satisfied_ge)
    ret.append([])
    ret[19].append(course_links_ges[course]["Title"])
    if course in prereq_info:
        prereq_array = []
        i = -1
        # prereq_string = "[ "
        for index, req_block in enumerate(prereq_info[course]): # right order?
            # prereq_string += prereq_info[course][index][0]
            prereq_array.append([prereq_info[course][index][0]])
            i += 1
            for local_index, course_req in enumerate(req_block):
                if local_index == 0:
                    continue
                # prereq_string += " or "
                prereq_array[i].append(prereq_info[course][index][local_index])
                # prereq_string += prereq_info[course][index][local_index]
        #     if index < len(prereq_info[course]) - 1:
        #         prereq_string += " ]  and  [ "
        # prereq_string += " ]"
        # ret[19].append(prereq_string)
        ret[19].append(prereq_array)
        # print(prereq_string)
        print(prereq_array)
    else:
        # ret[19].append("None")
        ret[19].append([])
    ret[19].append(course_links_ges[course]["Link"])
    return jsonify(ret) # could also include info to be displayed for newly added course

@bp.route("/prereqadd", methods = ["POST", "OPTIONS"])
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
    db.session.execute(text("""INSERT INTO planner (client_id, position, course)
                    VALUES (:client_id , :slot , :course )"""), {"client_id": client_id, "slot" : slot, "course" : course})
    db.session.commit()
    
    # ap_courses is an array of the satisfactions
    # schedule is a nested list of courses in each quarter
    ret, satisfied_courses, satisfied_ge = prereq_check(schedule, ap_courses)
    ret = major_check(ret, satisfied_courses)
    ret = ge_check(ret, satisfied_ge)
    ret.append([course, [], ""])
    # what to do for these
    return jsonify(ret) # could also include info to be displayed for newly added course

@bp.route("/prereqremove", methods = ["POST", "OPTIONS"])
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
    db.session.execute(text("""DELETE FROM planner
                    WHERE client_id = :client_id AND position = :slot AND course = :course"""), {"client_id": client_id, "slot" : slot, "course" : course})
    db.session.commit()
    
    # ap_courses is an array of the satisfactions
    # schedule is a nested list of courses in each quarter
    ret, satisfied_courses, satisfied_ge = prereq_check(schedule, ap_courses)
    ret = major_check(ret, satisfied_courses)
    ret = ge_check(ret, satisfied_ge)
    ret.append([course, [], ""])
    return jsonify(ret) # could also include info to be displayed for newly added course

@bp.route("/getinfo", methods = ["POST", "OPTIONS"])
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
        prereq_array = []
        i = -1
        # prereq_string = "[ "
        for index, req_block in enumerate(prereq_info[course]): # right order?
            # prereq_string += prereq_info[course][index][0]
            prereq_array.append([prereq_info[course][index][0]])
            i += 1
            for local_index, course_req in enumerate(req_block):
                if local_index == 0:
                    continue
                # prereq_string += " or "
                prereq_array[i].append(prereq_info[course][index][local_index])
                # prereq_string += prereq_info[course][index][local_index]
        #     if index < len(prereq_info[course]) - 1:
        #         prereq_string += " ]  and  [ "
        # prereq_string += " ]"
        # ret[19].append(prereq_string)
        ret[19].append(prereq_array)
        # print(prereq_string)
        print(prereq_array)
    else:
        # ret[19].append("None")
        ret[19].append([])
    ret[19].append(course_links_ges[course]["Link"])
    # what to do for these
    return jsonify(ret) # could also include info to be displayed for newly added course

@bp.after_request
def middleware(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response
