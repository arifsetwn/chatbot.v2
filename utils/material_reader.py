"""
PDF Material Reader
Reads and extracts text from PDF materials for RAG (Retrieval Augmented Generation)
"""
import os
from pathlib import Path
from typing import List, Dict, Optional
import PyPDF2


class MaterialReader:
    """Read and manage learning materials (PDF files)"""
    
    def __init__(self, materials_dir: str = "data/materials"):
        self.materials_dir = Path(materials_dir)
        self.materials_dir.mkdir(parents=True, exist_ok=True)
        self._cache = {}
    
    def list_materials(self) -> List[str]:
        """List all available PDF materials"""
        try:
            pdf_files = list(self.materials_dir.glob("*.pdf"))
            return [f.name for f in pdf_files]
        except Exception as e:
            print(f"Error listing materials: {e}")
            return []
    
    def read_pdf(self, filename: str, use_cache: bool = True) -> Optional[str]:
        """
        Read text content from a PDF file
        
        Args:
            filename: Name of the PDF file
            use_cache: Whether to use cached content
            
        Returns:
            Extracted text content or None if error
        """
        # Check cache
        if use_cache and filename in self._cache:
            return self._cache[filename]
        
        file_path = self.materials_dir / filename
        
        if not file_path.exists():
            print(f"File not found: {filename}")
            return None
        
        try:
            text_content = ""
            
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                # Extract text from each page
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text_content += page.extract_text() + "\n\n"
            
            # Cache the content
            self._cache[filename] = text_content
            
            return text_content
            
        except Exception as e:
            print(f"Error reading PDF {filename}: {e}")
            return None
    
    def get_all_materials_text(self, max_chars: int = 10000) -> str:
        """
        Get combined text from all PDF materials
        
        Args:
            max_chars: Maximum characters to return (to avoid token limits)
            
        Returns:
            Combined text from all materials
        """
        materials = self.list_materials()
        
        if not materials:
            return ""
        
        combined_text = "=== MATERI PEMBELAJARAN ===\n\n"
        total_chars = 0
        
        for material in materials:
            content = self.read_pdf(material)
            if content:
                # Add material with header
                material_text = f"## {material}\n\n{content}\n\n"
                
                # Check if adding this would exceed limit
                if total_chars + len(material_text) > max_chars:
                    # Add truncated version
                    remaining = max_chars - total_chars
                    if remaining > 200:
                        combined_text += material_text[:remaining] + "\n...(truncated)\n\n"
                    break
                
                combined_text += material_text
                total_chars += len(material_text)
        
        combined_text += "=== END MATERI ===\n\n"
        
        return combined_text if total_chars > 0 else ""
    
    def search_materials(self, query: str, max_results: int = 3) -> List[Dict[str, str]]:
        """
        Search for relevant content in materials based on query
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
            
        Returns:
            List of dicts with 'filename', 'excerpt', and 'relevance'
        """
        materials = self.list_materials()
        results = []
        
        query_lower = query.lower()
        
        for material in materials:
            content = self.read_pdf(material)
            if not content:
                continue
            
            content_lower = content.lower()
            
            # Simple keyword matching (can be enhanced with embeddings)
            if query_lower in content_lower:
                # Find excerpt around the query
                index = content_lower.find(query_lower)
                start = max(0, index - 200)
                end = min(len(content), index + 200)
                excerpt = content[start:end]
                
                # Count occurrences as relevance score
                relevance = content_lower.count(query_lower)
                
                results.append({
                    "filename": material,
                    "excerpt": f"...{excerpt}...",
                    "relevance": relevance
                })
        
        # Sort by relevance
        results.sort(key=lambda x: x['relevance'], reverse=True)
        
        return results[:max_results]
    
    def get_material_summary(self) -> str:
        """Get a summary of available materials"""
        materials = self.list_materials()
        
        if not materials:
            return "Tidak ada materi pembelajaran yang tersedia."
        
        summary = f"📚 Tersedia {len(materials)} materi pembelajaran:\n"
        for i, material in enumerate(materials, 1):
            summary += f"{i}. {material}\n"
        
        return summary
    
    def clear_cache(self):
        """Clear the content cache"""
        self._cache = {}


# Global instance
_reader_instance = None

def get_material_reader() -> MaterialReader:
    """Get or create global material reader instance"""
    global _reader_instance
    if _reader_instance is None:
        _reader_instance = MaterialReader()
    return _reader_instance
