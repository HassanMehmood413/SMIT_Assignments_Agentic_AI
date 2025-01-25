from typing import Optional, List
from fastapi import FastAPI , status , HTTPException
from pydantic import BaseModel , EmailStr , Field , validator
from typing import Optional , List


app = FastAPI()





class StudentCreate(BaseModel):
    id : int = Field(...,ge=1000,le=9999)
    name : str = Field(...,min_length=1,max_length=50)
    email : EmailStr
    age : int = Field(...,ge=18,le=30)
    courses: List[str] = Field(...,min_items=1,max_items=5)

    @validator('courses')
    def check_courses(cls,courses):
        unique_courses = set()
        for course in courses:
            if len(course) > 30 or len(course) < 1:
                raise ValueError('Courses must be between 1 and 5 characters')
            elif course.lower() in unique_courses:
                raise ValueError('Courses must be unique')
            unique_courses.add(course.lower())
        return courses






student_data = {
    1111:{
        'id':1001,
        'name':'hassan',
        'grades' : {
            'Fall2024':'A',
            'Spring2025':'B'
            }
    },
    2222:{
        'id':1002,
        'name':'mohammad',
        'grades' : {
            'Fall2024':'C',
            'Spring2025':'A'
            }
    },
    1023:{
        'id':1003,
        'name':'mohammad',
        'grades' : {
            'Fall2024':'B',
            'Spring2025':'C'
            }
    },

}


# Now we have to define routes or the APIs
@app.get('/student/{id}')
def get_student(id:int,semester:Optional[str]=None,grades:bool=False):
    
    try:
        if id > 1000 or id < 9999 :
            student = student_data.get(id)
            response = {
                'id' : student['id'],
                'name': student['name'],
            }

            if grades:
                if semester:
                    grades = student['grades'].get(semester,'Grades are not available for this semester')
                    response['grades'] = {semester:grades}
                else:
                    response['grades'] = student['grades']

                return response
            else:
                return response
                
    except Exception as e:
        return str(e)
    


@app.post('/student/register')
def register_student(student : StudentCreate):
    new_std_id = max(student_data.keys(),default=1111) + 1
    student_data[new_std_id] = {
        'id' : new_std_id,
        'name': student.name,
        'email' :  student.email,
        'age' : student.age,
        'courses' : student.courses
    }

    return {f"Student with id {new_std_id} and name {student.name} has been registered"}

@app.put('/student/{id}/email')
def update_email(id:int,email:str):
    try:
        student = student_data.get(id)
        if not student:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Student with id {} does not exist".format(id))
        
        student['email'] = email
        return {"Email has been updated"}
    except Exception as e:
        return str(e)
    

            
