---
sidebar_position: 6
title: gfx neighbors
---

# gfx neighbors

Find neighbors of a node in the graph.

## Synopsis

```bash
gfx neighbors <file> <node_id> [--direction in|out|all] [--depth N] [--json]
```

## Description

The `neighbors` command finds nodes that are directly connected to a specified node. For directed graphs, you can control whether to find predecessors (incoming edges), successors (outgoing edges), or both.

Use the `--depth` option to find multi-hop neighbors (nodes within N edges of the target).

## Arguments

| Argument | Description |
|----------|-------------|
| `file` | Path to the GEXF file (required) |
| `node_id` | ID of the node to find neighbors for (required) |

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--direction` | `all` | Direction for directed graphs: `in` (predecessors), `out` (successors), or `all` (both) |
| `--depth` | `1` | Number of hops to traverse |
| `--json` | | Output as JSON instead of a table |
| `--help` | | Show help message |

## Examples

### Basic Usage

Find all direct neighbors of a node:

```bash
gfx neighbors network.gexf server1
```

### Direction Control

Find only incoming neighbors (predecessors):

```bash
gfx neighbors network.gexf db1 --direction in
```

Find only outgoing neighbors (successors):

```bash
gfx neighbors network.gexf lb1 --direction out
```

### Multi-Hop Neighbors

Find all nodes within 2 hops:

```bash
gfx neighbors network.gexf lb1 --depth 2
```

### JSON Output

```bash
gfx neighbors network.gexf server1 --json
```

## Use Cases

### Dependency Analysis

Find what a component depends on:

```bash
gfx neighbors dagger-graph.gexf MyViewModel --direction out
```

### Impact Analysis

Find what depends on a component:

```bash
gfx neighbors dagger-graph.gexf SharedRepository --direction in
```

### Neighborhood Exploration

Explore the local structure around a node:

```bash
gfx neighbors network.gexf central-node --depth 3
```
