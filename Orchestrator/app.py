from controllers.vr_controller import router
from config.logger import init_logging
from fastapi import FastAPI
import uvicorn

app = FastAPI()
init_logging()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)