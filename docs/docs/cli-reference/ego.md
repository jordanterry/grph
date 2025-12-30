---
sidebar_position: 16
title: gfx ego
---

# gfx ego

Extract the ego graph (neighborhood) around a node.

## Synopsis

```bash
gfx ego <file> <node_id> [--radius N] [--output FILE] [--json]
```

## Description

The `ego` command extracts a subgraph containing a center node and all nodes within a specified radius. This is useful for focusing on the local neighborhood of a specific node.

For directed graphs, the ego graph follows outgoing edges.

## Arguments

| Argument | Description |
|----------|-------------|
| `file` | Path to the GEXF file (required) |
| `node_id` | ID of the center node (required) |

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--radius` | `1` | Number of hops to include |
| `--output` | | Save subgraph to a file (GEXF format) |
| `--json` | | Output summary as JSON |
| `--help` | | Show help message |

## Examples

### Basic Usage

```bash
gfx ego network.gexf server1
```

Output:
```
Ego graph for server1 (radius=1)

           Graph Summary
+------------------+------------------------+
| Property         | Value                  |
+------------------+------------------------+
| Node Count       | 4                      |
| Edge Count       | 3                      |
+------------------+------------------------+
```

### Larger Radius

```bash
gfx ego network.gexf lb1 --radius 2
```

### Save to File

```bash
gfx ego network.gexf server1 --output server1-neighborhood.gexf
```

Creates a new GEXF file containing only the ego subgraph, which can be:
- Opened in Gephi for visualization
- Further analyzed with other gfx commands

## Use Cases

### Focus on a Component

Extract and analyze a specific component's dependencies:

```bash
gfx ego dagger-graph.gexf MyViewModel --radius 2 --output viewmodel-deps.gexf
gfx stats viewmodel-deps.gexf
```

### Create Visualization Subset

Extract a manageable subset for visualization:

```bash
gfx ego large-graph.gexf important-node --radius 3 --output subset.gexf
# Open subset.gexf in Gephi
```

### Local Analysis

Analyze the local structure around a node:

```bash
gfx ego network.gexf hub --radius 2 --json
```
