from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import FileResponse
import tempfile
import os
from typing import Optional
import numpy as np
from plyfile import PlyData, PlyElement
import uvicorn

app = FastAPI(title="PLY Compress API", description="API for compressing PLY files")

def reduce_vertices(input_path: str, output_path: str, reduction_factor: float):
    """
    Reduce the number of vertices in a PLY file.
    
    Args:
        input_path: Path to input PLY file
        output_path: Path to output PLY file
        reduction_factor: Factor to reduce vertices by (0.1 to 1.0)
    """
    try:
        # Read PLY file
        plydata = PlyData.read(input_path)
        vertex_data = plydata['vertex']
        
        # Get original vertex count
        original_count = len(vertex_data)
        
        # Calculate number of vertices to keep
        keep_count = int(original_count * reduction_factor)
        
        if keep_count == 0:
            keep_count = 1
        
        # Random sampling of vertices
        indices = np.random.choice(original_count, keep_count, replace=False)
        indices = np.sort(indices)
        
        # Create reduced vertex array
        reduced_vertices = vertex_data[indices]
        
        # Create new PLY element
        reduced_vertex_element = PlyElement.describe(reduced_vertices, 'vertex')
        
        # Write reduced PLY file
        PlyData([reduced_vertex_element]).write(output_path)
        
        return {
            "original_count": original_count,
            "reduced_count": keep_count,
            "reduction_factor": reduction_factor
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PLY file: {str(e)}")

@app.post("/compress")
async def compress_ply(
    file: UploadFile = File(...),
    reduction_factor: float = Form(default=0.5, ge=0.1, le=1.0)
):
    """
    Compress a PLY file by reducing vertices.
    
    - **file**: PLY file to compress
    - **reduction_factor**: Factor to reduce vertices by (0.1 to 1.0, default 0.5)
    """
    
    # Validate file type
    if not file.filename.lower().endswith('.ply'):
        raise HTTPException(status_code=400, detail="File must be a PLY file")
    
    # Create temporary files
    with tempfile.NamedTemporaryFile(delete=False, suffix='.ply') as temp_input:
        # Save uploaded file
        content = await file.read()
        temp_input.write(content)
        temp_input_path = temp_input.name
    
    # Create output file path
    temp_output_path = temp_input_path.replace('.ply', '_compressed.ply')
    
    try:
        # Process the file
        result = reduce_vertices(temp_input_path, temp_output_path, reduction_factor)
        
        # Return the compressed file
        return FileResponse(
            path=temp_output_path,
            filename=f"compressed_{file.filename}",
            media_type='application/octet-stream',
            background=lambda: [os.unlink(temp_input_path), os.unlink(temp_output_path)]
        )
        
    except Exception as e:
        # Clean up temp files on error
        if os.path.exists(temp_input_path):
            os.unlink(temp_input_path)
        if os.path.exists(temp_output_path):
            os.unlink(temp_output_path)
        raise e

@app.get("/")
def read_root():
    """Health check endpoint"""
    return {"message": "PLY Compress API is running", "version": "1.0.0"}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)