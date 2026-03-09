import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_advice_by_type(acne_type: str):
    response = supabase.table("Advice").select("advice").eq("type", acne_type).execute()
    # Afficher les résultats
    if response.data:
        return response.data[0]["advice"]
    return "No advice found for this type."
