"""
Quick test script to verify the entire system works
"""
import asyncio
import sys
sys.path.insert(0, 'backend')

from agent.orchestrator import Orchestrator

async def test_system():
    print("[TEST] Testing Antigravity Remote Coding Assistant...")
    print()
    
    # 1. Initialize
    print("1. Initializing Orchestrator...")
    orchestrator = Orchestrator()
    print("   [OK] Orchestrator ready")
    print()
    
    # 2. Test simple query (should use Local Ollama)
    print("2. Testing Local LLM (simple query)...")
    simple_query = "Hello, how are you?"
    response = await orchestrator.process_request(simple_query)
    print(f"   Query: {simple_query}")
    print(f"   Source: {response['source']}")
    print(f"   Response: {response['response'][:100]}...")
    print()
    
    # 3. Test complex query (should use Gemini or fallback)
    print("3. Testing Complex Query (architecture)...")
    complex_query = "Design a scalable microservices architecture"
    response = await orchestrator.process_request(complex_query)
    print(f"   Query: {complex_query}")
    print(f"   Source: {response['source']}")
    print(f"   Response: {response['response'][:100]}...")
    print()
    
    print("[SUCCESS] All tests complete!")

if __name__ == "__main__":
    asyncio.run(test_system())
