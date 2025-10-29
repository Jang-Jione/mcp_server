# server_sse.py
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import json
import asyncio

app = FastAPI(title="MCP-RAG-Agent (SSE-compatible)")

@app.get("/tools")
async def get_tools():
    async def event_stream():
        tools = {
            "type": "tool_list",
            "tools": [
                {
                    "name": "hello",
                    "description": "Simple check tool",
                    "input_schema": {"type": "object", "properties": {}},
                }
            ],
        }
        # ✅ SSE 포맷
        yield f"event: message\ndata: {json.dumps(tools)}\n\n"
        yield "event: done\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.post("/call")
async def call_tool(req: Request):
    data = await req.json()
    name = data.get("name")

    async def event_stream():
        if name == "hello":
            content = {
                "type": "tool_response",
                "content": [{"type": "text", "text": "👋 Hello from MCP server (SSE)!"}],
            }
        else:
            content = {
                "type": "tool_response",
                "content": [{"type": "text", "text": f"❌ Unknown tool: {name}"}],
            }
        yield f"event: message\ndata: {json.dumps(content)}\n\n"
        yield "event: done\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    print("🚀 SSE MCP server running at http://127.0.0.1:8080/sse")
    uvicorn.run("server:app", host="0.0.0.0", port=8080)
