from sqlalchemy.orm import Mapped, mapped_column, Optional
from typing import Optional
from ..db import db
import os
import google.generativeai as genai

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

class Pet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Optional Mapped[str]
    animal_type: Mapped[str]
    personality: Mapped[str]
    color: Mapped[str]

    def to_dict(self):
        pet_dict = {
            "id" : self.id,
            "name" : self.name,
            "animal": self.animal_type,
            "personality": self.personality,
            "coloration": self.color
        }
        
        
        return pet_dict


    @classmethod
    def from_dict(cls, data_dict):
        if data_dict["name"]:
            pet_name = data_dict["name"]
        else: 
            pet_name = generate_pet_name(data_dict)
        new_pet = cls(
            name=pet_name,
            animal_type=data_dict["animal"],
            personality=data_dict["personality"],
            color=data_dict["coloration"]
        )

        return new_pet


    def generate_pet_name(pet_dict): 
        model = genai.GenerativeModel("gemini-1.5-flash")
        input_message = f"I have a pet name generator app. I would like to generate 1 pet name suggestion for a {pet_dict.animal}, that is {pet_dict.coloration}, with a {pet_dict.personality} personality. Please return just the name in a string without a variable name or square brackets."
        print("something on line 47")
        response = model.generate_content(input_message)
        print('our response was', response.text)
        return response.text