from fastapi import FastAPI

app = FastAPI()

@app.get("/order_processing")
async def process_order():
    #we'll put get ,post requests here that will get send to rabbitmq to communicate with other services
    return {"message": "Order processing service is up and running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)