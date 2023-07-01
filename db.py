from dotenv import load_dotenv
import os


from supabase import create_client, Client
load_dotenv()
try:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")

    if not url or not key:
        raise ValueError('Environment variables SUPABASE_URL or SUPABASE_KEY not set')

    supabase: Client = create_client(url, key)
    print('connected boi. good luck')
except ValueError as ve:
    print(f'Error: {ve}')
except Exception as e:
    print(f'Unexpected error: {e}')
