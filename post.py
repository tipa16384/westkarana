#!/usr/bin/Python

# ID,post_author,post_date,post_date_gmt,post_content,post_title,post_category,post_excerpt,post_status,comment_status,ping_status,post_password,
# # post_name,to_ping,pinged,post_modified,post_modified_gmt,post_content_filtered,post_parent,guid,menu_order,post_type,post_mime_type,comment_count

import os
from markdownify import markdownify

postfolder = './posts'

class Post:

    def __init__(self, row):
        self.ID = row['ID']
        self.post_author = row['post_author']
        self.post_date = row['post_date']
        self.post_date_gmt = row['post_date_gmt']
        self.post_content = row['post_content']
        self.post_title = row['post_title']
        self.post_category = row['post_category']
        self.post_excerpt = row['post_excerpt']
        self.post_status = row['post_status']
        self.comment_status = row['comment_status']
        self.ping_status = row['ping_status']
        self.post_password = row['post_password']
        self.post_name = row['post_name']
        self.to_ping = row['to_ping']
        self.pinged = row['pinged']
        self.post_modified = row['post_modified']
        self.post_modified_gmt = row['post_modified_gmt']
        self.post_content_filtered = row['post_content_filtered']
        self.post_parent = row['post_parent']
        self.guid = row['guid']
        self.menu_order = row['menu_order']
        self.post_type = row['post_type']
        self.post_mime_type = row['post_mime_type']
        self.comment_count = row['comment_count']

    def save(self):
        postpath = os.path.join(postfolder, self.ID + ".md")
        if os.path.exists(postpath):
            os.remove(postpath)
        with open(postpath, 'w', encoding="utf8") as f:
            print("# {}\n".format(self.post_title), file=f)
            md = markdownify(self.post_content)
            md = md.replace('\\r', '').replace('\\n', '\n')
            print("{}".format(md), file=f)
