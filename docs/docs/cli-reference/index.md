---
sidebar_position: 1
title: CLI Reference Overview
---

# CLI Reference

GFX CLI provides comprehensive commands for working with GEXF graph files.

## Commands Overview

### Basic Commands

| Command | Description |
|---------|-------------|
| [`gfx info`](./info) | Display a summary of the graph (counts, attributes) |
| [`gfx meta`](./meta) | Display full metadata from the GEXF file |
| [`gfx nodes`](./nodes) | List and filter nodes in the graph |
| [`gfx edges`](./edges) | List and filter edges in the graph |

### Graph Traversal

| Command | Description |
|---------|-------------|
| [`gfx neighbors`](./neighbors) | Find neighbors of a node |
| [`gfx path`](./path) | Find the shortest path between two nodes |
| [`gfx all-paths`](./all-paths) | Find all simple paths between two nodes |
| [`gfx has-path`](./has-path) | Check if a path exists between two nodes |
| [`gfx reachable`](./reachable) | Find all nodes reachable from a given node |
| [`gfx common-neighbors`](./common-neighbors) | Find nodes that are neighbors of both given nodes |

### Graph Analysis

| Command | Description |
|---------|-------------|
| [`gfx stats`](./stats) | Display comprehensive graph statistics |
| [`gfx centrality`](./centrality) | Calculate centrality metrics for nodes |
| [`gfx components`](./components) | Analyze connected components in the graph |
| [`gfx degree`](./degree) | Show node degree information |

### Subgraph Operations

| Command | Description |
|---------|-------------|
| [`gfx ego`](./ego) | Extract the ego graph (neighborhood) around a node |
| [`gfx subgraph`](./subgraph) | Extract a subgraph containing only specified nodes |

### Export

| Command | Description |
|---------|-------------|
| [`gfx export`](./export) | Export the graph to different formats |

## Global Options

These options are available for all commands:

```bash
gfx --version  # Show version and exit
gfx --help     # Show help message and exit
```

## Common Options

Most commands support these options:

| Option | Description |
|--------|-------------|
| `--json` | Output results as JSON instead of a table |
| `--help` | Show help for the specific command |

## File Argument

All commands require a GEXF file as the first argument:

```bash
gfx <command> <file.gexf> [options]
```

The file must:
- Exist and be readable
- Be a valid GEXF XML file
- Use a supported GEXF version (1.1, 1.2, or 1.3)

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Error (file not found, parse error, etc.) |

## Output Formats

### Table Output (Default)

Commands output rich, formatted tables by default:

```
                     Nodes (2)
┏━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID      ┃ Label        ┃ Attributes              ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ server1 │ Web Server 1 │ type=server, weight=1.5 │
│ server2 │ Web Server 2 │ type=server, weight=2.0 │
└─────────┴──────────────┴─────────────────────────┘
```

### JSON Output

Add `--json` for machine-readable output:

```bash
gfx nodes graph.gexf --json
```

```json
[
  {
    "id": "server1",
    "label": "Web Server 1",
    "attributes": {"type": "server", "weight": 1.5}
  }
]
```

JSON output is useful for:
- Piping to `jq` for further processing
- Integration with other tools
- Scripting and automation
