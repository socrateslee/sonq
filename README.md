# sonq

__sonq__ means son query, is a tool for querying son like objects, for example, JSON and BSON. You may use sonq to query .bson or newline separated .json files(JSON Lines) directly from the command line.


## Install

```
pip install sonq
```

## Basic Usage

- List the content of a .bson file
```
sonq source.bson
```
- Query a .bson file
```
sonq -f '{"name": "Stark"}' source.bson
```
- Convert query results to a newline separated .json file
```
sonq -f '{"name": "Stark"}' -o target.json source.bson
```
- Convert json from stdin to .bson
```
echo '{"name": "Stark"}' | python3 -m sonq.cmd -o target.bson - 
```