# Cara Menggunakan Algorithm Simulator

## Overview

`AlgorithmSimulator` adalah utility untuk mensimulasikan eksekusi algoritma secara step-by-step. Berguna untuk:
- Memvisualisasikan cara kerja algoritma
- Menampilkan langkah-langkah detail eksekusi
- Membantu mahasiswa memahami algoritma dengan trace execution

## Import

```python
from utils.algorithm_simulator import AlgorithmSimulator

# Initialize simulator
simulator = AlgorithmSimulator()
```

## Algoritma yang Didukung

1. **Sorting Algorithms:**
   - `bubble_sort` - Bubble Sort
   - `selection_sort` - Selection Sort
   - `insertion_sort` - Insertion Sort

2. **Searching Algorithms:**
   - `binary_search` - Binary Search (memerlukan array terurut)
   - `linear_search` - Linear Search

3. **Recursive Algorithms:**
   - `factorial` - Faktorial
   - `fibonacci` - Fibonacci

## Cara Penggunaan

### 1. Bubble Sort

```python
simulator = AlgorithmSimulator()

# Simulate bubble sort
result = simulator.simulate(
    algorithm="bubble_sort",
    data=[64, 34, 25, 12, 22, 11, 90]
)

# Check result
if result["success"]:
    print(f"Algorithm: {result['algorithm']}")
    print(f"Result: {result['result']}")
    print(f"Summary: {result['summary']}")
    print(f"Complexity: {result['complexity']}")
    
    # Display steps
    for step in result["steps"]:
        print(f"\nStep {step['step']}: {step['description']}")
        print(f"Array: {step['array']}")
        print(f"Explanation: {step['explanation']}")
    
    # Display visualization
    print("\n" + result["visualization"])
```

**Output:**
```
Algorithm: Bubble Sort
Result: [11, 12, 22, 25, 34, 64, 90]
Summary: Selesai dalam 28 langkah, 21 perbandingan, 13 swap
Complexity: {'time': 'O(n²)', 'space': 'O(1)', 'best_case': 'O(n) jika sudah terurut', 'worst_case': 'O(n²)'}

Step 0: Array awal: [64, 34, 25, 12, 22, 11, 90]
Array: [64, 34, 25, 12, 22, 11, 90]
Explanation: Bubble sort akan membandingkan elemen bersebelahan dan menukar jika tidak terurut

Step 1: Iterasi 1, Posisi 0: 34 < 64 → SWAP
Array: [34, 64, 25, 12, 22, 11, 90]
Explanation: Menukar 34 dengan 64 karena 34 lebih kecil
...
```

### 2. Binary Search

```python
# Binary search requires sorted array
result = simulator.simulate(
    algorithm="binary_search",
    data=[1, 3, 5, 7, 9, 11, 13, 15, 17, 19],
    target=13  # Value to search
)

if result["success"]:
    print(f"Found: {result['found']}")
    print(f"Index: {result['index']}")
    print(f"Summary: {result['summary']}")
    
    # Display steps
    for step in result["steps"]:
        print(f"\nStep {step['step']}: {step['description']}")
        print(f"Searching in range: {step.get('search_range', 'N/A')}")
```

### 3. Linear Search

```python
result = simulator.simulate(
    algorithm="linear_search",
    data=[64, 34, 25, 12, 22, 11, 90],
    target=22
)

if result["success"]:
    print(f"Found: {result['found']}")
    print(f"Index: {result['index']}")
    print(f"Comparisons: {result['comparisons']}")
```

### 4. Factorial

```python
result = simulator.simulate(
    algorithm="factorial",
    data=5  # Calculate 5!
)

if result["success"]:
    print(f"Result: {result['result']}")  # 120
    print(f"Summary: {result['summary']}")
    
    # Display recursion trace
    for step in result["steps"]:
        print(f"Level {step['level']}: {step['description']}")
```

### 5. Fibonacci

```python
result = simulator.simulate(
    algorithm="fibonacci",
    data=7  # Get 7th Fibonacci number
)

if result["success"]:
    print(f"Result: {result['result']}")
    print(f"Sequence: {result['sequence']}")
    
    # Display recursion tree
    for step in result["steps"]:
        print(f"fib({step['n']}) = {step.get('result', '...')}")
```

