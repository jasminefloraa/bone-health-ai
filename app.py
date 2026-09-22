import streamlit as st
import pandas as pd
import numpy as np
import joblib
import shap
import matplotlib.pyplot as plt
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Page Configuration
st.set_page_config(page_title="A3J Women's & Maternal Health Center", layout="wide")

# Polished Professional Clinical Theme CSS with Google Font Integration & Centered Banner Text
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700&display=swap');

    header[data-testid="stHeader"] {
        background-color: transparent !important;
        display: none;
    }
    .stApp {
        background-color: #F1F5F9;
        color: #1E293B;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    label, .stNumberInput label, .stSelectbox label {
        color: #0F172A !important;
        font-weight: 700 !important;
        font-size: 14px !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid #1E3A8A;
    }
    section[data-testid="stSidebar"] * {
        color: #F8FAFC !important;
    }
    
    section[data-testid="stSidebar"] div.stButton > button,
    section[data-testid="stSidebar"] div.stButton > button:hover,
    section[data-testid="stSidebar"] div.stButton > button:active,
    section[data-testid="stSidebar"] div.stButton > button:focus {
        background-color: #38BDF8 !important;
        color: #FFFFFF !important;
        border: 1px solid #0EA5E9 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        width: 100% !important;
        box-shadow: none !important;
    }

    .hospital-banner {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
        padding: 28px 20px;
        border-radius: 12px;
        color: white;
        margin-bottom: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        text-align: center !important;
    }
    .hospital-banner h1 {
        font-family: 'Montserrat', sans-serif !important;
        color: #FFFFFF !important;
        font-size: 24px !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        margin: 0 !important;
        text-align: center !important;
    }
    .hospital-banner p {
        color: #93C5FD !important;
        font-size: 12px !important;
        margin-top: 6px !important;
        text-align: center !important;
    }
    .clinical-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .stTextInput input, .stNumberInput input {
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        font-weight: 500;
    }

    div.stButton > button[kind="primary"],
    div.stButton > button[kind="primary"]:hover,
    div.stButton > button[kind="primary"]:active,
    div.stButton > button[kind="primary"]:focus,
    div.stDownloadButton > button,
    div.stDownloadButton > button:hover,
    div.stDownloadButton > button:active {
        background-color: #38BDF8 !important;
        color: #FFFFFF !important;
        border: 1px solid #0EA5E9 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        width: 100% !important;
        box-shadow: none !important;
    }

    div.stButton > button[kind="secondary"],
    div.stButton > button:not([kind="primary"]) {
        background-color: #E2E8F0 !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        box-shadow: none !important;
    }
    div.stButton > button[kind="secondary"]:hover,
    div.stButton > button:not([kind="primary"]):hover {
        background-color: #CBD5E1 !important;
        color: #0F172A !important;
    }

    .streamlit-expanderHeader, [data-testid="stExpander"] summary {
        background-color: #FFFFFF !important;
        color: #0F172A !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# State management
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

if 'patient_history' not in st.session_state:
    st.session_state['patient_history'] = []

# Load model safely
@st.cache_resource
def load_model():
    return joblib.load("bone_health_model.pkl")

try:
    model = load_model()
except Exception:
    model = None

# PDF Generator with 3-tier risk logic and weight adjustments
def generate_hospital_pdf_report(patient_name, patient_id, age, lactation, bed_rest, calcium, vit_d, pre_weight, post_weight, risk_label, proba):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=30, bottomMargin=30)
    styles = getSampleStyleSheet()
    story = []
    
    h1_style = ParagraphStyle('HospitalTitle', parent=styles['Heading1'], fontSize=16, leading=20, textColor=colors.HexColor('#0F172A'), fontName='Helvetica-Bold')
    sub_title = ParagraphStyle('HospitalSub', parent=styles['Normal'], fontSize=9, leading=12, textColor=colors.HexColor('#475569'))
    header_style = ParagraphStyle('SectionHeader', parent=styles['Heading2'], fontSize=12, leading=16, textColor=colors.HexColor('#1E3A8A'), fontName='Helvetica-Bold')
    normal_style = ParagraphStyle('BodyText', parent=styles['Normal'], fontSize=10, leading=14, textColor=colors.HexColor('#1E293B'))
    bold_style = ParagraphStyle('BoldText', parent=styles['Normal'], fontSize=10, leading=14, fontName='Helvetica-Bold', textColor=colors.HexColor('#0F172A'))
    
    story.append(Paragraph("A3J WOMEN'S & MATERNAL HEALTH CENTER", h1_style))
    story.append(Paragraph("Department of Orthopedics & Postpartum Rehabilitation | Clinical AI Analytics Division", sub_title))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#0F172A'), spaceAfter=15))
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    meta_data = [
        [Paragraph(f"<b>Patient Name:</b> {patient_name}", normal_style), Paragraph(f"<b>Report Date:</b> {current_time}", normal_style)],
        [Paragraph(f"<b>Patient ID / MRN:</b> {patient_id}", normal_style), Paragraph("<b>Referring Unit:</b> Post-Op C-Section Ward", normal_style)],
    ]
    meta_table = Table(meta_data, colWidths=[260, 270])
    meta_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')), ('PADDING', (0, 0), (-1, -1), 6), ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0'))]))
    story.append(meta_table)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("CLINICAL PARAMETERS & OBSERVATIONS", header_style))
    story.append(Spacer(1, 5))
    param_data = [
        [Paragraph("<b>Clinical Metric</b>", bold_style), Paragraph("<b>Recorded Value</b>", bold_style), Paragraph("<b>Reference Threshold</b>", bold_style)],
        [Paragraph("Pre-Pregnancy / Pre-Op Weight", normal_style), Paragraph(f"{pre_weight} kg", normal_style), Paragraph("Baseline measure", normal_style)],
        [Paragraph("Postpartum / Current Weight", normal_style), Paragraph(f"{post_weight} kg", normal_style), Paragraph("Post-op tracking", normal_style)],
        [Paragraph("Post-C-Section Bed Rest", normal_style), Paragraph(f"{bed_rest} Days", normal_style), Paragraph("< 14 Days", normal_style)],
        [Paragraph("Lactation Duration", normal_style), Paragraph(f"{lactation} Months", normal_style), Paragraph("Standard monitoring", normal_style)],
        [Paragraph("Daily Calcium Intake", normal_style), Paragraph(f"{calcium} mg/day", normal_style), Paragraph("1000 - 1300 mg/day", normal_style)],
        [Paragraph("Serum Vitamin D Level", normal_style), Paragraph(f"{vit_d} ng/mL", normal_style), Paragraph("30 - 50 ng/mL", normal_style)],
    ]
    param_table = Table(param_data, colWidths=[200, 150, 180])
    param_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F1F5F9')), ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')), ('PADDING', (0, 0), (-1, -1), 5)]))
    story.append(param_table)
    story.append(Spacer(1, 15))
    
    if "High" in risk_label:
        bg_color, border_color, text_color = colors.HexColor('#FEF2F2'), colors.HexColor('#EF4444'), "#991B1B"
    elif "Moderate" in risk_label:
        bg_color, border_color, text_color = colors.HexColor('#FEFCE8'), colors.HexColor('#EAB308'), "#854D0E"
    else:
        bg_color, border_color, text_color = colors.HexColor('#F0FDF4'), colors.HexColor('#22C55E'), "#166534"
    
    finding_html = f"<font color='{text_color}'><b>STATUS: {risk_label.upper()}</b></font><br/>Estimated BMD Loss Risk Probability: <b>{proba:.1%}</b>"
    finding_table = Table([[Paragraph(finding_html, normal_style)]], colWidths=[530])
    finding_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), bg_color), ('BOX', (0, 0), (-1, -1), 1.5, border_color), ('PADDING', (0, 0), (-1, -1), 8)]))
    story.append(finding_table)
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# Sidebar Navigation Setup
st.sidebar.markdown("### Hospital Navigation")
st.sidebar.markdown("---")
if st.sidebar.button("Home Overview", type="primary", use_container_width=True):
    st.session_state['page'] = 'home'
