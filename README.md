# data-monitor-tool

Data monitor tool (dmt for short) is the simplest way to 
understand your data resources.

# Profiles

Profiling helps you understand what work your database is doing.

- Which tables are most accessed? In terms of:
    - The # of times they were queried (accessed)
    - The # of rows scanned
    - The amount of time spent querying

```
$ python cmd/profile.py redshift --connection-string 'dbname=datawarehouse user=dannym password=X host=localhost port=5439' > profile.csv
```
