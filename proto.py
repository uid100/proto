#!/usr/bin/env python3

# ------ 1 ------- 2 ------- 3 ------- 4 ------- 5 ------- 6 ------- 7 ------- 8
# Proto - Parse a custom protocol format

# Assumptions:
# read the entire static (not-streaming) file to a buffer with a single disk read

# - What is the total amount in dollars of credits?
# - What is the total amount in dollars of debits?
# - How many autopays were started?
# - How many autopays were ended?
# - What is balance of user ID 2456938384156277127?
#  ./proto.py -r all -u 2456938384156277127
# ------ 1 ------- 2 ------- 3 ------- 4 ------- 5 ------- 6 ------- 7 ------- 8

import sys
import MPS7
import transaction
from local_exceptions import *

txn_file = 'txnlog.dat'
userIDs = []


def main():
    ''' parse a binary custom protocol transaction log format '''

    try:
        log = open( txn_file, 'rb' )
        buf = log.read()
    except:
        print( f'error reading file: {txn_file}', file=sys.stderr )
    file_size = len(buf)

    # parse header
    num_records, file_pos = get_number_of_records(buf)

    if print_transaction_log:
        print('id, type, time, user_id, amount')

    # parse records
    counter = 1
    done = counter > num_records and validate_count_strict
    while file_pos < file_size and not done:
        bytes_read,counter,type,timestamp,user_id,amount = get_next_transaction(buf, file_pos)
        file_pos += bytes_read
        if print_transaction_log:
            print(f'{counter},{type},{timestamp},{user_id},',end='')
            if type in [MPS7.credit,MPS7.debit]:
                print(amount,end='')
            print()
        if validate_count_strict and counter >= num_records:
            done = True
            if file_pos < file_size and validate_count_strict:
                print(f'\nWarning: stopped reading before EOF ({counter} records)', file=sys.stderr)
                print( '\tuse -r all to process all records in log file.\n')

    # list accounts and balances
    if validate_count_strict and counter != num_records:
        print(f'Warning: invalid record count. {counter}/{num_records} ' \
            +'records read.',file=sys.stderr)

    if print_summary:
        total_credit_amount = transaction.sum_transactions(MPS7.credit)
        total_debit_amount = transaction.sum_transactions(MPS7.debit)
        count_autopay_start = transaction.count_transactions(MPS7.startAutopay)
        count_autopay_end = transaction.count_transactions(MPS7.endAutopay)
        print(  f'total credit amount={total_credit_amount:.2f}\n' \
                f'total debit amount={total_debit_amount:.2f}\n' \
                f'autopays started={count_autopay_start}\n' \
                f'autopays ended={count_autopay_end}' )

    if print_user_balance:
        for u in userIDs:
            balance = transaction.get_balance(u)
            print( f'balance for user {u}={balance:.2f}')

    if not print_summary and not print_user_balance and not print_transaction_log:
        print( 'done.\n' \
                + '\tuse -l to list transaction log entries\n' \
                + '\t or -s to view transaction summary\n' \
                + '\t or -u user_id to view user balance\n', file=sys.stderr )


        
def get_number_of_records( buf ):
    try:
        nrecs, pos = MPS7.read_header( buf, data_file_version )
    except UnsupportedFileTypeException as ex:
        print( f'Error: unsupported file type {ex}', file=sys.stderr )
        sys.exit()
    except UnsupportedFileVersion as ex:
        print( f'Error: unsupported file version {ex}', file=sys.stderr)
        sys.exit()
    except Exception as ex:
        print( 'Generic exception reading header: ',ex)
        sys.exit()
    return nrecs, pos


def get_next_transaction( buf, pos ):
    nr_bytes, type, timestamp, user_id, amount = \
        MPS7.read_transaction( buf, pos)
    txn_id = transaction.add_transaction(type, timestamp, user_id, amount)
    return nr_bytes, txn_id, type, timestamp, user_id, amount


# ------ 1 ------- 2 ------- 3 ------- 4 ------- 5 ------- 6 ------- 7 ------- 8

validate_count_strict = True
data_file_version = '1'
read_all_records = False
print_summary = False
print_transaction_log = False
print_user_balance = False


def parse_command_line():
    global validate_count_strict
    global data_file_version
    global read_all_records
    global print_user_balance
    global print_summary
    global print_transaction_log

    if '-h' in sys.argv or '--help' in sys.argv:
        usage()
        sys.exit()

    opt = 1
    while opt<len(sys.argv):
        option = sys.argv[opt]
        if option in ['-r','--records']:
            validate_count_strict = False
            opt += 1
            if sys.argv[opt] == 'all':
                # read all records. ignore header count
                read_all_records = True
            elif sys.argv[opt] == 'header':
                # read only to record count
                read_all_records = False
            else:
                usage()
                sys.exit()
        if option in ['-f','--file']:
            opt += 1
            txn_file = sys.argv[opt]
        if option in ['-l','--list']:
            print_transaction_log = True
        if option in ['-s','--summary']:
            print_summary = True
        if option in ['-v','--version']:
            opt += 1
            data_file_version = sys.argv[opt]
        if option == '-u':
            print_user_balance = True
            opt += 1
            userIDs.append(sys.argv[opt])
        opt += 1

def usage():
        print('\n'\
            + 'NAME:\n' \
                + f'\t{sys.argv[0]} - parse MPS7 transaction log\n\n' \
            + 'SYNOPSIS:\n' \
                + f'\t{sys.argv[0]} [-h|--help]\n' \
                + f'\t{sys.argv[0]} [-l|--list] [-v|--version n] ' \
                + '[-r|--records all|header]\n' \
                + f'\t{sys.argv[0]} [-f file] [-v|--version n] ' \
                + '[-s [-u user_id]] ...\n' \
                + '\t\t[-0] [-r|--records [all|header]]\n\n' \
            + 'OPTIONS:\n' \
                + '\t-f | --file  read from specified filename. \n' \
                + '\t\tDefault is txnlog.dat from current directory.\n\n' \
                + '\t-h | --help  display this usage statement (stderr)\n\n' \
                + '\t-l | --list  list all records as CSV to stdout.\n\n' \
                + '\t-r | --records  all|header  By default, validates ' \
                + 'number of records\n\t\tin data file against record ' \
                + 'count in header and warns (to \n\t\tstderr) iI not ' \
                + 'matching. Suppress warning and optionally \n\t\tlimit ' \
                + 'records read by header declaration or read all to \n\t\t' \
                + 'end-of-file (EOF)\n\n' \
                + '\t-s | --summary  print summary report\n\n'
                + '\t-u user_id  display balance for user \n\n' \
                + '\t-v | --version  suppress unsupported file version '
                + 'error.\n\n' \
            ,file=sys.stderr )

if __name__ == '__main__':
    parse_command_line()
    main()
