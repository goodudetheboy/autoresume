from pydantic import BaseModel, EmailStr, HttpUrl, constr
from typing import List, Optional


class LinkAlias(BaseModel):
    link: HttpUrl
    alias: str


class Education(BaseModel):
    institution: str
    # Expects a year-month format like '2024-05'
    graduation: str
    degree: str
    extra_info: Optional[str]


class Skills(BaseModel):
    section_name: str
    details: List[str]


class Experience(BaseModel):
    company: str
    duration: str
    role: str
    location: str
    details: List[str]


class Project(BaseModel):
    name: str
    link: Optional[HttpUrl]
    summary: str
    duration: str
    details: List[str]


class Award(BaseModel):
    name: str
    description: str
    # Expects a year-month format like '2024-05'
    date: str


class Resume(BaseModel):
    name: str
    phone: str
    email: EmailStr
    website: Optional[LinkAlias]
    linkedin: Optional[LinkAlias]
    github: Optional[LinkAlias]

    education_list: List[Education]
    skills: List[Skills]
    experience_list: List[Experience]
    project_list: List[Project]
    awards_list: Optional[List[Award]]
