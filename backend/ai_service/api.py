"""
FastAPI routes for AI Processing Service.
"""

from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from fastapi.responses import JSONResponse

from .schemas import ProcessPostRequest, ProcessPostResponse
from .background_worker import process_post_background
from .utils import logger, validate_post_id, validate_user_id

router = APIRouter(prefix="/ai", tags=["AI Processing"])


@router.post(
    "/process_post",
    response_model=ProcessPostResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Process a post with AI",
    description="Initiates background processing of a post including caption generation, embedding creation, and vector storage."
)
async def process_post(
    request: ProcessPostRequest,
    background_tasks: BackgroundTasks
) -> ProcessPostResponse:
    """
    Process a post with AI services.
    
    This endpoint:
    - Accepts post data
    - Returns immediately with processing status
    - Processes the post in the background (caption, embeddings, vector storage)
    
    Args:
        request: ProcessPostRequest containing post_id, user_id, and optional text/image_url
        background_tasks: FastAPI background tasks manager
        
    Returns:
        ProcessPostResponse with status and post_id
        
    Raises:
        HTTPException: If validation fails
    """
    try:
        # Validate inputs
        if not validate_post_id(request.post_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid post_id"
            )
        
        if not validate_user_id(request.user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user_id"
            )
        
        # Add background task
        background_tasks.add_task(
            process_post_background,
            post_id=request.post_id,
            user_id=request.user_id,
            text=request.text,
            image_url=request.image_url
        )
        
        logger.info(f"Processing initiated for post: {request.post_id}")
        
        return ProcessPostResponse(
            status="processing_started",
            post_id=request.post_id,
            message="Post processing initiated successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error initiating post processing: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to initiate processing: {str(e)}"
        )


@router.get(
    "/health",
    summary="Health check endpoint",
    description="Check if the AI Processing Service is running"
)
async def health_check() -> dict:
    """
    Health check endpoint.
    
    Returns:
        Status dictionary
    """
    return {
        "status": "healthy",
        "service": "AI Processing Service"
    }

