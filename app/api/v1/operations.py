from fastapi import APIRouter

from app.schemas import OperationRequest
from app.service import operations as operations_service


router = APIRouter()

@router.post("/balance/income")
def add_income(operation: OperationRequest):
    return operations_service.add_income(operation)



@router.post("/balance/expense")
def add_expence(operation: OperationRequest):
    return operations_service.add_expense(operation)