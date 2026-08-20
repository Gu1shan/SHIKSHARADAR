"""
Concept mapping for Shiksha Radar.
Maps questions to concepts using rule-based lookup with embedding fallback.
"""
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np
from app.data.normalizer import normalize_answer


class ConceptMapper:
    """
    Three-tier concept mapping:
    1. Rule lookup (exact question_id match) - 100% accurate for known questions
    2. Embedding similarity - for unseen questions
    3. Flag for teacher review - below confidence threshold
    """
    
    def __init__(self, concept_map_df: pd.DataFrame, 
                 embedding_model=None,
                 embedding_threshold: float = 0.65):
        """
        Args:
            concept_map_df: DataFrame with question_id, concept, sub_concept
            embedding_model: SentenceTransformer model for embedding fallback
            embedding_threshold: Minimum cosine similarity for embedding match
        """
        self.concept_map_df = concept_map_df
        self.embedding_model = embedding_model
        self.embedding_threshold = embedding_threshold
        
        # Build rule-based lookup
        self.rule_lookup = concept_map_df.set_index("question_id")[["concept", "sub_concept"]].to_dict("index")
        
        # Pre-compute concept embeddings if model provided
        self.concept_embeddings = {}
        if self.embedding_model is not None:
            self._build_concept_embeddings()
    
    def _build_concept_embeddings(self):
        """Pre-compute embeddings for concept descriptions."""
        concept_descriptions = {
            "Fractions": "Fractions represent parts of a whole, including numerator and denominator, equivalent fractions, comparing fractions, adding and subtracting fractions",
            "Fractions_denominator_handling": "Finding common denominators, equivalent fractions, comparing fractions with different denominators",
            "Fractions_simplification": "Reducing fractions to lowest terms, greatest common factor, simplifying fractions",
            "Fractions_addition": "Adding fractions with like and unlike denominators",
            "Fractions_subtraction": "Subtracting fractions with like and unlike denominators",
            "Fractions_multiplication": "Multiplying fractions, numerator times numerator, denominator times denominator",
            "Fractions_comparison": "Comparing fractions, greater than, less than, equal to",
            "Decimals": "Decimal numbers, place value, tenths, hundredths, decimal operations",
            "Decimals_place_value": "Understanding decimal place value, tenths, hundredths, thousandths",
            "Decimals_addition_subtraction": "Adding and subtracting decimal numbers, aligning decimal points",
            "Decimals_multiplication": "Multiplying decimal numbers, counting decimal places",
            "Decimals_division": "Dividing decimal numbers, moving decimal points",
            "Algebra": "Algebraic thinking, patterns, variables, equations, signed numbers",
            "Algebra_patterns": "Identifying and extending number patterns, sequences",
            "Algebra_variables": "Using variables to represent unknown quantities, evaluating expressions",
            "Algebra_equations": "Solving simple linear equations, balancing equations",
            "Algebra_sign_rules": "Rules for positive and negative numbers, integer operations",
            "Geometry": "Geometric shapes, properties, area, perimeter, angles, symmetry",
            "Geometry_2d_shapes": "Two-dimensional shapes, polygons, circles, properties",
            "Geometry_3d_shapes": "Three-dimensional shapes, cubes, cuboids, spheres, cylinders, cones",
            "Geometry_area_perimeter": "Calculating area and perimeter of rectangles, squares, triangles",
            "Geometry_angles": "Types of angles, measuring angles, angle properties",
            "Geometry_symmetry": "Line symmetry, rotational symmetry, symmetric figures",
            "Measurement": "Measuring length, weight, capacity, time, unit conversions",
            "Measurement_length": "Measuring length, meters, centimeters, kilometers, conversions",
            "Measurement_weight": "Measuring weight, grams, kilograms, conversions",
            "Measurement_capacity": "Measuring capacity, liters, milliliters, conversions",
            "Measurement_time": "Measuring time, hours, minutes, seconds, conversions",
            "Data_Handling": "Data representation, tables, bar graphs, pictographs",
            "Data_Handling_tables": "Reading and interpreting data tables",
            "Data_Handling_bar_graphs": "Reading and interpreting bar graphs",
            "Data_Handling_pictographs": "Reading and interpreting pictographs",
        }
        
        for key, desc in concept_descriptions.items():
            self.concept_embeddings[key] = self.embedding_model.encode(desc)
    
    def map_question(self, question_id: str, question_text: str = "") -> Tuple[str, str, str, float]:
        """
        Map a question to concept and sub_concept.
        
        Returns:
            (concept, sub_concept, method, confidence)
            method: "rule", "embedding", or "unknown"
            confidence: 1.0 for rule, cosine similarity for embedding, 0.0 for unknown
        """
        # Tier 1: Rule-based lookup
        if question_id in self.rule_lookup:
            info = self.rule_lookup[question_id]
            return info["concept"], info["sub_concept"], "rule", 1.0
        
        # Tier 2: Embedding fallback
        if self.embedding_model is not None and question_text:
            concept, sub_concept, confidence = self._embedding_map(question_text)
            if confidence >= self.embedding_threshold:
                return concept, sub_concept, "embedding", confidence
        
        # Tier 3: Unknown
        return "Unknown", "Unknown", "unknown", 0.0
    
    def _embedding_map(self, question_text: str) -> Tuple[str, str, float]:
        """Map using embedding similarity."""
        question_embedding = self.embedding_model.encode(question_text)
        
        best_concept = "Unknown"
        best_sub_concept = "Unknown"
        best_similarity = 0.0
        
        for concept_key, concept_emb in self.concept_embeddings.items():
            similarity = self._cosine_similarity(question_embedding, concept_emb)
            if similarity > best_similarity:
                best_similarity = similarity
                if "_" in concept_key:
                    best_concept, best_sub_concept = concept_key.split("_", 1)
                else:
                    best_concept = concept_key
                    best_sub_concept = "general"
        
        return best_concept, best_sub_concept, best_similarity
    
    @staticmethod
    def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        """Compute cosine similarity between two vectors."""
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    def map_batch(self, question_ids: List[str], question_texts: List[str] = None) -> pd.DataFrame:
        """Map a batch of questions."""
        if question_texts is None:
            question_texts = [""] * len(question_ids)
        
        results = []
        for q_id, q_text in zip(question_ids, question_texts):
            concept, sub_concept, method, confidence = self.map_question(q_id, q_text)
            results.append({
                "question_id": q_id,
                "concept": concept,
                "sub_concept": sub_concept,
                "method": method,
                "confidence": confidence
            })
        
        return pd.DataFrame(results)


def load_concept_mapper(concept_map_path: str = None, 
                        use_embeddings: bool = False) -> ConceptMapper:
    """Factory function to create a ConceptMapper."""
    from app.data.loader import load_concept_map, SYNTHETIC_DIR
    from pathlib import Path
    
    if concept_map_path is None:
        concept_map_path = SYNTHETIC_DIR / "concept_map.csv"
    
    concept_map_df = load_concept_map(concept_map_path)
    
    embedding_model = None
    if use_embeddings:
        try:
            from sentence_transformers import SentenceTransformer
            embedding_model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")
        except ImportError:
            print("Warning: sentence-transformers not available, using rule-based only")
    
    return ConceptMapper(concept_map_df, embedding_model)


if __name__ == "__main__":
    from app.data.loader import load_all_synthetic
    
    students, questions, concept_map, responses = load_all_synthetic()
    
    mapper = load_concept_mapper()
    
    test_ids = questions["question_id"].head(10).tolist()
    test_texts = questions["text"].head(10).tolist()
    
    results = mapper.map_batch(test_ids, test_texts)
    print(results.to_string(index=False))