## Return Value Structure

Setiap simulasi mengembalikan dictionary dengan struktur:

```python
{
    "success": bool,           # True jika simulasi berhasil
    "algorithm": str,          # Nama algoritma
    "steps": List[Dict],       # List langkah-langkah eksekusi
    "result": Any,             # Hasil akhir algoritma
    "summary": str,            # Ringkasan eksekusi
    "visualization": str,      # Visualisasi text-based (untuk sorting)
    "complexity": Dict,        # Time & space complexity (untuk sorting)
    "error": str              # Error message (jika success=False)
}
```

### Step Structure (untuk Sorting)

```python
{
    "step": int,              # Nomor langkah
    "description": str,       # Deskripsi langkah
    "array": List,           # State array pada langkah ini
    "comparisons": int,      # Total perbandingan sejauh ini
    "swaps": int,           # Total swap sejauh ini
    "highlight": List[int], # Index yang di-highlight
    "action": str,          # "swap", "compare", atau "done"
    "explanation": str      # Penjelasan detail
}
```

## Integrasi dengan Chatbot

### Cara 1: Manual Trigger

User mengetik command khusus untuk simulasi:

```python
# Di Chat.py
user_message = st.chat_input("Tanya tentang algoritma...")

if user_message:
    # Check if it's a simulation request
    if user_message.lower().startswith("/simulate"):
        parts = user_message.split()
        
        # /simulate bubble_sort [64, 34, 25, 12]
        if len(parts) >= 3:
            algorithm = parts[1]
            data = eval(parts[2])  # Parse array
            
            result = algorithm_simulator.simulate(algorithm, data)
            
            if result["success"]:
                st.success(f"✅ {result['algorithm']} Simulation")
                st.write(f"**Result:** {result['result']}")
                st.write(f"**Summary:** {result['summary']}")
                
                # Display steps
                with st.expander("📊 View Detailed Steps"):
                    for step in result["steps"]:
                        st.write(f"**Step {step['step']}:** {step['description']}")
                        st.code(str(step['array']))
                
                # Display visualization
                if "visualization" in result:
                    with st.expander("🎨 Visualization"):
                        st.text(result["visualization"])
            else:
                st.error(f"❌ {result.get('error', 'Simulation failed')}")
```

### Cara 2: Smart Detection

Chatbot otomatis mendeteksi request simulasi:

```python
from utils.question_detector import QuestionDetector

detector = QuestionDetector()
question_type = detector.detect_question_type(user_message)

# If user asks about algorithm execution
if "simulasi" in user_message.lower() or "trace" in user_message.lower():
    # Extract algorithm name and data from message
    # Then run simulation
    
    # Example: "simulasikan bubble sort untuk array [5, 2, 8, 1]"
    if "bubble sort" in user_message.lower():
        # Extract array from message
        import re
        match = re.search(r'\[([\d,\s]+)\]', user_message)
        if match:
            data = eval(match.group(0))
            result = algorithm_simulator.simulate("bubble_sort", data)
            
            # Display simulation result
            # ... (same as above)
```

### Cara 3: Interactive Widget

Tambahkan widget di sidebar untuk simulasi interaktif:

```python
# Di sidebar Chat.py
st.sidebar.markdown("### 🔬 Algorithm Simulator")

algorithm = st.sidebar.selectbox(
    "Pilih Algoritma:",
    ["bubble_sort", "selection_sort", "binary_search", "factorial"]
)

if algorithm in ["bubble_sort", "selection_sort", "insertion_sort"]:
    # For sorting
    data_input = st.sidebar.text_input(
        "Input Array (pisahkan dengan koma):",
        "64, 34, 25, 12, 22"
    )
    
    if st.sidebar.button("🚀 Run Simulation"):
        try:
            data = [int(x.strip()) for x in data_input.split(",")]
            result = algorithm_simulator.simulate(algorithm, data)
            
            if result["success"]:
                st.sidebar.success("✅ Simulation Complete!")
                
                # Display in main area
                st.subheader(f"📊 {result['algorithm']} Simulation")
                st.write(f"**Input:** {data}")
                st.write(f"**Output:** {result['result']}")
                st.write(f"**Summary:** {result['summary']}")
                
                # Animated steps
                step_container = st.container()
                for i, step in enumerate(result["steps"]):
                    with step_container:
                        st.write(f"**Step {i}:** {step['description']}")
                        st.code(str(step['array']))
                        if i < len(result["steps"]) - 1:
                            st.markdown("---")
                
        except Exception as e:
            st.sidebar.error(f"Error: {str(e)}")

elif algorithm == "binary_search":
    data_input = st.sidebar.text_input(
        "Sorted Array:",
        "1, 3, 5, 7, 9, 11, 13"
    )
    target = st.sidebar.number_input("Target:", value=7)
    
    if st.sidebar.button("🚀 Run Simulation"):
        data = [int(x.strip()) for x in data_input.split(",")]
        result = algorithm_simulator.simulate(algorithm, data, target=target)
        # ... display result
```

