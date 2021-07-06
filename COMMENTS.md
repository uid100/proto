# COMMENTS

## Implementation
_(So much fun!)_
- The Python module files __MPS7.py__ and __transaction.py__ contain some amount of unit testing, and can be called independently if set as executable. __custom_exceptions.py__ defines local exception types. The __proto.py__ contains the main() entry point and is dependent on the other included files.
- The Python interpreter does not need to be up-to-date, but does require Python3. My development environment is ver 3.9.0.
- By default, the code is looking for an input (MPS7) data log file named __'txnlog.dat'__ in the local directory, but this maybe changed with a command line option.
- Data output is to stdout. Exception messages are written to stderr.
   - The program reads, parses, and stores the data header and transaction log in memory
   - Optionally, the application will output the list of transactions, summary data, and balance for a specified UserID
   - If the # records in the header is less than # of records in the data file, the application will read the spedified number and report the exception. With a command line switch, the error will be suppressed and optionally can read all records (to EOF) or limited to the number specified in the header

## Source files

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


## Usage
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

