# Command-Line Interface

`sonq` can be used from the command line to query and transform data in JSON and BSON formats.

## Basic Usage

The basic syntax is:

```bash
sonq [options] <input-file>
```

This will read the specified input file, apply any specified filters or transformations, and print the results to standard output in JSON format.

## Options

### `-f <filter>` or `--filter <filter>`

Apply a MongoDB-like query filter to the input data. The filter should be a JSON string.

**Example:**

```bash
sonq -f '{"name": "John"}' data.json
```

### `-o <output-file>` or `--output <output-file>`

Write the output to a specified file. If this option is not provided, the output is written to standard output.

**Example:**

```bash
sonq -o output.json data.json
```

### `--output-format <format>`

Specify the output format. Supported formats are `json`, `jsonl`, and `bson`.

**Example:**

```bash
sonq --output-format jsonl data.json
```

### `--input-format <format>`

Specify the input format. Supported formats are `json`, `jsonl`, and `bson`.

**Example:**

```bash
sonq --input-format bson data.bson
```

### `-n <number>`

Limit the number of entries in the output.

**Example:**

```bash
sonq -n 10 data.json
```

### JSON Output Options

These options control the formatting of JSON output:

- `--json-indent <indent>`: Indent the output JSON. Can be an integer or a string.
- `--json-ensure-ascii`: (Default: true) Ensure that all output characters are ASCII.
- `--json-skipkeys`: (Default: false) Skip keys that are not of a basic type.
- `--json-allow-nan`: (Default: true) Allow NaN, Infinity, and -Infinity.
- `--json-sort-keys`: (Default: false) Sort the keys in the output.

**Example:**

```bash
sonq --json-indent 4 --json-sort-keys data.json
```

## Example: Querying a MongoDB Dump

If you have a BSON file from a `mongodump`, you can query it directly. For example, to find all documents in `dump.bson` where the field `is_active` is `true` and output them to a JSON file, you would run:

```bash
sonq --input-format bson -f '{"is_active": true}' dump.bson -o active_users.json
```
