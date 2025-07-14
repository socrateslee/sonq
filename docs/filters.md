# Filters

`sonq` uses a MongoDB-like query syntax for filtering data. Filters are specified as a JSON string.

## Comparison Operators

- `$eq`: (Equal) Matches values that are equal to a specified value.
- `$ne`: (Not Equal) Matches all values that are not equal to a specified value.
- `$gt`: (Greater Than) Matches values that are greater than a specified value.
- `$gte`: (Greater Than or Equal) Matches values that are greater than or equal to a specified value.
- `$lt`: (Less Than) Matches values that are less than a specified value.
- `$lte`: (Less Than or Equal) Matches values that are less than or equal to a specified value.
- `$in`: (In) Matches any of the values specified in an array.
- `$nin`: (Not In) Matches none of the values specified in an array.

**Example:**

```bash
sonq -f '{"age": {"$gte": 18}}' users.json
```

## Logical Operators

- `$and`: Joins query clauses with a logical AND.
- `$or`: Joins query clauses with a logical OR.
- `$nor`: Joins query clauses with a logical NOR.
- `$not`: Inverts the effect of a query expression.

**Example:**

```bash
sonq -f '{"$and": [{"age": {"$gte": 18}}, {"city": "New York"}]}' users.json
```

## Element Operators

- `$exists`: Matches documents that have the specified field.

**Example:**

```bash
sonq -f '{"address": {"$exists": true}}' users.json
```
