#!/usr/bin/python

import os, csv
from post import Post

pathbackup = 'E:\\blog backup\\wp-content\\backup-a9adc\\westkara_wp_20131107_981.sql'
comment_key = 'INSERT INTO `wp_comments` VALUES ('
post_key = 'INSERT INTO `wp_posts` VALUES ('
post_csv = 'posts.csv'

def consume(l):
    state = 0
    stuff = None

    for c in l:
        if state == 0:
            if c.isdigit():
                state = 1
                stuff = int(c)
            elif c == "'":
                state = 2
                stuff = ''
        elif state == 1:
            if c.isdigit():
                stuff = stuff * 10 + int(c)
            elif stuff is not None:
                yield stuff
                stuff = None
                state = 0
        elif state == 2:
            if c == '\\':
                state = 3
            elif c == "'":
                yield stuff
                stuff = None
                state = 0
            else:
                stuff += c
        elif state == 3:
            if c == "'":
                stuff += "'"
            else:
                stuff += "\\" + c
            state = 2
    
    if stuff:
        yield stuff
                

def processComment(l):
    pass

def preparePostCsv():
    if os.path.exists(post_csv):
        os.remove(post_csv)
    with open(post_csv, 'w', encoding="utf8") as f:
        f.write('ID,post_author,post_date,post_date_gmt,post_content,post_title,post_category,post_excerpt,post_status,comment_status,ping_status,post_password,post_name,to_ping,pinged,post_modified,post_modified_gmt,post_content_filtered,post_parent,guid,menu_order,post_type,post_mime_type,comment_count\n')

def processPost(l):
    with open(post_csv, 'a', encoding="utf8", newline='') as f:
        writer = csv.writer(f)
        vals = [x for x in consume(l)]
        writer.writerow(vals)

def processLine(l):
    if l.startswith(comment_key):
        processComment(l[len(comment_key)])
    elif l.startswith(post_key):
        processPost(l[len(post_key):-4])

if __name__ == "__main__":
    with open(pathbackup, 'r', encoding="utf8") as f:
        print ("We found the backup!")
        preparePostCsv()
        lineno = 0
        try:
            for l in f:
                lineno += 1
                processLine(l)
        except UnicodeDecodeError as err:
            print ("Unicode error in line {}, was {}".format(lineno, err))

    with open(post_csv, 'r', encoding="utf8") as f:
        reader = csv.DictReader(f, dialect='excel')
        for l in reader:
            if l['post_status'] == 'publish':
                p = Post(l)
                p.save()
                

