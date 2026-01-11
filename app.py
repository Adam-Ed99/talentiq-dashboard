import streamlit as st
from supabase import create_client, Client
import os
import pandas as pd

# Supabase env vars (Elest.io)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY
