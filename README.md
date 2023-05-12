# sqlalchemy-challenge
## Module 10 Assignment 

### DB tool - DBeaver 

### Data Modeling
   - 6 csv files were analysed to sketch an Entity Relationship Diagram of the tables. 
   - QuickDBD tool was used to sketch the ERD and then exported to PostgreSQL to generate the DDL statements
   - https://app.quickdatabasediagrams.com/#/d/bvP7qM
   
   ![image](https://user-images.githubusercontent.com/126313924/235408364-1dd4e2ad-8349-4f44-9974-56ead6e5ec1f.png)

   
### Data Engineering
   - A new database, employee_DB is created in Postgres
   - 6 Tables created using DDL statements exported from QuickDBD: 
     - departments,titles,employee,salaries,dept_employee,dept_manager
   - The CSVs are then used to load the tables
   
### Data Analysis
    
#### Query to the tables to fetch the following data: 
    
    -List the employee number, last name, first name, sex, and salary of each employee.
    
    -List the first name, last name, and hire date for the employees who were hired in the year 1986.
    
    -List the number of employees who were hired in the year 1986.
      -36,150 employees were hired in the year 1986.
      
    -List the manager of each department along with their department number, department name, employee number, last name, and first name.
    
    -List the department number for each employee along with that employee’s employee number, last name, first name, and department name.
    
    -List each employees in the Sales department and their managers.
    
    -List each employee and their managers in the Sales and Development departments.
    
    -List the frequency counts, in descending order, of all the employee last names (that is, how many employees share each last name).

#### references: 
     
     - https://stackoverflow.com/questions/7729287/postgresql-change-the-size-of-a-varchar-column-to-lower-length
                 
     - https://www.tutorialrepublic.com/sql-reference/sql-server-data-types.php#precision-and-scale
     
     - https://commandprompt.com/education/how-to-extract-year-from-date-in-postgresql/
                 
                 
     
  
