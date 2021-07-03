# COMMENTS

## Assumptions

- The Python module files __MPS7.py__ and __rate_area.py__ contain some amount of unit testing, and can be called independently if set as executable. The __slcsp.py__ contains the main() entry point and is dependent on the other two.
- The Python interpreter does not need to be up-to-date, but does require Python3. My development environment is ver 3.9.0.
- The rate_area and health_plan data modules support different file names and locations, but the main() program configuration expects the files named __'zips.csv'__ and __'plans.csv'__ to be in the local directory.
- Data output is to stdout. Exception messages are written to stderr.
- Using the command line switch __'-'__ will enable the program to accept data from stdin, but by default, the program will look for a __'slcsp.csv'__ file in the local directory.

## Source files

- MPS7.py
   - __read_header()__ reads the _MPS7 v.1_ header
   - __read_transaction()__ read the _MPS7 v.1_ data records
   - if invoked independently, contains minimal unit testing
- rate_area.py
   - __class rate_area__ is the data model for reading the CSV
   - __read_rate_area_data()__ reads only the subset of data required to determine rate_area (default './plans.csv') into memory (no return)
   - __get_rate_area()__ finds rate_area and returns (as tuple) if available and unambiguous
   - if invoked independently, contains minimal unit testing  
- slcsp.py
   - __main()__ entry point
   - __input_filename()__ includes minimal command line parsing


## Usage
```
  chmod +x proto.py
  ./proto.py
```[output]
```
summary
```
  ./proto.py --help
  ...
```

(optional:)

(_includes minimal unit testing for the class module_)
``` 
chmod +x MPS7.py
    ./MPS7.py
```

(optional:)
```
chmod +x rate_area.py
    ./rate_area.py
    ./rate_area.py -f ./test_zips.csv
    ./rate_area.py -z 92040
```

(main entry point:)
```
chmod +x proto.py
    ./proto.py
    ./proto.py -h
    ./proto.py --help
```

