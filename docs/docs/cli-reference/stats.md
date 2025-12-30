---
sidebar_position: 12
title: gfx stats
---

# gfx stats

Display comprehensive graph statistics.

## Synopsis

```bash
gfx stats <file> [--json]
```

## Description

The `stats` command provides detailed statistical analysis of the graph, including:

- **Node and Edge Counts**: Basic size metrics
- **Density**: How connected the graph is (ratio of actual edges to possible edges)
- **Average Degree**: Mean number of connections per node
- **Clustering Coefficient**: Measure of how nodes cluster together
- **Connectivity**: Whether all nodes can reach each other
- **Components**: Number of disconnected subgraphs
- **Cycles**: Whether the graph contains cycles
- **Diameter/Radius**: Longest/shortest path metrics (for connected graphs)
- **Average Path Length**: Mean distance between node pairs

## Arguments

| Argument | Description |
|----------|-------------|
| `file` | Path to the GEXF file (required) |

## Options

| Option | Description |
|--------|-------------|
| `--json` | Output as JSON instead of a table |
| `--help` | Show help message |

## Examples

### Basic Usage

```bash
gfx stats network.gexf
```

Output:
```
           Graph Statistics
+--------------------------+--------+
| Metric                   | Value  |
+--------------------------+--------+
| Node Count               | 150    |
| Edge Count               | 420    |
| Directed                 | Yes    |
| Density                  | 0.0188 |
| Average Degree           | 5.60   |
| Avg Clustering Coefficient| 0.3214 |
| Connected                | Yes    |
| Number of Components     | 1      |
| Has Cycles               | No     |
| Diameter                 | 8      |
| Radius                   | 4      |
| Avg Path Length          | 3.2456 |
+--------------------------+--------+
```

### JSON Output

```bash
gfx stats network.gexf --json
```

```json
{
  "node_count": 150,
  "edge_count": 420,
  "density": 0.0188,
  "is_directed": true,
  "is_connected": true,
  "num_components": 1,
  "avg_degree": 5.6,
  "avg_clustering": 0.3214,
  "has_cycles": false,
  "diameter": 8,
  "radius": 4,
  "avg_path_length": 3.2456
}
```

## Metrics Explained

### Density

The ratio of actual edges to the maximum possible edges. A density of 1.0 means every node is connected to every other node.

### Clustering Coefficient

Measures how likely neighbors of a node are to also be connected to each other. High clustering indicates tight-knit communities.

### Diameter

The longest shortest path in the graph. Indicates the maximum "degrees of separation" between any two nodes.

### Average Path Length

The average number of steps needed to get from one node to another. Lower values indicate a more navigable graph.

## Use Cases

### Graph Quality Assessment

Check if a dependency graph is well-structured:

```bash
gfx stats dagger-graph.gexf
# Check for cycles in dependency injection graph
```

### Network Analysis

Analyze network topology:

```bash
gfx stats network.gexf --json | jq '.density'
```
