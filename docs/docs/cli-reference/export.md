---
sidebar_position: 18
title: gfx export
---

# gfx export

Export the graph to different formats.

## Synopsis

```bash
gfx export <file> [--format json|graphml|adjlist|edgelist] [--output FILE]
```

## Description

The `export` command converts a GEXF graph to other common graph formats. This enables interoperability with other graph tools and libraries.

## Arguments

| Argument | Description |
|----------|-------------|
| `file` | Path to the GEXF file (required) |

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `--format` | `json` | Output format: `json`, `graphml`, `adjlist`, `edgelist` |
| `--output` | stdout | Output file path |
| `--help` | | Show help message |

## Formats

### JSON (Node-Link Format)

Standard JSON format compatible with D3.js and other visualization libraries.

```bash
gfx export network.gexf --format json
```

```json
{
  "directed": true,
  "multigraph": false,
  "graph": {},
  "nodes": [
    {"id": "node1", "label": "Node 1", ...}
  ],
  "links": [
    {"source": "node1", "target": "node2", ...}
  ]
}
```

### GraphML

XML-based format widely supported by graph tools.

```bash
gfx export network.gexf --format graphml --output network.graphml
```

### Adjacency List

Simple text format showing each node and its neighbors.

```bash
gfx export network.gexf --format adjlist
```

```
node1 node2 node3 node4
node2 node3
node3
node4 node1
```

### Edge List

Simple text format listing all edges.

```bash
gfx export network.gexf --format edgelist
```

```
node1 node2 1.0
node1 node3 2.0
node2 node3 0.5
```

## Examples

### Export to JSON File

```bash
gfx export network.gexf --format json --output network.json
```

### Export to GraphML for Gephi

```bash
gfx export network.gexf --format graphml --output network.graphml
```

### Pipe to Other Tools

```bash
gfx export network.gexf --format edgelist | wc -l  # Count edges
```

## Use Cases

### Visualization with D3.js

```bash
gfx export network.gexf --format json --output graph.json
# Use graph.json with D3.js force-directed layout
```

### Analysis in NetworkX

```bash
gfx export network.gexf --format json --output graph.json
# Load in Python: nx.node_link_graph(json.load(open('graph.json')))
```

### Import into Other Tools

```bash
gfx export network.gexf --format graphml --output graph.graphml
# Import into Gephi, Cytoscape, yEd, etc.
```
