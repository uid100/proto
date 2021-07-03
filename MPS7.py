#!/usr/bin/env python3

# ------ 1 ------- 2 ------- 3 ------- 4 ------- 5 ------- 6 ------- 7 ------- 8
# MPS7 

# Assumptions:

# Header structure
#    | 4 byte magic string | 1 byte version | 4 byte (uint32) # of records |

# ------ 1 ------- 2 ------- 3 ------- 4 ------- 5 ------- 6 ------- 7 ------- 8

import sys
import struct

magic_string = "MPS7"
supported_version = '1'
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

def read_header(buf):
    ''' 
    Parse Header for MPS7 file. Return number of records.
    '''

    header = struct.unpack_from(header_format, buf, 0)

    magic = str(header[0],'utf-8')
    if( magic != magic_string ):
        print( f'Warning: unsupported file type {magic}', file=sys.stderr )
        if TEST:
            return -99, -99
        sys.exit()

    file_version = str(header[1])
    if file_version != supported_version:
        # support for other versions should be verified
        print( f'Warning: unsupported {magic_string} version {file_version}', file=sys.stderr)
        if TEST:
            return -99, -99
        if exit_on_unsupported_version:
            sys.exit()

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
    user_id = transaction[2]
    if transaction[0] in [debit, credit]:
        amount = struct.unpack_from(amount_format, buf, pos)[0] # don't return as tuple
        num_bytes += struct.calcsize(amount_format)
    
    return num_bytes, txn_type, timestamp, user_id, amount


def test_read_header():
    header_format = '>4sBI'

    x = struct.pack( header_format, b'MPS7', 0x01, 99 )
    nrecs, nbytes = read_header(x)
    print( f'{x} --> header_size: {nbytes}, # records: {nrecs}' )

    x = struct.pack( header_format, b'MPSx', 0x01, 99 )
    nrecs, nbytes = read_header(x)
    print( f'{x} --> header_size: {nbytes}, # records: {nrecs}' )

    x = struct.pack( header_format, b'MPS7', 0x02, 99 )
    nrecs, nbytes = read_header(x)
    print( f'{x} --> header_size: {nbytes}, # records: {nrecs}' )


TEST = False
if __name__ == '__main__':
    TEST = True
    test_read_header()