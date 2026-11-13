from student_success_platform.src.fluxbase_client import FluxbaseClient
import json

client = FluxbaseClient()
res = client.execute_query("""
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;
""")
print("Existing tables in Fluxbase:")
for r in res.get('rows', []):
    print(" -", r)

