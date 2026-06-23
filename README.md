# 🎪 CIRCUS - Multi-Model Orchestration System

A **14b "ringmaster"** model directs smaller **"performers"** to complete complex tasks collaboratively.

## How It Works

```
User Request: "Build a web server"
                     ↓
        ┌─────────────────────────┐
        │   CIRCUS RINGMASTER     │
        │      (14b model)        │
        │                         │
        │  "Break this down:      │
        │   1. Write server       │
        │   2. Write tests        │
        │   3. Write README       │
        │   Assign to performers" │
        └─────────────────────────┘
                     ↓
      ┌──────────────┼──────────────┐
      ↓              ↓              ↓
   ┌──────┐      ┌──────┐      ┌──────┐
   │Coder │      │Tester│      │ Docs │
   │ (2b) │      │ (1b) │      │ (1b) │
   └──┬───┘      └──┬───┘      └──┬───┘
      ↓              ↓              ↓
   server.py      tests.py     README.md
      └──────────────┼──────────────┘
                     ↓
           ┌─────────────────┐
           │   SYNTHESIZE    │
           │   RESULTS       │
           └─────────────────┘
                     ↓
              Final Output
```

## Why?

- **Faster** - Small models work in parallel
- **Cheaper** - Use smaller models for sub-tasks
- **Specialized** - Each performer is optimized for their task
- **Scalable** - Add more performers as needed

## Requirements

- **Ollama** running locally (http://localhost:11434)
- Models installed in Ollama

## Quick Start

```python
import asyncio
from circus import Circus

async def main():
    # Create circus with a 14b ringmaster
    circus = Circus("qwen2.5-coder-14b-instruct-abliterated:latest")
    
    # Add performers (small models)
    circus.add_performer("Coder", "qwen2.5:0.5b")
    circus.add_performer("Researcher", "qwen2.5:1.5b")
    
    # Execute a task
    result = await circus.perform("Write a fibonacci function in Python")
    print(result)

asyncio.run(main())
```

## Install Models

```bash
# Ringmaster (14b model)
ollama pull qwen2.5-coder-14b-instruct-abliterated:latest

# Performers (small models)
ollama pull qwen2.5:0.5b
ollama pull qwen2.5:1.5b
ollama pull phi3:3.8b
ollama pull llama3.2:1b
```

## Environment Variables

```env
RINGMASTER_MODEL=qwen2.5-coder-14b-instruct-abliterated:latest
OLLAMA_HOST=http://localhost:11434
```

## API

### Circus Class

```python
circus = Circus(ringmaster_model, ollama_url)
```

**Methods:**
- `add_performer(name, model)` - Add a performer
- `perform(request)` - Execute a task
- `status()` - Get circus status

### Performer Class

```python
performer = Performer(name, model, ollama_url)
result = await performer.execute(task, context)
```

### Ringmaster Class

```python
ringmaster = Ringmaster(model, ollama_url)
plan = await ringmaster.think(request, performers)
final = await ringmaster.synthesize(request, results)
```

## Example Output

```
🎪 CIRCUS starting for: Write a Python function to calculate fibonacci...
🧠 Ringmaster thinking...
📋 Objective: Create a Python fibonacci function
📋 Tasks: 2
🎯 Coder working on: Write a Python fibonacci function...
✅ Coder completed
🎯 Research working on: Add docstring and type hints...
✅ Research completed
🎭 Ringmaster synthesizing results...
🎪 CIRCUS COMPLETE!

Result:
Here's a complete fibonacci implementation:

```python
def fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number.
    
    Args:
        n: The position in the Fibonacci sequence (0-indexed)
    
    Returns:
        The nth Fibonacci number
    
    Examples:
        >>> fibonacci(0)
        0
        >>> fibonacci(10)
        55
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```
```

## Project Structure

```
circus/
├── circus/
│   └── core.py          # Main orchestration engine
├── examples/
│   └── demo.py          # Example usage
├── README.md
└── requirements.txt
```

## License

MIT