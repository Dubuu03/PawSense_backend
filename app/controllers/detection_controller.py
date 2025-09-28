"""
Detection controller for handling detection-related requests
"""

from fastapi import File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from app.models.schemas import DetectionResponse, ErrorResponse, ModelType
from app.services.detection_service_fixed import detection_service


class DetectionController:
    """Controller for detection endpoints"""
    
    @staticmethod
    async def detect_cats(file: UploadFile = File(...)) -> JSONResponse:
        """
        Detect skin conditions in cat images
        
        Args:
            file: Image file to analyze
            
        Returns:
            JSON response with detection results
        """
        try:
            result = await detection_service.process_detection(ModelType.CATS, file)
            return JSONResponse(content=result.model_dump())
        
        except HTTPException as e:
            error_response = ErrorResponse(
                error=e.detail,
                model_type=ModelType.CATS
            )
            return JSONResponse(
                status_code=e.status_code,
                content=error_response.model_dump()
            )
        except Exception as e:
            error_response = ErrorResponse(
                error=f"Unexpected error: {str(e)}",
                model_type=ModelType.CATS
            )
            return JSONResponse(
                status_code=500,
                content=error_response.model_dump()
            )
    
    @staticmethod
    async def detect_dogs(file: UploadFile = File(...)) -> JSONResponse:
        """
        Detect skin conditions in dog images
        
        Args:
            file: Image file to analyze
            
        Returns:
            JSON response with detection results
        """
        try:
            result = await detection_service.process_detection(ModelType.DOGS, file)
            return JSONResponse(content=result.model_dump())
        
        except HTTPException as e:
            error_response = ErrorResponse(
                error=e.detail,
                model_type=ModelType.DOGS
            )
            return JSONResponse(
                status_code=e.status_code,
                content=error_response.model_dump()
            )
        except Exception as e:
            error_response = ErrorResponse(
                error=f"Unexpected error: {str(e)}",
                model_type=ModelType.DOGS
            )
            return JSONResponse(
                status_code=500,
                content=error_response.model_dump()
            )
    
    @staticmethod
    async def debug_model_output(model_type: str, file: UploadFile = File(...)) -> JSONResponse:
        """
        Debug method to see raw model output
        
        Args:
            model_type: Either 'cats' or 'dogs'
            file: Image file to analyze
            
        Returns:
            JSON response with raw model debug info
        """
        try:
            from app.services.detection_service import detection_service
            import io
            import numpy as np
            from PIL import Image
            
            # Validate image
            detection_service.validate_image(file)
            
            # Read and process image
            image_data = await file.read()
            image = Image.open(io.BytesIO(image_data))
            
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Get model resources
            from app.services.model_service import model_service
            model = model_service.get_model(model_type)
            labels = model_service.get_labels(model_type)
            
            # Get input and output details
            input_details = model.get_input_details()
            output_details = model.get_output_details()
            
            # Preprocess image
            input_shape = input_details[0]['shape']
            height, width = input_shape[1], input_shape[2]
            
            image_resized = image.resize((width, height))
            image_rgb = image_resized.convert('RGB')
            input_data = np.array(image_rgb, dtype=np.float32) / 255.0
            input_data = np.expand_dims(input_data, axis=0)
            
            # Run inference
            model.set_tensor(input_details[0]['index'], input_data)
            model.invoke()
            
            # Get all outputs
            outputs = []
            for i, detail in enumerate(output_details):
                output = model.get_tensor(detail['index'])
                # Convert to native Python types for JSON serialization
                sample_values = output.flatten()[:10]
                sample_list = [float(x) for x in sample_values]  # Force conversion to Python float
                
                outputs.append({
                    "index": i,
                    "shape": [int(x) for x in output.shape],
                    "dtype": str(output.dtype),
                    "min": float(output.min()),
                    "max": float(output.max()),
                    "mean": float(output.mean()),
                    "sample_values": sample_list
                })
            
            # Convert labels to ensure JSON serialization
            json_labels = {str(k): str(v) for k, v in labels.items()}
            
            debug_info = {
                "filename": file.filename,
                "model_type": model_type,
                "image_size": [int(x) for x in image.size],
                "input_details": [{
                    "name": str(detail.get("name", "")),
                    "shape": [int(x) for x in detail["shape"]], 
                    "dtype": str(detail["dtype"])
                } for detail in input_details],
                "output_details": [{
                    "name": str(detail.get("name", "")),
                    "shape": [int(x) for x in detail["shape"]],
                    "dtype": str(detail["dtype"])
                } for detail in output_details],
                "outputs": outputs,
                "labels": json_labels
            }
            
            return JSONResponse(content=debug_info)
        
        except Exception as e:
            import traceback
            return JSONResponse(
                status_code=500,
                content={
                    "error": f"Debug error: {str(e)}",
                    "traceback": traceback.format_exc()
                }
            )


# Controller instance
detection_controller = DetectionController()