from src.database import init_db, save_bill
from decimal import Decimal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Energy Billing API")


class BillRequest(BaseModel):
    customer_id: str = Field(min_length=1)
    previous_reading: int = Field(ge=0)
    current_reading: int = Field(ge=0)
    unit_rate: Decimal = Field(ge=0)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/bills", status_code=201)
def create_bill(request: BillRequest):

    if request.current_reading < request.previous_reading:
        raise HTTPException(
            status_code=400,
            detail="Current reading cannot be lower than previous reading"
        )

    consumption = (
        request.current_reading - request.previous_reading
    )

    total = (
        Decimal(consumption) * request.unit_rate
    ).quantize(Decimal("0.01"))

    init_db()

    bill_id = save_bill(
        customer_id=request.customer_id,
        previous_reading=request.previous_reading,
        current_reading=request.current_reading,
        unit_rate=request.unit_rate,
        total_bill=total
    )

    return {
        "bill_id": bill_id,
        "customer_id": request.customer_id,
        "consumption_kwh": consumption,
        "unit_rate": str(request.unit_rate),
        "total_bill": str(total)
    }