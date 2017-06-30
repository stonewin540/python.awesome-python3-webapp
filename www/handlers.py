#!/usr/bin/env python
# coding=utf-8

import re, time, json, logging, hashlib, base64, asyncio
from www.coroweb import get, post
from www.models import User, Comment, Blog, next_id


@get('/')
async def index(request):
    users = await User.findAll()

    # # test start
    # words = {
    #     0: 'a',
    #     1: 'b',
    #     2: 'c',
    #     3: 'd',
    #     4: 'e',
    #     5: 'f',
    #     6: 'g',
    #     7: 'h',
    #     8: 'i',
    #     9: 'j',
    #     10: 'k',
    # }
    # max_count = 10
    # count = len(users)
    # if count < max_count:
    #     for i in range(count, max_count + 1):
    #         u = User(name='test%d' % i, email='%d@%s.com' % (i, words[i]), passwd='p%s' % i, image='about: blank')
    #         await u.save()
    #         users.append(u)
    # # test end

    return {
        '__template__': 'test.html',
        'users': users
    }
