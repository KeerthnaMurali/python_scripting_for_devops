mkdir paged-api && cd paged-api

python - <<'PY'
import json
users=[{"id":i,"name":f"User {i:03d}","email":f"user{i:03d}@example.com"} for i in range(1,121)]
with open("db.json","w") as f: json.dump({"users":users}, f, indent=2)
print("db.json written with 120 users")
PY
