from supabase import create_client, Client

SUPABASE_URL="https://gntxfeledxkmnuqeerng.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdudHhmZWxlZHhrbW51cWVlcm5nIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MDg5MjkyOSwiZXhwIjoyMDc2NDY4OTI5fQ.9Jeca_B3-TyIpD4kroaf16cILImoOs6zGtb3X0svV38"


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_advice_by_type(acne_type: str):
    response = supabase.table("Advice").select("advice").eq("type", acne_type).execute()
    # Afficher les résultats
    if response.data:
        return response.data[0]["advice"]
    return "No advice found for this type."
