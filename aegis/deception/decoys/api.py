from fastapi import FastAPI

app = FastAPI(title="AEGIS Decoy API")


@app.get("/api/payments")
def fake_payments():
    return {"status": "ok", "transactions": [{"id": "txn_8432", "amount": 912.44, "currency": "USD"}]}


@app.get("/api/users")
def fake_users():
    return {"users": [{"id": 1, "email": "cfo@example-corp.local", "role": "finance-admin"}]}
