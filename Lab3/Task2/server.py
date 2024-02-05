#run it with uvicorn server:app --host <ip address> --port 8000 --reload


from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse


app = FastAPI()

uploadFile = []


@app.get("/", response_class=HTMLResponse)
def read_root():
    return ("ok")


@app.get("/download/{fileName}")
def download_file(fileName: str):
    return FileResponse(fileName, media_type="application/octet-stream", filename=fileName)


@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
    uploadFile.append(file.filename)
    return {"filename": file.filename}


@app.get("/list")
def list_all_files():
    return {"files": uploadFile}
