from fastapi import FastAPI
app=FastAPI()
@app.get("/user/detail/")
def getuser():
    return {"message":"hello"}