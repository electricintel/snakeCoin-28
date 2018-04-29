#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
说明： 完成初步产品级区块链
作者： minsang
时间： 2017-4-29
'''

import json
import datetime as date
import block
from flask import Flask
from flask import request


def create_genesis_block():
    '''
    手动创建创世区块（区块链的第一个区块），索引为0，前一个区块哈希值设为任意值
    '''
    data = {
        "transaction": {
            "from": "71238uqirbfh894-random-public-key-a-alkjdflakjfewn204ij",
            "to": "93j4ivnqiopvh43-random-public-key-b-qjrgvnoeirbnferinfo",
            "amount": 3
        },
        "proof_of_work": 18
    }
    return block.Block(0, date.datetime.now(), data, "0")


def proof_of_work(last_proof):
    '''
    snakeCoin挖矿的工作量证明算法POW，限制矿工挖掘新的数据货币币种的难度
    snakeCoin的POW采用数字加1自增直到能被len('snakeCoin')=9整除，被前一个工作量证明数字整除
    '''
    # 创建自增器
    increment = last_proof + 1
    # 持续自增直到能被9和last_proof整除,即为本次工作量证明数字
    while not (increment % 9 == 0 and increment % last_proof ==0):
        increment += 1
    return increment




# 创建一个简单的 HTTP 服务器，以便每个用户都可以让我们的节点知道发生了新的交易。
# 节点可以接受 POST 请求，请求数据为如上的JSON交易信息，并支撑GET请求获取交易信息详情
node = Flask(__name__)

@node.route('/transaction', methods = ['POST'])
def transaction():
    if request.method == 'POST':
        # 从每次POST请求中提取出交易信息
        new_txion = request.get_json()
        # 将其增加到本node交易信息序列中
        this_nodes_transactions.append(new_txion)
        # 提交成功后由控制台给出提交成功log
        print "New Transaction"
        print "FROM: {}".format(new_txion['from'])
        print "TO: {}".format(new_txion['to'])
        print "Amount: {}\n".format(new_txion['amount'])
        # 通知客户端交易信息提交成功
        return "The Transaction is submitted sucessfully!"


miner_address = "b1bccf3744-random-miner-address-2d64466528ccd5c"

@node.route('/mine', methods = ['GET'])
def mine():
    # 获取区块链中最后一个区块的证明数字
    last_block = blockchain[-1]
    last_proof = last_block.data['proof_of_work']
    # 计算即将被挖掘区块的证明数字
    proof = proof_of_work(last_proof)
    # 一旦挖到新区块，则奖励矿工一笔交易
    this_nodes_transactions.append({'from': 'network', 'to': miner_address, 'amount': 1})
    # 收集交易信息等，生成新区块
    new_block_data = {
        "transactions": list(this_nodes_transactions),
        "proof_of_work": proof
    }
    this_block_index = last_block.index + 1
    this_block_timestamp = date.datetime.now()
    last_block_hash = last_block.hash
    # 清空本node交易信息列表
    this_nodes_transactions[:] = []
    # 创建新区块
    mined_block = block.Block(this_block_index, 
      this_block_timestamp, 
      new_block_data, 
      last_block_hash)
    # 加入到区块链
    blockchain.append(mined_block)
    # 让客户端知道我们挖到了新的区块
    return json.dumps({
        "index": this_block_index,
        "timestamp": str(this_block_timestamp),
        "data": new_block_data,
        "hash": last_block_hash
    }) + '\n'

# 共识算法：避免节点间区块链冲突
# 如果一个节点的链与其它的节点的不同（例如有冲突），那么最长的链保留，更短的链会被删除
@node.route('/blocks', methods = ['GET'])
def get_blocks():
    '''
    将本节点上的区块链转为json对象并发送给请求它的人
    '''
    chain_to_send = blockchain
    # 将blockchain中各个区块Block对象转python 字典结构，稍后当作json对象进行发送
    for block in blockchain:
        block_index = str(block.index)
        block_timestamp = str(block.timestamp)
        block_data = str(block.data)
        block_hash = block.hash
        block = {
            "index": block_index,
            "timestamp": block_timestamp,
            "data": block_data,
            "hash": block_hash
        }
    # 将json对象类型的区块链发送给请求该区块链的人
    # json.dumps:"""Serialize ``obj`` to a JSON formatted ``str``
    chain_to_send = json.dumps(chain_to_send)
    return chain_to_send


def find_new_chains():
    '''
    找到任何一个其他节点维护的区块链
    '''
    other_chains = []
    for node_url in peer_nodes:
        # 通过GET协议获取其他节点上的区块链
        blocks = request.get(node_url+'/blocks').content
        # 将json对象转为python字典
        # """Deserialize ``s`` (a ``str`` or ``unicode`` instance containing a JSON  document) to a Python object
        blocks = json.loads(blocks)
        # 将其追加到其他区块链序列中
        other_chains.append(blocks)
    return other_chains

def consensus():
    '''
    分布式、去中心化全网区块链共识算法
    '''
    # 获取其他节点上的区块链
    other_chains = find_new_chains()
    # 取最长的区块链进行存储
    longest_chain = blockchain
    for chain in other_chains:
        if len(chain) > len(longest_chain):
            longest_chain = chain
    # 将最长的区块链设为本节点的区块链
    blockchain = longest_chain


if __name__ == '__main__':
    # 将这个node上发生的交易信息存储在一个json元素类型的列表上
    this_nodes_transactions = []
    # 这个node上的区块链
    blockchain = [create_genesis_block()]
    
    node.run()