if st.sidebar.button("Postpartum BMD Risk Assessor", type="primary", use_container_width=True):
    st.session_state['page'] = 'assessor'

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='font-size:12px; color:#94A3B8;'>
<b>A3J Women's & Maternal Health Center</b><br>
Department of Orthopedics & Postpartum Recovery<br>
Clinical Decision-Support Tool v1.2
</div>
""", unsafe_allow_html=True)

# PAGE 1: HOME OVERVIEW
if st.session_state['page'] == 'home':
    st.markdown("""
        <div class="hospital-banner">
            <h1>A3J WOMEN'S & MATERNAL HEALTH CENTER</h1>
            <p>Department of Orthopedics & Postpartum Rehabilitation | Clinical Analytics Division</p>
        </div>
    """, unsafe_allow_html=True)

    col_h1, col_h2 = st.columns([2, 1], gap="medium")
    with col_h1:
        st.markdown("""
        <div class="clinical-card">
            <h3 style="color: #0F172A; margin-top:0;">Clinical AI Decision-Support Platform</h3>
            <p>Welcome to the <b>Postpartum Bone Health Screening Portal</b>. Our platform provides evidence-based predictive analytics to evaluate <b>Bone Mineral Density (BMD) loss risks</b> in post-C-section recovery patients.</p>
            <br>
            <h4 style="color: #1E3A8A; font-size: 16px; margin-bottom: 8px;">Key Operational Features</h4>
            <ul style="color: #334155; font-size: 14px; line-height: 1.6; margin-top: 0; padding-left: 20px;">
                <li><b>Early Risk Stratification:</b> Machine-learning evaluation of key clinical parameters like post-op bed rest, serum Vitamin D, calcium intake, and weight dynamics.</li>
                <li><b>Explainable AI (SHAP):</b> Transparent factor contribution analysis to understand individual patient risk drivers.</li>
                <li><b>Official PDF Reporting:</b> Direct generation of standardized hospital clinical summaries complete with diagnostic recommendation blocks.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch Clinical Assessor Portal", type="primary", use_container_width=True):
            st.session_state['page'] = 'assessor'
            st.rerun()

    with col_h2:
        st.markdown("""
        <div class="clinical-card">
            <h3 style="color: #0F172A; font-size: 18px; margin-top:0;">Center Quick Info</h3>
            <hr style="border:0; border-top:1px solid #E2E8F0; margin:12px 0;">
            <p style="font-size: 13px; color: #334155; margin-bottom: 8px;"><b>Protocol:</b> Post-C-Section BMD Risk</p>
            <p style="font-size: 13px; color: #334155; margin-bottom: 8px;"><b>Model:</b> Random Forest Classifier</p>
            <p style="font-size: 13px; color: #334155; margin-bottom: 15px;"><b>Target Population:</b> Postpartum Patients</p>
            <hr style="border:0; border-top:1px solid #E2E8F0; margin:12px 0;">
            <p style="font-size: 11px; color: #64748B; margin: 0;">Need technical support or workflow assistance? Contact the Clinical IT Helpdesk at Ext. 2831.</p>
        </div>
        """, unsafe_allow_html=True)

