#!/usr/bin/env python
# coding=utf-8

import re, time, json, logging, hashlib, base64, asyncio

from conf.config import configs
from www.coroweb import get, post
from www.models import User, Comment, Blog, next_id
from www.apis import *
from aiohttp import web


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


_RE_EMAIL = re.compile(r'^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')
COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.session.secret


def user2cookie(user, max_age):
    '''
    Generate cookie str by user.
    '''
    # build cookie string by: id-expires-sha1
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)


@post('/api/users')
def api_register_user(*, email, name, passwd):
    if not name or not name.strip():
        raise APIValueError('name')
    if not email or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd')

    users = yield from User.findAll('email=?', [email])
    if len(users) > 0:
        raise APIError('register:failed', 'email', 'Email is already in use.')

    uid = next_id()
    sha1_passwd = '%s:%s' %(uid, passwd)
    user = User(
        id=uid, name=name.strip(), email=email,
        passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(),
        image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest()
    )
    yield from user.save()

    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r


@get('/register')
def register():
    return {
        '__template__': 'register.html'
    }
