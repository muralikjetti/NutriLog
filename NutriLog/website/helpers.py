from re import match
import os
import requests

def is_valid_email(email):
    email_pattern = r'^\S+@\S+\.\S+$'

    if match(email_pattern, email):
        return True
    else:
        return False
    
def get_nutrition_info(food):
    url = "https://edamam-edamam-nutrition-analysis.p.rapidapi.com/api/nutrition-data"
    headers = {
        "X-RapidAPI-Key": os.environ.get('RAPIDAPI_KEY'),
        "X-RapidAPI-Host": "edamam-edamam-nutrition-analysis.p.rapidapi.com"
    }
    querystring = {"ingr": food, "nutrition-type": "cooking"}

    response = requests.get(url, headers=headers, params=querystring)
    data = response.json()

    if "status" in data and data["status"] == "failure":
        return None

    nutrition_info = {}
    nutrition_info['name'] = food
    if "totalNutrients" in data and "ENERC_KCAL" in data["totalNutrients"]:
        energy = round(data["totalNutrients"]["ENERC_KCAL"]["quantity"], 2)
        nutrition_info["energy"] = energy
    if "totalNutrients" in data and "FAT" in data["totalNutrients"]:
        fat = round(data["totalNutrients"]["FAT"]["quantity"], 2)
        nutrition_info["fat"] = fat
    if "totalNutrients" in data and "PROCNT" in data["totalNutrients"]:
        protein = round(data["totalNutrients"]["PROCNT"]["quantity"], 2)
        nutrition_info["protein"] = protein
    if "totalNutrients" in data and "CHOCDF" in data["totalNutrients"]:
        carbohydrates = round(data["totalNutrients"]["CHOCDF"]["quantity"], 2)
        nutrition_info["carbohydrates"] = carbohydrates

    return nutrition_info