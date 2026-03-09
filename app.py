import streamlit as st
from agent import plan_experiment
from workflow import scientific_workflow

st.set_page_config(page_title="Autonomous AI PID Tuner", layout="wide")
st.title("⚙️ Autonomous AI PID Tuner (Artificial Pancreas)")

if "belief" not in st.session_state:
    st.session_state.belief = "Initial state: Baseline PID (Kp=0.05, Ki=0.001, Kd=0.0) struggles with meal spikes."

hypothesis = st.text_input("Enter your tuning hypothesis:", "Increasing the derivative gain (Kd) will prevent the post-meal glucose spike by reacting to the rapid rise.")

if st.button("Run Iteration"):
    with st.spinner("Gemini is formulating a tuning design..."):
        design = plan_experiment(hypothesis, st.session_state.belief)
        
        st.write("### 🧠 Agent Reasoning")
        st.info(design.reasoning)
        
        st.write("### 🎛️ PID Parameters")
        st.json({"Kp": design.kp, "Ki": design.ki, "Kd": design.kd})
        
    with st.spinner("Executing Prefect DAG & Simulating Metabolism..."):
        ctrl_df, exp_df, stats = scientific_workflow(design) 
        
    st.write("### 📊 Clinical Results (Experiment vs Control)")
    col1, col2, col3 = st.columns(3)
    col1.metric("Experiment Time in Range (70-180 mg/dL)", f"{stats['experiment_TIR']:.1f}%", f"{stats['experiment_TIR'] - stats['control_TIR']:.1f}% vs Control")
    col2.metric("Mean Absolute Error (Target 100)", f"{stats['mae_improvement']:.2f} improvement")
    col3.metric("Clinically Significant (>2% TIR)", str(stats['significant']))
    
    st.write("---")
    st.write("### 📈 Continuous Glucose Monitor (CGM)")
    st.write("**Blood Glucose (mg/dL) over 4 hours**")
    st.line_chart(exp_df.set_index('time')['glucose'])
    
    st.write("### 💉 Insulin Pump Delivery")
    st.write("**Active Insulin Delivery (Units/min)**")
    st.line_chart(exp_df.set_index('time')['insulin'])
    st.write("---")
    
    st.session_state.belief += f"\nTested: '{hypothesis}'. Significant improvement: {stats['significant']}. Update: {design.reasoning}"
    
    st.write("### 📓 Updated Engineering Notebook")
    st.success(st.session_state.belief)