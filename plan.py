from flask import Blueprint, request, jsonify, session, make_response
from info import *
from functions import prereq_check, major_check, ge_check
import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="", # NHI UPDATE YOUR PASSWORD
  database = "4y"
)
mycursor = mydb.cursor(buffered=True)
plan = Blueprint(__name__, "plan")

@plan.route("/add", methods = ["POST", "OPTIONS"])
def add():
    # handle OPTIONS cleanly
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
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
    print(ret)
    return jsonify(ret) # could also include info to be displayed for newly added course

@plan.route("/remove", methods = ["POST", "OPTIONS"])
def remove():
    # handle OPTIONS cleanly
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
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
    print(ret)
    return jsonify(ret) # could also include info to be displayed for newly added course

@plan.route("/prereqadd", methods = ["POST", "OPTIONS"])
def prereqadd():
    # handle OPTIONS cleanly
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
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
    print(ret)
    return jsonify(ret) # could also include info to be displayed for newly added course

@plan.route("/prereqremove", methods = ["POST", "OPTIONS"])
def prereqremove():
    # handle OPTIONS cleanly
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add('Access-Control-Allow-Methods', 'POST')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
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
    print(ret)
    return jsonify(ret) # could also include info to be displayed for newly added course

@plan.after_request
def middleware(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response