## Tips Penggunaan

1. **Validasi Input:**
   - Pastikan data dalam format yang benar
   - Untuk sorting: list of numbers
   - Untuk search: list + target value
   - Untuk recursive: single integer

2. **Handle Errors:**
   - Selalu check `result["success"]` sebelum akses data lain
   - Display `result["error"]` jika gagal

3. **Optimasi Display:**
   - Untuk array besar, batasi jumlah steps yang ditampilkan
   - Gunakan expander untuk detail lengkap
   - Highlight step penting saja

4. **Educational Value:**
   - Tampilkan complexity analysis
   - Explain setiap step dengan jelas
   - Bandingkan dengan algoritma lain

## Contoh Lengkap di Streamlit

```python
import streamlit as st
from utils.algorithm_simulator import AlgorithmSimulator

st.title("🔬 Algorithm Simulator")

simulator = AlgorithmSimulator()

# Algorithm selection
algorithm = st.selectbox(
    "Pilih Algoritma:",
    ["bubble_sort", "selection_sort", "insertion_sort", 
     "binary_search", "linear_search", "factorial", "fibonacci"]
)

# Input based on algorithm type
if algorithm.endswith("_sort"):
    data = st.text_input("Array (pisahkan dengan koma):", "64, 34, 25, 12, 22, 11, 90")
    data = [int(x.strip()) for x in data.split(",")]
    kwargs = {}
    
elif algorithm.endswith("_search"):
    data = st.text_input("Array:", "1, 3, 5, 7, 9, 11, 13, 15")
    data = [int(x.strip()) for x in data.split(",")]
    target = st.number_input("Target:", value=7)
    kwargs = {"target": target}
    
else:  # factorial or fibonacci
    data = st.number_input("Input:", min_value=0, max_value=20, value=5)
    kwargs = {}

# Run simulation
if st.button("🚀 Jalankan Simulasi"):
    with st.spinner("Running simulation..."):
        result = simulator.simulate(algorithm, data, **kwargs)
    
    if result["success"]:
        st.success(f"✅ Simulasi {result['algorithm']} Selesai!")
        
        # Result
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Result", str(result["result"]))
        with col2:
            st.info(result["summary"])
        
        # Complexity (if available)
        if "complexity" in result:
            st.subheader("📈 Complexity Analysis")
            st.json(result["complexity"])
        
        # Steps
        st.subheader("📝 Execution Steps")
        for step in result["steps"]:
            with st.expander(f"Step {step['step']}: {step['description']}"):
                st.write(f"**Explanation:** {step.get('explanation', 'N/A')}")
                if "array" in step:
                    st.code(str(step['array']))
        
        # Visualization
        if "visualization" in result:
            st.subheader("🎨 Visualization")
            st.text(result["visualization"])
    else:
        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
```

## Troubleshooting

**Q: Simulation tidak jalan?**
- Check apakah `utils/algorithm_simulator.py` ada
- Pastikan import path benar
- Verifikasi algorithm name (case-sensitive)

**Q: Error "Algorithm not supported"?**
- Lihat list algoritma yang didukung di documentation
- Pastikan nama algoritma lowercase dengan underscore

**Q: Data format salah?**
- Sorting: `[64, 34, 25]` (list of numbers)
- Search: `data=[1,2,3], target=2`
- Factorial/Fibonacci: `5` (single integer)

---
*Update: 19 Oktober 2025*
