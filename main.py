from fastapi import FastAPI, UploadFile, File
from supabase_client import get_advice_by_type
from inference_sdk import InferenceHTTPClient
import tempfile


app = FastAPI()

# --- Roboflow Configuration ---
client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="sLue4JoTA2R66Awyfohx"
)

WORKSPACE_NAME = "beoseu"           
WORKFLOW_ID = "custom-workflow"


# --- API Route ---
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Sauvegarder temporairement l'image reçue du Flutter
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
            temp.write(await file.read())
            temp_path = temp.name

        # Appeler ton workflow Roboflow
        result = client.run_workflow(
            workspace_name=WORKSPACE_NAME,
            workflow_id=WORKFLOW_ID,
            images={"image": temp_path},
            use_cache=True
        )

        data = result[0]  
        predictions_dict = data["predictions"]
        detections = predictions_dict["predictions"]
        classes_detected = [d["class"] for d in detections]

        advice_dict = {}
        for acne_type in classes_detected:
            advice_dict[acne_type] = get_advice_by_type(acne_type)
        print(advice_dict)
        return {
            "status": "ok",
            "detected_types": list(classes_detected),
            "advice": advice_dict
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}