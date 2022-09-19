"""
### Tarea 3
Crear una nueva API, la cual contenga cuatro endpoints con las siguientes consideraciones:
"""

# Librerías a usar
import uvicorn
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

# ______________________________________________________________________________________________________________________
# Generando la APP
app = FastAPI()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info", reload=True)

# ______________________________________________________________________________________________________________________
"""1. Un endpoint para crear un diccionario en donde las llaves de dicho diccionario sea un id de tipo entero como 
identificador único para una lista de usuarios. El valor de dicha llave será otro diccionario con la siguiente estructura:
    ```
    {"user_name": "name",
    "user_id": id,
    "user_email": "email",
    "age" (optiona): age,
    "recommendations": list[str],
    "ZIP" (optional): ZIP
    }
    ```
    Cada vez que se haga un request a este endpoint, se debe actualizar el diccionario. 
    Hint: Definir un diccionario vacío fuera del endpoint.
    La respuesta de este endpoint debe enviar el id del usuario generado y una descripción 
    de usuario generado exitosamente.
    2. Si se envía datos con un id ya repetido, se debe regresar un mensaje de error que mencione este hecho.
    """
# Diccionario donde se guardará toda la información (Se reinicia junto con la APP)
users_dict = {}


# Clase de los Usuarios
class Users(BaseModel):
    user_name: str
    user_id: int
    user_email: str
    age: int
    recommendations: list[str]
    ZIP: str


# Función para agregar usuarios
@app.put('/users')
def create_users(user: Users):
    user = user.dict()
    # Se crea el usuario si NO está en el diccionario
    if user['user_id'] not in users_dict:
        users_dict[user['user_id']] = user
        return {'Description': f'User Created Successfully {user["user_id"]}'}
    else:
        return {'Error': f'The user {user["user_id"]} you want to create already exists.'}


# ______________________________________________________________________________________________________________________
# 3. Un endpoint para actualizar la información de un usuario específico buscándolo por ID. Si el id no existe,
# debe regresar un mensaje de error que mencione este hecho.
@app.put('/upgrade_users')
def update_users(user: Users):
    user = user.dict()
    if user['user_id'] in users_dict:
        users_dict[user['user_id']] = user
        return {'Description': f'User Updated Successfully {user["user_id"]}'}
    else:
        return {'Error': f'The user {user["user_id"]} you want to update does not exist.'}


# ______________________________________________________________________________________________________________________
# 4. Un endpoint para obtener la información de un usuario específico buscándolo por ID. Si el id no existe,
# debe regresar un mensaje de error que mencione este hecho.
@app.get('/users/{user_id}')
def get_information_id(user_id: int):
    if user_id in users_dict:
        info = users_dict[user_id]
        return {'Description': f"The User's {user_id} information is: {info}"}
    else:
        return {'Error': f'The user does not exist in the database'}


# ______________________________________________________________________________________________________________________
# 5. Un endpoint para eliminar la información de un usuario específico buscándolo por ID. Si el id no existe,
# debe regresar un mensaje de error que mencione este hecho.
@app.delete('/delete_user/{user_id}')
def delete_user(user_id: int):
    if user_id in users_dict:
        info = users_dict.pop(user_id)
        return {'Description': f"The User {user_id} has been deleted"}
    else:
        return {'Error': f'The User {user_id} does not exist'}
