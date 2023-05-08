import hashlib
import json
import datetime

class Blockchain:  #类负责管理链式数据，它会存储交易并且还有添加新的区块到链式数据的Method
    zero_num = 4
    def __init__(self,_index):
        self.current_transactions = []
        self.chain = []
        self.chain_index = _index

        """
        zero_num，用于指定工作量证明中前导零的数量。该类的构造函数__init__(self, _index) 接受一个参数_index，用于设置区块链的初始索引
        self.current_transactions和self.chain都被初始化为空列表，用于存储当前交易和区块链中的所有区块。
        self.chain_index被设置为传入的参数_index。
        """

    def new_block(self, previous_hash):#一个区块包含索引、事务列表、时间戳、校验、前哈希
        block = {
            'chain_index' : self.chain_index,
            'index': len(self.chain) ,
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'transactions': self.current_transactions,
            'nonce': 0,
            'previous_hash': previous_hash,
            'cur_hash':'0',
        }
        self.current_transactions = []  #改成累加
        return block


    """
    chain_index：表示该区块链的索引。
    index：表示该区块在该链中的位置。
    timestamp：表示该区块创建的时间戳。
    transactions：表示该区块中包含的所有交易。
    nonce：表示工作量证明中的随机数。
    previous_hash：表示前一个区块的哈希值。
    cur_hash：表示该区块的哈希值，初始值为0。
    self.current_transactions被清空以准备接受新的交易。最后，block被返回。
    """





    def add_block(self,block,proof):
        if (len(self.chain)==0):
            previous_hash = 0
        else :
            previous_hash = self.last_block()['cur_hash']
            print("last_block_hash = " ,self.last_block['cur_hash'])

        print("block_pre_hash = " , block['previous_hash'])
        
        if previous_hash != block['previous_hash']:
            return False
        print("proof = " + proof)
        if not self.valid_proof(block,proof):
            return False

        block['cur_hash']=proof
        print("block_hash = ", block['cur_hash'])
        self.chain.append(block)
        return True

    """
    block表示要添加的区块，proof表示工作量证明的哈希值。在该方法中，首先通过判断当前链的长度是否为0，
    确定前一个区块的哈希值previous_hash。如果当前链的长度为0，前一个区块的哈希值被设为0；否则，取最
    后一个区块的哈希值作为前一个区块的哈希值。
    然后，方法检查block的previous_hash字段是否与前一个区块的哈希值相等，如果不相等，返回False。接下来
    方法检查工作量证明是否有效，如果无效，返回False。如果工作量证明有效，将block的哈希值cur_hash设为proof
    并将其添加到区块链中。最后，返回True表示添加成功。
    """

    @staticmethod
    def hash(block):
        _data = block['transactions'] + list(str(block['nonce']))
        block_string = json.dumps(_data, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


    """
    这是一个静态方法，它接受一个区块作为输入，将该区块的交易列表和当前的nonce值
    合并成一个列表_data，将_data使用json.dumps()函数进行编码，并进行排序，
    然后将编码后的结果转换为bytes类型，并使用哈希算法进行加密，最后返回哈希值作为该区块的校验值。
    哈希值的生成过程是不可逆的，因此该校验值可以用来确保该区块的完整性和一致性，从而防止区块被篡改。
    """

    def new_transaction(self, sender, contents):  #添加交易到区块
        self.current_transactions.append({
            'sender': sender,
            'contents': contents,
        })
        # return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        block['nonce']=0

        compute_hash = self.hash(block)
        while not compute_hash.startswith('0' * self.zero_num):
            block['nonce'] += 1
            compute_hash=self.hash(block)
        return compute_hash

    # @staticmethod
    def valid_proof(self,block,block_hash):
        return (block_hash.startswith('0' * self.zero_num ) and
                block_hash == self.hash(block))

    def list_chain(self):
        return self.chain
