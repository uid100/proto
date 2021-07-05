#!/usr/bin/env python3

# ------ 1 ------- 2 ------- 3 ------- 4 ------- 5 ------- 6 ------- 7 ------- 8
# MPS7 

# Assumptions:

# Header structure
#    | 4 byte magic string | 1 byte version | 4 byte (uint32) # of records |

# ------ 1 ------- 2 ------- 3 ------- 4 ------- 5 ------- 6 ------- 7 ------- 8

import sys
import struct
import datetime
import time
from local_exceptions import *

magic_string = "MPS7"
tested_version = '1'
exit_on_unsupported_version = False


debit = 0
credit = 1
startAutopay = 2
endAutopay = 3


# '>'  - big-endian, override native OS default
# '4s' - 4 byte char string       - file id
# 'B'  - 1 byte unsigned char     - version id
# 'I'  - (4 bytes) uint32         - # of records
header_format = '> 4s B I'

def read_header(buf, version=tested_version):
    ''' 
    Parse Header for MPS7 file. Return number of records.
    If file contains version different than supported version
    number, pass as argument to suppress the error.
    '''

    header = struct.unpack_from(header_format, buf, 0)

    magic = str(header[0],'utf-8')
    if( magic != magic_string ):
        raise UnsupportedFileTypeException

    file_version = str(header[1])
    if file_version != version:
        raise UnsupportedFileVersion

    number_of_records = header[2]
    header_size = struct.calcsize(header_format)

    return number_of_records, header_size


# '>'  - big-endian   (override native OS default)
# 'B'  - 1 byte unsigned char          - record type
# 'I'  - 4 byte uint32                 - timestamp
# 'Q'  - 8 bytes unsigned long long    - user ID
# 'd'  - 8 bytes double float          - amount
transaction_format = '> B I Q'
amount_format = '> d'

def read_transaction( buf, pos):
    '''
    Parse transaction log item for MPS7 file.
    '''

    transaction = struct.unpack_from(transaction_format, buf, pos)
    num_bytes = struct.calcsize(transaction_format)
    pos += num_bytes

    amount = 0.0
    txn_type = transaction[0]
    timestamp = transaction[1]
    user_id = str(transaction[2])
    if transaction[0] in [debit, credit]:
        amount = struct.unpack_from(amount_format, buf, pos)[0] # don't return as tuple
        num_bytes += struct.calcsize(amount_format)
    
    return num_bytes, txn_type, timestamp, user_id, amount


def test_read_header():
    x = struct.pack( header_format, b'MPS7', 0x01, 99 )
    nrecs, nbytes = read_header(x)
    print( f'{x} --> header_size: {nbytes}, # records: {nrecs}' )

    x = struct.pack( header_format, b'MPSx', 0x01, 99 )
    nrecs, nbytes = read_header(x)
    print( f'{x} --> header_size: {nbytes}, # records: {nrecs}' )

    x = struct.pack( header_format, b'MPS7', 0x02, 99 )
    nrecs, nbytes = read_header(x)
    print( f'{x} --> header_size: {nbytes}, # records: {nrecs}' )

def test_read_transaction():
    x = struct.pack( transaction_format + 'd', credit, int(time.time()), 12345678, 1.25 )
    print_transaction(x)
    x = struct.pack( transaction_format + 'd', credit, int(time.time()), 12345678, 1.75 )
    print_transaction(x)
    x = struct.pack( transaction_format + 'd', debit, int(time.time()), 12345678, 1.50 )
    print_transaction(x)
    x = struct.pack( transaction_format, startAutopay, int(time.time()), 12345678 )
    print_transaction(x)

def print_transaction(x):
    size, what, when, who, how_much = read_transaction(x,0)
    print( f'{x} --> rec_size: {size} {when} {who} ', end='')
    if what == startAutopay:
        print('start')
    elif what == endAutopay:
        print('end')
    elif what == credit:
        print(f'{how_much:.2f}')
    elif what == debit:
        print(f'-{how_much:.2f}')
    else:
        print('unrecognized {what}')


TEST = False
if __name__ == '__main__':
    TEST = True
    print('\n\nTest: read header')
    test_read_header()

    print('\n\nTest: read data records')
    test_read_transaction()

    print()