# PAGE 2: CLINICAL ASSESSOR
elif st.session_state['page'] == 'assessor':
    st.markdown("""
        <div class="hospital-banner">
            <h1>Postpartum Bone Health Risk Assessor</h1>
            <p>Patient Diagnostic Evaluation & Explainable AI Risk Profiling</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="clinical-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: #0F172A; font-size:16px; margin-top:0;'>Patient Chart Management & Lookup</h3>", unsafe_allow_html=True)
    
    col_ctrl1, col_ctrl2 = st.columns([4, 1], gap="medium")
    
    with col_ctrl1:
        unique_patients = {}
        for item in st.session_state['patient_history']:
            unique_patients[item['MRN']] = item['Patient Name']
            
        patient_list_opts = ["-- Select Existing Patient Record --"]
        if len(unique_patients) > 0:
            patient_list_opts += [f"Patient: {name} (MRN: {mrn})" for mrn, name in unique_patients.items()]

        selected_patient_lookup = st.selectbox("Returning Patient Chart Lookup", patient_list_opts)
        
        if selected_patient_lookup != "-- Select Existing Patient Record --":
            selected_mrn = selected_patient_lookup.split("(MRN: ")[1].replace(")", "").strip()
            patient_visits = [v for v in st.session_state['patient_history'] if v['MRN'] == selected_mrn]
            if patient_visits:
                latest_visit = patient_visits[0]
                st.session_state['form_name'] = latest_visit['Patient Name']
                st.session_state['form_id'] = latest_visit['MRN']
                st.session_state['form_age'] = latest_visit['Age']
                st.session_state['form_lac'] = latest_visit['Lactation (Mo)']
                st.session_state['form_bed'] = latest_visit['Bed Rest (Days)']
                st.session_state['form_calc'] = latest_visit['Calcium (mg)']
                st.session_state['form_vit'] = latest_visit['Vit D (ng/mL)']
                st.session_state['form_pre_wt'] = latest_visit.get('Pre Weight (kg)', 65.0)
                st.session_state['form_post_wt'] = latest_visit.get('Post Weight (kg)', 60.0)

    with col_ctrl2:
        st.markdown("<div style='height: 27px;'></div>", unsafe_allow_html=True)
        if st.button("➕ New Patient", type="primary", use_container_width=True):
            st.session_state['form_name'] = ""
            st.session_state['form_id'] = f"PAT-2026-{np.random.randint(1000, 9999)}"
            st.session_state['form_age'] = 28
            st.session_state['form_lac'] = 4
            st.session_state['form_bed'] = 14
            st.session_state['form_calc'] = 800
            st.session_state['form_vit'] = 22
            st.session_state['form_pre_wt'] = 65.0
            st.session_state['form_post_wt'] = 60.0
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

    f_name = st.session_state.get('form_name', '')
    f_id = st.session_state.get('form_id', f"PAT-2026-{np.random.randint(1000, 9999)}")
    f_age = st.session_state.get('form_age', 28)
    f_lac = st.session_state.get('form_lac', 4)
    f_bed = st.session_state.get('form_bed', 14)
    f_calc = st.session_state.get('form_calc', 800)
    f_vit = st.session_state.get('form_vit', 22)
    f_pre_wt = st.session_state.get('form_pre_wt', 65.0)
    f_post_wt = st.session_state.get('form_post_wt', 60.0)

    col1, col2 = st.columns([1, 1], gap="medium")
    
    with col1:
        st.markdown('<div class="clinical-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color: #0F172A; font-size:18px;'>Patient Demographics & Identification</h3>", unsafe_allow_html=True)
        patient_name = st.text_input("Patient Full Name", f_name)
        patient_id = st.text_input("Patient ID / MRN", f_id)
        
        st.markdown("<hr style='border:0; border-top:1px solid #E2E8F0; margin:20px 0;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #0F172A; font-size:18px;'>Recorded Clinical Observations (Today's Follow-up)</h3>", unsafe_allow_html=True)
        
        age = st.number_input("Patient Age (Years)", 18, 50, int(f_age))
        pre_weight = st.number_input("Pre-Pregnancy / Pre-Op Weight (kg)", 30.0, 200.0, float(f_pre_wt), step=0.5)
        post_weight = st.number_input("Postpartum / Current Weight (kg)", 30.0, 200.0, float(f_post_wt), step=0.5)
        lactation = st.number_input("Lactation Duration (Months)", 0, 24, int(f_lac))
        bed_rest = st.number_input("Post-C-Section Bed Rest (Days)", 1, 60, int(f_bed))
        calcium = st.number_input("Daily Calcium Intake (mg/day)", 300, 2000, int(f_calc))
        vit_d = st.number_input("Serum Vitamin D (ng/mL)", 5, 80, int(f_vit))
        
        st.markdown("<br>", unsafe_allow_html=True)
        evaluate = st.button("Run Diagnostic Evaluation & Log Visit", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="clinical-card">', unsafe_allow_html=True)
        st.markdown("<h3 style='color: #0F172A; font-size:18px;'>Diagnostic Assessment Results</h3>", unsafe_allow_html=True)
        
        if evaluate and model is not None:
            input_data = pd.DataFrame(
                [[age, lactation, bed_rest, calcium, vit_d, pre_weight, post_weight]], 
                columns=['age', 'lactation_months', 'bed_rest_days', 'calcium_intake_mg', 'vit_d_ngml', 'pre_weight_kg', 'post_weight_kg']
            )
            
            try:
                base_probability = model.predict_proba(input_data)[0][1]
            except Exception:
                input_data_5 = pd.DataFrame(
                    [[age, lactation, bed_rest, calcium, vit_d]], 
                    columns=['age', 'lactation_months', 'bed_rest_days', 'calcium_intake_mg', 'vit_d_ngml']
                )
                base_probability = model.predict_proba(input_data_5)[0][1]
            
            # --- CLINICAL WEIGHT FACTOR ADJUSTMENT LOGIC ---
            weight_loss = pre_weight - post_weight
            weight_adjustment = 0.0

            if weight_loss > 18.0 or post_weight < 45.0:
                weight_adjustment = 0.35  # Substantial risk bump for rapid weight loss / low mass
            elif weight_loss > 10.0:
                weight_adjustment = 0.15  # Moderate risk bump

            probability = min(1.0, base_probability + weight_adjustment)

            # --- 3-TIER RISK ASSIGNMENT LOGIC ---
            if probability >= 0.65:
                risk_text = "High Risk of BMD Loss"
            elif probability >= 0.35:
                risk_text = "Moderate Risk of BMD Loss"
            else:
                risk_text = "Low Risk"
            
            st.session_state['last_eval_input'] = input_data
            st.session_state['last_probability'] = probability
            st.session_state['last_risk_text'] = risk_text
            st.session_state['last_patient_name'] = patient_name
            st.session_state['last_patient_id'] = patient_id
            st.session_state['last_age'] = age
            st.session_state['last_lactation'] = lactation
            st.session_state['last_bed_rest'] = bed_rest
            st.session_state['last_calcium'] = calcium
            st.session_state['last_vit_d'] = vit_d
            st.session_state['last_pre_wt'] = pre_weight
            st.session_state['last_post_wt'] = post_weight

            past_visits = [v for v in st.session_state['patient_history'] if v['MRN'] == patient_id]
            
            current_visit_record = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Patient Name": patient_name,
                "MRN": patient_id,
                "Age": age,
                "Pre Weight (kg)": pre_weight,
                "Post Weight (kg)": post_weight,
                "Lactation (Mo)": lactation,
                "Bed Rest (Days)": bed_rest,
                "Calcium (mg)": calcium,
                "Vit D (ng/mL)": vit_d,
                "Status": risk_text,
                "Probability": f"{probability:.1%}"
            }
            if not past_visits or past_visits[0]['Timestamp'] != current_visit_record['Timestamp']:
                st.session_state['patient_history'].insert(0, current_visit_record)

        if 'last_probability' in st.session_state and model is not None:
            probability = st.session_state['last_probability']
            risk_text = st.session_state['last_risk_text']
            input_data = st.session_state['last_eval_input']
            patient_name = st.session_state['last_patient_name']
            patient_id = st.session_state['last_patient_id']
            age = st.session_state['last_age']
            lactation = st.session_state['last_lactation']
            bed_rest = st.session_state['last_bed_rest']
            calcium = st.session_state['last_calcium']
            vit_d = st.session_state['last_vit_d']
            pre_weight = st.session_state['last_pre_wt']
            post_weight = st.session_state['last_post_wt']

            past_visits = [v for v in st.session_state['patient_history'] if v['MRN'] == patient_id and v['Timestamp'] != st.session_state['patient_history'][0]['Timestamp']]
            previous_visit = past_visits[0] if past_visits else None

            # --- DYNAMIC UI ALERTS BASED ON RISK TIER ---
            if "High" in risk_text:
                st.error(f"**STATUS: {risk_text.upper()}**\n\nEstimated Probability: **{probability:.1%}**")
                st.markdown("""
                    <div style='background-color: #FEE2E2; border-left: 4px solid #DC2626; padding: 12px; border-radius: 4px; margin-top: 15px; margin-bottom: 15px;'>
                        <b style='color: #991B1B;'> URGENT CLINICAL RECOMMENDATION:</b><br>
                        <span style='color: #7F1D1D; font-size: 13px;'>Patient exhibits high indicators for postpartum BMD depletion. Recommended protocol: Encourage supervised ambulation, prescribe high-dose Vitamin D supplementation, review calcium infusion therapy, evaluate weight changes, and schedule a follow-up scan within 14 days.</span>
                    </div>
                """, unsafe_allow_html=True)
            elif "Moderate" in risk_text:
                st.markdown(f"""
                    <div style='background-color: #FEFCE8; border: 1px solid #EAB308; border-left: 6px solid #EAB308; padding: 16px; border-radius: 8px; margin-bottom: 15px;'>
                        <b style='color: #854D0E; font-size: 15px;'>STATUS: {risk_text.upper()}</b><br>
                        <span style='color: #713F12; font-size: 14px;'>Estimated Probability: <b>{probability:.1%}</b></span>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown("""
                    <div style='background-color: #FEFCE8; border-left: 4px solid #EAB308; padding: 12px; border-radius: 4px; margin-top: 15px; margin-bottom: 15px;'>
                        <b style='color: #854D0E;'>⚠️ MODERATE CLINICAL WATCH:</b><br>
                        <span style='color: #713F12; font-size: 13px;'>Patient shows bordering indicators for bone mineral density loss. Recommended protocol: Increase dietary calcium, monitor Vitamin D levels and weight fluctuations closely, encourage progressive physical activity, and schedule a re-evaluation in 30 days.</span>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.success(f"**STATUS: {risk_text.upper()}**\n\nEstimated Probability: **{probability:.1%}**")
                st.markdown("""
                    <div style='background-color: #ECFDF5; border-left: 4px solid #059669; padding: 12px; border-radius: 4px; margin-top: 15px; margin-bottom: 15px;'>
                        <b style='color: #065F46;'>✅ ROUTINE MANAGEMENT PROTOCOL:</b><br>
                        <span style='color: #064E3B; font-size: 13px;'>Parameters are stable. Maintain standard dietary calcium guidelines, encourage light postpartum mobility, ensure proper lactation support, track healthy postpartum weight recovery, and schedule routine follow-up at the 6-month checkup.</span>
                    </div>
                """, unsafe_allow_html=True)
                
            if previous_visit is not None:
                st.markdown("<hr style='border:0; border-top:1px solid #E2E8F0; margin:15px 0;'>", unsafe_allow_html=True)
                st.markdown(f"<h4 style='color: #1E3A8A; font-size:15px;'>Clinical Progress & Delta Comparison (vs Last Visit on {previous_visit['Timestamp']})</h4>", unsafe_allow_html=True)
                
                prev_vit = previous_visit['Vit D (ng/mL)']
                prev_calc = previous_visit['Calcium (mg)']
                prev_bed = previous_visit['Bed Rest (Days)']
                prev_prob = previous_visit['Probability']
                prev_post_wt = previous_visit.get('Post Weight (kg)', post_weight)
                
                vit_diff = vit_d - prev_vit
                calc_diff = calcium - prev_calc
                bed_diff = bed_rest - prev_bed
                wt_diff = post_weight - prev_post_wt
                
                vit_str = f"📈 Improved (+{vit_diff} ng/mL)" if vit_diff > 0 else (f"📉 Declined ({vit_diff} ng/mL)" if vit_diff < 0 else "No Change")
                calc_str = f"📈 Improved (+{calc_diff} mg)" if calc_diff > 0 else (f"📉 Declined ({calc_diff} mg)" if calc_diff < 0 else "No Change")
                bed_str = f"✅ Reduced Bed Rest ({bed_diff} days)" if bed_diff < 0 else (f"⚠️ Increased Bed Rest (+{bed_diff} days)" if bed_diff > 0 else "No Change")
                wt_str = f"Change: {wt_diff:+.1f} kg"

                st.markdown(f"""
                * **Current Postpartum Weight:** {prev_post_wt} kg &rarr; **{post_weight} kg** &nbsp;|&nbsp; `{wt_str}`
                * **Serum Vitamin D:** {prev_vit} ng/mL &rarr; **{vit_d} ng/mL** &nbsp;|&nbsp; `{vit_str}`
                * **Calcium Intake:** {prev_calc} mg &rarr; **{calcium} mg** &nbsp;|&nbsp; `{calc_str}`
                * **Bed Rest Duration:** {prev_bed} days &rarr; **{bed_rest} days** &nbsp;|&nbsp; `{bed_str}`
                * **Risk Probability Trend:** {prev_prob} &rarr; **{probability:.1%}**
                """)
            else:
                st.info("ℹ️ This is the first recorded baseline evaluation for this patient ID. Future checkups will automatically compare against this record.")
            
            pdf_data = generate_hospital_pdf_report(
                patient_name, patient_id, age, lactation, bed_rest, calcium, vit_d, pre_weight, post_weight, risk_text, probability
            )
            
            clean_filename = patient_name.replace(" ", "_")
            st.download_button(
                label="Download Official Hospital PDF Report",
                data=pdf_data,
                file_name=f"Hospital_BMD_Report_{clean_filename}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            
            st.markdown("<hr style='border:0; border-top:1px solid #E2E8F0; margin:20px 0;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='color: #0F172A; font-size:18px;'>SHAP Risk Driver Analysis</h3>", unsafe_allow_html=True)
            
            explainer = shap.TreeExplainer(model)
            shap_values = explainer(input_data.iloc[:, :5] if input_data.shape[1] > 5 else input_data)
            
            fig, ax = plt.subplots(figsize=(6, 4))
            shap.plots.bar(shap_values[0][:, 1], show=False)
            st.pyplot(fig, use_container_width=True)
        elif model is None:
            st.error("Model file `bone_health_model.pkl` not found in current directory.")
        else:
            st.info("Fill out patient details or select a returning patient chart from the dropdown above to run a follow-up assessment.")
            
        st.markdown('</div>', unsafe_allow_html=True)

    with st.expander(" Complete Hospital Ward Consultation History", expanded=False):
        if len(st.session_state['patient_history']) > 0:
            history_df = pd.DataFrame(st.session_state['patient_history'])
            st.dataframe(history_df, use_container_width=True)
            
            if st.button("Clear Consultation History"):
                st.session_state['patient_history'] = []
                if 'last_probability' in st.session_state:
                    del st.session_state['last_probability']
                st.rerun()
        else:
            st.info("No consultation history logged during this session yet.")