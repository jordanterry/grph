---
sidebar_position: 10
title: gfx reachable
---

# gfx reachable

Find all nodes reachable from a given node.

## Synopsis

```bash
gfx reachable <file> <node_id> [--direction forward|backward|both] [--max-depth N] [--json]
```

## Description

The `reachable` command finds all nodes that can be reached from a starting node. For directed graphs, you can search forward (descendants), backward (ancestors), or both.

## Arguments

| Argument | Description |
|----------|-------------|
| `file` | Path to the GEXF file (required) |
| `node_id` | ID of the starting node (required) |

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--direction` | `forward` | Direction: `forward` (descendants), `backward` (ancestors), `both` |
| `--max-depth` | unlimited | Maximum traversal depth |
| `--json` | | Output as JSON |
| `--help` | | Show help message |

## Examples

### Forward Reachability (Descendants)

Find all nodes reachable from a starting point:

```bash
gfx reachable network.gexf lb1
```

### Backward Reachability (Ancestors)

Find all nodes that can reach a target:

```bash
gfx reachable network.gexf db1 --direction backward
```

### Both Directions

Find the entire connected component:

```bash
gfx reachable network.gexf server1 --direction both
```

### Depth-Limited Search

Find nodes within 2 hops:

```bash
gfx reachable network.gexf lb1 --max-depth 2
```

## Use Cases

### Impact Analysis

Find all components affected by a change:

```bash
gfx reachable dagger-graph.gexf SharedRepository --direction backward
# Shows everything that depends on SharedRepository
```

### Dependency Tree

Find all dependencies of a component:

```bash
gfx reachable dagger-graph.gexf MainActivity --direction forward
# Shows everything MainActivity depends on
```

### Transitive Closure

Find all transitively connected nodes:

```bash
gfx reachable network.gexf central-node --direction both
```
