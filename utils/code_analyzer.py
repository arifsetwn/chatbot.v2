"""
Python Code Analyzer
Parse dan analisis kode Python yang diupload user
"""
import ast
import re
from typing import Dict, Any, List, Optional
from pathlib import Path


class CodeAnalyzer:
    """Analyze Python code for learning purposes"""
    
    def __init__(self):
        """Initialize analyzer"""
        pass
    
    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a Python file
        
        Args:
            file_path: Path to Python file
            
        Returns:
            Dict with analysis results
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            return self.analyze_code(code)
        except Exception as e:
            return {
                "success": False,
                "error": f"Error reading file: {str(e)}",
                "analysis": {}
            }
    
    def analyze_code(self, code: str) -> Dict[str, Any]:
        """
        Analyze Python code string
        
        Args:
            code: Python code as string
            
        Returns:
            Dict with:
            - success: bool
            - is_valid: bool
            - syntax_errors: List[str]
            - structure: Dict (functions, classes, imports)
            - algorithms: List[str] (detected algorithms)
            - complexity_indicators: Dict
            - learning_points: List[str]
            - suggestions: List[str]
        """
        result = {
            "success": True,
            "is_valid": False,
            "syntax_errors": [],
            "structure": {},
            "algorithms": [],
            "complexity_indicators": {},
            "learning_points": [],
            "suggestions": [],
            "code_length": len(code.split('\n'))
        }
        
        # Check syntax validity
        try:
            tree = ast.parse(code)
            result["is_valid"] = True
            
            # Analyze structure
            result["structure"] = self._analyze_structure(tree, code)
            
            # Detect algorithms
            result["algorithms"] = self._detect_algorithms(code, tree)
            
            # Analyze complexity
            result["complexity_indicators"] = self._analyze_complexity(tree, code)
            
            # Generate learning points
            result["learning_points"] = self._generate_learning_points(result)
            
            # Generate suggestions
            result["suggestions"] = self._generate_suggestions(result, code)
            
        except SyntaxError as e:
            result["is_valid"] = False
            result["syntax_errors"].append({
                "line": e.lineno,
                "message": e.msg,
                "text": e.text.strip() if e.text else ""
            })
        except Exception as e:
            result["success"] = False
            result["syntax_errors"].append({
                "line": None,
                "message": str(e),
                "text": ""
            })
        
        return result
    
    def _analyze_structure(self, tree: ast.AST, code: str) -> Dict[str, Any]:
        """Analyze code structure"""
        structure = {
            "imports": [],
            "functions": [],
            "classes": [],
            "global_variables": [],
            "has_main": False,
            "docstrings": []
        }
        
        for node in ast.walk(tree):
            # Imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    structure["imports"].append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    structure["imports"].append(f"{module}.{alias.name}")
            
            # Functions
            elif isinstance(node, ast.FunctionDef):
                func_info = {
                    "name": node.name,
                    "args": [arg.arg for arg in node.args.args],
                    "is_recursive": self._is_recursive(node),
                    "has_docstring": ast.get_docstring(node) is not None,
                    "line": node.lineno
                }
                structure["functions"].append(func_info)
                
                if node.name == "main":
                    structure["has_main"] = True
            
            # Classes
            elif isinstance(node, ast.ClassDef):
                class_info = {
                    "name": node.name,
                    "methods": [m.name for m in node.body if isinstance(m, ast.FunctionDef)],
                    "has_docstring": ast.get_docstring(node) is not None,
                    "line": node.lineno
                }
                structure["classes"].append(class_info)
            
            # Global variables (assignments at module level)
            elif isinstance(node, ast.Assign):
                if isinstance(node.targets[0], ast.Name):
                    var_name = node.targets[0].id
                    if not var_name.startswith('_'):  # Skip private vars
                        structure["global_variables"].append(var_name)
        
        return structure
    
    def _is_recursive(self, func_node: ast.FunctionDef) -> bool:
        """Check if function is recursive"""
        func_name = func_node.name
        
        for node in ast.walk(func_node):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id == func_name:
                    return True
        
        return False
    
    def _detect_algorithms(self, code: str, tree: ast.AST) -> List[str]:
        """Detect common algorithms in code"""
        algorithms = []
        code_lower = code.lower()
        
        # Algorithm patterns
        patterns = {
            "Binary Search": [
                r'\bmid\s*=.*\(.*low.*\+.*high.*\)',
                r'\bmiddle\s*=',
                r'binary.*search',
                r'while.*low.*<=.*high'
            ],
            "Linear Search": [
                r'for.*in.*range.*len\(',
                r'if.*==.*return',
                r'linear.*search'
            ],
            "Bubble Sort": [
                r'bubble.*sort',
                r'for.*range.*len.*for.*range.*len',
                r'if.*>.*swap'
            ],
            "Selection Sort": [
                r'selection.*sort',
                r'min.*index',
                r'for.*range.*for.*range'
            ],
            "Insertion Sort": [
                r'insertion.*sort',
                r'while.*>.*0.*and',
                r'key\s*='
            ],
            "Quick Sort": [
                r'quick.*sort',
                r'pivot',
                r'partition'
            ],
            "Merge Sort": [
                r'merge.*sort',
                r'def.*merge\(',
                r'mid.*=.*len.*//.*2'
            ],
            "Recursion": [],  # Handled separately
            "Dynamic Programming": [
                r'dp\s*=.*\[',
                r'memo',
                r'cache'
            ],
            "Stack": [
                r'\.append\(',
                r'\.pop\(\)',
                r'stack\s*='
            ],
            "Queue": [
                r'queue',
                r'deque',
                r'enqueue|dequeue'
            ]
        }
        
        # Check patterns
        for algo_name, algo_patterns in patterns.items():
            for pattern in algo_patterns:
                if re.search(pattern, code_lower):
                    if algo_name not in algorithms:
                        algorithms.append(algo_name)
                    break
        
        # Check for recursion via AST
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if self._is_recursive(node):
                    if "Recursion" not in algorithms:
                        algorithms.append("Recursion")
        
        # Check for loops
        has_loop = any(isinstance(node, (ast.For, ast.While)) for node in ast.walk(tree))
        if has_loop and not any(algo in algorithms for algo in ["Binary Search", "Linear Search", "Bubble Sort", "Selection Sort", "Insertion Sort"]):
            algorithms.append("Iterasi/Loop")
        
        return algorithms
    
    def _analyze_complexity(self, tree: ast.AST, code: str) -> Dict[str, Any]:
        """Analyze code complexity indicators"""
        complexity = {
            "nested_loops": 0,
            "recursion_depth": 0,
            "cyclomatic_complexity": 1,  # Start with 1
            "total_loops": 0,
            "total_conditionals": 0,
            "max_nesting_level": 0
        }
        
        # Count nested loops
        def count_nested_loops(node, depth=0):
            max_depth = depth
            for child in ast.iter_child_nodes(node):
                if isinstance(child, (ast.For, ast.While)):
                    complexity["total_loops"] += 1
                    child_depth = count_nested_loops(child, depth + 1)
                    max_depth = max(max_depth, child_depth)
                else:
                    child_depth = count_nested_loops(child, depth)
                    max_depth = max(max_depth, child_depth)
            return max_depth
        
        complexity["nested_loops"] = count_nested_loops(tree)
        complexity["max_nesting_level"] = complexity["nested_loops"]
        
        # Count conditionals
        for node in ast.walk(tree):
            if isinstance(node, ast.If):
                complexity["total_conditionals"] += 1
                complexity["cyclomatic_complexity"] += 1
            elif isinstance(node, (ast.For, ast.While)):
                complexity["cyclomatic_complexity"] += 1
        
        # Estimate time complexity category
        if complexity["nested_loops"] >= 3:
            complexity["estimated_time_complexity"] = "O(n³) or worse"
        elif complexity["nested_loops"] == 2:
            complexity["estimated_time_complexity"] = "O(n²)"
        elif complexity["nested_loops"] == 1:
            complexity["estimated_time_complexity"] = "O(n)"
        elif any(isinstance(node, ast.FunctionDef) and self._is_recursive(node) for node in ast.walk(tree)):
            complexity["estimated_time_complexity"] = "O(log n) atau O(n) tergantung rekursi"
        else:
            complexity["estimated_time_complexity"] = "O(1)"
        
        return complexity
    
    def _generate_learning_points(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate learning points from analysis"""
        points = []
        
        structure = analysis.get("structure", {})
        algorithms = analysis.get("algorithms", [])
        complexity = analysis.get("complexity_indicators", {})
        
        # Structure points
        if structure.get("functions"):
            func_names = [f["name"] for f in structure["functions"]]
            points.append(f"✓ Kode terstruktur dengan {len(func_names)} fungsi: {', '.join(func_names[:3])}")
        
        if structure.get("classes"):
            points.append(f"✓ Menggunakan OOP dengan {len(structure['classes'])} class")
        
        # Algorithm points
        if algorithms:
            points.append(f"✓ Mengimplementasikan: {', '.join(algorithms[:3])}")
        
        # Recursion
        recursive_funcs = [f["name"] for f in structure.get("functions", []) if f.get("is_recursive")]
        if recursive_funcs:
            points.append(f"✓ Fungsi rekursif: {', '.join(recursive_funcs)}")
        
        # Complexity points
        if complexity.get("nested_loops", 0) >= 2:
            points.append(f"⚠️ Loop bersarang {complexity['nested_loops']} level - pertimbangkan kompleksitas waktu")
        
        if complexity.get("estimated_time_complexity"):
            points.append(f"📊 Estimasi kompleksitas: {complexity['estimated_time_complexity']}")
        
        # Documentation
        funcs_with_docs = sum(1 for f in structure.get("functions", []) if f.get("has_docstring"))
        total_funcs = len(structure.get("functions", []))
        if total_funcs > 0 and funcs_with_docs == 0:
            points.append("💡 Tip: Tambahkan docstring untuk dokumentasi fungsi")
        
        return points
    
    def _generate_suggestions(self, analysis: Dict[str, Any], code: str) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        structure = analysis.get("structure", {})
        complexity = analysis.get("complexity_indicators", {})
        
        # No functions
        if len(structure.get("functions", [])) == 0 and analysis.get("code_length", 0) > 20:
            suggestions.append("Pertimbangkan memecah kode menjadi fungsi-fungsi untuk reusability")
        
        # High complexity
        if complexity.get("nested_loops", 0) >= 3:
            suggestions.append("Loop bersarang terlalu dalam - pertimbangkan refactoring atau algoritma lebih efisien")
        
        # No main function
        if not structure.get("has_main") and len(structure.get("functions", [])) > 2:
            suggestions.append("Tambahkan fungsi main() sebagai entry point program")
        
        # Variable naming (simple check)
        if re.search(r'\b(a|b|c|x|y|z)\s*=', code) and analysis.get("code_length", 0) > 10:
            suggestions.append("Gunakan nama variabel yang lebih deskriptif (bukan a, b, c, x, y, z)")
        
        # No error handling
        if not re.search(r'try:|except:', code) and analysis.get("code_length", 0) > 30:
            suggestions.append("Pertimbangkan menambahkan error handling (try-except) untuk robustness")
        
        return suggestions
    
    def get_guided_questions(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate guided questions untuk Socratic method"""
        questions = []
        
        algorithms = analysis.get("algorithms", [])
        structure = analysis.get("structure", {})
        complexity = analysis.get("complexity_indicators", {})
        
        # Algorithm understanding
        if "Binary Search" in algorithms:
            questions.append("Mengapa binary search harus menggunakan array yang sudah terurut?")
            questions.append("Apa yang terjadi jika array tidak terurut?")
        
        if "Bubble Sort" in algorithms or "Selection Sort" in algorithms:
            questions.append("Berapa kali perbandingan yang dilakukan untuk n elemen?")
            questions.append("Bisakah kamu jelaskan mengapa kompleksitasnya O(n²)?")
        
        if "Recursion" in algorithms:
            questions.append("Apa base case dari fungsi rekursif ini?")
            questions.append("Bagaimana cara kerja call stack pada rekursi ini?")
        
        # Complexity
        if complexity.get("nested_loops", 0) >= 2:
            questions.append("Berapa iterasi total yang dilakukan dengan nested loop ini?")
            questions.append("Apakah ada cara membuat algoritma ini lebih efisien?")
        
        # General
        if structure.get("functions"):
            questions.append("Coba jelaskan dengan kata-kata sendiri, apa yang dilakukan setiap fungsi?")
        
        questions.append("Apa input dan output yang diharapkan dari kode ini?")
        questions.append("Sudah coba test dengan beberapa contoh input?")
        
        return questions


# Example usage
if __name__ == "__main__":
    analyzer = CodeAnalyzer()
    
    # Test code
    sample_code = """
def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    
    return -1

# Test
arr = [1, 3, 5, 7, 9, 11]
result = binary_search(arr, 7)
print(result)
"""
    
    print("=" * 60)
    print("CODE ANALYZER TEST")
    print("=" * 60)
    
    result = analyzer.analyze_code(sample_code)
    
    print(f"\nValid: {result['is_valid']}")
    print(f"Algorithms: {result['algorithms']}")
    print(f"Functions: {[f['name'] for f in result['structure']['functions']]}")
    print(f"Complexity: {result['complexity_indicators']['estimated_time_complexity']}")
    print(f"\nLearning Points:")
    for point in result['learning_points']:
        print(f"  - {point}")
    print(f"\nGuided Questions:")
    questions = analyzer.get_guided_questions(result)
    for i, q in enumerate(questions, 1):
        print(f"  {i}. {q}")
