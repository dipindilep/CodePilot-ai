from fastapi import FastAPI

app=FastAPI(
    title="CodePilot-ai",
    description="A Local AI Software engineering assistant",
    version="0.1.0",
)

@app.get("/")
def root():
    return {
        "message": "Welcome to CodePilot-ai!"
    }

