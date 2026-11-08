"""
Multi-level Chunked Code Hashing for Semantic Code Comparison

Implements multi-level chunked code hashing for semantic code comparison:
- File-level hash (overall structure)
- Function/class-level chunks (semantic units)
- Statement-level chunks (fine-grained)
- Import/dependency signatures
- Control flow patterns
- CST-based structural fingerprints
"""

import hashlib
import ast
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set, Tuple
from collections import defaultdict, Counter
import hashlib

try:
    import libcst as cst
    HAVE_LIBCST = True
except ImportError:
    HAVE_LIBCST = False


@dataclass
class CodeChunk:
    """Represents a semantic chunk of code."""
    chunk_type: str  # function, class, method, statement, import, module
    name: str
    content: str
    hash: str
    parent_hash: Optional[str] = None
    line_start: int = 0
    line_end: int = 0
    metadata: Dict = field(default_factory=dict)


@dataclass
class FileHashProfile:
    """Multi-level hash profile for a file."""
    file_path: str = ""
    file_hash: str = ""
    module_hash: str = ""
    chunks: List['CodeChunk'] = field(default_factory=list)
    import_signature: str = ""
    control_flow_hash: str = ""
    structural_hash: str = ""
    complexity_score: float = 0.0


class MultiLevelCodeHasher:
    """
    Multi-level chunked code hashing for semantic code comparison.
    
    Generates hashes at multiple granularities:
    1. File-level: Overall file hash
    2. Module-level: Import/dependency signature
    3. Structural: AST structural hash
    4. Chunk-level: Function/class/method hashes
    5. Control flow patterns
    """
    
    def __init__(self, chunk_size: int = 10, min_chunk_size: int = 3):
        self.chunk_size = chunk_size
        self.min_chunk_size = min_chunk_size
    
    def hash_file(self, content: str, filepath: str = "") -> 'FileHashProfile':
        """Generate multi-level hash profile for a file."""
        profile = FileHashProfile(file_path=filepath)
        
        if not content.strip():
            return profile
        
        # 1. File-level hash (full content)
        profile.file_hash = self._hash_content(content)
        
        # Parse AST once
        try:
            tree = ast.parse(content)
        except SyntaxError:
            # If Python parsing fails, return basic profile
            profile.file_hash = self._hash_content(content)
            return profile
        
        # 2. Module-level import/dependency signature
        profile.import_signature = self._extract_import_signature(content)
        
        # 3. Structural hash (AST structure)
        profile.structural_hash = self._compute_structural_hash(content)
        
        # 4. Control flow hash
        profile.control_flow_hash = self._extract_control_flow_hash(content)
        
        # 5. Extract semantic chunks (functions, classes, methods)
        chunks = self._extract_semantic_chunks(content)
        profile.chunks = chunks
        
        # 6. Module-level structural hash (from chunks)
        profile.module_hash = self._compute_module_hash(chunks)
        
        # 7. Complexity score
        profile.complexity_score = self._compute_complexity_score(chunks)
        
        return profile
    
    def _hash_content(self, content: str) -> str:
        """Generate SHA256 hash of content."""
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def _extract_import_signature(self, content: str) -> str:
        """Extract import/dependency signature."""
        try:
            tree = ast.parse(content)
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name.split('.')[0])
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        imports.append(f"{module}.{alias.name}")
            
            imports.sort()
            return hashlib.sha256(",".join(imports).encode()).hexdigest()[:16]
        except:
            return ""
    
    def _compute_structural_hash(self, content: str) -> str:
        """Compute structural hash from AST structure."""
        try:
            tree = ast.parse(content)
            # Generate structural representation
            struct = []
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, 
                                   ast.ClassDef, ast.If, ast.For, ast.While,
                                   ast.Try, ast.With, ast.Try)):
                    struct.append(type(node).__name__)
            struct_str = "|".join(struct)
            return hashlib.sha256(struct_str.encode()).hexdigest()[:16]
        except:
            return ""
    
    def _extract_control_flow_hash(self, content: str) -> str:
        """Extract control flow pattern hash."""
        try:
            tree = ast.parse(content)
            patterns = []
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.IfExp, ast.For, ast.While, 
                                    ast.Try, ast.TryStar, ast.With, 
                                    ast.Match, ast.Raise, ast.Assert)):
                    patterns.append(type(node).__name__)
                elif isinstance(node, (ast.Return, ast.Yield, ast.YieldFrom)):
                    patterns.append(type(node).__name__)
            return hashlib.sha256("|".join(patterns).encode()).hexdigest()[:16]
        except:
            return ""
    
    def _extract_semantic_chunks(self, content: str) -> List['CodeChunk']:
        """Extract semantic chunks (functions, classes, methods, imports)."""
        chunks = []
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    chunk = self._extract_function_chunk(node, content)
                    chunks.append(chunk)
                elif isinstance(node, ast.ClassDef):
                    chunk = self._extract_class_chunk(node, content)
                    chunks.append(chunk)
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    chunk = self._extract_import_chunk(node, content)
                    chunks.append(chunk)
        except:
            pass
        return chunks
    
    def _extract_function_chunk(self, node: ast.FunctionDef, content: str) -> 'CodeChunk':
        """Extract function chunk with hash."""
        lines = content.split('\n')
        start = node.lineno - 1
        end = node.end_lineno if hasattr(node, 'end_lineno') else start
        chunk_content = '\n'.join(lines[start:end+1])
        
        chunk_hash = hashlib.sha256(chunk_content.encode()).hexdigest()[:16]
        
        # Extract metadata
        args = [arg.arg for arg in node.args.args]
        defaults = len(node.args.defaults) if node.args.defaults else 0
        has_type_hints = bool(node.returns or any(a.annotation for a in node.args.args))
        
        decorators = []
        for d in node.decorator_list:
            if isinstance(d, ast.Name):
                decorators.append(d.id)
            elif isinstance(d, ast.Call):
                if isinstance(d.func, ast.Name):
                    decorators.append(d.func.id)
            decorators = decorators
        
        return CodeChunk(
            chunk_type="function",
            name=node.name,
            content=chunk_content,
            hash=chunk_hash,
            line_start=node.lineno,
            line_end=node.end_lineno if hasattr(node, 'end_lineno') else node.lineno,
            metadata={
                "args": args,
                "arg_count": len(args),
                "default_count": defaults,
                "has_type_hints": has_type_hints,
                "is_async": isinstance(node, ast.AsyncFunctionDef),
                "decorators": decorators
            }
        )
    
    def _extract_class_chunk(self, node: ast.ClassDef, content: str) -> 'CodeChunk':
        """Extract class chunk with hash."""
        lines = content.split('\n')
        start = node.lineno - 1
        end = node.end_lineno if hasattr(node, 'end_lineno') else start
        chunk_content = '\n'.join(lines[start:end+1])
        
        chunk_hash = hashlib.sha256(chunk_content.encode()).hexdigest()[:16]
        
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(base.attr)
        
        methods = []
        for n in node.body:
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                methods.append(n.name)
        
        decorators = []
        for d in node.decorator_list:
            if isinstance(d, ast.Name):
                decorators.append(d.id)
            elif isinstance(d, ast.Call):
                if isinstance(d.func, ast.Name):
                    decorators.append(d.func.id)
            decorators = decorators
        
        return CodeChunk(
            chunk_type="class",
            name=node.name,
            content=chunk_content,
            hash=chunk_hash,
            line_start=node.lineno,
            line_end=node.end_lineno if hasattr(node, 'end_lineno') else node.lineno,
            metadata={
                "bases": bases,
                "methods": methods,
                "decorators": decorators
            }
        )
    
    def _extract_import_chunk(self, node: ast.AST, content: str) -> 'CodeChunk':
        """Extract import chunk."""
        lines = content.split('\n')
        start = node.lineno - 1
        end = node.end_lineno if hasattr(node, 'end_lineno') else start
        chunk_content = '\n'.join(lines[start:end+1])
        
        imports = []
        if isinstance(node, ast.Import):
            imports = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            imports = [f"{module}.{alias.name}" for alias in node.names]
        
        chunk_hash = hashlib.sha256('\n'.join(imports).encode()).hexdigest()[:16]
        
        return CodeChunk(
            chunk_type="import",
            name="imports",
            content=chunk_content,
            hash=chunk_hash,
            line_start=node.lineno,
            line_end=end,
            metadata={"imports": imports}
        )
    
    def _get_decorator_name(self, decorator: ast.AST) -> str:
        """Extract decorator name."""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name):
                return decorator.func.id
            elif isinstance(decorator.func, ast.Attribute):
                return decorator.func.attr
        return "unknown"
    
    def _get_base_name(self, base: ast.AST) -> str:
        """Extract base class name."""
        if isinstance(base, ast.Name):
            return base.id
        elif isinstance(base, ast.Attribute):
            return base.attr
        return "unknown"
    
    def _compute_module_hash(self, chunks: List['CodeChunk']) -> str:
        """Compute module-level hash from chunks."""
        chunk_hashes = sorted([c.hash for c in chunks])
        return hashlib.sha256("|".join(chunk_hashes).encode()).hexdigest()[:16]
    
    def _compute_complexity_score(self, chunks: List['CodeChunk']) -> float:
        """Compute complexity score based on chunks."""
        if not chunks:
            return 0.0
        
        total = len(chunks)
        functions = sum(1 for c in chunks if c.chunk_type == "function")
        classes = sum(1 for c in chunks if c.chunk_type == "class")
        imports = sum(1 for c in chunks if c.chunk_type == "import")
        
        # Weighted complexity
        score = (functions * 1.0 + classes * 2.0 + imports * 0.5) / max(len(chunks), 1)
        return min(score, 10.0)
    
    def compute_similarity(self, profile1: 'FileHashProfile', profile2: 'FileHashProfile') -> float:
        """Compute similarity between two file profiles."""
        if not profile1.chunks and not profile2.chunks:
            return 1.0
        if not profile1.chunks or not profile2.chunks:
            return 0.0
        
        # Compare chunk hashes
        hashes1 = set(c.hash for c in profile1.chunks)
        hashes2 = set(c.hash for c in profile2.chunks)
        
        intersection = len(hashes1 & hashes2)
        union = len(hashes1 | hashes2)
        chunk_sim = intersection / union if union > 0 else 0.0
        
        # Module hash similarity
        mod_sim = 1.0 if profile1.module_hash == profile2.module_hash else 0.0
        
        # Import signature similarity
        import_sim = 1.0 if profile1.import_signature == profile2.import_signature else 0.0
        
        # Structural hash similarity
        struct_sim = 1.0 if profile1.structural_hash == profile2.structural_hash else 0.0
        
        # Control flow similarity
        flow_sim = 1.0 if profile1.control_flow_hash == profile2.control_flow_hash else 0.0
        
        # Weighted combination
        weights = {
            "chunks": 0.40,
            "module": 0.20,
            "imports": 0.15,
            "structural": 0.15,
            "control_flow": 0.10
        }
        
        scores = {
            "chunks": chunk_sim,
            "module": mod_sim,
            "imports": import_sim,
            "structural": struct_sim,
            "control_flow": flow_sim
        }
        
        total = sum(weights[k] * scores[k] for k in weights)
        total_weight = sum(weights.values())
        return sum(weights[k] * scores[k] for k in weights) / sum(weights.values())
