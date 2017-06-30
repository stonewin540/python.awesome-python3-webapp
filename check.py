#!/usr/bin/env python
# coding=utf-8

import asyncio

import www.static.orm as orm

from www.models import User


async def check(loop):
    await orm.create_pool(loop, user='www-data', password='www-data', db='awesome')

    u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')

    await u.save()

# for x in test():
#     pass
loop = asyncio.get_event_loop()
loop.run_until_complete(check(loop))
loop.close()
