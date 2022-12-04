from distutils.log import debug
from imp import reload
import uvicorn
from core.settings import PORT, HOSTNAME, DEBUG

if __name__ == '__main__':
    uvicorn.run(
        app = 'main:app',
        host=HOSTNAME,
        port=PORT,
        reload=DEBUG,
        log_level='info',
        lifespan='on'
    )