# Python
from typing import Optional
from enum import Enum

# Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr

# FastAPI
from fastapi import FastAPI
from fastapi import status
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File

app = FastAPI()

# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="The city where the person lives",
        example="New York",
    )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="The state where the person lives",
        example="New York",
    )
    country: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="The country where the person lives",
        example="United States",
    )

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Miguel"
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Gonzalez"
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=25
    )
    hair_color: Optional[HairColor  ] = Field(default=None, example=HairColor.brown)
    is_married: Optional[bool] = Field(default=None, example=False)

class Person(PersonBase):
        password: str = Field(..., min_length=8)

    #class Config:
    #    schema_extra = {
    #        "example": {
    #            "first_name": "Facundo",
    #            "last_name": "García Martoni",
    #            "age": 29,
    #            "hair_color": "blonde",
    #            "is_married": False,
    #        }
    #    }

class PersonOut(PersonBase):
    pass

class LoginOut(BaseModel):
    username: str = Field(..., max_length=20, example="miguel2021")
    message: str = Field(default="Login Succesfully!")

@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    tags=["Home"],
    summary="Home page",
    )
def home():
    """
    Home page

    This is the home page of the API.

    Parameters:
        None

    Returns:
        200:
            - message: Welcome to the API!
    """
    return {"Hello": "World!"}

# Request and Response Body

@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"],
    summary="Create Person in the app"
    )
def create_person(person: Person = Body(...)):
    """"
    Create Person

    This path operation creates a person in the app and save the information in the database.

    Parameters:
    - Request body parameter:
        - **person: Person** -> A person model with first name, last name, age, hair color and marital status.

    Return a person model with first name, last name, age, hair color and marital status.
    """
    return person

# Validaciones: Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary="Get Person detail",
    deprecated=True,
    )
def show_person(
    name: Optional[str] = Query(
        None, min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person name,  It's between 1 and 50 characters",
        example="Rocio"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age, It's required",
        example="25"
        )
):
    """
    Get Person detail

    This path operation shows the person detail.

    Parameters:
    - Query parameters:
        - **name: str** -> The person name.
        - **age: str** -> The person age.

    Return a person model with first name, last name, age, hair color and marital status.
    """
    return {name: age}

# Validaciones Path Paremeters

persons = [1, 2, 3, 4, 5]

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary="Get Person detail by ID"
    )
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        example=123
    )
):
    """
    Get Person detail by ID

    This path operation shows the person detail by ID.

    Parameters:
    - Path parameters:
        - **person_id: int** -> The person ID.

    Return a person model with first name, last name, age, hair color and marital status.
    """
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="¡This person doesn't exist!"
            )
    return {person_id: "It exists!"}

# Validaciones: Request Body

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary="Update Person detail by ID"
    )
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=123
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    """
    Update Person detail by ID

    This path operation updates the person detail by ID.

    Parameters:
    - Path parameters:
        - **person_id: int** -> The person ID.
    - Request body parameter:
        - **person: Person** -> A person model with first name, last name, age, hair color and marital status.
        - **location: Location** -> A location model with city, state and country.

    Return a person model with first name, last name, age, hair color and marital status.
    """
    #results = person.dict()
    #results.update(location.dict())
    #return results
    return person

# Forms

@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    tags=["Persons"],
    summary="Login"
)
def login(username: str = Form(...), password: str = Form(...)):
    """
    Login

    This path operation login a person.

    Parameters:
    - Request body parameter:
        - **username: str** -> The person username.
        - **password: str** -> The person password.

    Return a person model with first name, last name, age, hair color and marital status.
    """
    return LoginOut(username=username)

# Cookies and Headers Parameters
@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Contact"],
    summary="Contact"
)
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    """
    Contact

    This path operation contact a person.

    Parameters:
    - Request body parameter:
        - **first_name: str** -> The person first name.
        - **last_name: str** -> The person last name.
        - **email: EmailStr** -> The person email.
        - **message: str** -> The person message.
        - **user_agent: Optional[str]** -> The person user agent.
        - **ads: Optional[str]** -> The person ads.

    Return a person model with first name, last name, age, hair color and marital status.
    """
    return user_agent

# Files

@app.post(
    path="/post-image",
    tags=["Image"],
    summary="Post Image"
)
def post_image(
    image: UploadFile = File(...)
):
    """
    Post Image

    This path operation post a image.

    Parameters:
    - Request body parameter:
        - **image: UploadFile** -> The image.

    Return a person model with first name, last name, age, hair color and marital status.
    """
    return {
        "Filename": image.filename,
        "Format": image.content_type,
        "Size(kb)": round(len(image.file.read())/1024, ndigits=2)
    }