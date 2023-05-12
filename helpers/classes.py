import re
from openedx.core.lib.xblock_serializer.api import serialize_xblock_to_olx
from helpers.config import (
    LMS_URL,
    STUDIO_URL,
)

class Block:
    '''
    Represents each block in a course
    '''
    def __init__(self, block_obj, parent) -> None:
        self.usage_key = str(block_obj.location)
        self.id = block_obj.location.block_id
        self.obj = block_obj
        self.studio_url = ''
        if block_obj.category == 'vertical':
            self.studio_url = f"{STUDIO_URL}/container/{str(block_obj.location)}"
        self.display_name = block_obj.display_name_with_default
        self.parent = parent
        self.data = ''
        if block_obj.category not in ['chapter', 'sequential', 'vertical']:
            self.data = serialize_xblock_to_olx(block_obj).olx_str

    def __repr__(self) -> str:
        return f"{self.display_name} : {self.usage_key}"
    
    def get_studio_url(self):
        '''
        If studio url not present in the leaf block, return the url
        of the parent block.
        '''
        if self.studio_url:
            return self.studio_url
        elif self.parent:
            return self.parent.get_studio_url()
        else:
            return None
        
    def get_lists_of_links(self):
        jump_to_list = set()
        other_course_list = set()
        external_list = set()
        if self.data:
            # Find all strings starting with `href=` and discard the `href="`
            list_of_links = [link.split('"')[1] for link in re.findall('href=.+?(?=\\">)', self.data)]

            for link in list_of_links:
                # If link has /jump_to_id/ its an internal link
                if re.search('\/jump_to_id\/', link):
                    jump_to_list.add(link.split('/')[2].split('\\')[0])

                # If link has the lms url in it then its a link to other courses
                elif re.search(LMS_URL, link):
                    other_course_list.add(link.split('\\')[0])

                # All other links starting with http are external links
                elif link.startswith('http'):
                    external_list.add(link.split('\\')[0])

        return (jump_to_list, other_course_list, external_list)

class Course:
    '''
    Represents a course
    '''
    def __init__(self, course_obj) -> None:
        self.name = course_obj.display_name
        self.id = str(course_obj.id)
        self.obj = course_obj
        self.url = f"{STUDIO_URL}/course/{str(course_obj.id)}"
        self.blocks = {}
        self.block_id_map = {}
        self.jump_pairs = []
        self.other_courses = []
        self.external_links = []

    def __repr__(self) -> str:
        return f"{self.name} : {self.id}"
    
    @property
    def total_links(self):
        return self.jump_pair_count + self.external_link_count + self.other_course_link_count
    
    @property
    def jump_pair_count(self):
        return len(self.jump_pairs)
    
    @property
    def jump_pair_percentage(self):
        return self.find_percentage(self.jump_pair_count)
    
    @property
    def external_link_count(self):
        return len(self.external_links)
    
    @property
    def external_link_percentage(self):
        return self.find_percentage(self.external_link_count)
    
    @property
    def other_course_link_count(self):
        return len(self.other_courses)
    
    @property
    def other_course_link_percentage(self):
        return self.find_percentage(self.other_course_link_count)
    
    def find_percentage(self, number):
        percentage = (number/self.total_links)*100 if self.total_links != 0 else 0
        return f"{round(percentage, 1)}%"
    
    def add_block(self, block: Block):
        self.blocks[block.usage_key] = block
        self.block_id_map[block.id] = block
    
    def find_links_in_blocks(self):
        for key in self.blocks:
            block = self.blocks.get(key)
            (jump_to_list, other_course_list, external_list) = block.get_lists_of_links()
            if jump_to_list:
                for jump in jump_to_list:
                    jump_to_block = self.block_id_map.get(jump, None)
                    if jump_to_block:
                        self.jump_pairs.append(JumpToPair(block, jump_to_block))

            if other_course_list:
                for link in other_course_list:
                    self.other_courses.append(JumpToPair(block, link))

            if external_list:
                for link in external_list:
                    self.external_links.append(JumpToPair(block, link))

class JumpToPair:
    def __init__(self, jump_from, jump_to) -> None:
        self.jump_from = jump_from
        self.jump_to = jump_to

    def __str__(self) -> str:
        return f"Jump from {self.jump_from} to {self.jump_to}"
