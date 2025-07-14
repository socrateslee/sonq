# Tutorial

This tutorial will walk you through the basic usage of `sonq` using a sample `users.json` file.

## Sample Data

First, let's create a sample file named `users.json` with the following content:

```json
[
  {"name": "John Doe", "age": 30, "city": "New York", "is_active": true, "tags": ["user", "admin"]},
  {"name": "Jane Smith", "age": 25, "city": "London", "is_active": true, "tags": ["user"]},
  {"name": "Peter Jones", "age": 42, "city": "New York", "is_active": false, "tags": ["user", "editor"]},
  {"name": "Mary Johnson", "age": 17, "city": "Paris", "is_active": true, "tags": ["user"]},
  {"name": "David Williams", "age": 35, "city": "London", "is_active": false, "tags": ["user", "viewer"]}
]
```

## Basic Querying

You can query the `users.json` file using the `sonq` command. For example, to get all users from "New York", you can run:

```bash
sonq -f '{"city": "New York"}' users.json
```

This will output:

```json
[  
  {"name": "John Doe", "age": 30, "city": "New York", "is_active": true, "tags": ["user", "admin"]},
  {"name": "Peter Jones", "age": 42, "city": "New York", "is_active": false, "tags": ["user", "editor"]}
]
```

## Using Operators

You can use operators to create more complex queries. For example, to find all users who are 30 years old or older, you can use the `$gte` operator:

```bash
sonq -f '{"age": {"$gte": 30}}' users.json
```

This will output:

```json
[
  {"name": "John Doe", "age": 30, "city": "New York", "is_active": true, "tags": ["user", "admin"]},
  {"name": "Peter Jones", "age": 42, "city": "New York", "is_active": false, "tags": ["user", "editor"]},
  {"name": "David Williams", "age": 35, "city": "London", "is_active": false, "tags": ["user", "viewer"]}
]
```

## Combining Filters

You can combine multiple filters using the `$and` operator. For example, to find all active users in London:

```bash
sonq -f '{"$and": [{"is_active": true}, {"city": "London"}]}' users.json
```

This will output:

```json
[
  {"name": "Jane Smith", "age": 25, "city": "London", "is_active": true, "tags": ["user"]}
]
```

## Outputting to a File

You can save the output to a file using the `-o` option:

```bash
sonq -f '{"age": {"$gte": 30}}' users.json -o older_users.json
```

This will create a file named `older_users.json` with the query results.
