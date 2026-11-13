import sys
sys.path.insert(0, 'student_success_platform/src')
from fluxbase_client import FluxbaseClient

db = FluxbaseClient()
rows_res = db.execute_query('SELECT score_id, student_srn, course_id, ia_number, question_no FROM ia_question_scores ORDER BY score_id DESC;')
rows = rows_res.get('rows', [])
seen = set()
to_delete = []
for r in rows:
    key = (r.get('student_srn'), r.get('course_id'), str(r.get('ia_number')), str(r.get('question_no')))
    if key in seen:
        to_delete.append(r.get('score_id'))
    else:
        seen.add(key)

print(f"Total rows: {len(rows)}, Unique keys: {len(seen)}, To delete: {len(to_delete)}")
for sid in to_delete:
    db.execute_query(f"DELETE FROM ia_question_scores WHERE score_id = '{sid}';")
print("Deduplication complete!")

