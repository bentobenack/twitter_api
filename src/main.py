from imp import reload
import uvicorn 

from config.settings import PORT
from config.settings import DEBUG

if __name__ == "__main__":
    uvicorn.run(
        app="app:app",
        host="127.0.0.1",
        port=int(PORT),
        reload=DEBUG
    )