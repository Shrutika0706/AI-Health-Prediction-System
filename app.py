import streamlit as st
from ai_service import generate_health_remark
import pandas as pd

import traceback

st.set_page_config(

    page_title="Health Prediction System",

    page_icon="🏥",

    layout="wide"

)


st.markdown("""
<style>

.main{
    padding-top:1rem;
}

.metric-card{
    background:#1e1e1e;
    padding:18px;
    border-radius:12px;
    border:1px solid #333;
}

.patient-card{
    background:#1f1f1f;
    padding:20px;
    border-radius:15px;
    border:1px solid #444;
    margin-bottom:20px;
}

.small-text{
    color:#bdbdbd;
    font-size:15px;
}

.green{
    color:#00c853;
    font-weight:bold;
}

.orange{
    color:#ff9800;
    font-weight:bold;
}

.red{
    color:#ff5252;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

with st.sidebar:

    st.title("🏥 Health Prediction")

    st.markdown("---")

    st.success("✅ Patient Registration")

    st.success("✅ AI Health Assessment")

    st.success("✅ SQLite Database")

    st.success("✅ Search Patients")

    st.success("✅ CSV Download")

    st.markdown("---")

    st.info(
      """
        Version : 1.0

        Developer

        Shrutika Deshmukh

        Powered by

        • Streamlit

        • Gemini AI

        • SQLite
        """
)



from database import (
    create_table,
    add_patient,
    get_all_patients,
    delete_patient,
    update_patient_email,
    patient_exists
)
# Create table
create_table()

st.title("🏥 AI Health Prediction System")
# =======================
# Dashboard Statistics
# =======================

patients = get_all_patients()

total_patients = len(patients)

high_risk = 0

for patient in patients:

    glucose = patient[4]
    haemoglobin = patient[5]
    cholesterol = patient[6]

    if glucose >= 180 or cholesterol >= 240 or haemoglobin < 10:
        high_risk += 1

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "👥 Total Patients",
        total_patients
    )

with col2:
    st.metric(
        "🤖 AI Reports",
        total_patients
    )

with col3:
    st.metric(
    "🔴 High Risk Patients",
    high_risk
)

st.divider()

st.header("Patient Registration")



col1, col2 = st.columns(2)

with col1:
    name = st.text_input("👤 Full Name")

with col2:
    email = st.text_input("📧 Email")

col3, col4 = st.columns(2)

with col3:
    from datetime import date

    dob = st.date_input(
        "📅 Date of Birth",
        value=date(2000, 1, 1),
        min_value=date(1900, 1, 1),
        max_value=date.today()
    )

with col4:
    glucose = st.number_input(
        "🩸 Glucose",
        min_value=0.0,
        format="%.2f"
    )

col5, col6 = st.columns(2)

with col5:
    haemoglobin = st.number_input(
        "🧪 Haemoglobin",
        min_value=0.0,
        format="%.2f"
    )

with col6:
    cholesterol = st.number_input(
        "❤️ Cholesterol",
        min_value=0.0,
        format="%.2f"
    )


if st.button(
    "💾 Register Patient",
    use_container_width=True
):

    if not name.strip():
        st.error("Please enter Full Name")

    elif "@" not in email or "." not in email:
        st.error("Invalid Email Address")

    elif glucose < 40 or glucose > 600:
        st.error("Glucose must be between 40 and 600 mg/dL")

    elif haemoglobin < 3 or haemoglobin > 25:
        st.error("Haemoglobin must be between 3 and 25 g/dL")

    elif cholesterol < 50 or cholesterol > 500:
        st.error("Cholesterol must be between 50 and 500 mg/dL")

    else:

        if patient_exists(
            name,
            str(dob),
            email,
            glucose,
            haemoglobin,
            cholesterol
        ):
            st.warning(
                "⚠ An identical patient record already exists."
            )
            st.stop()

        with st.spinner("Generating AI Health Assessment..."):

            try:

                remarks = generate_health_remark(
                    glucose,
                    haemoglobin,
                    cholesterol
                )
            except Exception:
                st.code(traceback.format_exc())
                st.stop()

        add_patient(
            name,
            str(dob),
            email,
            glucose,
            haemoglobin,
            cholesterol,
            remarks
        )

        st.success("🎉 Patient Registered Successfully!" \
        "AI Health Report Generated.")

        with st.expander("🤖 AI Health Assessment", expanded=True):
            st.markdown(remarks)
            st.warning("⚠ This AI assessment is for informational purposes only and should not replace professional medical advice."
        )
            

st.header("📋 Patient Records")
st.caption(f"Showing {len(patients)} Patient Records")
st.write(f"Total Records: **{len(patients)}**")

patients = get_all_patients()

search = st.text_input(
    "🔍 Search by Patient Name",
    placeholder="Type patient's name..."
)

if search:
    patients = [
        p for p in patients
        if search.lower() in p[1].lower()
    ]


df = pd.DataFrame(
    patients,
    columns=[
        "ID","Full Name","DOB","Email",
        "Glucose","Haemoglobin","Cholesterol","Remarks"
    ]
)

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Export Records as CSV",
    data=csv,
    file_name="patients.csv",
    mime="text/csv"
)


if len(patients) == 0:
    st.info("📂 No patient records available.\n\nRegister your first patient to begin."
    )

else:

    for patient in patients:

        patient_id = patient[0]
        name = patient[1]
        dob = patient[2]
        email = patient[3]
        glucose = patient[4]
        haemoglobin = patient[5]
        cholesterol = patient[6]
        remarks = patient[7]

        # --------------------------
        # Risk Level
        # --------------------------

        if glucose >= 180 or cholesterol >= 240 or haemoglobin < 10:
            risk = "🔴 High Risk"
            color = "#ff4b4b"

        elif glucose >= 100 or cholesterol >= 200 or haemoglobin < 12:
            risk = "🟠 Moderate Risk"
            color = "#ff9800"

        else:
            risk = "🟢 Low Risk"
            color = "#00c853"

        with st.container(border=True):

            st.subheader(f"👤 {name}")
            st.caption(f"Patient ID : {patient_id}")
            st.write(f"📧 **Email:** {email}")
            st.write(f"🎂 **DOB:** {dob}")
            

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("🩸 Glucose", glucose)

            with col2:
                st.metric("🧪 Haemoglobin", haemoglobin)

            with col3:
                st.metric("❤️ Cholesterol", cholesterol)

            if "High" in risk:
                st.error(risk)

            elif "Moderate" in risk:
                st.warning(risk)

            else:
                st.success(risk)

            with st.expander("🤖 AI Health Assessment", expanded=False):

                st.success("AI Generated Health Report")

                st.markdown(remarks)
            

            # ==========================
            # Update & Delete Buttons
            # ==========================

            col_update, col_delete = st.columns(2)

            with col_update:

                new_email = st.text_input(
                    "New Email",
                    value=email,
                    key=f"email_{patient_id}"
                )

                if st.button(
                    "✏ Update Email",
                    key=f"update_{patient_id}",
                    use_container_width=True
                ):

                    if "@" not in new_email or "." not in new_email:
                        st.error("Please enter a valid email address.")

                    else:
                        update_patient_email(patient_id, new_email)
                        st.success("✅ Email updated successfully!")
                        st.rerun()

            with col_delete:

                    st.write("")      # spacing
                    st.write("")      # spacing

                    if st.button(
                        "❌ Delete Patient",
                        key=f"delete_{patient_id}",
                        use_container_width=True
                    ):

                        delete_patient(patient_id)
                        st.toast("Patient Deleted Successfully ✅")
                        st.rerun()

            st.divider()

st.divider()

st.caption(
    "Developed by Shrutika Deshmukh | AI Health Prediction System | Streamlit + Gemini + SQLite"
)

           