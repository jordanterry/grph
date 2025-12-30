---
sidebar_position: 14
title: gfx components
---

# gfx components

Analyze connected components in the graph.

## Synopsis

```bash
gfx components <file> [--type connected|strongly|weakly] [--list] [--json]
```

## Description

The `components` command analyzes the connected components of a graph. A connected component is a maximal set of nodes where every node can reach every other node.

For directed graphs, there are two types of connectivity:
- **Weakly connected**: Ignoring edge direction, can you reach all nodes?
- **Strongly connected**: Following edge direction, can you reach all nodes and return?

## Arguments

| Argument | Description |
|----------|-------------|
| `file` | Path to the GEXF file (required) |

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--type` | `connected` | Type of components: `connected`, `strongly`, `weakly` |
| `--list` | | Show component members |
| `--json` | | Output as JSON |
| `--help` | | Show help message |

## Examples

### Basic Usage

```bash
gfx components network.gexf
```

Output:
```
Number of Components: 3
Largest Component Size: 145

           Components
+-----------+------+
| Component | Size |
+-----------+------+
| 1         | 145  |
| 2         | 4    |
| 3         | 1    |
+-----------+------+
```

### Show Component Members

```bash
gfx components network.gexf --list
```

Output:
```
           Components
+-----------+------+-----------------------------+
| Component | Size | Members                     |
+-----------+------+-----------------------------+
| 1         | 145  | node1, node2, ... (+135)    |
| 2         | 4    | orphan1, orphan2, orphan3   |
| 3         | 1    | isolated1                   |
+-----------+------+-----------------------------+
```

### Strongly Connected Components

For directed graphs, find strongly connected components:

```bash
gfx components dagger-graph.gexf --type strongly
```

### JSON Output

```bash
gfx components network.gexf --json
```

```json
{
  "num_components": 3,
  "component_sizes": [145, 4, 1],
  "largest_component_size": 145,
  "components": [
    ["node1", "node2", "..."],
    ["orphan1", "orphan2", "orphan3", "orphan4"],
    ["isolated1"]
  ]
}
```

## Use Cases

### Find Isolated Nodes

Identify nodes that aren't connected to the main graph:

```bash
gfx components network.gexf --list | grep "Size: 1"
```

### Detect Circular Dependencies

Strongly connected components in a dependency graph indicate circular dependencies:

```bash
gfx components dagger-graph.gexf --type strongly --list
# Any component with size > 1 has circular dependencies
```

### Validate Graph Connectivity

Check if the graph is fully connected:

```bash
gfx components network.gexf --json | jq '.num_components == 1'
```
