from fastapi import APIRouter, HTTPException, Depends
from app.schemas.vector import VectorAddRequest, VectorSearchRequest
from app.db.vector_store import vector_db
from app.core.security import get_current_active_user

router = APIRouter()

@router.post("/add")
async def add_to_vector_store(
    request: VectorAddRequest, user=Depends(get_current_active_user)
):
    """
    Add a text to the FAISS vector store.
    """
    try:
        vector_db.add_text(request.text, request.metadata)
        return {"message": "Text added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/search")
async def search_vector_store(
    request: VectorSearchRequest, user=Depends(get_current_active_user)
):
    """
    Perform a similarity search in the FAISS vector store.
    """
    try:
        results = vector_db.search(request.query, request.k)
        return {
            "query": request.query,
            "results": [
                {"text": result.page_content, "metadata": result.metadata}
                for result in results
            ],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
