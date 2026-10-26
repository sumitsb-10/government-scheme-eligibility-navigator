import httpx

print("Getting full error detail...")
r = httpx.post(
    "http://localhost:8000/query",
    json={"description": "I am a 28-year-old woman from a rural village in Rajasthan. I belong to SC community. My husband is a daily wage labourer and we earn about Rs. 6000 per month. We have no LPG connection. I have Aadhaar card."},
    timeout=270,
)
print("Status:", r.status_code)
detail = r.json().get("detail", "")
# Print first 3000 chars
print(detail[:3000])
