#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
说明： 定义一个区块类型，类包含块索引、时间戳、数据、前一个区块的哈希值，类方法包含对象初始化方法和对区块求解哈希值
作者： minsang
时间： 2017-4-28
'''
import hashlib as hasher

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash

    def hash_block(self):
        sha = hasher.sha256()
        sha.update(str(self.index) + 
                       str(self.timestamp) + 
                       str(self.data) + 
                       str(self.previous_hash))
        return sha.hexdigest()
