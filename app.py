from fastapi import FastAPI

app = FastAPI()

@app.get("/golu")
def home():
    return {"status": "Hello Golu"}

@app.get('/display')
def display():
    return {'This is another page...'}






import json
#Create a function that loads the json file in read mode.
@app.get('/')
def show_products():
    with open('products.json','r') as file:
        products = json.load(file)

    return products



# max = 9+1 = 10 -> id -> naya product banega.
# # newid = max([for i ]) + 1

@app.get('/show/{id}')
def getby_id(id: int): #id:int -> variable:data type.
    with open('products.json','r') as file:
        product = json.load(file)
        for i in product:
            if i['id'] == id:
                return i



#Creating a post route which will add new data in json.
@app.post('/add')
def add_product(userProduct: dict):
    try:
        with open('products.json', 'r') as file:
            oldProducts = json.load(file)
        
        oldProducts.append(userProduct)

        with open('products.json','w') as file:
            json.dump(oldProducts, file)
    except Exception as e:
        return {"status": "error", "message": str(e)}
    












#PUT -> Update Values
def update_product(id:int, updateProduct:dict):
    with open('products.json', 'r') as file:
        products = json.load(file)

    for i in products:
       if i['id']  ==  id:
         i.update(updateProduct)
    
    with open('products.json', 'w') as file:
        json.dump(products, file)



@app.delete('/delete/{id}')
def delete_product(id:int):
    with open('products.json', 'r') as file:
        products = json.load(file)

    for i in products:
        if i['id'] == id:
            products.remove(i)
            with open('products.json', 'w') as file:
                 json.dump(products, file)
                 return{"item added successfully"}
         
            
    else:
        return{"item not found"}
            
       
    


# Start =(page-1) * limit
# end = start + limit
# or 
# end = page * limit


@app.delete('/delete/{id}')
def delete_product(id:int):
    with open('products.json', 'r') as file:
        products = json.load(file)

    for i in products:
        if i['id'] == id:
            products.remove(i)
            with open('products.json', 'w') as file:
                 json.dump(products, file)
                 return{"item added successfully"}
         
            
    else:
        return{"item not found"}
            