"""
Algorithm Simulator
Simulate and trace algorithm execution step-by-step
"""
from typing import Dict, Any, List, Tuple, Optional


class AlgorithmSimulator:
    """Simulate common algorithms step-by-step"""
    
    def __init__(self):
        """Initialize simulator"""
        pass
    
    def simulate(self, algorithm: str, data: Any, **kwargs) -> Dict[str, Any]:
        """
        Simulate algorithm execution
        
        Args:
            algorithm: Algorithm name (e.g., "bubble_sort", "binary_search")
            data: Input data
            **kwargs: Additional parameters (e.g., target for search)
            
        Returns:
            Dict with:
            - success: bool
            - steps: List[Dict] (each step of execution)
            - result: Any (final result)
            - summary: str
            - visualization: str (text-based visualization)
        """
        algorithm = algorithm.lower().replace(" ", "_")
        
        simulators = {
            "bubble_sort": self._simulate_bubble_sort,
            "selection_sort": self._simulate_selection_sort,
            "insertion_sort": self._simulate_insertion_sort,
            "binary_search": self._simulate_binary_search,
            "linear_search": self._simulate_linear_search,
            "factorial": self._simulate_factorial,
            "fibonacci": self._simulate_fibonacci,
        }
        
        if algorithm not in simulators:
            return {
                "success": False,
                "error": f"Algorithm '{algorithm}' not supported. Available: {', '.join(simulators.keys())}",
                "steps": [],
                "result": None
            }
        
        try:
            return simulators[algorithm](data, **kwargs)
        except Exception as e:
            return {
                "success": False,
                "error": f"Simulation error: {str(e)}",
                "steps": [],
                "result": None
            }
    
    def _simulate_bubble_sort(self, arr: List, **kwargs) -> Dict[str, Any]:
        """Simulate bubble sort"""
        arr = list(arr)  # Copy to avoid modifying original
        steps = []
        n = len(arr)
        
        steps.append({
            "step": 0,
            "description": f"Array awal: {arr}",
            "array": list(arr),
            "comparisons": 0,
            "swaps": 0,
            "explanation": "Bubble sort akan membandingkan elemen bersebelahan dan menukar jika tidak terurut"
        })
        
        total_comparisons = 0
        total_swaps = 0
        
        for i in range(n):
            swapped = False
            
            for j in range(0, n - i - 1):
                total_comparisons += 1
                
                if arr[j] > arr[j + 1]:
                    # Swap
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    total_swaps += 1
                    swapped = True
                    
                    steps.append({
                        "step": len(steps),
                        "description": f"Iterasi {i+1}, Posisi {j}: {arr[j+1]} < {arr[j]} → SWAP",
                        "array": list(arr),
                        "comparisons": total_comparisons,
                        "swaps": total_swaps,
                        "highlight": [j, j+1],
                        "action": "swap",
                        "explanation": f"Menukar {arr[j+1]} dengan {arr[j]} karena {arr[j+1]} lebih kecil"
                    })
                else:
                    steps.append({
                        "step": len(steps),
                        "description": f"Iterasi {i+1}, Posisi {j}: {arr[j]} <= {arr[j+1]} → Tidak perlu swap",
                        "array": list(arr),
                        "comparisons": total_comparisons,
                        "swaps": total_swaps,
                        "highlight": [j, j+1],
                        "action": "compare",
                        "explanation": "Sudah dalam urutan yang benar"
                    })
            
            if not swapped:
                steps.append({
                    "step": len(steps),
                    "description": f"Iterasi {i+1} selesai: Tidak ada swap, array sudah terurut!",
                    "array": list(arr),
                    "comparisons": total_comparisons,
                    "swaps": total_swaps,
                    "explanation": "Early termination - bubble sort selesai lebih cepat"
                })
                break
        
        return {
            "success": True,
            "algorithm": "Bubble Sort",
            "steps": steps,
            "result": arr,
            "summary": f"Selesai dalam {len(steps)} langkah, {total_comparisons} perbandingan, {total_swaps} swap",
            "visualization": self._visualize_sort_steps(steps),
            "complexity": {
                "time": "O(n²)",
                "space": "O(1)",
                "best_case": "O(n) jika sudah terurut",
                "worst_case": "O(n²)"
            }
        }
    
    def _simulate_selection_sort(self, arr: List, **kwargs) -> Dict[str, Any]:
        """Simulate selection sort"""
        arr = list(arr)
        steps = []
        n = len(arr)
        
        steps.append({
            "step": 0,
            "description": f"Array awal: {arr}",
            "array": list(arr),
            "explanation": "Selection sort mencari elemen terkecil dan menempatkannya di posisi yang benar"
        })
        
        total_comparisons = 0
        total_swaps = 0
        
        for i in range(n):
            min_idx = i
            
            # Find minimum element
            for j in range(i + 1, n):
                total_comparisons += 1
                
                if arr[j] < arr[min_idx]:
                    steps.append({
                        "step": len(steps),
                        "description": f"Iterasi {i+1}: {arr[j]} < {arr[min_idx]}, update min_idx ke {j}",
                        "array": list(arr),
                        "min_idx": j,
                        "current_i": i,
                        "comparisons": total_comparisons,
                        "explanation": f"Menemukan nilai lebih kecil: {arr[j]}"
                    })
                    min_idx = j
            
            # Swap if needed
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                total_swaps += 1
                
                steps.append({
                    "step": len(steps),
                    "description": f"Swap posisi {i} dengan posisi {min_idx}: {arr}",
                    "array": list(arr),
                    "swaps": total_swaps,
                    "comparisons": total_comparisons,
                    "highlight": [i, min_idx],
                    "explanation": f"Menempatkan elemen terkecil ({arr[i]}) di posisi {i}"
                })
        
        return {
            "success": True,
            "algorithm": "Selection Sort",
            "steps": steps,
            "result": arr,
            "summary": f"Selesai dalam {len(steps)} langkah, {total_comparisons} perbandingan, {total_swaps} swap",
            "visualization": self._visualize_sort_steps(steps),
            "complexity": {
                "time": "O(n²)",
                "space": "O(1)"
            }
        }
    
    def _simulate_insertion_sort(self, arr: List, **kwargs) -> Dict[str, Any]:
        """Simulate insertion sort"""
        arr = list(arr)
        steps = []
        
        steps.append({
            "step": 0,
            "description": f"Array awal: {arr}",
            "array": list(arr),
            "explanation": "Insertion sort membangun sorted array satu elemen per iterasi"
        })
        
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            
            steps.append({
                "step": len(steps),
                "description": f"Iterasi {i}: Key = {key}",
                "array": list(arr),
                "key": key,
                "position": i,
                "explanation": f"Akan menyisipkan {key} ke posisi yang tepat"
            })
            
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
                
                steps.append({
                    "step": len(steps),
                    "description": f"Geser {arr[j+1]} ke kanan",
                    "array": list(arr),
                    "explanation": f"Mencari posisi untuk {key}"
                })
            
            arr[j + 1] = key
            steps.append({
                "step": len(steps),
                "description": f"Sisipkan {key} di posisi {j+1}",
                "array": list(arr),
                "explanation": f"Posisi yang tepat untuk {key} adalah index {j+1}"
            })
        
        return {
            "success": True,
            "algorithm": "Insertion Sort",
            "steps": steps,
            "result": arr,
            "summary": f"Selesai dalam {len(steps)} langkah",
            "visualization": self._visualize_sort_steps(steps),
            "complexity": {
                "time": "O(n²)",
                "space": "O(1)",
                "best_case": "O(n) untuk array yang hampir terurut"
            }
        }
    
    def _simulate_binary_search(self, arr: List, target: Any = None, **kwargs) -> Dict[str, Any]:
        """Simulate binary search"""
        if target is None:
            return {
                "success": False,
                "error": "Binary search requires 'target' parameter",
                "steps": []
            }
        
        steps = []
        low = 0
        high = len(arr) - 1
        
        steps.append({
            "step": 0,
            "description": f"Array: {arr}, Target: {target}",
            "array": list(arr),
            "low": low,
            "high": high,
            "explanation": "Binary search hanya bekerja pada array yang sudah terurut"
        })
        
        iteration = 0
        result_idx = -1
        
        while low <= high:
            iteration += 1
            mid = (low + high) // 2
            
            steps.append({
                "step": len(steps),
                "description": f"Iterasi {iteration}: low={low}, high={high}, mid={mid}",
                "array": list(arr),
                "low": low,
                "high": high,
                "mid": mid,
                "mid_value": arr[mid],
                "explanation": f"Memeriksa elemen tengah: arr[{mid}] = {arr[mid]}"
            })
            
            if arr[mid] == target:
                result_idx = mid
                steps.append({
                    "step": len(steps),
                    "description": f"✓ FOUND! Target {target} ditemukan di index {mid}",
                    "array": list(arr),
                    "result": mid,
                    "explanation": f"arr[{mid}] == {target}"
                })
                break
            elif arr[mid] < target:
                steps.append({
                    "step": len(steps),
                    "description": f"{arr[mid]} < {target}, cari di bagian kanan",
                    "array": list(arr),
                    "explanation": f"Karena {arr[mid]} lebih kecil, target pasti di sebelah kanan"
                })
                low = mid + 1
            else:
                steps.append({
                    "step": len(steps),
                    "description": f"{arr[mid]} > {target}, cari di bagian kiri",
                    "array": list(arr),
                    "explanation": f"Karena {arr[mid]} lebih besar, target pasti di sebelah kiri"
                })
                high = mid - 1
        
        if result_idx == -1:
            steps.append({
                "step": len(steps),
                "description": f"✗ NOT FOUND! Target {target} tidak ada dalam array",
                "array": list(arr),
                "result": -1,
                "explanation": "Search space habis, elemen tidak ditemukan"
            })
        
        return {
            "success": True,
            "algorithm": "Binary Search",
            "steps": steps,
            "result": result_idx,
            "summary": f"Selesai dalam {iteration} iterasi. Target {'ditemukan' if result_idx != -1 else 'tidak ditemukan'}",
            "visualization": self._visualize_search_steps(steps),
            "complexity": {
                "time": "O(log n)",
                "space": "O(1)"
            }
        }
    
    def _simulate_linear_search(self, arr: List, target: Any = None, **kwargs) -> Dict[str, Any]:
        """Simulate linear search"""
        if target is None:
            return {
                "success": False,
                "error": "Linear search requires 'target' parameter",
                "steps": []
            }
        
        steps = []
        steps.append({
            "step": 0,
            "description": f"Array: {arr}, Target: {target}",
            "array": list(arr),
            "explanation": "Linear search memeriksa setiap elemen satu per satu"
        })
        
        result_idx = -1
        
        for i, val in enumerate(arr):
            steps.append({
                "step": len(steps),
                "description": f"Iterasi {i+1}: Cek arr[{i}] = {val}",
                "array": list(arr),
                "current_index": i,
                "current_value": val,
                "explanation": f"Membandingkan {val} dengan target {target}"
            })
            
            if val == target:
                result_idx = i
                steps.append({
                    "step": len(steps),
                    "description": f"✓ FOUND! Target {target} ditemukan di index {i}",
                    "array": list(arr),
                    "result": i,
                    "explanation": "Pencarian selesai"
                })
                break
        
        if result_idx == -1:
            steps.append({
                "step": len(steps),
                "description": f"✗ NOT FOUND! Target {target} tidak ada dalam array",
                "array": list(arr),
                "result": -1,
                "explanation": "Sudah memeriksa semua elemen"
            })
        
        return {
            "success": True,
            "algorithm": "Linear Search",
            "steps": steps,
            "result": result_idx,
            "summary": f"Selesai dalam {len(arr) if result_idx == -1 else result_idx + 1} iterasi",
            "visualization": self._visualize_search_steps(steps),
            "complexity": {
                "time": "O(n)",
                "space": "O(1)"
            }
        }
    
    def _simulate_factorial(self, n: int, **kwargs) -> Dict[str, Any]:
        """Simulate factorial calculation (recursive)"""
        steps = []
        call_stack = []
        
        def factorial_trace(n, depth=0):
            indent = "  " * depth
            
            steps.append({
                "step": len(steps),
                "description": f"{indent}factorial({n}) dipanggil",
                "n": n,
                "depth": depth,
                "call_stack": list(call_stack),
                "explanation": f"Level rekursi: {depth}"
            })
            
            call_stack.append(f"factorial({n})")
            
            if n <= 1:
                steps.append({
                    "step": len(steps),
                    "description": f"{indent}Base case: factorial({n}) = 1",
                    "n": n,
                    "depth": depth,
                    "result": 1,
                    "call_stack": list(call_stack),
                    "explanation": "Mencapai base case, mulai return"
                })
                call_stack.pop()
                return 1
            else:
                result = n * factorial_trace(n - 1, depth + 1)
                steps.append({
                    "step": len(steps),
                    "description": f"{indent}factorial({n}) = {n} * factorial({n-1}) = {result}",
                    "n": n,
                    "depth": depth,
                    "result": result,
                    "call_stack": list(call_stack),
                    "explanation": f"Return {result} ke pemanggil"
                })
                call_stack.pop()
                return result
        
        result = factorial_trace(n)
        
        return {
            "success": True,
            "algorithm": "Factorial (Recursive)",
            "steps": steps,
            "result": result,
            "summary": f"factorial({n}) = {result}, {len(steps)} langkah rekursi",
            "visualization": self._visualize_recursion_steps(steps),
            "complexity": {
                "time": "O(n)",
                "space": "O(n) untuk call stack"
            }
        }
    
    def _simulate_fibonacci(self, n: int, **kwargs) -> Dict[str, Any]:
        """Simulate Fibonacci calculation"""
        steps = []
        
        steps.append({
            "step": 0,
            "description": f"Menghitung Fibonacci ke-{n}",
            "explanation": "Fibonacci: F(n) = F(n-1) + F(n-2), F(0)=0, F(1)=1"
        })
        
        if n <= 1:
            return {
                "success": True,
                "algorithm": "Fibonacci",
                "steps": steps,
                "result": n,
                "summary": f"Fibonacci({n}) = {n} (base case)"
            }
        
        # Iterative approach for visualization
        fib = [0, 1]
        
        for i in range(2, n + 1):
            next_fib = fib[i-1] + fib[i-2]
            fib.append(next_fib)
            
            steps.append({
                "step": len(steps),
                "description": f"F({i}) = F({i-1}) + F({i-2}) = {fib[i-1]} + {fib[i-2]} = {next_fib}",
                "index": i,
                "sequence": list(fib),
                "explanation": f"Fibonacci ke-{i} adalah {next_fib}"
            })
        
        return {
            "success": True,
            "algorithm": "Fibonacci",
            "steps": steps,
            "result": fib[n],
            "summary": f"Fibonacci({n}) = {fib[n]}",
            "sequence": fib,
            "visualization": f"Sequence: {fib}",
            "complexity": {
                "time": "O(n) iteratif, O(2ⁿ) rekursif naive",
                "space": "O(n) untuk menyimpan sequence"
            }
        }
    
    def _visualize_sort_steps(self, steps: List[Dict]) -> str:
        """Create text visualization of sorting steps"""
        vis = []
        for i, step in enumerate(steps[:10]):  # Limit to first 10 steps
            array = step.get("array", [])
            highlight = step.get("highlight", [])
            
            # Create visual representation
            visual_line = ""
            for idx, val in enumerate(array):
                if idx in highlight:
                    visual_line += f"[{val}] "
                else:
                    visual_line += f" {val}  "
            
            vis.append(f"Step {i}: {visual_line}")
            vis.append(f"       {step.get('description', '')}")
        
        if len(steps) > 10:
            vis.append(f"... ({len(steps) - 10} more steps)")
        
        return "\n".join(vis)
    
    def _visualize_search_steps(self, steps: List[Dict]) -> str:
        """Create text visualization of search steps"""
        vis = []
        for step in steps:
            desc = step.get("description", "")
            vis.append(f"Step {step['step']}: {desc}")
        
        return "\n".join(vis)
    
    def _visualize_recursion_steps(self, steps: List[Dict]) -> str:
        """Create text visualization of recursion"""
        vis = []
        for step in steps:
            vis.append(step.get("description", ""))
        
        return "\n".join(vis)


# Example usage
if __name__ == "__main__":
    sim = AlgorithmSimulator()
    
    print("=" * 60)
    print("ALGORITHM SIMULATOR TEST")
    print("=" * 60)
    
    # Test bubble sort
    print("\n--- Bubble Sort ---")
    result = sim.simulate("bubble_sort", [5, 2, 8, 1, 9])
    print(f"Result: {result['result']}")
    print(f"Summary: {result['summary']}")
    print(f"Steps: {len(result['steps'])}")
    
    # Test binary search
    print("\n--- Binary Search ---")
    result = sim.simulate("binary_search", [1, 3, 5, 7, 9, 11], target=7)
    print(f"Result: {result['result']}")
    print(f"Summary: {result['summary']}")
    
    # Test factorial
    print("\n--- Factorial ---")
    result = sim.simulate("factorial", 5)
    print(f"Result: {result['result']}")
    print(f"Summary: {result['summary']}")
    print("\nVisualization:")
    print(result['visualization'])
