from helpers import login
from helpers.helper import (
    fetch_all_active_courses,
    fetch_all_course_blocks,
    fetch_block_data,
    generate_report
)

# Login the user and fetch the session cookies
cookie_jar = login.login_to_lms()

active_courses = fetch_all_active_courses(cookie_jar)

course_count = 1
for course in active_courses:
    print(f"Course {course_count}/{len(active_courses)} : Fetching all blocks of course {course}")
    fetch_all_course_blocks(course, cookie_jar)

    # Figure out the ancenstors for each block
    course.map_block_hierarchy()

    # Fetch xblock data
    print(f"Course {course_count}/{len(active_courses)} : Fetching xblock data for course {course.id}")
    fetch_block_data(cookie_jar, course)

    # Find and list internal cross section links
    course.find_links_in_blocks()

    course_count += 1

generate_report(active_courses)
