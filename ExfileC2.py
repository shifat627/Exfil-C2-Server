from fastapi import FastAPI,File,UploadFile,Path
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import PlainTextResponse
import shutil,uvicorn,sys,os
from datetime import datetime

from typing import Annotated

if (len(sys.argv)!=2):
    print(f"usage {sys.argv[0]} <port>")




UPLOAD_DIR = os.path.join(os.path.dirname(__file__),'uploaded_file')
STATIC_DIR = os.path.join(os.path.dirname(__file__),'static')
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__),'templates')

if not os.path.exists(UPLOAD_DIR):
    os.mkdir(UPLOAD_DIR)

if not os.path.exists(STATIC_DIR):
    os.mkdir(STATIC_DIR)

app = FastAPI()
app.mount('/s',StaticFiles(directory=STATIC_DIR),'staticfiles')
app.mount('/files',StaticFiles(directory=UPLOAD_DIR),'myfiles')
Templates = Jinja2Templates(TEMPLATE_DIR)






@app.post('/give')
async def RecieveFile(fp:UploadFile = File(alias='file')):
    with open(os.path.join(UPLOAD_DIR,fp.filename),'wb') as origFile:
        shutil.copyfileobj(fp.file,origFile)
    
    res = PlainTextResponse(content="I got Your File.Thank You",status_code=200)
    return res


@app.post('/giveRaw/{filename}')
async def RecieveFileRaw(req:Request,filename : str = Path()):
    filename = filename.replace('../','_').replace('..\\','_')
    with open(os.path.join(UPLOAD_DIR,filename),'wb') as origFile:
        origFile.write(await req.body())
    
    res = PlainTextResponse(content="I got Your File.Thank You",status_code=200)
    return res

@app.post('/multiple_upload_Files')
async def handle_Multiple_Files(files: Annotated[list[UploadFile],File(description="Multiple files as UploadFile")]):
    for fp in files:
        with open(os.path.join(UPLOAD_DIR,fp.filename),'wb') as origFile:
            shutil.copyfileobj(fp.file,origFile)
    
    res = PlainTextResponse(content="I got Your File.Thank You",status_code=200)
    return res



@app.get('/guf')
async def uploadForm(req : Request):
    return Templates.TemplateResponse('upload.html',context={'date':datetime.now(),"request":req})

@app.get('/')
async def Index(req : Request):
    return Templates.TemplateResponse('index.html',context={'date':datetime.now(),"request":req })

if __name__ == "__main__":
    uvicorn.run(app=app,host='0.0.0.0',port=int(sys.argv[1]),access_log=True)