from typing import Any
from mcp.server.fastmcp import FastMCP
import os
import subprocess  # Import the full subprocess module
import asyncio
import requests
import time

# Initialize FastMCP server
mcp = FastMCP("Hackermcp")

@mcp.tool()
def create_memory_for_your_self(what_to_add: str) -> str:
    """Create a memory for yourself.
    Args:
        what_to_add: what to add to the text file to store for your memory
    """
    with open("memory.txt", "a") as f:
        f.write(what_to_add + "\n")
    return f"Created memory for yourself: {what_to_add}"

@mcp.tool()
def read_memory() -> str:
    """Read the memory.
    """
    with open("memory.txt", "r") as f:
        return f.read()
        
# @mcp.tool()
# async def tcpdump(command: str,timeout: int = 10) -> str:
#     """Capture network traffic using tcpdump.
    
#     Args:
#         command: command to run like -i eth0 -w output.pcap and timeout is the time to wait for the command to finish no need to mention tcpdump it is already there
#     """
#     result = subprocess.run(f"sudo tcpdump {command}", shell=True, check=True, capture_output=True, text=True,timeout=timeout)
#     return result.stdout

@mcp.tool()
async def get_public_ip() -> str:
    """Get your public IP address."""
    response = requests.get("https://api.ipify.org?format=json")
    return response.json()["ip"]

@mcp.tool()
async def mylocalip_with_ifconfig() -> str:
    """Get your local IP address with ifconfig."""
    result = subprocess.run("ifconfig", shell=True, check=True, capture_output=True, text=True)
    return result.stdout
    
@mcp.tool()
async def nmapscan(command: str) -> str:
    """Scan network using nmap with command
    
    Args:
        command: nmap command to run like -p as nmap is already there no need to mention nmap
    """
    try:
        result = subprocess.run(f"nmap {command}", shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error executing nmap command: {e}\n{e.stderr}"

@mcp.tool()
async def create_tmux_session(session_name: str = "msf_session") -> str:
    """Create a new tmux session.
    
    Args:
        session_name: Name for the tmux session
    """
    try:
        # Check if session already exists
        check_result = subprocess.run(f"tmux has-session -t {session_name}", 
                                      shell=True, capture_output=True, text=True)
        if check_result.returncode == 0:
            return f"Session '{session_name}' already exists"
        
        # Create new detached session
        result = subprocess.run(f"tmux new-session -d -s {session_name}", 
                                shell=True, check=True, capture_output=True, text=True)
        return f"Created tmux session: {session_name}"
    except subprocess.CalledProcessError as e:
        return f"Error creating tmux session: {e}\n{e.stderr}"

@mcp.tool()
async def list_tmux_sessions() -> str:
    """List all tmux sessions."""
    try:
        result = subprocess.run("tmux list-sessions", 
                              shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            return "No tmux sessions found"
        return f"Error listing tmux sessions: {e}\n{e.stderr}"

@mcp.tool()
async def run_in_tmux(session_name: str, command: str) -> str:
    """Run a command in a tmux session.
    
    Args:
        session_name: Name of the tmux session
        command: Command to run in the session
    """
    try:
        # Check if session exists
        check_result = subprocess.run(f"tmux has-session -t {session_name}", 
                                      shell=True, capture_output=True)
        if check_result.returncode != 0:
            return f"Session '{session_name}' does not exist"
        
        # Send command to session
        result = subprocess.run(f"tmux send-keys -t {session_name} '{command}' C-m", 
                              shell=True, check=True, capture_output=True, text=True)
        return f"Command sent to session '{session_name}': {command}"
    except subprocess.CalledProcessError as e:
        return f"Error sending command to tmux session: {e}\n{e.stderr}"

@mcp.tool()
async def capture_tmux_output(session_name: str, wait_time: int = 2) -> str:
    """Capture the current output of a tmux session.
    
    Args:
        session_name: Name of the tmux session
        wait_time: Time to wait before capturing output (seconds)
    """
    try:
        # Check if session exists
        check_result = subprocess.run(f"tmux has-session -t {session_name}", 
                                      shell=True, capture_output=True)
        if check_result.returncode != 0:
            return f"Session '{session_name}' does not exist"
        
        # Wait for output
        time.sleep(wait_time)
        
        # Capture pane content
        result = subprocess.run(f"tmux capture-pane -p -t {session_name}", 
                              shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error capturing tmux output: {e}\n{e.stderr}"

@mcp.tool()
async def start_msfconsole(session_name: str = "msf_session") -> str:
    """Start msfconsole in a tmux session.
    
    Args:
        session_name: Name of the tmux session to use
    """
    # First ensure the session exists
    create_result = await create_tmux_session(session_name)
    
    # Start msfconsole in the session
    run_result = await run_in_tmux(session_name, "msfconsole")
    
    # Wait for msfconsole to initialize
    time.sleep(5)
    
    # Get initial output
    output = await capture_tmux_output(session_name)
    
    return f"Started msfconsole in session '{session_name}'.\nInitial output:\n{output}"

@mcp.tool()
async def kill_tmux_session(session_name: str) -> str:
    """Kill a tmux session.
    
    Args:
        session_name: Name of the tmux session to kill
    """
    try:
        result = subprocess.run(f"tmux kill-session -t {session_name}", 
                              shell=True, check=True, capture_output=True, text=True)
        return f"Killed tmux session: {session_name}"
    except subprocess.CalledProcessError as e:
        return f"Error killing tmux session: {e}\n{e.stderr}"

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')