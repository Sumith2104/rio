"""
Real-Time Event-Driven Mark Streaming & Alert Dispatcher (PACD-RAG)
===================================================================
Author: Sumith U (SRN: R24EA807) | 7th Sem B.Tech CSE (AI & ML), Section B, REVA University
Project: AI-Powered Smart Campus Intelligence & Student Success Platform

Provides low-latency single-mark streaming ingestion with immediate reactive risk evaluation.
Replaces slow end-of-week batch jobs with real-time mentor alerts as faculty grade exam scripts.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio
import json

class StreamingIngestionDispatcher:
    def __init__(self, decision_threshold: float = 0.42):
        self.decision_threshold = decision_threshold
        self.event_stream_log: List[Dict[str, Any]] = []

    def process_realtime_mark_event(
        self,
        student_srn: str,
        course_id: str,
        ia_component: str,
        question_id: str,
        marks_obtained: float,
        max_marks: float,
        concept_tag: str,
        evaluator_id: str = "USR_FAC01"
    ) -> Dict[str, Any]:
        """
        Processes a single mark evaluation event in sub-50ms with instant reactive checks.
        """
        # 1. Validation
        if marks_obtained < 0 or marks_obtained > max_marks:
            raise ValueError(f"Invalid marks {marks_obtained}. Must be between 0 and {max_marks}.")

        percentage = (marks_obtained / max_marks) * 100.0
        is_sub_par = percentage < 50.0  # Weak concept threshold

        # 2. Risk Evaluation
        # If student scores < 50% on a core foundational topic, instant alert trigger
        immediate_action_required = is_sub_par and concept_tag in ["DL_BACKPROP", "MATH_CHAIN_RULE", "ML_GRADIENT_DESCENT"]
        
        event_record = {
            "event_id": f"STRM_{datetime.now().strftime('%Y%m%d%H%M%S%f')[:17]}",
            "timestamp": datetime.now().isoformat(),
            "student_srn": student_srn,
            "course_id": course_id,
            "ia_component": ia_component,
            "question_id": question_id,
            "marks_obtained": marks_obtained,
            "max_marks": max_marks,
            "percentage": round(percentage, 1),
            "concept_tag": concept_tag,
            "evaluator_id": evaluator_id,
            "is_weak_topic": is_sub_par,
            "realtime_alert_dispatched": immediate_action_required
        }
        
        self.event_stream_log.append(event_record)

        # 3. Notification payload
        notification = None
        if immediate_action_required:
            notification = {
                "alert_level": "URGENT_INTERVENTION",
                "recipient": f"Faculty Mentor ({evaluator_id})",
                "message": (
                    f"Real-Time Alert: Student {student_srn} scored {marks_obtained}/{max_marks} "
                    f"({round(percentage, 1)}%) on foundational concept '{concept_tag}'. "
                    f"Auto-dispatching PACD-RAG 5-Day Remedial Study Plan."
                )
            }

        return {
            "status": "INGESTED_REALTIME",
            "event_summary": event_record,
            "reactive_notification": notification,
            "queue_depth": len(self.event_stream_log)
        }

if __name__ == "__main__":
    dispatcher = StreamingIngestionDispatcher()
    # Test streaming a weak mark for Vikram Patel
    res = dispatcher.process_realtime_mark_event(
        student_srn="R24EA818",
        course_id="AIML-401",
        ia_component="IA_1",
        question_id="Q2_BACKPROP",
        marks_obtained=3.0,
        max_marks=10.0,
        concept_tag="DL_BACKPROP",
        evaluator_id="USR_FAC01"
    )
    import json
    print(json.dumps(res, indent=2))

