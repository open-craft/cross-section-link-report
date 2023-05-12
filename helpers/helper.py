from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import os
import requests
from .config import (
    LMS_URL,
    STUDIO_URL,
    INSTANCE_NAME,
    REPORT_PATH
)
from .classes import (
    Course,
    Block
)

FETCH_ALL_COURSES_URL = f"{LMS_URL}/api/courses/v1/courses/"

def fetch_all_course_blocks(course: Course, cookie_jar):
    '''
    Fetch list of all course blocks in a course. Include the children blocks if present.
    '''
    fetch_blocks_url = f"{course.blocks_url}&all_blocks=true&depth=all&requested_fields=children"

    print(f"Fetching all blocks of course {course}")
    r = requests.get(fetch_blocks_url, cookies=cookie_jar)
    
    blocks = r.json().get('blocks')

    for key in blocks:
        block = Block(blocks.get(key))
        course.add_block(block)

def fetch_all_active_courses(cookie_jar):
    '''
    Fetch list of all courses.
    Discards courses whose end date is defined and is in the past.
    Returns the other courses as active courses.
    '''
    active_courses = []

    print("Fetching list of all courses")
    r = requests.get(FETCH_ALL_COURSES_URL, cookies=cookie_jar)
    
    courses = r.json().get('results')
    today = datetime.now()
    for course in courses:
        course_active = False
        end_date_str = course.get('end', None)
        if end_date_str:
            end_date_str = end_date_str.split('T')[0]
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
            if end_date >= today:
                course_active = True
        else:
            course_active = True
        
        if course_active:
            course = Course(course)
            course.url = f"{STUDIO_URL}/course/{course.id}"
            active_courses.append(course)

    return active_courses

def fetch_block_data(cookie_jar, course: Course):
    block_count = 1
    for usage_key in course.blocks:
        block = course.blocks[usage_key]
        block_data_url = f"{STUDIO_URL}/xblock/{block.usage_key}"
        headers = {"Accept": "application/json, text/plain, */*"}

        print(f"Fetching xblock data for course {course.id} : {block_count}/{len(course.blocks)}")
        r = requests.get(block_data_url, cookies=cookie_jar, headers=headers)
        
        try:
            block_studio_url = r.json().get('studio_url', None)
            if block_studio_url:
                block.studio_url = f"{STUDIO_URL}{block_studio_url}"
        except:
            block.data = r.text
        finally:
            block.data = r.text

        block_count += 1

def generate_report(courses):
    print("Generating Report")
    instance_data = {
        "instance_name": INSTANCE_NAME,
        "lms_url": LMS_URL,
        "cms_url": STUDIO_URL
    }
    outputfile = f"{REPORT_PATH}/report.html"

    report_content = Environment( 
              loader=FileSystemLoader(os.path.dirname(__file__))
              ).get_template('template.html').render(instance_data=instance_data, courses=courses)

    with open(outputfile, 'w') as f:
        f.write(report_content)

    print(f"Report generated at location {outputfile}")
