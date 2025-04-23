# HackerMCP

HackerMCP is a module built for AI assistants to access and utilize common penetration testing and security tools. This module enables AI systems to leverage powerful security tools through a simple interface.

## Currently Supported Tools

- **Nmap**: Network discovery and security auditing
- **Metasploit Framework**: Penetration testing framework

## Future Goals

- Add support for SQLMap
- Expand available security tools and capabilities

## Installation

Add the following configuration to your MCP configuration file:

```json
{
    "mcpServers": {
        "hackermcp": {
            "command": "uv",
            "args": [
                "--directory",
                "~/dir/to/hackermcp",
                "run",
                "hacker.py"
            ]
        }
    }
}
```

Replace `~/dir/to/hackermcp` with the actual path to the hackermcp directory.

## Environment Setup

### Prerequisites
- Python 3.8 or higher
- Nmap installed on your system
- Metasploit Framework installed on your system

### Virtual Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/R3verseIN/HackerMCP
   cd HackerMCP
   ```

2. Set up a virtual environment using `uv`:
   ```bash
   uv venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

### Installing UV

If you don't have the `uv` package manager then install it:

```bash
pip3 install uv
```

Or use curl to download the installation script:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

If your system doesn't have curl, you can use wget:

```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

## Disclaimer

**This tool is provided for educational and legitimate security testing purposes only.**

No warranty is provided with this software. The creator is not responsible for any unethical or illegal use of this tool. Users are solely responsible for ensuring they have proper authorization before conducting any security testing activities.

## License
[GNU GPL v3 License](LICENSE)
