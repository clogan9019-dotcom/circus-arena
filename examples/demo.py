"""
Circus Demo - See it in action!
"""

import asyncio
import os
from circus import Circus, run

# Load from .env if exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


async def demo_basic():
    """Basic example with one performer."""
    print("=" * 50)
    print("DEMO 1: Basic single performer")
    print("=" * 50)
    
    ringmaster = os.getenv("RINGMASTER_MODEL", "qwen2.5-coder-14b-instruct-abliterated:latest")
    circus = Circus(ringmaster)
    circus.add_performer("Coder", "qwen2.5:0.5b")
    
    result = await circus.perform("Write a Python function to reverse a string")
    print("\n📤 RESULT:")
    print(result)


async def demo_multi_performer():
    """Example with multiple performers."""
    print("\n" + "=" * 50)
    print("DEMO 2: Multiple performers")
    print("=" * 50)
    
    ringmaster = os.getenv("RINGMASTER_MODEL", "qwen2.5-coder-14b-instruct-abliterated:latest")
    circus = Circus(ringmaster)
    
    # Add specialized performers
    circus.add_performer("Coder", "qwen2.5:1.5b")
    circus.add_performer("Documenter", "qwen2.5:0.5b")
    
    result = await circus.perform(
        "Create a Python class for a Stack data structure with push, pop, and peek methods"
    )
    print("\n📤 RESULT:")
    print(result)


async def demo_quick_run():
    """Quick one-liner using the run() function."""
    print("\n" + "=" * 50)
    print("DEMO 3: Quick run() function")
    print("=" * 50)
    
    result = await run(
        "Explain what a decorator is in Python in one sentence",
        ringmaster="qwen2.5-coder-14b-instruct-abliterated:latest",
        performers=[("Explainer", "qwen2.5:0.5b")]
    )
    print("\n📤 RESULT:")
    print(result)


async def demo_status():
    """Show circus status."""
    print("\n" + "=" * 50)
    print("DEMO 4: Circus status")
    print("=" * 50)
    
    circus = Circus("qwen2.5-coder-14b-instruct-abliterated:latest")
    circus.add_performer("Coder", "qwen2.5:0.5b")
    circus.add_performer("Tester", "qwen2.5:1.5b")
    
    status = circus.status()
    print("\n📊 STATUS:")
    import json
    print(json.dumps(status, indent=2))


async def main():
    print("\n🎪 CIRCUS DEMO")
    print("=" * 50)
    
    # Check if Ollama is running
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.get("http://localhost:11434/api/tags", timeout=5)
            models = response.json().get("models", [])
            print(f"✅ Ollama connected! Found {len(models)} models:")
            for m in models[:5]:
                print(f"   - {m.get('name', 'unknown')}")
    except Exception as e:
        print(f"❌ Ollama not running: {e}")
        print("   Start with: ollama serve")
        return
    
    # Run demos
    await demo_basic()
    await demo_multi_performer()
    await demo_quick_run()
    await demo_status()
    
    print("\n" + "=" * 50)
    print("✅ All demos complete!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())