#!/usr/bin/python

import os
from post import Post, post_key, post_columns
from utils import consume
from user import User, user_key, user_columns
from pages import create_year_page, create_year_month_page, create_year_month_day_page

pathbackup = 'E:\\blog backup\\wp-content\\backup-a9adc\\westkara_wp_20131107_981.sql'
comment_key = 'INSERT INTO `wp_comments` VALUES ('

post_dict = {}
user_dict = {}
by_year = {}
by_year_month = {}


def processComment(l):
    pass


def processPost(l):
    l = l.replace('http://westkarana.com/wp-content', '../../..')
    l = l.replace('http://westkarana.com', '../../..')

    vals = [x for x in consume(l)]
    post_val_dict = {}
    for i in range(len(post_columns)):
        post_val_dict[post_columns[i]] = vals[i] if i < len(vals) else None
    return Post(post_val_dict)


def processUser(l):
    vals = [x for x in consume(l)]
    user_val_dict = {}
    for i in range(len(user_columns)):
        user_val_dict[user_columns[i]] = vals[i] if i < len(vals) else None
    return User(user_val_dict)


def processLine(l):
    if l.startswith(comment_key):
        processComment(l[len(comment_key)])
    elif l.startswith(post_key):
        post = processPost(l[len(post_key):-4])
        if post.post_status == 'publish':
            post_dict[post.ID] = post
    elif l.startswith(user_key):
        user = processUser(l)
        user_dict[user.ID] = user


def post_associate_author():
    for post in post_dict.values():
        post.setPostAuthorUser(user_dict)


def addPostToYear(post):
    if post.post_year in by_year:
        by_year[post.post_year] += 1
    else:
        by_year[post.post_year] = 1
    #print ("by_year now {}".format(by_year))


def addPostToMonth(post):
    tups = (post.post_year, post.post_month)

    if tups in by_year_month:
        by_year_month[tups].append(post)
    else:
        by_year_month[tups] = [post]


if __name__ == "__main__":
    with open(pathbackup, 'r', encoding="utf8") as f:
        print("We found the backup!")
        lineno = 0
        try:
            for l in f:
                lineno += 1
                processLine(l)
        except UnicodeDecodeError as err:
            print("Unicode error in line {}, was {}".format(lineno, err))

    post_associate_author()

    for post in post_dict.values():
        post.save()
        addPostToYear(post)
        addPostToMonth(post)

    create_year_page(by_year)
    create_year_month_page(by_year_month)
    for ym in by_year_month:
        create_year_month_day_page(ym, by_year_month[ym])
