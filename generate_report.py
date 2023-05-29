from datetime import datetime
from django.db.models import Q
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
import pytz
from xmodule.modulestore.django import modulestore
from helpers.classes import Course
from helpers.helper import (
    populate_block_hierarchy,
    generate_html_report
)

def generate_report():
    active_courses = []
    store = modulestore()

    print("Fetching list of all courses")
    course_overviews = CourseOverview.get_all_courses()
    # This can be replaced with `CourseOverview.get_all_courses(active_only=True)` in Palm.
    active_course_overviews = course_overviews.filter(
        Q(end__isnull=True) | Q(end__gte=datetime.now().replace(tzinfo=pytz.UTC))
    )
    for course_number, course_overview in enumerate(active_course_overviews, start=1):
        course_obj = store.get_course(course_overview.id)
        course = Course(course_obj)
        
        print(f"Course {course_number}/{len(active_course_overviews)} : Fetching all blocks for course {course}")
        populate_block_hierarchy(course, course)

        # Find and list internal cross section links
        course.find_links_in_blocks()
        
        active_courses.append(course)

    generate_html_report(active_courses)
