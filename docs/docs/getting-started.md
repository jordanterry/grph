---
sidebar_position: 2
title: Getting Started
---

# Getting Started

This guide will help you install GFX CLI and run your first commands.

## Prerequisites

For pip/pipx installation:
- Python 3.10 or higher
- pip or pipx

For Homebrew installation:
- Homebrew (manages Python automatically)

## Installation

### Homebrew (macOS/Linux)

```bash
brew tap jordanterry/gefx-cli https://github.com/jordanterry/gefx-cli
brew install gfx-cli
```

### From PyPI

```bash
pip install gfx-cli
```

### Using pipx (Isolated Environment)

```bash
pipx install gfx-cli
```

### From Source

```bash
git clone https://github.com/jordanterry/gefx-cli.git
cd gefx-cli
pip install -e .
```

### Verify Installation

```bash
gfx --version
# gfx, version 0.1.0
```

## Your First Commands

### 1. Get Help

```bash
gfx --help
```

This displays all available commands:

```
Usage: gfx [OPTIONS] COMMAND [ARGS]...

  GFX - A CLI tool for interrogating and browsing GEXF graph files.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  edges  List and filter edges in the graph.
  info   Display a summary of the graph.
  meta   Display metadata from a GEXF file.
  nodes  List and filter nodes in the graph.
```

### 2. Inspect a Graph

Use `gfx info` to get a quick overview of your graph:

```bash
gfx info your-graph.gexf
```

Output:
```
                  Graph Summary
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Property          ┃ Value                      ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ File              │ your-graph.gexf            │
│ Version           │ 1.2                        │
│ Mode              │ static                     │
│ Default Edge Type │ directed                   │
│ Node Count        │ 5                          │
│ Edge Count        │ 6                          │
└───────────────────┴────────────────────────────┘

Node Attributes: type, weight
Edge Attributes: relationship
```

### 3. List Nodes

```bash
gfx nodes your-graph.gexf
```

Output:
```
                        Nodes (5)
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID      ┃ Label            ┃ Attributes                    ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ server1 │ Web Server 1     │ type=server, weight=1.5       │
│ server2 │ Web Server 2     │ type=server, weight=2.0       │
│ db1     │ Database Primary │ type=database, weight=3.0     │
│ cache1  │ Redis Cache      │ type=cache, weight=1.0        │
│ lb1     │ Load Balancer    │ type=loadbalancer, weight=0.5 │
└─────────┴──────────────────┴───────────────────────────────┘
```

### 4. Filter Nodes

Find nodes with a specific attribute:

```bash
gfx nodes your-graph.gexf --attr type=server
```

Output:
```
                     Nodes (2)
┏━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ ID      ┃ Label        ┃ Attributes              ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ server1 │ Web Server 1 │ type=server, weight=1.5 │
│ server2 │ Web Server 2 │ type=server, weight=2.0 │
└─────────┴──────────────┴─────────────────────────┘
```

### 5. Get JSON Output

Add `--json` to any command for machine-readable output:

```bash
gfx nodes your-graph.gexf --attr type=server --json
```

```json
[
  {
    "id": "server1",
    "label": "Web Server 1",
    "attributes": {
      "type": "server",
      "weight": 1.5
    }
  },
  {
    "id": "server2",
    "label": "Web Server 2",
    "attributes": {
      "type": "server",
      "weight": 2.0
    }
  }
]
```

## Next Steps

Now that you have GFX CLI installed and running, explore:

- [CLI Reference](./cli-reference/) - Complete documentation for all commands
- [Filtering Examples](./examples/filtering) - Advanced filtering techniques
- [Scripting](./examples/scripting) - Using GFX CLI in scripts and pipelines
