from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from bson import ObjectId
from app.schemas import ServerCreate, ServerUpdate, ServerResponse, UserInDB, CommandRequest
from app.database import db
from app.auth import get_current_user
import asyncssh
import datetime

router = APIRouter(prefix="/servers", tags=["Servers"])

@router.get("/", response_model=List[ServerResponse])
async def get_servers(current_user: UserInDB = Depends(get_current_user)):
    servers = await db.servers.find({"owner_email": current_user.email}).to_list(100)
    return [ServerResponse(**server, id=str(server["_id"])) for server in servers]

@router.post("/", response_model=ServerResponse)
async def create_server(server: ServerCreate, current_user: UserInDB = Depends(get_current_user)):
    server_data = server.dict()
    server_data["owner_email"] = current_user.email
    result = await db.servers.insert_one(server_data)
    created_server = await db.servers.find_one({"_id": result.inserted_id})
    return ServerResponse(**created_server, id=str(created_server["_id"]))

@router.get("/{server_id}", response_model=ServerResponse)
async def get_server(server_id: str, current_user: UserInDB = Depends(get_current_user)):
    try:
        obj_id = ObjectId(server_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid server ID")
        
    server = await db.servers.find_one({"_id": obj_id, "owner_email": current_user.email})
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    return ServerResponse(**server, id=str(server["_id"]))

@router.put("/{server_id}", response_model=ServerResponse)
async def update_server(
    server_id: str, 
    server_update: ServerUpdate, 
    current_user: UserInDB = Depends(get_current_user)
):
    try:
        obj_id = ObjectId(server_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid server ID")
    
    update_data = {k: v for k, v in server_update.dict().items() if v is not None}
    
    if update_data:
        result = await db.servers.update_one(
            {"_id": obj_id, "owner_email": current_user.email},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Server not found")
            
    updated_server = await db.servers.find_one({"_id": obj_id})
    return ServerResponse(**updated_server, id=str(updated_server["_id"]))

@router.delete("/{server_id}")
async def delete_server(server_id: str, current_user: UserInDB = Depends(get_current_user)):
    try:
        obj_id = ObjectId(server_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid server ID")
        
    result = await db.servers.delete_one({"_id": obj_id, "owner_email": current_user.email})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Server not found")
    return {"message": "Server deleted successfully"}

DESTRUCTIVE_COMMANDS = ["rm -rf", "mkfs", "dd", "shutdown", "reboot", ":(){ :|:& };:"]

@router.post("/{server_id}/execute")
async def execute_command(
    server_id: str, 
    command_req: CommandRequest, 
    current_user: UserInDB = Depends(get_current_user)
):
    try:
        obj_id = ObjectId(server_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid server ID")
        
    server = await db.servers.find_one({"_id": obj_id, "owner_email": current_user.email})
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")

    command = command_req.command
    
   
    for d_cmd in DESTRUCTIVE_COMMANDS:
        if d_cmd in command:
             raise HTTPException(status_code=400, detail="Command not allowed (destructive)")

   
    host = server["ip_address"]
    port = server.get("port", 22)
    username = server["username"]
    password = server.get("password")
    
    stdout = ""
    stderr = ""
    exit_status = -1
    
    try:
        async with asyncssh.connect(
            host, 
            port=port, 
            username=username, 
            password=password,
            known_hosts=None 
        ) as conn:
            result = await conn.run(command, check=False)
            stdout = result.stdout
            stderr = result.stderr
            exit_status = result.exit_status
            
    except Exception as e:
        stderr = f"SSH Connection Error: {str(e)}"
        
    log_entry = {
        "server_id": str(obj_id),
        "user_email": current_user.email,
        "command": command,
        "stdout": stdout,
        "stderr": stderr,
        "exit_status": exit_status,
        "timestamp": datetime.datetime.utcnow()
    }
    await db.command_logs.insert_one(log_entry)
    
    return {
        "stdout": stdout,
        "stderr": stderr,
        "exit_status": exit_status
    }
