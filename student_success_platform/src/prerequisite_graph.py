"""
=============================================================================
PREREQUISITE KNOWLEDGE GRAPH MODULE (PACD-RAG STEP 4)
AI-Powered Agentic Smart Campus Intelligence & Student Success Platform
Author: Sumith U (SRN: R24EA807), 7th Sem B.Tech CSE (AI & ML), REVA University
=============================================================================
This module constructs, validates, and queries a Directed Acyclic Graph (DAG)
of academic curriculum concepts. It models prerequisite dependencies to:
  1. Identify prerequisite dependencies (Prerequisite -> Dependent).
  2. Perform topological sort for valid pedagogical learning sequences.
  3. Map formative learner quiz/assessment evidence to concept nodes.
  4. Trace root-cause prerequisite deficits when a student faces difficulty.
  5. Export structured retrieval plans for downstream RAG (Part 5) and
     Agentic Coaching (Part 6).
=============================================================================
"""

import os
import json
import logging
from typing import List, Dict, Set, Any, Optional, Tuple
import networkx as nx
import matplotlib.pyplot as plt

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class PrerequisiteKnowledgeGraph:
    """
    Curriculum Knowledge Graph modeling course concepts and directed prerequisite dependencies.
    Enforces Directed Acyclic Graph (DAG) constraints for valid pedagogical sequences.
    """

    def __init__(self, json_path: Optional[str] = None):
        """
        Initialize the Knowledge Graph.
        
        Args:
            json_path: Path to the concept_prerequisites.json file.
        """
        self.graph = nx.DiGraph()
        self.course_metadata: Dict[str, Any] = {}
        self.concept_catalog: Dict[str, Dict[str, Any]] = {}
        
        if json_path:
            self.load_from_json(json_path)

    def load_from_json(self, json_path: str) -> None:
        """
        Load concepts and directed prerequisite edges from a JSON file.
        
        Edge direction convention:
            source (Prerequisite) ----> target (Dependent Concept)
            Example: "Partial Derivatives" -> "Chain Rule" -> "Backpropagation"
        """
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Prerequisite JSON file not found: {json_path}")

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.course_metadata = data.get("course_metadata", {})
        self.graph.clear()
        self.concept_catalog.clear()

        # Step 1: Add concept nodes with rich metadata
        concepts = data.get("concepts", [])
        for c in concepts:
            c_id = c["id"]
            self.concept_catalog[c_id] = c
            self.graph.add_node(
                c_id,
                name=c.get("name", c_id),
                unit=c.get("unit", "General"),
                level=c.get("level", "Foundational"),
                bloom_taxonomy=c.get("bloom_taxonomy", "Understand"),
                competencies=c.get("competencies", []),
                primary_formula=c.get("primary_formula", ""),
                syllabus_slide_ref=c.get("syllabus_slide_ref", ""),
                estimated_study_minutes=c.get("estimated_study_minutes", 45),
                description=c.get("description", "")
            )

        # Step 2: Add directed prerequisite edges
        prerequisites = data.get("prerequisites", [])
        for edge in prerequisites:
            src = edge["source"]
            tgt = edge["target"]
            rel_type = edge.get("relationship_type", "prerequisite")
            weight = edge.get("cognitive_weight", 0.90)
            desc = edge.get("description", edge.get("pedagogical_justification", ""))
            
            self.graph.add_edge(
                src,
                tgt,
                relationship_type=rel_type,
                weight=weight,
                description=desc
            )

        logger.info(
            f"Loaded {self.graph.number_of_nodes()} concepts and "
            f"{self.graph.number_of_edges()} prerequisite edges from {json_path}"
        )

    # =========================================================================
    # GRAPH INTEGRITY VALIDATION
    # =========================================================================

    def validate_graph(self) -> Dict[str, Any]:
        """
        Perform rigorous structural validation of the concept graph:
          1. Verify all edge endpoints exist in concept inventory.
          2. Check for self-loops and multi-edge redundancies.
          3. Verify Directed Acyclic Graph (DAG) property (zero cycles).
          4. Confirm topological sort existence.
          5. Identify isolated (disconnected) concepts if any.

        Returns:
            Dict containing validation status, cycle list, and topological order.
        """
        results: Dict[str, Any] = {
            "is_valid_dag": False,
            "has_cycles": False,
            "cycle_details": [],
            "unknown_endpoints": [],
            "isolated_concepts": [],
            "topological_order": [],
            "num_nodes": self.graph.number_of_nodes(),
            "num_edges": self.graph.number_of_edges()
        }

        # 1. Unknown endpoint check
        for u, v in self.graph.edges():
            if u not in self.concept_catalog:
                results["unknown_endpoints"].append(f"Source concept '{u}' not in inventory")
            if v not in self.concept_catalog:
                results["unknown_endpoints"].append(f"Target concept '{v}' not in inventory")

        # 2. Cycle detection
        is_dag = nx.is_directed_acyclic_graph(self.graph)
        results["is_valid_dag"] = is_dag

        if not is_dag:
            results["has_cycles"] = True
            # Find simple cycles
            cycles = list(nx.simple_cycles(self.graph))
            results["cycle_details"] = cycles
            logger.error(f"Validation FAILED: Graph contains cycles: {cycles}")
        else:
            results["has_cycles"] = False
            # 3. Generate valid pedagogical topological learning sequence
            results["topological_order"] = list(nx.topological_sort(self.graph))
            logger.info("Validation PASSED: Graph is a strictly valid Directed Acyclic Graph (DAG).")

        # 4. Isolated nodes
        isolated = list(nx.isolates(self.graph))
        results["isolated_concepts"] = isolated
        if isolated:
            logger.warning(f"Graph has {len(isolated)} isolated concept(s): {isolated}")

        return results

    # =========================================================================
    # REUSABLE GRAPH QUERY FUNCTIONS
    # =========================================================================

    def get_direct_prerequisites(self, concept_id: str) -> List[str]:
        """
        Return the immediate 1-hop prerequisites required before studying this concept.
        In edge direction (u -> v), u is a direct prerequisite of v.
        """
        self._check_concept_exists(concept_id)
        return list(self.graph.predecessors(concept_id))

    def get_all_prerequisites(self, concept_id: str) -> Set[str]:
        """
        Return the complete transitive ancestral closure of prerequisites.
        All concepts that must be learned prior to reaching this concept.
        """
        self._check_concept_exists(concept_id)
        return nx.ancestors(self.graph, concept_id)

    def get_dependent_concepts(self, concept_id: str) -> List[str]:
        """
        Return immediate downstream concepts that depend directly on this concept.
        """
        self._check_concept_exists(concept_id)
        return list(self.graph.successors(concept_id))

    def get_all_dependents(self, concept_id: str) -> Set[str]:
        """
        Return all downstream concepts enabled by mastering this concept (descendants).
        """
        self._check_concept_exists(concept_id)
        return nx.descendants(self.graph, concept_id)

    def get_learning_sequence(self, concept_ids: Optional[List[str]] = None) -> List[str]:
        """
        Return a valid pedagogical learning sequence (topologically sorted).
        If concept_ids is provided, returns the topological order for that subset.
        """
        if concept_ids is None:
            return list(nx.topological_sort(self.graph))

        # Validate subset
        for cid in concept_ids:
            self._check_concept_exists(cid)

        # Induce subgraph and sort
        subgraph = self.graph.subgraph(concept_ids)
        return list(nx.topological_sort(subgraph))

    def get_critical_path(self, source_concept_id: str, target_concept_id: str) -> List[str]:
        """
        Compute the longest directed prerequisite path (critical learning spine)
        between an upstream foundation concept and a downstream target concept.
        """
        self._check_concept_exists(source_concept_id)
        self._check_concept_exists(target_concept_id)

        try:
            all_paths = list(nx.all_simple_paths(self.graph, source_concept_id, target_concept_id))
            if not all_paths:
                return []
            # Return path with maximum cognitive steps
            return max(all_paths, key=len)
        except Exception:
            return []

    def get_concept_info(self, concept_id: str) -> Dict[str, Any]:
        """Retrieve full metadata for a specific concept."""
        self._check_concept_exists(concept_id)
        info = dict(self.concept_catalog[concept_id])
        info["direct_prerequisites"] = self.get_direct_prerequisites(concept_id)
        info["all_prerequisites"] = sorted(list(self.get_all_prerequisites(concept_id)))
        info["direct_dependents"] = self.get_dependent_concepts(concept_id)
        return info

    # =========================================================================
    # LEARNER EVIDENCE & DEFICIT TRACING
    # =========================================================================

    def map_learner_evidence(
        self,
        evidence_dict: Dict[str, float],
        review_threshold: float = 0.60
    ) -> Dict[str, Any]:
        """
        Map student assessment evidence (quiz scores / mastery estimates) to concepts.
        
        Note on Pedagogy:
          A score below the threshold indicates formative difficulty requiring
          concept review; it is never treated as a permanent label of student ability.

        Args:
            evidence_dict: Mapping of concept_id -> score (0.0 to 1.0, or 0 to 100).
            review_threshold: Normalized threshold below which review is recommended.

        Returns:
            Structured diagnostic summary.
        """
        diagnostics = {
            "proficient_concepts": [],
            "needs_review_concepts": [],
            "concept_scores": {},
            "threshold_used": review_threshold
        }

        for cid, raw_score in evidence_dict.items():
            if cid not in self.concept_catalog:
                logger.warning(f"Concept '{cid}' in evidence not found in curriculum graph. Skipping.")
                continue

            # Normalize to 0.0 - 1.0 if entered as 0 - 100
            score = raw_score / 100.0 if raw_score > 1.0 else raw_score
            diagnostics["concept_scores"][cid] = round(score, 3)

            concept_name = self.concept_catalog[cid]["name"]
            item = {
                "id": cid,
                "name": concept_name,
                "score": round(score, 3),
                "unit": self.concept_catalog[cid].get("unit", "")
            }

            if score < review_threshold:
                item["status"] = "Needs Review"
                diagnostics["needs_review_concepts"].append(item)
            else:
                item["status"] = "Proficient"
                diagnostics["proficient_concepts"].append(item)

        return diagnostics

    def calculate_prerequisite_gap_score(
        self,
        target_concept_id: str,
        mastery_evidence: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Compute depth-weighted Prerequisite Gap Score (PGS) for a target concept:
            PGS(c) = sum_{a in Ancestors(c)} [ 1 / (depth(a, c) + 1) * (1.0 - Mastery(a)) ]

        Args:
            target_concept_id: Target concept identifier
            mastery_evidence: Dict of concept_id -> normalized mastery score (0.0 to 1.0)

        Returns:
            Dict containing composite PGS, ancestral breakdown, and normalized risk tier.
        """
        self._check_concept_exists(target_concept_id)
        ancestors = self.get_all_prerequisites(target_concept_id)
        
        breakdown = []
        total_pgs = 0.0

        for a in ancestors:
            # Shortest directed distance from ancestor a to target_concept_id
            try:
                depth = nx.shortest_path_length(self.graph, a, target_concept_id)
            except Exception:
                depth = 1

            # Default mastery score is 0.50 if unobserved, or student's verified score
            raw_mastery = mastery_evidence.get(a, 0.50)
            mastery = raw_mastery / 100.0 if raw_mastery > 1.0 else raw_mastery
            mastery = min(1.0, max(0.0, mastery))
            
            deficit = 1.0 - mastery
            depth_weight = 1.0 / (depth + 1.0)
            node_penalty = depth_weight * deficit
            total_pgs += node_penalty

            breakdown.append({
                "ancestor_id": a,
                "ancestor_name": self.concept_catalog[a]["name"],
                "graph_depth": depth,
                "mastery_score": round(mastery, 3),
                "deficit": round(deficit, 3),
                "depth_weight": round(depth_weight, 3),
                "penalty_contribution": round(node_penalty, 4)
            })

        # Sort breakdown by penalty contribution descending
        breakdown.sort(key=lambda x: x["penalty_contribution"], reverse=True)
        max_possible_pgs = sum(1.0 / (item["graph_depth"] + 1.0) for item in breakdown) if breakdown else 1.0
        normalized_pgs = round(total_pgs / max(0.001, max_possible_pgs), 4)

        risk_tier = "CRITICAL" if normalized_pgs >= 0.55 else ("MODERATE" if normalized_pgs >= 0.25 else "LOW")

        return {
            "target_concept_id": target_concept_id,
            "target_concept_name": self.concept_catalog[target_concept_id]["name"],
            "raw_pgs_score": round(total_pgs, 4),
            "normalized_pgs_score": normalized_pgs,
            "risk_tier": risk_tier,
            "ancestor_count": len(ancestors),
            "ancestral_gap_breakdown": breakdown
        }

    def find_root_cause_bottleneck(
        self,
        target_concept_id: str,
        weak_concept_ids: List[str]
    ) -> Optional[Dict[str, Any]]:
        """
        Identifies the upstream ancestor bottleneck concept that blocks the maximum number
        of downstream weak concepts along the critical path to target_concept_id.
        """
        self._check_concept_exists(target_concept_id)
        ancestors = self.get_all_prerequisites(target_concept_id)
        relevant_weak = set(weak_concept_ids).intersection(ancestors)

        if not relevant_weak:
            return None

        bottlenecks = []
        for a in relevant_weak:
            descendants = self.get_all_dependents(a)
            blocked_weak_downstream = descendants.intersection(relevant_weak)
            bottlenecks.append({
                "concept_id": a,
                "name": self.concept_catalog[a]["name"],
                "blocked_downstream_count": len(blocked_weak_downstream),
                "blocked_concepts": list(blocked_weak_downstream)
            })

        # Bottleneck with maximum blocked downstream nodes is the primary root cause
        bottlenecks.sort(key=lambda x: x["blocked_downstream_count"], reverse=True)
        primary = bottlenecks[0] if bottlenecks else None
        return primary

    def trace_prerequisite_gaps(
        self,
        target_concept_id: str,
        weak_concept_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Trace root-cause prerequisite gaps for a difficult target concept.
        
        Workflow:
          1. Retrieve all upstream prerequisite ancestors of target_concept_id.
          2. Find intersection between weak concepts and the target's ancestors.
          3. Sort these prerequisite deficits in valid pedagogical topological order.
          4. Return clear, non-punitive learning pathway recommendations with Open Knowledge Format metadata.
        """
        self._check_concept_exists(target_concept_id)

        target_name = self.concept_catalog[target_concept_id]["name"]
        ancestors = self.get_all_prerequisites(target_concept_id)
        
        # Identify weak concepts that are genuine prerequisites of this target
        relevant_weak_set = set(weak_concept_ids).intersection(ancestors)
        unrelated_weak_set = set(weak_concept_ids).difference(ancestors)

        # Order the relevant prerequisite gaps topologically
        if relevant_weak_set:
            ordered_gaps = self.get_learning_sequence(list(relevant_weak_set))
        else:
            ordered_gaps = []

        # Find primary root-cause bottleneck
        bottleneck = self.find_root_cause_bottleneck(target_concept_id, weak_concept_ids)

        # Build simulated evidence dict for PGS calculation
        simulated_evidence = {cid: 0.35 for cid in weak_concept_ids}
        pgs_eval = self.calculate_prerequisite_gap_score(target_concept_id, simulated_evidence)

        # Build step-by-step remediation plan with rich OKF metadata
        remediation_steps = []
        for step_num, cid in enumerate(ordered_gaps, start=1):
            c_meta = self.concept_catalog[cid]
            remediation_steps.append({
                "step": step_num,
                "concept_id": cid,
                "name": c_meta["name"],
                "unit": c_meta.get("unit", ""),
                "level": c_meta.get("level", ""),
                "bloom_taxonomy": c_meta.get("bloom_taxonomy", "Understand"),
                "competencies": c_meta.get("competencies", []),
                "primary_formula": c_meta.get("primary_formula", ""),
                "syllabus_slide_ref": c_meta.get("syllabus_slide_ref", ""),
                "estimated_study_minutes": c_meta.get("estimated_study_minutes", 45),
                "description": c_meta.get("description", "")
            })

        # Pedagogical explanation
        if ordered_gaps:
            names_seq = " -> ".join([self.concept_catalog[cid]["name"] for cid in ordered_gaps])
            bottleneck_text = f" Primary foundational blocker identified at '{bottleneck['name']}'." if bottleneck else ""
            explanation = (
                f"To master '{target_name}', the student should first reinforce "
                f"the unmastered foundational prerequisite(s): {names_seq}.{bottleneck_text} "
                f"Reviewing in this sequence builds necessary cognitive scaffolding."
            )
        else:
            explanation = (
                f"No foundational prerequisite deficits detected for '{target_name}'. "
                f"The student is ready to focus directly on '{target_name}' practice exercises."
            )

        return {
            "target_concept": {
                "id": target_concept_id,
                "name": target_name,
                "unit": self.concept_catalog[target_concept_id].get("unit", ""),
                "bloom_taxonomy": self.concept_catalog[target_concept_id].get("bloom_taxonomy", "Apply"),
                "primary_formula": self.concept_catalog[target_concept_id].get("primary_formula", ""),
                "syllabus_slide_ref": self.concept_catalog[target_concept_id].get("syllabus_slide_ref", "")
            },
            "prerequisite_gap_score": pgs_eval["normalized_pgs_score"],
            "risk_tier": pgs_eval["risk_tier"],
            "root_cause_bottleneck": bottleneck,
            "total_upstream_prerequisites": len(ancestors),
            "diagnosed_prerequisite_gaps": ordered_gaps,
            "remediation_pathway": remediation_steps,
            "unrelated_weak_concepts": list(unrelated_weak_set),
            "pedagogical_explanation": explanation
        }

    # =========================================================================
    # INTEGRATION PAYLOAD GENERATORS (FOR RAG & MULTI-AGENT COACH)
    # =========================================================================

    def get_rag_retrieval_plan(
        self,
        target_concept_id: str,
        weak_concept_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Generate structured retrieval keywords and document targets for Part 5 RAG.
        Ensures RAG fetches slides/notes for the root-cause prerequisite concepts first,
        rather than just retrieving target concept slides.
        """
        gap_analysis = self.trace_prerequisite_gaps(target_concept_id, weak_concept_ids)
        retrieval_queries = []

        # First priority: Root-cause prerequisite gaps in learning order
        for step in gap_analysis["remediation_pathway"]:
            retrieval_queries.append({
                "priority": "HIGH_PREREQUISITE",
                "concept_id": step["concept_id"],
                "query": f"{step['name']} core concepts foundational review",
                "module_target": step["unit"]
            })

        # Second priority: Target concept itself
        target = gap_analysis["target_concept"]
        retrieval_queries.append({
            "priority": "TARGET_APPLICATION",
            "concept_id": target["id"],
            "query": f"{target['name']} worked examples and practical applications",
            "module_target": target["unit"]
        })

        return {
            "target_concept_id": target_concept_id,
            "num_retrieval_targets": len(retrieval_queries),
            "ordered_retrieval_plan": retrieval_queries
        }

    def get_agent_coach_payload(
        self,
        student_id: str,
        target_concept_id: str,
        weak_concept_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Generate structured intervention payload for the Part 6 AI Student Coach.
        """
        gap_analysis = self.trace_prerequisite_gaps(target_concept_id, weak_concept_ids)
        return {
            "student_id": student_id,
            "intervention_type": "PREREQUISITE_COGNITIVE_REMEDIATION",
            "target_concept": gap_analysis["target_concept"]["name"],
            "prerequisite_gap_count": len(gap_analysis["diagnosed_prerequisite_gaps"]),
            "recommended_learning_sequence": [
                s["name"] for s in gap_analysis["remediation_pathway"]
            ],
            "coach_guidance_text": gap_analysis["pedagogical_explanation"],
            "status": "ACTIONABLE"
        }

    # =========================================================================
    # OPEN KNOWLEDGE FORMAT (OKF) EXPORT APIS
    # =========================================================================

    def export_to_okf_jsonld(self) -> Dict[str, Any]:
        """
        Export curriculum graph into Open Knowledge Format (OKF) standard JSON-LD
        for semantic web inter-operability, LMS portability, and academic data sharing.
        """
        nodes_ld = []
        for c_id, c in self.concept_catalog.items():
            nodes_ld.append({
                "@id": f"concept:{c_id}",
                "@type": "okf:CurriculumConcept",
                "name": c.get("name"),
                "module": c.get("unit"),
                "level": c.get("level"),
                "bloomTaxonomy": c.get("bloom_taxonomy", "Understand"),
                "competencies": c.get("competencies", []),
                "primaryFormula": c.get("primary_formula", ""),
                "slideCitation": c.get("syllabus_slide_ref", ""),
                "estimatedMinutes": c.get("estimated_study_minutes", 45),
                "directPrerequisites": [f"concept:{p}" for p in self.get_direct_prerequisites(c_id)],
                "description": c.get("description", "")
            })

        edges_ld = []
        for u, v, d in self.graph.edges(data=True):
            edges_ld.append({
                "@type": "okf:PrerequisiteDependency",
                "source": f"concept:{u}",
                "target": f"concept:{v}",
                "dependencyType": d.get("relationship_type", "hard_prerequisite"),
                "cognitiveWeight": d.get("weight", 0.90),
                "pedagogicalJustification": d.get("description", "")
            })

        return {
            "@context": {
                "okf": "https://w3id.org/okf/v1#",
                "concept": "https://w3id.org/okf/concept/",
                "name": "http://schema.org/name",
                "description": "http://schema.org/description"
            },
            "courseMetadata": self.course_metadata,
            "conceptCount": len(nodes_ld),
            "dependencyCount": len(edges_ld),
            "graph": {
                "nodes": nodes_ld,
                "edges": edges_ld
            }
        }

    def export_to_cytoscape_elements(
        self,
        highlight_target: Optional[str] = None,
        highlight_weak: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Export graph in Cytoscape.js format for interactive frontend canvas rendering.
        """
        elements = []
        weak_set = set(highlight_weak or [])

        for c_id, c in self.concept_catalog.items():
            node_class = "default"
            if c_id == highlight_target:
                node_class = "target-node"
            elif c_id in weak_set:
                node_class = "weak-gap-node"

            elements.append({
                "group": "nodes",
                "data": {
                    "id": c_id,
                    "label": c.get("name", c_id),
                    "unit": c.get("unit", ""),
                    "level": c.get("level", ""),
                    "bloom": c.get("bloom_taxonomy", "Understand"),
                    "slide": c.get("syllabus_slide_ref", ""),
                    "formula": c.get("primary_formula", ""),
                    "nodeClass": node_class
                }
            })

        for u, v, d in self.graph.edges(data=True):
            is_active_path = (u in weak_set or u == highlight_target) and (v in weak_set or v == highlight_target)
            elements.append({
                "group": "edges",
                "data": {
                    "id": f"edge_{u}_{v}",
                    "source": u,
                    "target": v,
                    "type": d.get("relationship_type", "prerequisite"),
                    "weight": d.get("weight", 0.90),
                    "activeCritical": is_active_path
                }
            })

        return elements

    def export_to_graphml(self, output_path: str) -> None:
        """Export graph to standard GraphML format for NetworkX / Gephi import."""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        # NetworkX GraphML export requires string or numeric attributes
        export_g = nx.DiGraph()
        for node, data in self.graph.nodes(data=True):
            clean_data = {}
            for k, val in data.items():
                if isinstance(val, (list, dict)):
                    clean_data[k] = json.dumps(val)
                else:
                    clean_data[k] = str(val)
            export_g.add_node(node, **clean_data)

        for u, v, data in self.graph.edges(data=True):
            clean_data = {}
            for k, val in data.items():
                if isinstance(val, (list, dict)):
                    clean_data[k] = json.dumps(val)
                else:
                    clean_data[k] = str(val)
            export_g.add_edge(u, v, **clean_data)

        nx.write_graphml(export_g, output_path)
        logger.info(f"Exported GraphML to: {output_path}")

    # =========================================================================
    # GRAPH VISUALIZATION EXPORT (MONOCHROME / EXECUTIVE THEME)
    # =========================================================================

    def plot_graph(
        self,
        output_path: str,
        highlight_target: Optional[str] = None,
        highlight_weak: Optional[List[str]] = None
    ) -> None:
        """
        Render a clean, high-resolution visualization of the Directed Acyclic Graph.
        Adheres to clean academic publication standards (monochrome, high-contrast).
        """
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        plt.figure(figsize=(14, 10), facecolor="#FFFFFF")
        ax = plt.gca()
        ax.set_facecolor("#FFFFFF")

        # Compute hierarchical topological layout
        try:
            # Group nodes by topological generation
            generations = list(nx.topological_generations(self.graph))
            pos = {}
            for layer_idx, gen in enumerate(generations):
                num_in_gen = len(gen)
                for item_idx, node in enumerate(gen):
                    x = layer_idx * 2.5
                    y = (item_idx - (num_in_gen - 1) / 2.0) * 1.8
                    pos[node] = (x, y)
        except Exception:
            # Fallback layout
            pos = nx.spring_layout(self.graph, seed=42, k=1.8)

        # Style nodes
        node_colors = []
        node_border_colors = []
        node_sizes = []

        highlight_weak_set = set(highlight_weak or [])

        for node in self.graph.nodes():
            if node == highlight_target:
                # Black node with white text
                node_colors.append("#111827")
                node_border_colors.append("#000000")
                node_sizes.append(2800)
            elif node in highlight_weak_set:
                # Charcoal grey node for weak prerequisites
                node_colors.append("#6B7280")
                node_border_colors.append("#374151")
                node_sizes.append(2400)
            else:
                # Light grey node for proficient / default
                node_colors.append("#F3F4F6")
                node_border_colors.append("#D1D5DB")
                node_sizes.append(2200)

        # Draw edges
        nx.draw_networkx_edges(
            self.graph,
            pos,
            ax=ax,
            edge_color="#4B5563",
            arrows=True,
            arrowsize=18,
            arrowstyle="-|>",
            width=1.6,
            min_source_margin=18,
            min_target_margin=18
        )

        # Draw nodes
        nx.draw_networkx_nodes(
            self.graph,
            pos,
            ax=ax,
            node_color=node_colors,
            edgecolors=node_border_colors,
            linewidths=1.8,
            node_size=node_sizes
        )

        # Draw labels (short display name)
        labels = {}
        for node in self.graph.nodes():
            name = self.concept_catalog[node]["name"]
            # Multi-line wrap for neat display
            parts = name.split()
            if len(parts) > 2:
                labels[node] = f"{parts[0]} {parts[1]}\n{' '.join(parts[2:])}"
            else:
                labels[node] = name

        # Labels formatting
        for node, (x, y) in pos.items():
            text_color = "#FFFFFF" if (node == highlight_target or node in highlight_weak_set) else "#111827"
            font_weight = "bold" if node == highlight_target else "semibold"
            ax.text(
                x, y,
                labels[node],
                color=text_color,
                fontsize=8.5,
                fontweight=font_weight,
                ha="center",
                va="center",
                fontfamily="sans-serif"
            )

        title_text = "Curriculum Prerequisite Directed Acyclic Graph (DAG)"
        if highlight_target:
            title_text += f"\nHighlighted Target: {self.concept_catalog[highlight_target]['name']}"

        plt.title(
            title_text,
            fontsize=13,
            fontweight="bold",
            color="#111827",
            pad=15
        )

        # Legend / Guide
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor="#F3F4F6", edgecolor="#D1D5DB", label="Curriculum Concept (Node)"),
            Patch(facecolor="#6B7280", edgecolor="#374151", label="Weak Prerequisite Gap"),
            Patch(facecolor="#111827", edgecolor="#000000", label="Target Learning Concept")
        ]
        ax.legend(
            handles=legend_elements,
            loc="lower right",
            frameon=True,
            facecolor="#FFFFFF",
            edgecolor="#E5E7EB",
            fontsize=9
        )

        plt.axis("off")
        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()
        logger.info(f"Saved prerequisite graph visualization to: {output_path}")

    # =========================================================================
    # INTERNAL HELPERS
    # =========================================================================

    def _check_concept_exists(self, concept_id: str) -> None:
        """Verify concept ID exists in catalog."""
        if concept_id not in self.concept_catalog:
            valid_ids = list(self.concept_catalog.keys())
            raise ValueError(
                f"Concept ID '{concept_id}' not found in curriculum graph. "
                f"Valid IDs: {valid_ids[:6]}... (Total {len(valid_ids)})"
            )


# Self-contained CLI execution demonstration
if __name__ == "__main__":
    import sys
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_file = os.path.join(base_dir, "data", "concept_prerequisites.json")
    
    print("\n" + "=" * 75)
    print("  PREREQUISITE KNOWLEDGE GRAPH INITIALIZATION (PACD-RAG STEP 4)")
    print("=" * 75)

    pkg = PrerequisiteKnowledgeGraph(json_file)
    val = pkg.validate_graph()

    print(f"\n1. Graph Architecture:")
    print(f"   * Total Academic Concepts (Nodes): {val['num_nodes']}")
    print(f"   * Total Prerequisite Dependencies (Edges): {val['num_edges']}")
    print(f"   * Is Valid Directed Acyclic Graph (DAG): {val['is_valid_dag']}")
    print(f"   * Zero Cycles Detected: {not val['has_cycles']}")

    print(f"\n2. Global Pedagogical Learning Sequence (Topological Order):")
    for i, cid in enumerate(val["topological_order"][:6], 1):
        print(f"   {i}. [{cid}] {pkg.concept_catalog[cid]['name']}")
    print("   ... (truncated for brevity)")

    # Demonstration of Example from PDF:
    # Partial Derivatives -> Chain Rule -> Backpropagation -> Neural Network Training
    print("\n3. Verifying Key Curriculum Pathway from PDF Specification:")
    print("   Partial Derivatives -> Chain Rule -> Backpropagation -> Neural Network Training")
    nn_train_preds = pkg.get_direct_prerequisites("DL_NN_TRAIN")
    backprop_preds = pkg.get_direct_prerequisites("DL_BACKPROP")
    chain_rule_preds = pkg.get_direct_prerequisites("MATH_CHAIN_RULE")
    print(f"   * Direct Predecessors of 'DL_NN_TRAIN': {nn_train_preds}")
    print(f"   * Direct Predecessors of 'DL_BACKPROP': {backprop_preds}")
    print(f"   * Direct Predecessors of 'MATH_CHAIN_RULE': {chain_rule_preds}")

    # Demonstration of Prerequisite Gap Tracing
    print("\n4. Learner Case Simulation: Student struggling with 'Neural Network Training'")
    sample_evidence = {
        "MATH_DERIV": 0.85,
        "MATH_CHAIN_RULE": 0.42,   # Weak
        "DL_PERCEPTRON": 0.78,
        "DL_FEEDFORWARD": 0.80,
        "DL_BACKPROP": 0.45,      # Weak
        "ML_DEC_TREE": 0.35       # Weak, but unrelated to DL_NN_TRAIN
    }
    learner_diag = pkg.map_learner_evidence(sample_evidence, review_threshold=0.60)
    weak_ids = [item["id"] for item in learner_diag["needs_review_concepts"]]
    print(f"   * Formative Weak Concepts Identified: {weak_ids}")

    gap_analysis = pkg.trace_prerequisite_gaps("DL_NN_TRAIN", weak_ids)
    print(f"\n   * Diagnosed Root-Cause Prerequisite Gaps for 'DL_NN_TRAIN':")
    for step in gap_analysis["remediation_pathway"]:
        print(f"     Step {step['step']}: [{step['concept_id']}] {step['name']} ({step['unit']})")
    print(f"\n   * Pedagogical Guidance:\n     \"{gap_analysis['pedagogical_explanation']}\"")
    print(f"   * Unrelated Weak Concepts (Filtered Out): {gap_analysis['unrelated_weak_concepts']}")

    # Render and export graph figure
    fig_path = os.path.join(base_dir, "reports", "figures", "prerequisite_knowledge_graph.png")
    pkg.plot_graph(fig_path, highlight_target="DL_NN_TRAIN", highlight_weak=weak_ids)
    print(f"\n5. Graph Diagram Exported: {fig_path}")
    print("=" * 75 + "\n")

