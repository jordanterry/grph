---
sidebar_position: 11
title: gfx common-neighbors
---

# gfx common-neighbors

Find nodes that are neighbors of both given nodes.

## Synopsis

```bash
gfx common-neighbors <file> <node1> <node2> [--json]
```

## Description

The `common-neighbors` command finds nodes that are connected to both specified nodes. For directed graphs, this considers both incoming and outgoing edges.

## Arguments

| Argument | Description |
|----------|-------------|
| `file` | Path to the GEXF file (required) |
| `node1` | ID of the first node (required) |
| `node2` | ID of the second node (required) |

## Options

| Option | Description |
|--------|-------------|
| `--json` | Output as JSON |
| `--help` | Show help message |

## Examples

### Basic Usage

```bash
gfx common-neighbors network.gexf server1 server2
```

Output:
```
Common neighbors of server1 and server2

                     Nodes (3)
+---------+------------------+---------------------------+
| ID      | Label            | Attributes                |
+---------+------------------+---------------------------+
| lb1     | Load Balancer    | type=loadbalancer         |
| db1     | Database Primary | type=database             |
| cache1  | Redis Cache      | type=cache                |
+---------+------------------+---------------------------+
```

### JSON Output

```bash
gfx common-neighbors network.gexf server1 server2 --json
```

## Use Cases

### Find Shared Dependencies

Find libraries used by both modules:

```bash
gfx common-neighbors dagger-graph.gexf FeatureA FeatureB
```

### Network Bridge Detection

Find nodes connecting two parts of the network:

```bash
gfx common-neighbors network.gexf subnetA subnetB
```

### Similarity Analysis

Nodes with many common neighbors are often similar:

```bash
gfx common-neighbors social-graph.gexf user1 user2 --json | jq 'length'
```
