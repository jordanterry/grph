---
sidebar_position: 7
title: gfx path
---

# gfx path

Find the shortest path between two nodes.

## Synopsis

```bash
gfx path <file> <source> <target> [--weighted] [--json]
```

## Description

The `path` command finds the shortest path between two nodes in the graph. It uses Dijkstra's algorithm (or BFS for unweighted paths) to find the optimal route.

If no path exists between the nodes, the command will indicate this.

## Arguments

| Argument | Description |
|----------|-------------|
| `file` | Path to the GEXF file (required) |
| `source` | ID of the starting node (required) |
| `target` | ID of the destination node (required) |

## Options

| Option | Description |
|--------|-------------|
| `--weighted` | Use edge weights for path calculation |
| `--json` | Output as JSON instead of formatted text |
| `--help` | Show help message |

## Examples

### Basic Usage

Find the shortest path between two nodes:

```bash
gfx path network.gexf lb1 db1
```

Output:
```
Path from lb1 to db1
Length: 2 edges

Path: lb1 -> server1 -> db1
```

### Weighted Path

Find the shortest path considering edge weights:

```bash
gfx path network.gexf lb1 db1 --weighted
```

Output:
```
Path from lb1 to db1
Length: 2 edges
Total Weight: 3.0

Path: lb1 -> server1 -> db1
```

### JSON Output

```bash
gfx path network.gexf lb1 db1 --json
```

```json
{
  "source": "lb1",
  "target": "db1",
  "path": ["lb1", "server1", "db1"],
  "length": 2,
  "total_weight": null
}
```

## Use Cases

### Dependency Chain Analysis

Find how two components are connected:

```bash
gfx path dagger-graph.gexf MainActivity SharedRepository
```

### Network Routing

Find the route between two network nodes:

```bash
gfx path network.gexf client1 server5 --weighted
```
