from fastapi import FastAPI ,Path,HTTPException, Query
import json

app=FastAPI()

def load_data():
    with open("patients.json","r") as f:
        data=json.load(f)
    return data
    

@app.get("/")
def hello():
    return {"message": "Patient Management System API"}


@app.get("/about")
def about():
    return {"message": "A fully functional API to manage your patient records"}


@app.get("/view")
def view():
    data=load_data()

    return data


@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description ="The id of the patient")):
    data =load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="patient not found")


@app.get("/sort")
def sort_data(sort_by:str =Query(...,description="Sort on the basis of heigh ,weight,bmi"), order: str= Query('asc',descripton="sort in asc or desc order")):
    data=load_data()

    valid_fields = ['height', 'weight', 'bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid field selected from{valid_fields}")
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400, detail="Invalid order selected, please select asc or desc")    
    sort_order= True if order=='desc' else False
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)
    return sorted_data
    

    