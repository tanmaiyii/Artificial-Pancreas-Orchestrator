# ⚙️ Autonomous AI PID Tuner: Artificial Pancreas Orchestrator

An end-to-end, LLM-powered scientific workflow orchestrator designed for closed-loop control systems. This project demonstrates an "AI Control Engineer" loop: an autonomous agent takes a natural-language hypothesis, designs a Proportional-Integral-Derivative (PID) tuning strategy, executes a simulated metabolic environment (an Artificial Pancreas), performs clinical statistical analysis, and dynamically updates its internal "Engineering Notebook."

## 🏗️ System Architecture & Tech Stack

This application emphasizes a strict separation of concerns, ensuring the LLM acts only as the reasoning engine while deterministic Python handles the math and orchestration:

* **Frontend Interface:** [Streamlit](https://streamlit.io/) for rapid, stateful UI and dual-axis data visualization (Glucose & Insulin).
* **Workflow Orchestration:** [Prefect](https://www.prefect.io/) for mapping the Directed Acyclic Graph (DAG) with automatic retries and execution tracking.
* **AI Agent:** Google's `gemini-2.5-flash` via the `google-genai` SDK, leveraging strict JSON schema enforcement via Pydantic for type-safe parameter generation.
* **Simulation Engine:** Pure Python (`numpy`, `pandas`) simulating a discrete-time metabolic plant model and closed-loop controller.

## 🎛️ The Domain: What is a PID Controller?



[Image of a PID controller block diagram]


A PID controller is the industry standard for automated control systems. In this app, it acts as an **Artificial Pancreas**, continuously calculating an error value $e(t)$ as the difference between a desired setpoint (Target Blood Glucose: 100 mg/dL) and a measured process variable (Current Blood Glucose). 

The controller applies a correction based on three terms that the AI agent must tune:
* **Proportional ($K_p$):** Reacts to the *current* error. If glucose is high, it delivers more insulin.
* **Integral ($K_i$):** Reacts to the *accumulation* of past error. It helps eliminate steady-state offsets (e.g., if glucose is slightly high for a long time).
* **Derivative ($K_d$):** Predicts *future* error based on its rate of change. It dampens the system to prevent post-meal insulin over-delivery (hypoglycemia).

**The Controller Equation:**
$$u(t) = K_p e(t) + K_i \int e(t) dt + K_d \frac{de(t)}{dt}$$
*(Where $u(t)$ is the calculated active insulin delivery).*

## 🧮 The Metabolic Plant Model

Once the insulin $u(t)$ is calculated, the simulation updates the patient's biological state using a simplified metabolic model. The patient is subjected to a "disturbance" (a carbohydrate meal $M(t)$ entering the bloodstream at $t=30$ minutes).

**1. Insulin Dynamics:** Active insulin clears from the blood slowly but increases when the pump delivers it.
$$\frac{dI}{dt} = -0.05 I(t) + 0.1 u(t)$$

**2. Glucose Dynamics:** Glucose reverts to baseline, drops when active insulin is high, and spikes when the meal is absorbed.
$$\frac{dG}{dt} = -0.01 (G(t) - 100) - 0.1 I(t) + M(t)$$



*The system uses Time in Range (TIR) and Mean Absolute Error (MAE) as clinical metrics to judge the AI's success.*

## 📂 Project Structure

```text
autonomous-scientist/
├── .env                  # Secure API key storage (ignored by git)
├── .gitignore            # Git exclusion rules
├── requirements.txt      # Reproducible Python dependencies
├── app.py                # Streamlit UI & state management
├── agent.py              # Gemini LLM logic & Pydantic schemas
├── analysis.py           # Clinical metrics (Time in Range, MAE)
├── simulator.py          # PID Controller and Metabolic Plant math
├── workflow.py           # Prefect DAG definition
└── README.md             # Project documentation