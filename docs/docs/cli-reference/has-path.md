---
sidebar_position: 9
title: gfx has-path
---

# gfx has-path

Check if a path exists between two nodes.

## Synopsis

```bash
gfx has-path <file> <source> <target>
```

## Description

The `has-path` command quickly checks whether any path exists between two nodes. This is faster than `gfx path` when you only need to know if connectivity exists.

## Arguments

| Argument | Description |
|----------|-------------|
| `file` | Path to the GEXF file (required) |
| `source` | ID of the starting node (required) |
| `target` | ID of the destination node (required) |

## Examples

### Basic Usage

```bash
gfx has-path network.gexf lb1 db1
```

Output (if path exists):
```
Yes - a path exists from lb1 to db1
```

Output (if no path):
```
No - no path exists from lb1 to db1
```

## Use Cases

### Connectivity Check

Verify two components can communicate:

```bash
gfx has-path network.gexf client server
```

### Dependency Verification

Check if a dependency relationship exists:

```bash
gfx has-path dagger-graph.gexf FeatureModule CoreLibrary
```

### Scripting

Use in scripts for conditional logic:

```bash
if gfx has-path graph.gexf nodeA nodeB 2>&1 | grep -q "Yes"; then
  echo "Connected"
fi
```
