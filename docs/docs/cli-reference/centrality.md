---
sidebar_position: 13
title: gfx centrality
---

# gfx centrality

Calculate centrality metrics for nodes.

## Synopsis

```bash
gfx centrality <file> [--type degree|betweenness|closeness|pagerank|eigenvector] [--top N] [--json]
```

## Description

The `centrality` command calculates various centrality metrics to identify the most important or influential nodes in the graph. Different centrality measures capture different aspects of node importance.

## Arguments

| Argument | Description |
|----------|-------------|
| `file` | Path to the GEXF file (required) |

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--type` | `degree` | Type of centrality: `degree`, `betweenness`, `closeness`, `pagerank`, `eigenvector` |
| `--top` | `10` | Number of top nodes to display |
| `--json` | | Output as JSON (includes all nodes) |
| `--help` | | Show help message |

## Centrality Types

### Degree Centrality

The simplest measure: how many connections a node has. Nodes with high degree centrality are "hubs" with many direct connections.

```bash
gfx centrality network.gexf --type degree
```

### Betweenness Centrality

Measures how often a node lies on the shortest path between other nodes. High betweenness nodes are "bridges" that control information flow.

```bash
gfx centrality network.gexf --type betweenness
```

### Closeness Centrality

Measures how close a node is to all other nodes. High closeness nodes can quickly reach or spread information to the entire network.

```bash
gfx centrality network.gexf --type closeness
```

### PageRank

Google's famous algorithm. Nodes are important if they are linked to by other important nodes. Good for finding authoritative nodes.

```bash
gfx centrality network.gexf --type pagerank
```

### Eigenvector Centrality

Similar to PageRank but for undirected graphs. A node is important if it's connected to other important nodes.

```bash
gfx centrality network.gexf --type eigenvector
```

## Examples

### Basic Usage

```bash
gfx centrality network.gexf
```

Output:
```
     Degree Centrality (Top 10)
+------+----------+----------+
| Rank | Node     | Score    |
+------+----------+----------+
| 1    | hub1     | 0.450000 |
| 2    | server1  | 0.350000 |
| 3    | server2  | 0.300000 |
+------+----------+----------+
```

### PageRank Analysis

```bash
gfx centrality dagger-graph.gexf --type pagerank --top 20
```

### JSON Output

```bash
gfx centrality network.gexf --type betweenness --json
```

```json
{
  "type": "betweenness",
  "scores": {
    "hub1": 0.523456,
    "server1": 0.234567,
    "..."
  }
}
```

## Use Cases

### Find Critical Dependencies

Use betweenness centrality to find components that many others depend on:

```bash
gfx centrality dagger-graph.gexf --type betweenness --top 5
```

### Identify Hub Components

Use degree centrality to find highly connected components:

```bash
gfx centrality dagger-graph.gexf --type degree
```

### Find Authoritative Sources

Use PageRank to find the most referenced nodes:

```bash
gfx centrality citation-graph.gexf --type pagerank
```
