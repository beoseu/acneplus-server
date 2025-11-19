from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware   
from supabase_client import get_advice_by_type
from inference_sdk import InferenceHTTPClient
import tempfile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Roboflow Configuration ---
client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="sLue4JoTA2R66Awyfohx"
)

WORKSPACE_NAME = "beoseu"
WORKFLOW_ID = "detect-count-and-visualize"


# --- API Route ---
@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp:
            temp.write(await file.read())
            temp_path = temp.name

        result = client.run_workflow(
    workspace_name=WORKSPACE_NAME,
    workflow_id=WORKFLOW_ID,
    images={"image": temp_path},
    use_cache=True
)
        
        data = result[0]


        output_image_b64 = data.get("output_image")

        predictions_dict = data["predictions"]
        detections = predictions_dict["predictions"]
        classes_detected = [d["class"] for d in detections]

        advice_dict = {}
        for acne_type in classes_detected:
            advice_dict[acne_type] = get_advice_by_type(acne_type)

        return {
            "status": "ok",
            "detected_types": list(classes_detected),
            "advice": advice_dict,
            "output_image": output_image_b64,   # 👈 ส่งกลับไปด้วย
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
