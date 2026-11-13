"""
RAG Faithfulness & Hallucination Guard Service (PACD-RAG)
=========================================================
Author: Sumith U (SRN: R24EA807) | 7th Sem B.Tech CSE (AI & ML), Section B, REVA University
Project: AI-Powered Smart Campus Intelligence & Student Success Platform

Implements automated evaluation of RAG responses against retrieved syllabus chunks.
Evaluates Faithfulness, Context Recall, Semantic Grounding, and Hallucination Risk
before any AI-synthesized remedial study plan is presented to students or faculty.
"""

import re
import math
from typing import Dict, Any, List, Set

class RAGFaithfulnessGuard:
    def __init__(self, faithfulness_threshold: float = 0.65):
        self.faithfulness_threshold = faithfulness_threshold
        # Stopwords and generic pedagogical vocabulary to avoid penalizing standard study instructions
        self.stopwords = {
            "the", "and", "is", "in", "to", "of", "a", "an", "with", "for", "on", "as",
            "at", "by", "this", "that", "it", "from", "are", "be", "was", "will", "or",
            "student", "study", "day", "plan", "hour", "hours", "module", "step", "steps",
            "review", "practice", "implement", "solve", "understanding", "learn", "basics",
            "focus", "notes", "questions", "key", "topics", "lecture", "material", "test"
        }

    def _tokenize_terms(self, text: str) -> Set[str]:
        """Extract meaningful domain terms, tokens, and technical keywords."""
        tokens = re.findall(r'[a-zA-Z0-9_\-]+', text.lower())
        return {t for t in tokens if len(t) > 2 and t not in self.stopwords}

    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extracts technical bi-grams and noun phrases."""
        words = re.findall(r'[a-zA-Z0-9_\-]+', text.lower())
        bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1) 
                   if words[i] not in self.stopwords and words[i+1] not in self.stopwords]
        return bigrams

    def evaluate_grounding(
        self,
        query: str,
        retrieved_contexts: List[str],
        generated_response: str
    ) -> Dict[str, Any]:
        """
        Calculates Faithfulness, Context Overlap, and Hallucination Index.
        """
        if not retrieved_contexts:
            return {
                "faithfulness_score": 0.20,
                "hallucination_risk": "HIGH",
                "is_grounded": False,
                "verdict": "REJECT: No retrieved syllabus contexts provided.",
                "details": {"context_count": 0}
            }

        combined_context = " ".join(retrieved_contexts).lower()
        context_tokens = self._tokenize_terms(combined_context)
        context_bigrams = set(self._extract_key_phrases(combined_context))

        resp_tokens = self._tokenize_terms(generated_response)
        resp_bigrams = set(self._extract_key_phrases(generated_response))

        if not resp_tokens:
            return {
                "faithfulness_score": 0.0,
                "hallucination_risk": "HIGH",
                "is_grounded": False,
                "verdict": "EMPTY_RESPONSE"
            }

        # 1. Lexical and Concept Overlap Ratio
        supported_tokens = resp_tokens.intersection(context_tokens)
        unsupported_tokens = resp_tokens - context_tokens
        token_overlap_ratio = len(supported_tokens) / len(resp_tokens)

        # 2. Keyphrase / technical term alignment
        if resp_bigrams:
            supported_bigrams = resp_bigrams.intersection(context_bigrams)
            bigram_overlap_ratio = len(supported_bigrams) / len(resp_bigrams)
        else:
            bigram_overlap_ratio = token_overlap_ratio

        # 3. Faithfulness Composite Score (0.0 to 1.0)
        faithfulness = (0.60 * token_overlap_ratio) + (0.40 * bigram_overlap_ratio)
        faithfulness = float(round(min(1.0, max(0.0, faithfulness * 1.25)), 4))

        # 4. Hallucination Risk Classification
        if faithfulness >= 0.75:
            hallucination_risk = "LOW"
            verdict = "VERIFIED_FAITHFUL"
        elif faithfulness >= self.faithfulness_threshold:
            hallucination_risk = "MODERATE"
            verdict = "ACCEPTABLE_WITH_PROVENANCE"
        else:
            hallucination_risk = "HIGH"
            verdict = "REJECT_OR_REGENERATE"

        # 5. Extract citation sources from retrieved contexts
        citations = []
        for idx, ctx in enumerate(retrieved_contexts):
            match_terms = [t for t in self._tokenize_terms(ctx) if t in resp_tokens]
            if len(match_terms) >= 3:
                citations.append({
                    "context_id": f"CHUNK_{idx+1}",
                    "supported_concepts": list(set(match_terms))[:5],
                    "excerpt": ctx[:140] + ("..." if len(ctx) > 140 else "")
                })

        return {
            "faithfulness_score": faithfulness,
            "faithfulness_threshold": self.faithfulness_threshold,
            "hallucination_risk": hallucination_risk,
            "is_grounded": bool(faithfulness >= self.faithfulness_threshold),
            "verdict": verdict,
            "metrics": {
                "token_grounding_ratio": round(token_overlap_ratio, 4),
                "keyphrase_grounding_ratio": round(bigram_overlap_ratio, 4),
                "total_response_terms": len(resp_tokens),
                "grounded_terms_count": len(supported_tokens),
                "unsupported_terms_sample": list(unsupported_tokens)[:8]
            },
            "citations": citations,
            "safeguard_recommendation": (
                "Response is strongly anchored in verified REVA University syllabus corpus."
                if hallucination_risk == "LOW"
                else "Response contains external concepts not explicitly matched in syllabus chunks."
            )
        }

if __name__ == "__main__":
    guard = RAGFaithfulnessGuard()
    sample_contexts = [
        "Module 2: Neural Networks. Backpropagation algorithm requires chain rule of differentiation. Gradient descent updates weights using learning rate.",
        "Loss computation in Backpropagation: Mean Squared Error and Cross-Entropy loss functions. Forward pass computes activations."
    ]
    sample_response = (
        "Day 1: Review differentiation chain rule. Day 2: Implement forward pass and compute loss function. "
        "Day 3: Practice gradient descent weight updates and backpropagation error back-propagation equations."
    )
    result = guard.evaluate_grounding("What are prerequisites for backpropagation?", sample_contexts, sample_response)
    import json
    print(json.dumps(result, indent=2))
