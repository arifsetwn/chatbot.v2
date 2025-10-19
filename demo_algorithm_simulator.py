#!/usr/bin/env python3
"""
Demo: Algorithm Simulator
Demonstrasi penggunaan AlgorithmSimulator
"""

from utils.algorithm_simulator import AlgorithmSimulator

def print_separator():
    print("\n" + "=" * 80 + "\n")

def demo_bubble_sort():
    """Demo Bubble Sort"""
    print("🔷 DEMO: Bubble Sort")
    print_separator()
    
    simulator = AlgorithmSimulator()
    data = [64, 34, 25, 12, 22, 11, 90]
    
    print(f"Input Array: {data}")
    print("\nRunning simulation...")
    
    result = simulator.simulate("bubble_sort", data)
    
    if result["success"]:
        print(f"\n✅ Algorithm: {result['algorithm']}")
        print(f"📊 Result: {result['result']}")
        print(f"📝 Summary: {result['summary']}")
        print(f"\n📈 Complexity:")
        for key, value in result['complexity'].items():
            print(f"  - {key}: {value}")
        
        print(f"\n📋 Showing first 5 steps:")
        for step in result['steps'][:5]:
            print(f"\nStep {step['step']}: {step['description']}")
            print(f"  Array: {step['array']}")
            print(f"  Explanation: {step['explanation']}")
        
        print(f"\n... (total {len(result['steps'])} steps)")
        
        print("\n🎨 Visualization (first 10 lines):")
        viz_lines = result['visualization'].split('\n')[:10]
        print('\n'.join(viz_lines))
        print("...")
    else:
        print(f"❌ Error: {result['error']}")

def demo_binary_search():
    """Demo Binary Search"""
    print("🔷 DEMO: Binary Search")
    print_separator()
    
    simulator = AlgorithmSimulator()
    data = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    target = 13
    
    print(f"Sorted Array: {data}")
    print(f"Target: {target}")
    print("\nRunning simulation...")
    
    result = simulator.simulate("binary_search", data, target=target)
    
    if result["success"]:
        print(f"\n✅ Algorithm: {result['algorithm']}")
        print(f"🔍 Found: {'Yes' if result['found'] else 'No'}")
        if result['found']:
            print(f"📍 Index: {result['index']}")
        print(f"📝 Summary: {result['summary']}")
        
        print(f"\n📋 Search Steps:")
        for step in result['steps']:
            print(f"\nStep {step['step']}: {step['description']}")
            if 'search_range' in step:
                print(f"  Search Range: {step['search_range']}")
            if 'mid_value' in step:
                print(f"  Mid Value: {step['mid_value']}")
    else:
        print(f"❌ Error: {result['error']}")

def demo_factorial():
    """Demo Factorial"""
    print("🔷 DEMO: Factorial")
    print_separator()
    
    simulator = AlgorithmSimulator()
    n = 5
    
    print(f"Calculate: {n}!")
    print("\nRunning simulation...")
    
    result = simulator.simulate("factorial", n)
    
    if result["success"]:
        print(f"\n✅ Algorithm: {result['algorithm']}")
        print(f"📊 Result: {n}! = {result['result']}")
        print(f"📝 Summary: {result['summary']}")
        
        print(f"\n📋 Recursion Steps:")
        for step in result['steps']:
            indent = "  " * step.get('level', 0)
            print(f"{indent}Step {step['step']}: {step['description']}")
    else:
        print(f"❌ Error: {result['error']}")

def demo_fibonacci():
    """Demo Fibonacci"""
    print("🔷 DEMO: Fibonacci")
    print_separator()
    
    simulator = AlgorithmSimulator()
    n = 7
    
    print(f"Calculate: fib({n})")
    print("\nRunning simulation...")
    
    result = simulator.simulate("fibonacci", n)
    
    if result["success"]:
        print(f"\n✅ Algorithm: {result['algorithm']}")
        print(f"📊 Result: fib({n}) = {result['result']}")
        print(f"📊 Sequence: {result.get('sequence', [])}")
        print(f"📝 Summary: {result['summary']}")
        
        print(f"\n📋 First 10 Recursion Calls:")
        for step in result['steps'][:10]:
            indent = "  " * step.get('level', 0)
            desc = step['description']
            print(f"{indent}{desc}")
        
        if len(result['steps']) > 10:
            print(f"\n... (total {len(result['steps'])} calls)")
    else:
        print(f"❌ Error: {result['error']}")

def demo_selection_sort():
    """Demo Selection Sort"""
    print("🔷 DEMO: Selection Sort")
    print_separator()
    
    simulator = AlgorithmSimulator()
    data = [29, 10, 14, 37, 13]
    
    print(f"Input Array: {data}")
    print("\nRunning simulation...")
    
    result = simulator.simulate("selection_sort", data)
    
    if result["success"]:
        print(f"\n✅ Algorithm: {result['algorithm']}")
        print(f"📊 Result: {result['result']}")
        print(f"📝 Summary: {result['summary']}")
        
        print(f"\n📋 All Steps:")
        for step in result['steps']:
            print(f"\nStep {step['step']}: {step['description']}")
            print(f"  Array: {step['array']}")
            if 'explanation' in step:
                print(f"  → {step['explanation']}")
    else:
        print(f"❌ Error: {result['error']}")

def demo_error_handling():
    """Demo Error Handling"""
    print("🔷 DEMO: Error Handling")
    print_separator()
    
    simulator = AlgorithmSimulator()
    
    # Test 1: Unsupported algorithm
    print("Test 1: Unsupported algorithm")
    result = simulator.simulate("quick_sort", [5, 2, 8])
    print(f"Result: {result['success']}")
    if not result['success']:
        print(f"Error: {result['error']}")
    
    # Test 2: Binary search on unsorted array (should still work but may not find correctly)
    print("\nTest 2: Binary search on unsorted array")
    result = simulator.simulate("binary_search", [5, 2, 8, 1, 9], target=2)
    print(f"Result: {result['success']}")
    print(f"Found: {result.get('found', False)}")
    print(f"Note: Binary search requires sorted array for correct results!")

def main():
    """Run all demos"""
    print("=" * 80)
    print("ALGORITHM SIMULATOR - DEMO")
    print("=" * 80)
    
    demos = [
        ("Bubble Sort", demo_bubble_sort),
        ("Binary Search", demo_binary_search),
        ("Factorial", demo_factorial),
        ("Fibonacci", demo_fibonacci),
        ("Selection Sort", demo_selection_sort),
        ("Error Handling", demo_error_handling),
    ]
    
    for i, (name, demo_func) in enumerate(demos, 1):
        print(f"\n\n{'*' * 80}")
        print(f"DEMO {i}/{len(demos)}: {name}")
        print(f"{'*' * 80}")
        
        try:
            demo_func()
        except Exception as e:
            print(f"\n❌ Demo failed with error: {str(e)}")
        
        if i < len(demos):
            input("\n\nPress Enter to continue to next demo...")
    
    print("\n\n" + "=" * 80)
    print("ALL DEMOS COMPLETED!")
    print("=" * 80)
    
    print("\n📚 For more information, see:")
    print("  - ALGORITHM_SIMULATOR_USAGE.md")
    print("  - utils/algorithm_simulator.py")

if __name__ == "__main__":
    main()
