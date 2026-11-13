"""
Script to populate AIML-402 instructor and additional student enrollments in Fluxbase.
"""
from student_success_platform.src.fluxbase_client import FluxbaseClient

def populate_enrollments():
    fb = FluxbaseClient()
    
    # 1. Update instructor for AIML-402
    fb.execute_query("UPDATE courses SET instructor_faculty_id = 'FAC_AIML_02' WHERE course_id = 'AIML-402'")
    
    # 2. Add enrollments
    enrollments = [
        ("R24EA807", "AIML-402", 7, 28.0, 29.0, 10.0, 96.0, "A+", 92.0),
        ("R24EA801", "AIML-402", 7, 25.0, 26.0, 8.5, 88.0, "A", 84.0),
        ("R24EA818", "AIML-402", 7, 14.0, 15.0, 6.0, 62.0, "C", 54.0),
        ("R24EA842", "AIML-402", 7, 18.0, 20.0, 7.0, 74.0, "B", 68.0),
        ("R24EA895", "AIML-402", 7, 10.0, 12.0, 4.5, 52.0, "D", 45.0),
    ]
    
    for srn, cid, sem, ia1, ia2, asgn, att, gr, exam in enrollments:
        # Check if exists
        check = fb.execute_query(f"SELECT * FROM course_enrollments WHERE srn = '{srn}' AND course_id = '{cid}'")
        if check.get("rows"):
            print(f"Enrollment {srn} -> {cid} already exists.")
        else:
            q = f"""INSERT INTO course_enrollments 
                    (srn, course_id, semester, ia1_score, ia2_score, assignment_score, attendance_pct, overall_grade, exam_score)
                    VALUES ('{srn}', '{cid}', {sem}, {ia1}, {ia2}, {asgn}, {att}, '{gr}', {exam})"""
            res = fb.execute_query(q)
            print(f"Inserted {srn} -> {cid}: {res.get('success')}")

if __name__ == "__main__":
    populate_enrollments()

