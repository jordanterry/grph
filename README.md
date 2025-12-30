# grph

> Like grep, but for graphs.

A powerful CLI tool for exploring, analyzing, and querying graph files from the command line. Built for developers, data scientists, and anyone who works with graph data.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **Graph Traversal**: Find neighbors, paths, and reachable nodes
- **Graph Analysis**: Calculate centrality, find components, get statistics
- **Subgraph Extraction**: Create ego graphs and filtered subgraphs
- **Multiple Export Formats**: JSON, GraphML, adjacency list, edge list
- **Rich Output**: Beautiful tables with optional JSON output for scripting
- **Fast**: Built on NetworkX with scipy for advanced algorithms

## Installation

### Via pip

```bash
pip install grph-cli
```

### Via Homebrew (macOS)

```bash
brew install jordanterry/grph/grph-cli
```

Or manually:

```bash
brew tap jordanterry/grph https://github.com/jordanterry/grph
brew install grph-cli
```

### From source

```bash
git clone https://github.com/jordanterry/grph.git
cd grph
pip install -e .
```

## Quick Start

```bash
# Get graph info
grph info graph.gexf

# List all nodes
grph nodes graph.gexf

# Find neighbors of a node
grph neighbors graph.gexf server1

# Find shortest path between nodes
grph path graph.gexf nodeA nodeB

# Calculate PageRank centrality
grph centrality graph.gexf --type pagerank

# Get comprehensive statistics
grph stats graph.gexf

# Export to JSON
grph export graph.gexf --format json --output graph.json
```

## Commands

### Basic Commands

| Command | Description |
|---------|-------------|
| `grph info` | Display graph summary (counts, attributes) |
| `grph meta` | Display GEXF metadata |
| `grph nodes` | List and filter nodes |
| `grph edges` | List and filter edges |

### Graph Traversal

| Command | Description |
|---------|-------------|
| `grph neighbors` | Find neighbors of a node (with depth and direction) |
| `grph path` | Find shortest path between two nodes |
| `grph all-paths` | Find all simple paths between nodes |
| `grph has-path` | Check if path exists between nodes |
| `grph reachable` | Find all nodes reachable from a node |
| `grph common-neighbors` | Find shared neighbors between two nodes |

### Graph Analysis

| Command | Description |
|---------|-------------|
| `grph stats` | Comprehensive statistics (density, clustering, cycles) |
| `grph centrality` | Calculate centrality (degree, betweenness, PageRank, etc.) |
| `grph components` | Analyze connected components |
| `grph degree` | Show node degree information |

### Subgraph Operations

| Command | Description |
|---------|-------------|
| `grph ego` | Extract neighborhood around a node |
| `grph subgraph` | Extract subgraph with specific nodes |

### Export

| Command | Description |
|---------|-------------|
| `grph export` | Export to JSON, GraphML, adjacency list, or edge list |

## Examples

### Dependency Analysis

```bash
# Find what a module depends on
grph neighbors dagger-graph.gexf MyViewModel --direction out

# Find what depends on a module
grph neighbors dagger-graph.gexf SharedRepository --direction in

# Find the dependency chain between two modules
grph path dagger-graph.gexf MainActivity DatabaseHelper

# Find circular dependencies (strongly connected components > 1)
grph components dagger-graph.gexf --type strongly --list
```

### Network Analysis

```bash
# Find the most connected nodes (hubs)
grph centrality network.gexf --type degree --top 10

# Find bridge nodes (high betweenness)
grph centrality network.gexf --type betweenness --top 10

# Check if network is fully connected
grph stats network.gexf | grep "Connected"

# Find all routes between two endpoints
grph all-paths network.gexf client server --max-depth 5
```

### Data Export

```bash
# Export for D3.js visualization
grph export graph.gexf --format json --output graph.json

# Export for Gephi or other tools
grph export graph.gexf --format graphml --output graph.graphml

# Extract a subgraph for focused analysis
grph ego graph.gexf important-node --radius 2 --output focused.gexf
```

### Scripting

```bash
# Get node count as JSON
grph info graph.gexf --json | jq '.node_count'

# Check if path exists (for CI/CD)
if grph has-path graph.gexf nodeA nodeB 2>&1 | grep -q "Yes"; then
  echo "Connected"
fi

# Find all nodes of a type
grph nodes graph.gexf --attr type=server --json | jq '.[].id'
```

## Supported Formats

### Input
- **GEXF** (Graph Exchange XML Format) - versions 1.1, 1.2, 1.3

### Export
- **JSON** - Node-link format (D3.js compatible)
- **GraphML** - XML format for graph tools
- **Adjacency List** - Simple text format
- **Edge List** - Source-target pairs

## JSON Output

All commands support `--json` for machine-readable output:

```bash
grph nodes graph.gexf --json
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

## Requirements

- Python 3.10+
- NetworkX 3.0+
- Click 8.0+
- Rich 13.0+
- SciPy 1.11+

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Built on [NetworkX](https://networkx.org/) for graph algorithms
- Uses [Rich](https://rich.readthedocs.io/) for beautiful terminal output
- CLI powered by [Click](https://click.palletsprojects.com/)
