import os
import openai
import streamlit as st
from dotenv import load_dotenv
from tools.parser import parse_input
from tools.scheduler import generate_schedule
from tools.reminders import schedule_reminders
from tools.blocker import block_sites, unblock_sites

# Load API key
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
openai.api_key = os.getenv('OPENAI_API_KEY')

# --- Streamlit UI ---
st.set_page_config(page_title='Intelligent Daily Planner', layout='centered')
st.title('📅 Intelligent Daily Planner Assistant')

user_input = st.text_area(
    'Enter your tasks, meetings, habits, goals (starting from 06:00 AM Morning):',
    height=200,
    placeholder='Write report (2h)\nTeam meeting at 11:00 (1h)\nGym (1h)\nBlock: https://facebook.com'
)

if st.button('Generate Plan'):
    if not user_input.strip():
        st.warning('Please add at least one item.')
    else:
        data = parse_input(user_input)
        plan = generate_schedule(data)

        st.subheader('Your Daily Plan (from 06:00 AM)')
        for start, end, desc in plan:
            st.write(f'**{start} – {end}**: {desc}')

        # Attempt to block sites
        urls = data.get('block_list', [])
        if urls:
            try:
                block_sites(urls)
                st.info('🔒 Sites blocked for focus sessions.')
            except Exception as e:
                st.error(f'Could not block sites: {e}')

        # Schedule reminders
        try:
            schedule_reminders(plan)
            st.info('⏰ Reminders scheduled (runs in background).')
        except Exception as e:
            st.error(f'Could not schedule reminders: {e}')

st.markdown('---')
st.markdown('Built with OpenAI & Streamlit')