from jinja2 import Environment, FileSystemLoader
import os
from .config import (
    LMS_URL,
    STUDIO_URL,
    INSTANCE_NAME
)
from .classes import (
    Course,
    Block
)

def populate_block_heirarchy(block, course: Course):
    for child in block.obj.get_children():
        parent = None
        if block != course:
            parent = block
        block = Block(child, parent)
        course.add_block(block)
        populate_block_heirarchy(block, course)

def generate_html_report(courses):
    print("Generating Report")
    instance_data = {
        "instance_name": INSTANCE_NAME,
        "lms_url": LMS_URL,
        "cms_url": STUDIO_URL
    }
    outputfile = f"/tmp/report.html"

    report_content = Environment( 
              loader=FileSystemLoader(os.path.dirname(__file__))
              ).get_template('template.html').render(instance_data=instance_data, courses=courses)

    with open(outputfile, 'w') as f:
        f.write(report_content)

    print(f"Report generated at location {outputfile}")
