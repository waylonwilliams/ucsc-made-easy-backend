from info import *

def prereq_check(schedule, ap_courses):
    satisfied_courses = set()
    satisfied_ges = set()
    quarter_satisfied = []
    ret = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [0 for i in range(len(major_info) + 6)], [0 for _ in range(len(ge_requirements))], 0]
    # credits = ret[18]

    for course in ap_courses:
        ret[18] += ap_prereq_info[course][2]
        for credit in ap_prereq_info[course][1]:
            satisfied_courses.add(credit)
        for ge in ap_prereq_info[course][0]:
            satisfied_ges.add(ge)

    for index, quarter in enumerate(schedule):
        quarter_satisfied = [] # store current courses here so they aren't counted incorrectly
        for local_index, course in enumerate(quarter):
            ret[index].append(0) # temp satisfaction value
            if course in prereq_info: # has prereqs
                for prereq in prereq_info[course]:
                    current_prereq_satisfied = False
                    for prereq_course in prereq:
                        if prereq_course in satisfied_courses:
                            current_prereq_satisfied = True
                            break
                    if not current_prereq_satisfied:
                        ret[index][local_index] = 1
            if ret[index][local_index] != 1:
                quarter_satisfied.append(course)
                if course in course_links_ges:
                    ret[18] += course_links_ges[course]["Credits"]
                    if course_links_ges[course]["GE"] != None:
                        satisfied_ges.add(course_links_ges[course]["GE"])
        satisfied_courses = satisfied_courses.union(set(quarter_satisfied))
    
    return ret, satisfied_courses, satisfied_ges

def major_check(ret, satisfied_courses):
    # major satisfaction is ret[16]
    for index, requirement in enumerate(major_info):
        for course in major_info[index]:
            if course in satisfied_courses:
                ret[16][index] = 1
                break
    elective_index = 18
    for course in list(satisfied_courses):
        if course in cse_electives:
            if elective_index <= 21:
                ret[16][elective_index] = 1
                elective_index += 1
            if course in cse_dc:
                ret[16][22] = 1
            if course in cse_capstone:
                ret[16][23] = 1
    return ret
            
def ge_check(ret, ge_satisfaction):
    # ret[17] is ges
    for index, req in enumerate(ge_requirements):
        if req in ge_satisfaction:
            ret[17][index] = 1
    return ret
