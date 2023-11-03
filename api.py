from fastapi import FastAPI, HTTPException
import traceback

# uvicorn api:app --reload --port 8002

app = FastAPI()

def read_invite_url():
    try:
        with open('invite_url.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None
    except Exception as e:
        traceback.print_exc()
        return None

@app.get("/invite/")
async def get_invite_url():
    invite_url = read_invite_url()
    if invite_url:
        return {"invite_url": invite_url}
    else:
        raise HTTPException(status_code=404, detail="Invite URL not available yet")
