---
sidebar_position: 8
title: gfx all-paths
---

# gfx all-paths

Find all simple paths between two nodes.

## Synopsis

```bash
gfx all-paths <file> <source> <target> [--max-depth N] [--json]
```

## Description

The `all-paths` command finds all simple paths (paths without repeated nodes) between two nodes. This is useful for understanding all possible routes or dependency chains between components.

**Warning**: The number of paths can grow exponentially in dense graphs. Use `--max-depth` to limit the search.

## Arguments

| Argument | Description |
|----------|-------------|
| `file` | Path to the GEXF file (required) |
| `source` | ID of the starting node (required) |
| `target` | ID of the destination node (required) |

## Options

| Option | Description |
|--------|-------------|
| `--max-depth` | Maximum path length to search |
| `--json` | Output as JSON |
| `--help` | Show help message |

## Examples

### Basic Usage

```bash
gfx all-paths network.gexf lb1 db1
```

Output:
```
Found 2 path(s)

Path 1 (length 2):
  lb1 -> server1 -> db1
Path 2 (length 2):
  lb1 -> server2 -> db1
```

### With Depth Limit

```bash
gfx all-paths network.gexf nodeA nodeZ --max-depth 4
```

### JSON Output

```bash
gfx all-paths network.gexf lb1 db1 --json
```

```json
[
  {
    "source": "lb1",
    "target": "db1",
    "path": ["lb1", "server1", "db1"],
    "length": 2
  },
  {
    "source": "lb1",
    "target": "db1",
    "path": ["lb1", "server2", "db1"],
    "length": 2
  }
]
```

## Use Cases

### Redundancy Analysis

Find all routes between critical components:

```bash
gfx all-paths network.gexf gateway database
```

### Dependency Path Analysis

Find all dependency chains:

```bash
gfx all-paths dagger-graph.gexf MainActivity Repository --max-depth 5
```
