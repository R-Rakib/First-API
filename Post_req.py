from fastapi import FastAPI, Path, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ValidationError
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

class Patient(BaseModel):
    id: Annotated[str, Field(..., description='Id of the patient', example='P001')]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="City of the patient")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Literal['Male', 'Female', 'Others'], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in meters")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kg")]

    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height ** 2), 2)

    @property
    def verdict(self) -> str:
        bmi = self.bmi
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(None, description="Name of the patient")]
    city: Annotated[Optional[str], Field(None, description="City of the patient")]
    age: Annotated[Optional[int], Field(None, gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Optional[Literal['Male', 'Female', 'Others']], Field(None, description="Gender of the patient")]
    height: Annotated[Optional[float], Field(None, gt=0, description="Height of the patient in meters")]
    weight: Annotated[Optional[float], Field(None, gt=0, description="Weight of the patient in kg")]

    @property
    def bmi(self) -> Optional[float]:
        if self.height and self.weight:
            return round(self.weight / (self.height ** 2), 2)
        return None

    @property
    def verdict(self) -> Optional[str]:
        bmi = self.bmi
        if bmi is None:
            return None
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

def load_data():
    try:
        with open("patients.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f, indent=4)

@app.post("/create")
def create_patient(patient: Patient):
    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient with this ID already exists")

    data[patient.id] = patient.dict(exclude={"id"})
    save_data(data)

    return JSONResponse(
        status_code=201,
        content={
            "message": "Patient created successfully",
            "patient_id": patient.id
        }
    )

@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    patient_data = data[patient_id]
    updated_info = patient_update.dict(exclude_unset=True)

    for key, value in updated_info.items():
        patient_data[key] = value

    patient_data["id"] = patient_id

    try:
        patient_pydantic = Patient(**patient_data)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    data[patient_id] = patient_pydantic.dict(exclude={"id"})
    save_data(data)

    return JSONResponse(
        status_code=200,
        content={
            "message": "Patient updated successfully",
            "bmi": patient_pydantic.bmi,
            "verdict": patient_pydantic.verdict
        }
    )

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    del data[patient_id]
    save_data(data)

    return JSONResponse(
        status_code=200,
        content={
            "message": "Patient deleted successfully"
        }
    )