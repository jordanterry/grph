---
sidebar_position: 17
title: gfx subgraph
---

# gfx subgraph

Extract a subgraph containing only specified nodes.

## Synopsis

```bash
gfx subgraph <file> --nodes <id1,id2,...> [--output FILE] [--json]
```

## Description

The `subgraph` command extracts a subgraph containing only the specified nodes and all edges between them. This is useful for focusing on a specific set of nodes.

## Arguments

| Argument | Description |
|----------|-------------|
| `file` | Path to the GEXF file (required) |

## Options

| Option | Description |
|--------|-------------|
| `--nodes` | Comma-separated list of node IDs to include (required) |
| `--output` | Save subgraph to a file (GEXF format) |
| `--json` | Output summary as JSON |
| `--help` | Show help message |

## Examples

### Basic Usage

```bash
gfx subgraph network.gexf --nodes server1,server2,db1
```

Output:
```
Subgraph with nodes: server1, server2, db1

           Graph Summary
+------------------+------------------------+
| Property         | Value                  |
+------------------+------------------------+
| Node Count       | 3                      |
| Edge Count       | 2                      |
+------------------+------------------------+
```

### Save to File

```bash
gfx subgraph network.gexf --nodes lb1,server1,server2,db1 --output core-path.gexf
```

### JSON Output

```bash
gfx subgraph network.gexf --nodes server1,server2 --json
```

## Use Cases

### Extract Specific Components

Create a subgraph with only certain components:

```bash
gfx subgraph dagger-graph.gexf --nodes ViewModel1,ViewModel2,SharedRepo --output viewmodels.gexf
```

### Create Test Fixture

Extract a small subset for testing:

```bash
gfx subgraph production-graph.gexf --nodes nodeA,nodeB,nodeC --output test-fixture.gexf
```

### Focus Analysis

Analyze relationships between specific nodes:

```bash
gfx subgraph network.gexf --nodes critical1,critical2,critical3 --json
gfx edges network.gexf | grep -E "critical1|critical2|critical3"
```
