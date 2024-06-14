import streamlit as st
import pandas as pd

# Initialize session state for data storage
if 'employee_data' not in st.session_state:
    st.session_state['employee_data'] = pd.DataFrame(columns=['Empno', 'Ename', 'Job', 'Deptno'])

if 'department_data' not in st.session_state:
    st.session_state['department_data'] = pd.DataFrame(columns=['Deptno', 'Dname', 'Loc'])

# Function to add employee data
def add_employee(empno, ename, job, deptno):
    new_employee = pd.DataFrame({'Empno': [empno], 'Ename': [ename], 'Job': [job], 'Deptno': [deptno]})
    st.session_state['employee_data'] = pd.concat([st.session_state['employee_data'], new_employee], ignore_index=True)
    st.success("Employee data added successfully!")

# Function to add department data
def add_department(deptno, dname, loc):
    new_department = pd.DataFrame({'Deptno': [deptno], 'Dname': [dname], 'Loc': [loc]})
    st.session_state['department_data'] = pd.concat([st.session_state['department_data'], new_department], ignore_index=True)
    st.success("Department data added successfully!")

# Main application
def main():
    st.title("Data Entry Application")

    menu = ["Employee Data Entry", "Department Data Entry", "Data Visualization"]
    choice = st.sidebar.selectbox("Select Page", menu)

    if choice == "Employee Data Entry":
        st.header("Employee Data Entry")
        with st.form(key='employee_form'):
            empno = st.text_input("Employee Number (Empno)")
            ename = st.text_input("Employee Name (Ename)")
            job = st.text_input("Job")
            deptno = st.text_input("Department Number (Deptno)")
            submit_button = st.form_submit_button(label='Add Employee')
            
            if submit_button:
                if empno and ename and job and deptno:
                    add_employee(empno, ename, job, deptno)
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
                    add_department(deptno, dname, loc)
                else:
                    st.error("Please fill all the fields")

    elif choice == "Data Visualization":
        st.header("Data Visualization")
        if not st.session_state['employee_data'].empty and not st.session_state['department_data'].empty:
            joined_data = pd.merge(st.session_state['employee_data'], st.session_state['department_data'], on='Deptno', how='inner')
            st.write(joined_data)
        else:
            st.warning("Please add data in both Employee and Department sections")

if __name__ == "__main__":
    main()
