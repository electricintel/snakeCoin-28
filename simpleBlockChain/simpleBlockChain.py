#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
说明： 以列链方式模拟区块链生成
作者： minsang
时间： 2017-4-28
'''

import datetime as date
import block

def create_genesis_block():
    '''
    手动创建创世区块（区块链的第一个区块），索引为0，前一个区块哈希值设为任意值
    '''
    return block.Block(0, date.datetime.now(), "Genesis Block", "0")

def next_block(last_block):
    '''
    在区块链中添加新的区块，即产生区块链的后继区块
    '''
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    this_data = "Hey! I'm Block" + str(this_index)
    this_previous_hash = last_block.hash
    return block.Block(this_index, this_timestamp, this_data, this_previous_hash)

if __name__ == '__main__':
    '''
    使用简单列表代表一个最初区块链,并以列别中添加20个新交易区块为区块链增长的模拟过程
    '''
    blockchain = [create_genesis_block()]
    previous_block = blockchain[0]

    # 定义要添加到区块链的区块个数
    num_of_blocks_to_add = 20

    # 增加区块到区块链
    for i in xrange(num_of_blocks_to_add):
        block_to_add = next_block(previous_block)
        blockchain.append(block_to_add)
        previous_block = block_to_add
        # 打印显示信息
        print "Block {} has been added to the blockchain!".format(block_to_add.index)
        print "Hash: {}\n".format(block_to_add.hash_block())