import httpx

print("Running end-to-end pipeline test...")
r = httpx.post(
    "http://localhost:8000/query",
    json={"description": "I am a 28-year-old woman from a rural village in Rajasthan. I belong to SC community. My husband is a daily wage labourer and we earn about Rs. 6000 per month. We have no LPG connection. I have Aadhaar card."},
    timeout=120,
)
print("Status:", r.status_code)
if r.status_code == 200:
    d = r.json()
    print(f"Eligible schemes: {d['eligible_scheme_count']}")
    print(f"Scheme titles: {d['scheme_titles']}")
    print(f"Guides returned: {len(d['application_guides'])}")
    print(f"Summary preview: {d['plain_summary'][:350]}")
    if d["application_guides"]:
        g = d["application_guides"][0]
        print(f"\nFirst guide: {g['scheme_title']}")
        print(f"  Documents: {g['required_documents'][:2]}")
        print(f"  Steps: {g['application_steps'][:2]}")
else:
    print("Error:", r.text[:500])
