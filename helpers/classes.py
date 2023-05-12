import re
from .config import LMS_URL

class Block:
    '''
    Represents each block in a course
    '''
    def __init__(self, block_dict) -> None:
        self.usage_key = block_dict.get('id', '')
        self.id = block_dict.get('block_id', '')
        self.lms_url = block_dict.get('lms_web_url', '')
        self.studio_url = None
        self.type = block_dict.get('type', '')
        self.display_name = block_dict.get('display_name', '')
        self.children = block_dict.get('children', None)
        self.parent = None
        self.data = None

    def __str__(self) -> str:
        return f"{self.display_name} : {self.usage_key}"
    
    def print_ancestry(self):
        if self.parent:
            ancestry = self.parent.print_ancestry()
            return f"{ancestry} -> {self.usage_key}"
        
        return self.usage_key
    
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
    def __init__(self, course_dict) -> None:
        self.name = course_dict['name']
        self.id = course_dict['id']
        self.url = ''
        self.blocks_url = course_dict['blocks_url']
        self.blocks = {}
        self.block_id_map = {}
        self.jump_pairs = []
        self.other_courses = []
        self.external_links = []

    def __str__(self) -> str:
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
    
    def map_block_hierarchy(self):
        '''
        Link the parent block for each block
        '''
        for key in self.blocks:
            parent_block = self.blocks.get(key)
            if parent_block.children:
                for child in parent_block.children:
                    child_block = self.blocks.get(child)
                    child_block.parent = parent_block

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
