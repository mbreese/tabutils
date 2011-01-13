tabutils
===

These are a set of utility scripts for dealing with tab-delimited files.  In this setup tab-delimited files can comment lines starting with '#'.  They may or may not contain headers.

There are three main scripts:

* tab_filter
* tab_merge
* tab_view

tab_filter
---
Allows you to view only lines that meet certain criteria.

tab_filter.py file.txt {criteria}

Eg: 

1 eq foo

- Column 1 (first column) is equal to 'foo'

1 eq foo 2 lt 3

- Column 1 (first column) is equal to 'foo' and column 2 is less than 3

Valid operations:
eq
ne
lt
lte
gt
gte
contains

tab_merge
---
Merges tab-delimited files together, combining common columns and adding uncommon columns.

tab_view
---
Displays tab-delimited files, spacing columns appropriately to keep them in-line.