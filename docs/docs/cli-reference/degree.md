---
sidebar_position: 15
title: gfx degree
---

# gfx degree

Show node degree information.

## Synopsis

```bash
gfx degree <file> [--node NODE_ID] [--top N] [--json]
```

## Description

The `degree` command shows degree information for nodes. For directed graphs, it displays in-degree (incoming edges), out-degree (outgoing edges), and total degree.

## Arguments

| Argument | Description |
|----------|-------------|
| `file` | Path to the GEXF file (required) |

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--node` | | Show degree for a specific node |
| `--top` | `10` | Number of top nodes to display |
| `--json` | | Output as JSON |
| `--help` | | Show help message |

## Examples

### Top Nodes by Degree

```bash
gfx degree network.gexf
```

Output for directed graph:
```
     Node Degrees (Top 10)
+------+---------+----+-----+-------+
| Rank | Node    | In | Out | Total |
+------+---------+----+-----+-------+
| 1    | hub1    | 5  | 8   | 13    |
| 2    | server1 | 3  | 4   | 7     |
| 3    | db1     | 4  | 0   | 4     |
+------+---------+----+-----+-------+
```

### Specific Node

```bash
gfx degree network.gexf --node server1
```

Output:
```
        Node Degree
+-------------+-------+
| Property    | Value |
+-------------+-------+
| Node        | server1|
| In-Degree   | 3     |
| Out-Degree  | 4     |
| Total Degree| 7     |
+-------------+-------+
```

### More Results

```bash
gfx degree network.gexf --top 25
```

### JSON Output

```bash
gfx degree network.gexf --json
```

## Use Cases

### Find Hub Nodes

Identify highly connected nodes:

```bash
gfx degree network.gexf --top 5
```

### Find Leaf Nodes

Nodes with low degree are often endpoints:

```bash
gfx degree network.gexf --json | jq '.degrees | map(select(.total_degree == 1))'
```

### Dependency Analysis

Find components with many dependencies:

```bash
gfx degree dagger-graph.gexf --top 10
# High out-degree = many dependencies
# High in-degree = many dependents
```
