#!/usr/bin/env python
# coding=utf-8

import re, time, json, logging, hashlib, base64, asyncio
from www.coroweb import get, post
from www.models import User, Comment, Blog, next_id


# @get('/')
# async def index(request):
#     users = await User.findAll()
#
#     # # test start
#     # words = {
#     #     0: 'a',
#     #     1: 'b',
#     #     2: 'c',
#     #     3: 'd',
#     #     4: 'e',
#     #     5: 'f',
#     #     6: 'g',
#     #     7: 'h',
#     #     8: 'i',
#     #     9: 'j',
#     #     10: 'k',
#     # }
#     # max_count = 10
#     # count = len(users)
#     # if count < max_count:
#     #     for i in range(count, max_count + 1):
#     #         u = User(name='test%d' % i, email='%d@%s.com' % (i, words[i]), passwd='p%s' % i, image='about: blank')
#     #         await u.save()
#     #         users.append(u)
#     # # test end
#
#     return {
#         '__template__': 'test.html',
#         'users': users
#     }

@get('/')
def index(request):
    summary = \
        'Lorem ipsum dolor sit amet, ' \
        'consectetur adipisicing elit, ' \
        'sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.'
    blogs = [
        Blog(id='1', name='Test blog', summary=summary, created_at=time.time()-120),
        Blog(id='2', name='Something New', summary=summary, created_at=time.time() - 3600),
        Blog(id='3', name='Learn Swift', summary=summary, created_at=time.time() - 7200),
    ]
    return {
        '__template__': 'blogs.html',
        'blogs': blogs
    }


@get('/api/users')
async def api_get_users():
    users = await User.findAll(orderBy='created_at desc')
    for u in users:
        u.passwd = '******'
    return dict(users=users)


@get('/api/blogs')
async def api_get_blogs():
    blogs = await Blog.findAll(orderBy='created_at desc')
    return dict(blogs=blogs)
