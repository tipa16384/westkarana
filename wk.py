#!/usr/bin/python

import os
from post import Post, post_key, post_columns
from utils import consume
from user import User, user_key, user_columns


pathbackup = 'E:\\blog backup\\wp-content\\backup-a9adc\\westkara_wp_20131107_981.sql'
comment_key = 'INSERT INTO `wp_comments` VALUES ('

post_dict = {}
user_dict = {}


def processComment(l):
    pass


def processPost(l):
    l = l.replace('http://westkarana.com/wp-content', '..')
    l = l.replace('http://westkarana.com', '..')

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
        post_dict[post.ID] = post
    elif l.startswith(user_key):
        user = processUser(l)
        user_dict[user.ID] = user


def post_associate_author():
    for post in post_dict.values():
        post.setPostAuthorUser(user_dict)


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
        if post.post_status == 'publish':
            post.save()
