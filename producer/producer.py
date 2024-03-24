from fastapi import FastAPI

app = FastAPI()

@app.get("/health_check")
async def health_check():
    #we'll put get ,post requests here that will get send to rabbitmq to communicate with other services
    return {"message": "health check service is up and running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)