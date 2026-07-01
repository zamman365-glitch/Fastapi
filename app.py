from fastapi import FastAPI

app = FastAPI()

@app.get("/display")
def home():
    return {"status": "ZaikaAPI is live!"}
@app.get("/name")
def get_name():
    return {"name": "Zamman"}



@app.get("/menu")
def get_menu():
    return [{"item": "Biryani", "price": 220}]

@app.post("/orders")
def place_order():
    return {"message": "Order placed!"}

@app.delete("/orders/{order_id}")
def cancel_order(order_id: int):
    return {"message": f"Order {order_id} cancelled"}






#Create a function that loads the json file in read mode
import json
@app.get("/show")
def show_products():
    with open('products.json', 'r') as file:
        products = json.load(file)  # json mei jaayega data uth kar python mei le aayega  
    return products





        
@app.get("/show/{id}")
def getby_id(id: int):
    with open('products.json', 'r') as file:
        products = json.load(file)  # json mei jaayega data uth kar python mei le aayega  
    
    for i in products:
        if i['id'] == id:
            print(i)
        

import json
with open('products.json', 'r') as file:
    product= json.load(file)  

d=[
    {
    "id": 9,
    "name": "Default",
    "category": "Ese tese",
    "price": 1000,
    "in_stock": True
    }
]
product.append(d)

with open('products.json', 'w') as file:
    json.dump(product,file)

print(product)



# creating a post route which will add new data in json
@app.post("/add")
def add_product(userProduct: dict):
    try:
        with open('products.json', 'r') as file:
            oldProducts=json.load(file)
        
        oldProducts.append(userProduct)

        with open('products.json', 'w') as file:
            json.dump(oldProducts,file)
    except Exception as e:
        return {"message": "Error occurred while adding product", "error": str(e)}
            







# PUT -> Update Values
# id=5
# with open ('products.json', 'r') as file:
#     products= json.load(file)
#     for i in products:
#         if i['id']==id:
#             print(i)



def update_product(id: int, updated_product: dict):
    with open('products.json', 'r') as file:
        products = json.load(file)

    for i in products:
        if i['id'] == id:
            i.update(updated_product)
            
    with open('products.json', 'w') as file:
        json.dump(products, file)



