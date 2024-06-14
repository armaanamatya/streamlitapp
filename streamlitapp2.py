import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from pydantic import BaseModel, Field, ValidationError, field_validator, PositiveInt
import os

# Initialize database connection
DATABASE_URL = os.getenv("URL")
engine = create_engine(DATABASE_URL)

# Pydantic Models for data validation
class Employee(BaseModel):
    Empno: PositiveInt = Field(..., description="Employee Number")
    Empname: str = Field(..., description="Employee Name")
    Job: str = Field(..., description="Job")
    Deptno: PositiveInt = Field(..., description="Department Number")

    @field_validator('Empname', 'Job')
    def must_not_be_empty(cls, v):
        if isinstance(v, str) and not v.strip():
            raise ValueError('Field must not be empty')
        return v

    @field_validator('Deptno')
    def must_not_be_empty(cls, v):
        if not isinstance(v, int):
            raise ValueError("Should be an integer")
        return v

class Department(BaseModel):
    Deptno: PositiveInt = Field(..., description="Department Number")
    Dname: str = Field(..., description="Department Name")
    Loc: str = Field(..., description="Location")

    @field_validator('Dname', 'Loc')
    def must_not_be_empty(cls, v):
        if isinstance(v, str) and not v.strip():
            raise ValueError('Field must not be empty')
        return v

    @field_validator('Deptno')
    def must_not_be_empty(cls, v):
        if not isinstance(v, int):
            raise ValueError("Should be an integer")
        return v

# Function to add employee data
def add_employee(Empno, ename, job, deptno):
    try:
        employee = Employee(Empno=Empno, Empname=ename, Job=job, Deptno=deptno)
        new_employee = pd.DataFrame([employee.dict()])

        # Check if Empno already exists
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1 FROM employees WHERE Empno = :Empno"), {"Empno": Empno})
            exists = result.fetchone()

        if exists:
            # Update existing record
            with engine.connect() as connection:
                connection.execute(text("""
                    UPDATE employees
                    SET Empname = :Empname, Job = :Job, Deptno = :Deptno
                    WHERE Empno = :Empno
                """), {"Empname": ename, "Job": job, "Deptno": deptno, "Empno": Empno})
            st.success(f"Employee data updated successfully for Empno {Empno}!")
        else:
            # Insert new record
            new_employee.to_sql('employees', engine, if_exists='append', index=False)
            st.success("Employee data added successfully!")
    except ValidationError as e:
        st.error(f"Validation Error: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Function to add department data
def add_department(deptno, dname, loc):
    try:
        department = Department(Deptno=deptno, Dname=dname, Loc=loc)
        new_department = pd.DataFrame([department.dict()])
        new_department.to_sql('Departments', engine, if_exists='append', index=False)
        st.success("Department data added successfully!")
    except ValidationError as e:
        st.error(f"Validation Error: {e}")

# Main application
def main():
    st.title("Data Entry Application")

    menu = ["Employee Data Entry", "Department Data Entry", "Data Visualization"]
    choice = st.sidebar.selectbox("Select Page", menu)

    if choice == "Employee Data Entry":
        st.header("Employee Data Entry")
        with st.form(key='employee_form'):
            empno = st.text_input("Employee Number (Empno)")
            ename = st.text_input("Employee Name (Empname)")
            job = st.text_input("Job")
            deptno = st.text_input("Department Number (Deptno)")
            submit_button = st.form_submit_button(label='Add Employee')
            
            if submit_button:
                if empno and ename and job and deptno:
                    add_employee(int(empno), ename, job, int(deptno))
                else:
                    st.error("Please fill all the fields")

    elif choice == "Department Data Entry":
        st.header("Department Data Entry")
        with st.form(key='department_form'):
            deptno = st.text_input("Department Number (Deptno)")
            dname = st.text_input("Department Name (Dname)")
            loc = st.text_input("Location (Loc)")
            submit_button = st.form_submit_button(label='Add Department')
            
            if submit_button:
                if deptno and dname and loc:
                    add_department(int(deptno), dname, loc)
                else:
                    st.error("Please fill all the fields")

    elif choice == "Data Visualization":
        st.header("Data Visualization")
        
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        if uploaded_file is not None:
            # Read the CSV file and clean the data
            new_data = pd.read_csv(uploaded_file, delimiter=',')
            st.write(new_data.head())  # Display the first few rows of the dataframe

            # Check if the required columns exist in the uploaded CSV file
            required_columns = ["Empno", "Empname", "Job", "Deptno"]
            if all(col in new_data.columns for col in required_columns):
                if st.button("Upload Data"):
                    try:
                        new_data.to_sql('employees', engine, if_exists='append', index=False)
                        st.success("Data uploaded to the database successfully!")
                    except Exception as e:
                        st.error(f"Failed to upload data: {e}")
            else:
                st.error(f"CSV file must contain the following columns: {', '.join(required_columns)}")

        # SELECT e.*, d."Dname", d."Loc" 
        #     FROM employees e
        #     JOIN "Departments" d ON e."Deptno" = d."Deptno"
        if st.button("Show Joined Data"):
            query = """
            SELECT * FROM employees
            """
            joined_data = pd.read_sql(query, engine)
            st.write(joined_data)

if __name__ == "__main__":
    main()
