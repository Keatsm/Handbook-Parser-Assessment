"""
Inside conditions.json, you will see a subset of UNSW courses mapped to their 
corresponding text conditions. We have slightly modified the text conditions
to make them simpler compared to their original versions.

Your task is to complete the is_unlocked function which helps students determine 
if their course can be taken or not. 

We will run our hidden tests on your submission and look at your success rate.
We will only test for courses inside conditions.json. We will also look over the 
code by eye.

NOTE: We do not expect you to come up with a perfect solution. We are more interested
in how you would approach a problem like this.
"""
import json

# NOTE: DO NOT EDIT conditions.json
with open("./conditions.json") as f:
    CONDITIONS = json.load(f)
    f.close()


PREFIXES = ['COMP', 'MATH', 'DPST', 'MTRN', 'ELEC']
COURSE_UNITS = 6
COURSE_CODE_SIZE = 8


def check_statement(courses_list, prereq):
    
    meets_prereq = True
    skip = False
    
    for index, character in enumerate(prereq):
        
        if character == ')' and skip:
            skip = False
            continue
            
        if skip:
            continue
        
        if character == '(':
            meets_prereq = check_statement(courses_list, prereq[slice(index + 1, len(prereq))])
            skip = True
            
        if any(prereq[slice(index, len(prereq))].startswith(prefix) for prefix in PREFIXES):
            if prereq[slice(index, index + COURSE_CODE_SIZE)] not in courses_list:
                meets_prereq = False
                
        if prereq[slice(index, len(prereq))].lower().startswith('and') and not meets_prereq:
            return False
        
        if prereq[slice(index, len(prereq))].lower().startswith('or') and meets_prereq:
            return True
        
        if prereq[slice(index, len(prereq))].lower().startswith('units of credit in') or prereq[slice(index, len(prereq))].lower().startswith('units oc credit in'):
            i = index - 2
            
            while i > 0 and prereq[i] != ' ' and prereq[i] != '(':
                i -= 1
                
            UOC = int(prereq[slice(i, index - 1)])
            
            continue
            
        if prereq[slice(index, len(prereq))].lower().startswith('units of credit'):
            i = index - 2
            
            while i > 0 and prereq[i] != ' ' and prereq[i] != '(':
                i -= 1
                
            UOC = int(prereq[slice(i, index - 1)])
            
            if len(courses_list) * COURSE_UNITS < UOC:
                meets_prereq = False
            
            
        
        
    
    return meets_prereq

def is_unlocked(courses_list, target_course):
    """
    
    Given a list of course codes a student has taken, return true if the target_course 
    can be unlocked by them.
    
    You do not have to do any error checking on the inputs and can assume that
    the target_course always exists inside conditions.json
    
    ASSUMPTION: course_list is a list (array) of course codes
    
    
    """
    
    prequisites = CONDITIONS[target_course]
    
    if len(prequisites) == 0:
        return True
    
    return check_statement(courses_list, prequisites)
    
    





    