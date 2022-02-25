# Proto

## Problem Statement

### Parse a custom protocol format

Your payment processing application must interface with an old-school mainframe format that we've named "MPS7".
This means consuming a proprietary binary protocol format that no one on your team is familiar with yet.

### Task

You must write a program that reads in a transaction log and parses it. The transaction log will be named `txnlog.dat` and be in the same directory as your program. A sample `txnlog.dat` file is provided for you. The log should be parsed according to the specification in the **Notes** section below. Your program must answer the following 5 questions:


- What is the total amount in dollars of credits?
- What is the total amount in dollars of debits?
- How many autopays were started?
- How many autopays were ended?
- What is balance of user ID 2456938384156277127?

Your program must output the answers in the format below. For example, if your program determined that the
answer for each question was zero, your program would output:

```
total credit amount=0.00
total debit amount=0.00
autopays started=0
autopays ended=0
balance for user 2456938384156277127=0.00
```

You must supply your source code as part of your answer. Write your code in your
best programming language. We'll want to compile your code from source and run it from a Unix-like command line, so please include the complete instructions for doing so in a COMMENTS file.

### Notes

Because `txnlog.dat` is a binary file, it can't be read by a normal text editor like sublime or vim.
Instead, you'll need to read it programatically and parse the data you read in from there.

This is how the transaction log is structured:

Header:

| 4 byte magic string "MPS7" | 1 byte version | 4 byte (uint32) # of records |

The header contains the canonical information about how the records should be processed. Be sure to validate the magic string from the header to ensure you're parsing the correct file format.
Note: there are fewer than 100 records in the sample `txnlog.dat`, this is not true of all transaction logs though.

Record:

| 1 byte record type enum | 4 byte (uint32) Unix timestamp | 8 byte (uint64) user ID |

Record type enum:

- 0x00: Debit
- 0x01: Credit
- 0x02: StartAutopay
- 0x03: EndAutopay

For Debit and Credit record types, there is an additional field, an 8 byte
(float64) amount in dollars, at the end of the record.

All multi-byte fields are encoded in network byte order.

The first record in the file, when fully parsed, will have these values:

| Record type | Unix timestamp | user ID             | amount in dollars |
| ----------- | -------------- | ------------------- | ----------------- |
| 'Debit'     | 1393108945     | 4136353673894269217 | 604.274335557087  |




------------

## Solution

### Implementation

- The Python module files __MPS7.py__ and __transaction.py__ contain some amount of unit testing, and can be called independently if set as executable. __custom_exceptions.py__ defines local exception types. The __proto.py__ contains the main() entry point and is dependent on the other included files.
- The Python interpreter does not need to be up-to-date, but does require Python3. My development environment is ver 3.9.0.
- By default, the code is looking for an input (MPS7) data log file named __'txnlog.dat'__ in the local directory, but this maybe changed with a command line option.
- Data output is to stdout. Exception messages are written to stderr.
   - The program reads, parses, and stores the data header and transaction log in memory
   - Optionally, the application will output the list of transactions, summary data, and balance for a specified UserID
   - If the # records in the header is less than # of records in the data file, the application will read the spedified number and report the exception. With a command line switch, the error will be suppressed and optionally can read all records (to EOF) or limited to the number specified in the header

### Source files

- MPS7.py
   - __read_header()__ reads the _MPS7 v.1_ header
   - __read_transaction()__ read the _MPS7 v.1_ data records
   - __test_read_header()__ unit test
   - __test_read_transaction()__ unit test
   - __print_transaction()__ 
   - if invoked independently, contains minimal unit testing
- transaction.py
   - __class transaction__ is the data model for data log entities
       - class constructor, properties, and getter methods
   - __add_transaction()__ 
   - __count_transactions()__ 
   - __sum_transactions()__
   - __get_balance()__
   - module also maintains the collection of data entities
   - if invoked independently, contains minimal unit testing  
- local_exceptions.py
   - custom exceptions 
- proto.py
   - __main()__ entry point
   - __get_number_of_records()__ return
   - __get_next_transaction()__ 
   - __parse_command_line()__ 
   - __usage()__


### Usage
```
  chmod +x proto.py
```
print summary usage data
```
  ./proto.py --help
```
main entry point
(to produce the requested output):
```
  ./proto.py -r all -s -u 2456938384156277127
```

(optional:)

(_includes minimal unit testing for the class module_)
``` 
  chmod +x MPS7.py
  ./MPS7.py
  
  chmod +x tranaction.py
  ./transaction
```

```
chmod +x proto.py
    ./proto.py
    ./proto.py -h
    ./proto.py --help
```

