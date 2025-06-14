from mcp.server.fastmcp import FastMCP
from typing import List


# Create an MCP server
mcp = FastMCP(
    name="Calculator",
    host="127.0.0.1",  # only used for SSE transport (localhost)
    port=8050,  # only used for SSE transport (set this to any port)
)


# Add a simple calculator tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    return a - b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

@mcp.tool()
def divide(a: int, b: int) -> int:
    """Divide two numbers"""
    return a / b


@mcp.tool()
def power(a: int, b: int) -> int:
    """Raise a number to a power"""
    return a ** b


@mcp.tool()
def square_root(a: int) -> int:
    """Calculate the square root of a number"""
    return a ** 0.5


@mcp.tool()
def absolute_value(a: int) -> int:
    """Calculate the absolute value of a number"""
    return abs(a)

@mcp.tool()
def factorial(a: int) -> int:
    """Calculate the factorial of a number"""
    if a < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    elif a == 0:
        return 1
    else:
        return a * factorial(a - 1)

@mcp.tool()
def fibonacci(a: int) -> int:
    """Calculate the Fibonacci sequence up to a number"""
    if a < 0:
        raise ValueError("Fibonacci is not defined for negative numbers")
    elif a == 0:
        return 0
    elif a == 1:
        return 1
    else:
        return fibonacci(a - 1) + fibonacci(a - 2)

@mcp.tool()
def fibonacci_sequence(a: int) -> int:
    """Calculate the Fibonacci sequence up to a number"""
    if a < 0:
        raise ValueError("Fibonacci is not defined for negative numbers")
    elif a == 0:
        return 0
    elif a == 1:
        return 1
    else:
        return fibonacci_sequence(a - 1) + fibonacci_sequence(a - 2)


# Run the server
if __name__ == "__main__":
    transport = "sse"
    if transport == "stdio":
        print("Running server with stdio transport")
        mcp.run(transport="stdio")
    elif transport == "sse":
        print("Running server with SSE transport")
        mcp.run(transport="sse")
    else:
        raise ValueError(f"Unknown transport: {transport}")