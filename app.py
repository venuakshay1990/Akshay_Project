from flask import Flask, render_template, request					
import pickle						
import numpy as np
					
						
app=Flask(__name__)		
						
@app.route('/')						
def hello():
    return render_template('readmission.html') 					
						
@app.route('/prediction', methods=['POST']) 						
def predict():
    Race=request.form['race']						
    if Race=='Caucasian':
       	Race=2
    elif Race=='AfricanAmerican':						
        Race=0
    elif Race=='Other':
        Race=4
    elif Race=='Hispanic':
        Race=3
    elif Race=='Asian':
        Race=1

    Age=request.form['age']
    if Age=='[0-20)':
        Age=0
    elif Age=='[20-40)':
        Age=1
    elif Age=='[40-60)':
        Age=2
    elif Age=='[60-80)':
        Age=3
    elif Age=='[80-100)':
        Age=4   

    AdmissionType=request.form['admission type']						
    if AdmissionType=='Emergency':
       	AdmissionType=1
    elif AdmissionType=='Elective':						
        AdmissionType=0
    elif AdmissionType=='Not Available':
        AdmissionType=2
    
    Discharge=request.form['discharge']
    if Discharge=='Discharged to home':
        Discharge=0
    elif Discharge=='Transferred to another medical facility':
        Discharge=4
    elif Discharge=='Discharged to home with home health service':
        Discharge=1
    elif Discharge=='Not Available':
        Discharge=3
    elif Discharge=='Left Against Medical Advice':
        Discharge=2

    AdmissionSource=request.form['admission source']						
    if AdmissionSource=='Emergency':
       	AdmissionSource=0
    elif AdmissionSource=='Referral':						
        AdmissionSource=2
    elif AdmissionSource=='Transferred from another health care facility':
        AdmissionSource=3
    elif AdmissionSource=='Not Available':
        AdmissionSource=1
    
    Time=int(request.form['time_in_hospital'])	

    LabProcedures=int(request.form['num_lab_procedures'])	

    Procedures=int(request.form['num_of_procedures'])	

    Medications=int(request.form['num_of_medications'])	

    Diagnoses=request.form['diag_1']						
    if Diagnoses=='Circulatory':
       	Diagnoses=0
    elif Diagnoses=='Other':						
        Diagnoses=7
    elif Diagnoses=='Respiratory':
        Diagnoses=8
    elif Diagnoses=='Digestive':
        Diagnoses=2
    elif Diagnoses=='Diabetes':						
        Diagnoses=1
    elif Diagnoses=='Injury':
        Diagnoses=4
    elif Diagnoses=='Musculoskeletal':
        Diagnoses=5    
    elif Diagnoses=='Genitourinary':						
        Diagnoses=3
    elif Diagnoses=='Neoplasms':
        Diagnoses=6
     
    DiagnosesNumber=int(request.form['number_diagnoses'])	
    
    GlucoseSerum =request.form['max_glu_serum']
    if GlucoseSerum=='Not Available':  
       	GlucoseSerum=0
    elif GlucoseSerum=='Norm':						
        GlucoseSerum=1
    elif GlucoseSerum=='>200':
        GlucoseSerum=2
    elif GlucoseSerum=='>300':
        GlucoseSerum=3

    A1CResult=request.form['A1Cresult']
    if A1CResult=='Not Available':  
       	A1CResult=0
    elif A1CResult=='>8':
        A1CResult=3
    elif A1CResult=='>7':
        A1CResult=2 
    elif A1CResult=='Norm':
        A1CResult=1 
    
    Metformin=request.form['metformin']
    if Metformin=='No':  
       	Metformin=1
    elif Metformin=='Down':
        Metformin=0
    elif Metformin=='Steady':
        Metformin=2
    elif Metformin=='Up':
        Metformin=3

    Repaglinide=request.form['repaglinide']
    if Repaglinide=='No':  
       	Repaglinide=1
    elif Repaglinide=='Down':
        Repaglinide=0
    elif Repaglinide=='Steady':
        Repaglinide=2
    elif Repaglinide=='Up':
        Repaglinide=3

    Glimepiride=request.form['glimepiride']
    if Glimepiride=='No':  
       	Glimepiride=1
    elif Glimepiride=='Down':
        Glimepiride=0
    elif Glimepiride=='Steady':
       Glimepiride=2
    elif Glimepiride=='Up':
        Glimepiride=3
       
    Glipizide=request.form['glipizide']
    if Glipizide=='No':  
       	Glipizide=1
    elif Glipizide=='Down':
        Glipizide=0
    elif Glipizide=='Steady':
        Glipizide=2
    elif Glipizide=='Up':
        Glipizide=3

    Pioglitazone=request.form['pioglitazone']
    if Pioglitazone=='No':  
       	Pioglitazone=1
    elif Pioglitazone=='Down':
        Pioglitazone=0
    elif Pioglitazone=='Steady':
        Pioglitazone=2
    elif  Pioglitazone=='Up':
        Pioglitazone=3

    Rosiglitazone=request.form['rosiglitazone']						
    if Rosiglitazone=='No':
       	Rosiglitazone=1
    elif Rosiglitazone=='Steady':						
        Rosiglitazone=2
    elif Rosiglitazone=='Up':
        Rosiglitazone=3
    elif Rosiglitazone=='Down':
        Rosiglitazone=0
    
    Acarbose=request.form['acarbose']						
    if Acarbose=='No':
        Acarbose=1
    elif Acarbose=='Steady':						
        Acarbose=2
    elif Acarbose=='Up':
        Acarbose=3
    elif Acarbose=='Down':
        Acarbose=0

    Insulin=request.form['insulin']						
    if Insulin=='No':
       	Insulin=1
    elif Insulin=='Steady':						
        Insulin=2
    elif Insulin=='Up':
        Insulin=3
    elif Insulin=='Down':
        Insulin=0
    
    Change=request.form['change']						
    if Change=='No':
       	Change=1
    elif Change=='Ch':						
        Change=0

    DiabetesMed=request.form['diabetesMed']						
    if DiabetesMed=='Yes':
       	DiabetesMed=1
    elif DiabetesMed=='No':						
        DiabetesMed=0

    Visits=float(request.form['preceding_year_visits'])	

    print(Race,Age,AdmissionType,Discharge,AdmissionSource,Time,LabProcedures,Procedures,Medications,Diagnoses,DiagnosesNumber,GlucoseSerum,A1CResult,Metformin,Repaglinide,Glimepiride,Glipizide,Pioglitazone,Rosiglitazone,Acarbose,Insulin,Change,DiabetesMed,Visits)						
    diabetic=pickle.load(open('readmission.pkl','rb'))					
    feature=np.array([[Race,Age,AdmissionType,Discharge,AdmissionSource,Time,LabProcedures,Procedures,Medications,Diagnoses,DiagnosesNumber,GlucoseSerum,A1CResult,Metformin,Repaglinide,Glimepiride,Glipizide,Pioglitazone,Rosiglitazone,Acarbose,Insulin,Change,DiabetesMed,Visits]])						
    diabetes=diabetic.predict(feature)						
    print(diabetes)						
    print(diabetes[0])
    if diabetes[0]==1:
        diabetes='There is a likelihood of the patient getting Readmitted'
    elif diabetes[0]==0:
        diabetes='The Patient is NOT likely to get Readmitted'
    print(diabetes)				

    return render_template('prediction.html',predicted=diabetes)						
						
if __name__=='__main__':						
    app.run(debug=True)