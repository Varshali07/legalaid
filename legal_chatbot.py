import streamlit as st
from googletrans import Translator
from gtts import gTTS
import pandas as pd
import base64

# Load lawyer data
lawyer_data = pd.read_csv("data/lawyerdata.csv")

# Legal Aid Chatbot Homepage (no login)
def legal_aid_homepage():
    translator = Translator()

    lang_dict = {
        "English": "en",
        "Hindi (हिंदी)": "hi",
        "Telugu (తెలుగు)": "te",
        "Tamil (தமிழ்)": "ta",
        "Malayalam (മലയാളം)": "ml"
    }

    sample_cases = {
        "C001": {"status": "Pending court date", "last_updated": "2025-04-20"},
        "C002": {"status": "Hearing completed, verdict awaited", "last_updated": "2025-04-18"}
    }

    @st.cache_data(show_spinner=False)
    def translate_text(text, dest):
        if dest == "en":
            return text
        try:
            return translator.translate(text, dest=dest).text
        except Exception as e:
            return f"Translation error: {e}"

    def get_legal_response(query):
        query = query.lower()
        if "file case" in query:
            return "To file a case, submit a written complaint or petition to the court explaining your issue."
        elif "resolve case" in query:
            return "The time varies based on complexity and court schedule; cases can take months to years."
        elif "miss hearing" in query or "don't show up" in query:
            return "Missing a hearing can result in a warrant or dismissal of your case. Always attend hearings."
        elif "settlement" in query:
            return "Courts encourage settlements through mediation if both parties agree."
        elif "criminal" in query and "civil" in query:
            return "Criminal cases involve crimes; civil cases are disputes between individuals or organizations."
        elif "multiple people" in query or "class action" in query:
            return "Court hears the case with all involved parties, as in class action lawsuits."
        elif "role of lawyer" in query:
            return "Lawyers represent parties by presenting evidence, questioning witnesses, and making arguments."
        elif "guilty" in query:
            return "If found guilty, the court imposes a sentence like jail, fines, or penalties."
        elif "change verdict" in query or "appeal" in query:
            return "Courts can change decisions on appeal or with new evidence."
        elif "lose case" in query:
            return "If you lose, you might have to pay costs and can consider an appeal."
        elif "dismiss case" in query:
            return "Courts can dismiss cases without merit; sometimes cases can be refiled."
        elif "interim order" in query:
            return "Temporary decisions during a case providing immediate relief."
        elif "judge" in query:
            return "The judge ensures fair proceedings, evaluates evidence, and makes final decisions."
        elif "damages" in query:
            return "Courts can order payment of damages to compensate for losses in civil cases."
        elif "bail" in query:
            return "Bail releases someone from custody before trial; surety is the person responsible."
        elif "minor" in query:
            return "Courts prioritize the best interests of minors in cases like custody or offenses."
        elif "represent myself" in query:
            return "You can represent yourself (pro se), but having a lawyer is recommended."
        elif "stay order" in query:
            return "Stay orders temporarily halt an action like eviction or construction."
        elif "court order" in query:
            return "Court orders require someone to do or stop doing something officially."
        elif "criminal case" in query:
            return "Police file FIRs, investigate, and courts hear criminal cases, punishing if guilty."
        elif "civil case" in query:
            return "Civil cases involve filing petitions, presenting evidence, and seeking compensation."
        elif "family court" in query:
            return "Family courts handle divorce, custody, and may suggest mediation."
        elif "consumer case" in query:
            return "Consumer courts resolve complaints against goods and services providers."
        elif "labor court" in query:
            return "Labor courts handle wage disputes and workplace grievances."
        elif "intellectual property" in query or "patent" in query or "copyright" in query:
            return "IP cases involve protecting patents or copyrights and seeking compensation."
        elif "public interest" in query or "pil" in query:
            return "PILs address public issues; courts investigate and order corrective actions."
        elif "property dispute" in query:
            return "Court examines evidence like documents to resolve ownership disputes."
        elif "divorce" in query:
            return "Court decides divorce, custody, and support matters after hearing both parties."
        elif "section 302" in query or "murder" in query:
            return "Section 302 IPC deals with murder, punishable with life imprisonment or death."
        elif "complaint" in query:
            return "You can file complaints at the police station or through online portals."
        elif "constitution" in query:
            return "The Indian Constitution defines citizen rights and government responsibilities."
        elif "section 498a" in query or "domestic violence" in query:
            return "Section 498A IPC protects women from abuse by husband or his family."
        elif "rti" in query:
            return "RTI lets you request information from government authorities."
        elif "alimony" in query:
            return "Failure to pay court-ordered alimony can result in jail."
        elif "anticipatory bail" in query:
            return "Anticipatory bail protects against arrest before trial."
        elif "supreme court" in query or "high court" in query or "district court" in query:
            return "Supreme Court, High Courts, and District Courts handle cases at different levels."
        elif "ipc" in query:
            return "IPC defines crimes and corresponding punishments."
        elif "accident compensation" in query:
            return "You can claim compensation through the Motor Accident Claims Tribunal."
        elif "theft" in query:
            return "Report theft immediately by filing an FIR at the nearest police station."
        elif "business fraud" in query:
            return "File police complaint for fraud and civil suit for compensation."
        elif "cheque bounce" in query:
            return "Send legal notice and then file a cheque bounce case under Section 138."
        elif "land dispute" in query:
            return "Land disputes are handled in civil court and may take years to resolve."
        elif "insurance claim" in query:
            return "Notify your insurer and submit documents; claims take weeks to months."
        elif "labor dispute" in query:
            return "Labor courts address wage and employment-related disputes."
        elif "wrongful arrest" in query:
            return "Apply for bail and challenge wrongful arrests in court."
        elif "child custody" in query:
            return "Family courts decide custody based on the child's best interests."
        elif "eviction" in query:
            return "Challenge unfair evictions through rent control courts."
        elif "defamation" in query:
            return "File a defamation case in civil court if reputation is harmed."
        elif "consumer complaint" in query:
            return "File complaints for faulty goods/services in consumer court."
        elif "fir" in query:
            return "FIR starts a criminal case; without it, police can't investigate."
        elif "police custody" in query:
            return "Without court permission, police custody cannot exceed 24 hours."
        elif "online complaint" in query:
            return "Many police and court services allow online complaint filing."
        elif "women harassment" in query:
            return "Women can file harassment complaints online via special portals."
        elif "judgment copy" in query:
            return "Request certified copies of court judgments from the filing section."
        elif "public prosecutor" in query:
            return "Public prosecutors represent victims and society in criminal cases."
        else:
            return "Thank you for your query. A legal expert will respond shortly."

    def track_case(case_id):
        case = sample_cases.get(case_id.upper())
        if case:
            return f"Status: {case['status']}\nLast Updated: {case['last_updated']}"
        else:
            return "No case found with that ID. Please verify and try again."

    def text_to_speech(text, lang_code):
        tts = gTTS(text=text, lang=lang_code)
        tts.save("response.mp3")
        with open("response.mp3", "rb") as audio_file:
            audio_bytes = audio_file.read()
        b64_audio = base64.b64encode(audio_bytes).decode()
        audio_html = f"""
            <audio controls autoplay>
                <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
        """
        return audio_html

    st.set_page_config(page_title="Legal Aid Chatbot", page_icon="🧑‍⚖️")
    st.title("🧑‍⚖️ Legal Aid Chatbot")

    

    language = st.selectbox("Choose your language", list(lang_dict.keys()))
    lang_code = lang_dict[language]

    ask_label = translate_text("Ask a Legal Question", lang_code)
    track_label = translate_text("Track My Case", lang_code)
    connect_label = translate_text("Connect to Volunteer Lawyer", lang_code)
    support_label = translate_text("Rehabilitation & Support", lang_code)

    menu = st.selectbox(
        translate_text("Choose a service", lang_code),
        [ask_label, track_label, connect_label, support_label]
    )

    if menu == ask_label:
        user_input = st.text_input(translate_text("Enter your legal question:", lang_code))
        if user_input:
            query_en = translate_text(user_input, dest="en")
            response_en = get_legal_response(query_en)
            response_translated = translate_text(response_en, dest=lang_code)
            st.success(response_translated)
            audio_html = text_to_speech(response_translated, lang_code)
            st.markdown(audio_html, unsafe_allow_html=True)

    elif menu == track_label:
        case_id = st.text_input(translate_text("Enter your Case ID (e.g., C001):", lang_code))
        if case_id:
            status_en = track_case(case_id)
            status_translated = translate_text(status_en, dest=lang_code)
            st.info(status_translated)

    elif menu == connect_label:
        lawyer_type = st.selectbox(
            translate_text("Select the type of lawyer you need:", lang_code),
            [
                "Family Law", "Criminal Law", "Property Law", "Consumer Law",
                "Labor Law", "Cybercrime Law", "Intellectual Property Law", "Other"
            ]
        )

        if lawyer_type:  # Ensure lawyer_type is not empty
            filtered_lawyers = lawyer_data[lawyer_data["Specialization"].str.contains(lawyer_type.split()[0], case=False)]

            if not filtered_lawyers.empty:
                st.write(f"### Available {lawyer_type} Lawyers")
                
                # Column Titles
                cols = st.columns([3, 2, 3, 2, 2])
                cols[0].markdown("**Name**")
                cols[1].markdown("**Place**")
                cols[2].markdown("**Specialization**")
                cols[3].markdown("**Cases Solved**")
                cols[4].markdown("**Connect**")

                # Lawyer Details
                for idx, row in filtered_lawyers.iterrows():
                    cols = st.columns([3, 2, 3, 2, 2])  # Widths: Name, Place, Specialization, Cases, Connect
                    cols[0].markdown(f"**{row['Name']}**")
                    cols[1].markdown(row['Place'])
                    cols[2].markdown(row['Specialization'])
                    cols[3].markdown(str(row['Cases_Solved']))
                    connect = cols[4].button(f"Connect", key=f"connect_{idx}")
                    if connect:
                        st.success(f"You have successfully connected with {row['Name']}!")
                        st.stop()
            else:
                st.warning("No lawyers available for the selected category.")

    # elif menu == support_label:
    #     st.write("### Rehabilitation and Support Options")
    #     st.write("Details on legal aid, social services, and rehabilitation programs.")
    elif menu == support_label:
        st.write("### Rehabilitation and Support Options")
        st.write("Details on legal aid, social services, and rehabilitation programs.")

        # Load rehabilitation centers data
        rehab_data = pd.read_csv("data/rehabilitation_centres_states.csv")  # Make sure the correct path

        state_name = st.text_input(translate_text("Enter your State Name:", lang_code))

        if state_name:
            # Filter rehabilitation centers by state
            filtered_rehab = rehab_data[rehab_data["State"].str.contains(state_name, case=False, na=False)]

            if not filtered_rehab.empty:
                st.write(f"### Rehabilitation Centers in {state_name.title()}")

                # Column Titles
                cols = st.columns([3, 3, 2, 3,3])
                cols[0].markdown("**Center Name**")
                cols[1].markdown("**Location**")
                cols[2].markdown("**State**")
                cols[3].markdown("**Mobile Number**")
                cols[4].markdown("**Consultant Name**")

                # List Centers
                for idx, row in filtered_rehab.iterrows():
                    cols = st.columns([3, 3, 2, 3,3])
                    cols[0].markdown(f"**{row['Center Name']}**")
                    cols[1].markdown(row['Location'])  # or row['Address'] based on your dataset
                    cols[2].markdown(row['State'])
                    cols[2].markdown(row['Contact Number'])
                    cols[3].markdown(row['Consultant Name'])
            else:
                st.warning(f"No rehabilitation centers found for {state_name}. Please check your spelling and try again.")


    footer = translate_text("This is a prototype. Always consult a licensed lawyer for formal legal advice.", dest=lang_code)
    st.markdown("---")
    st.caption(footer)

# Run the app
legal_aid_homepage()
