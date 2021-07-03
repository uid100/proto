#!/usr/bin/env python3

# ------ 1 ------- 2 ------- 3 ------- 4 ------- 5 ------- 6 ------- 7 ------- 8
# Proto - Parse a custom protocol format

# Assumptions:
# if the file is static (not streaming), read the entire file to a buffer 
# with a single disk read

# - What is the total amount in dollars of credits?
# - What is the total amount in dollars of debits?
# - How many autopays were started?
# - How many autopays were ended?
# - What is balance of user ID 2456938384156277127?
# ------ 1 ------- 2 ------- 3 ------- 4 ------- 5 ------- 6 ------- 7 ------- 8

import sys
import MPS7
import transaction

txn_file = 'txnlog.dat'
default_userID = '2456938384156277127'


def main():
    ''' parse a binary custom protocol transaction log format '''

    try:
        log = open( txn_file, 'rb' )
        buf = log.read()
    except:
        print( f'error reading file: {txn_file}', file=sys.stderr )

    file_size = len(buf)
    if VERBOSE:
        print( f'read {file_size} bytes', file=sys.stderr )

    # parse header
    num_records, file_pos = get_number_of_records(buf)
    if VERBOSE:
        print( f'{num_records} records to read. starting at {file_pos}', \
            file=sys.stderr )

    if LIST:
        print('id, type, time, user_id, amount')

    # parse records
    done = not VALIDATE_COUNT or num_records > 0
    while file_pos < file_size and not done:
        bytes_read,counter,type,timestamp,user_id,amount = get_next_transaction(buf, file_pos)
        file_pos += bytes_read
        if LIST:
            print(f'{counter},{type},{timestamp},{user_id},',end='')
            if type in [MPS7.credit,MPS7.debit]:
                print(amount,end='')
            print()
        if VALIDATE_COUNT and counter >= num_records:
            done = True

    # list accounts and balances
    if VALIDATE_COUNT and counter != num_records:
        print(f'Warning: invalid record count. {counter}/{num_records} ' \
            +'records read.',file=sys.stderr)
        

def get_number_of_records( buf ):
    nrecs, pos = MPS7.read_header( buf )
    return nrecs, pos

def get_next_transaction( buf, pos ):
    nr_bytes, type, timestamp, user_id, amount = MPS7.read_transaction( buf, pos)
    txn_id = transaction.add_transaction(type, timestamp, user_id, amount)
    return nr_bytes, txn_id, type, timestamp, user_id, amount


# ------ 1 ------- 2 ------- 3 ------- 4 ------- 5 ------- 6 ------- 7 ------- 8

VERBOSE = False
VALIDATE_COUNT = True
READ_ALL_RECORDS = False
LIST = False

def parse_command_line():
    global VERBOSE
    global VALIDATE_COUNT
    global READ_ALL_RECORDS
    global LIST

    if '-h' in sys.argv or '--help' in sys.argv:
        usage()
        sys.exit()

    opt = 1
    while opt<len(sys.argv):
        if option in ['-r','--records']:
            VALIDATE_COUNT = False
            opt += 1
            if sys.argv[opt] == 'all':
                # read all records. ignore header count
                READ_ALL_RECORDS = True
            elif sys.argv[opt] == 'header':
                # read only to record count
                READ_ALL_RECORDS = False
            else:
                usage()
                sys.exit()
        if option in ['-l','--list']:
            LIST = True
        if option in ['-v','--verbose']:
            VERBOSE = True
        if option in ['-f','--file']:
            opt += 1
            txn_file = argv[opt]
        if option == '-u':
            opt += 1
            report_user = argv[opt]
        opt += 1

def usage():
        print('\n'\
            + 'NAME:\n' \
                + f'\t{sys.argv[0]} - read and parse MPS7 transaction log ' \
                + 'file. Print summary.\n\n' \
            + 'SYNOPSIS:\n' \
                + f'\t{sys.argv[0]} [-h | --help]\n' \
                + f'\t{sys.argv[0]} [-l | --list] ' 
                + '[-r | --records all | header]\n' \
                + f'\t{sys.argv[0]} [[-] | [-f file]] [-v | --verbose] ' \
                + '[-s [-u user_id]] ...\n' \
                + '\t\t[--records [all|header]] | [-ra|-rh]\n\n' \
            + 'OPTIONS:\n' \
                + '\t-f  file  read from specified filename. \n' \
                + '\t\tDefault is txnlog.dat from current directory.\n\n' \
                + '\t-h | --help  display this usage statement (stderr)\n\n' \
                + '\t-l | --list  list all records as CSV to stdout.\n\n' \
                # TODO: add support for read from stdin
                # + '\t-   read from stdin (see -f for default behavior)\n\n' \
                + '\t-u  specify user to include in formatted summary \n' \
                + '\t\t(default is id:2456938384156277127)\n\n' \
                + '\t-ra  read all records in log file (suppress warning)\n' \
                + '\t\tby default, read all and warn if record number in \n' \
                + '\t\theader does not match (to stderr).\n' \
                + '\t-rh  read only number of records specified in header\n' \
                + '\t\twarn if number of records does not match (stderr)\n\n' \
                + '\t-v|--verbose  include detailed process/status messages ' \
                + '\noutput to stderr (disabled by default)\n\n' \
                # + '\t-s  output formatted summary detail (default is on) to ' \
                # + 'stdout\n' \
                # TODO: add support for output sorted user list only
                # + '\t-l  print sorted list of userIDs for user selection ' \
                # + 'from stdin \n\t\t(for user summary)\n' \
            ,file=sys.stderr )

if __name__ == '__main__':
    if len(sys.argv) > 0:
        parse_command_line()
        main()
    else:
        # wrapper:  configure default usage
        main()