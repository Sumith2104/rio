"""
LMS / VLE Engagement Event Ingestion & Feature Engineering Service (PACD-RAG)
=============================================================================
Author: Sumith U (SRN: R24EA807) | 7th Sem B.Tech CSE (AI & ML), Section B, REVA University
Project: AI-Powered Smart Campus Intelligence & Student Success Platform

Ingests fine-grained Virtual Learning Environment (VLE / Moodle / Canvas) activity events:
video playback, lecture note downloads, assignment submission latency, and quiz drills.
Engineers behavioral engagement velocity features to complement classroom attendance.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import numpy as np

class LMSEngagementService:
    def __init__(self):
        # In-memory storage for raw telemetry events (keyed by student_srn)
        self.events_db: Dict[str, List[Dict[str, Any]]] = {}

    def ingest_event(
        self,
        student_srn: str,
        event_type: str,
        course_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Ingests a single atomic learning interaction event."""
        valid_events = {"LOGIN", "VIDEO_WATCH", "RESOURCE_DOWNLOAD", "QUIZ_ATTEMPT", "ASSIGNMENT_SUBMISSION", "FORUM_POST"}
        if event_type.upper() not in valid_events:
            raise ValueError(f"Invalid event_type {event_type}. Allowed: {valid_events}")

        event = {
            "timestamp": datetime.now().isoformat(),
            "student_srn": student_srn,
            "event_type": event_type.upper(),
            "course_id": course_id,
            "metadata": metadata or {}
        }
        
        self.events_db.setdefault(student_srn, []).append(event)
        return {
            "status": "RECORDED",
            "event_type": event["event_type"],
            "total_student_events": len(self.events_db[student_srn])
        }

    def compute_engagement_profile(self, student_srn: str, course_id: Optional[str] = None) -> Dict[str, Any]:
        """Calculates normalized behavioral metrics from ingested telemetry."""
        events = self.events_db.get(student_srn, [])
        if course_id:
            events = [e for e in events if e.get("course_id") == course_id]

        if not events:
            # Baseline default profile when no LMS telemetry exists yet
            return {
                "student_srn": student_srn,
                "telemetry_status": "NO_ACTIVITY_LOGGED",
                "engagement_score": 50.0,
                "engagement_tier": "UNKNOWN / UNMONITORED",
                "metrics": {
                    "login_count": 0,
                    "video_watch_hours": 0.0,
                    "avg_video_completion_pct": 0.0,
                    "quizzes_completed": 0,
                    "avg_assignment_delay_hours": 0.0,
                    "downloads_count": 0
                }
            }

        logins = sum(1 for e in events if e["event_type"] == "LOGIN")
        downloads = sum(1 for e in events if e["event_type"] == "RESOURCE_DOWNLOAD")
        quizzes = [e for e in events if e["event_type"] == "QUIZ_ATTEMPT"]
        quiz_scores = [q["metadata"].get("score_pct", 70.0) for q in quizzes]
        
        video_events = [e for e in events if e["event_type"] == "VIDEO_WATCH"]
        video_durations = [v["metadata"].get("duration_minutes", 0.0) for v in video_events]
        total_video_hours = sum(video_durations) / 60.0
        avg_completion = np.mean([v["metadata"].get("completion_pct", 50.0) for v in video_events]) if video_events else 0.0

        sub_events = [e for e in events if e["event_type"] == "ASSIGNMENT_SUBMISSION"]
        delays = [s["metadata"].get("delay_hours", 0.0) for s in sub_events]
        avg_delay = float(np.mean(delays)) if delays else 0.0

        # Composite Engagement Score Formula (0 to 100):
        # 25% login regularity + 30% video watch + 25% quiz effort + 20% on-time submission
        score_login = min(25.0, (logins / 10.0) * 25.0)
        score_video = min(30.0, (avg_completion / 100.0) * 30.0)
        score_quiz = min(25.0, (len(quizzes) / 4.0) * 25.0)
        score_punctuality = max(0.0, min(20.0, 20.0 - (avg_delay / 12.0) * 10.0))

        composite_score = float(round(score_login + score_video + score_quiz + score_punctuality, 1))

        if composite_score >= 75.0:
            tier = "HIGHLY_ACTIVE_ENGAGED"
            risk_adjustment = -0.10  # Lowers dropout risk prediction
        elif composite_score >= 50.0:
            tier = "MODERATE_ENGAGEMENT"
            risk_adjustment = 0.0
        else:
            tier = "DORMANT_DISENGAGED"
            risk_adjustment = +0.15  # Increases dropout risk prediction

        return {
            "student_srn": student_srn,
            "telemetry_status": "ACTIVE_TRACKING",
            "total_events_analyzed": len(events),
            "engagement_score": composite_score,
            "engagement_tier": tier,
            "risk_probability_modifier": risk_adjustment,
            "metrics": {
                "login_count": logins,
                "video_watch_hours": round(total_video_hours, 1),
                "avg_video_completion_pct": round(avg_completion, 1),
                "quizzes_completed": len(quizzes),
                "avg_quiz_score": round(float(np.mean(quiz_scores)), 1) if quiz_scores else None,
                "avg_assignment_delay_hours": round(avg_delay, 1),
                "materials_downloaded": downloads
            }
        }

if __name__ == "__main__":
    service = LMSEngagementService()
    # Ingest sample activity for Sumith U
    for _ in range(8):
        service.ingest_event("R24EA807", "LOGIN", "AIML-401")
    service.ingest_event("R24EA807", "VIDEO_WATCH", "AIML-401", {"duration_minutes": 45, "completion_pct": 92.0})
    service.ingest_event("R24EA807", "RESOURCE_DOWNLOAD", "AIML-401", {"file": "Unit2_Backprop_Notes.pdf"})
    service.ingest_event("R24EA807", "QUIZ_ATTEMPT", "AIML-401", {"score_pct": 88.0, "time_spent_mins": 14})
    service.ingest_event("R24EA807", "ASSIGNMENT_SUBMISSION", "AIML-401", {"delay_hours": -4.0})  # Submitted early!

    prof = service.compute_engagement_profile("R24EA807")
    import json
    print(json.dumps(prof, indent=2))

