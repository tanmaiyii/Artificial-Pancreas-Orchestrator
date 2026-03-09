import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

load_dotenv()

class ExperimentDesign(BaseModel):
    reasoning: str = Field(description="Engineering reasoning for tuning the PID parameters based on the hypothesis.")
    
    # SAFETY BOUNDS ADDED HERE
    kp: float = Field(
        ge=0.0, le=0.5, 
        description="Proportional gain. Must be strictly between 0.0 and 0.5 for patient safety."
    )
    ki: float = Field(
        ge=0.0, le=0.05, 
        description="Integral gain. Must be strictly between 0.0 and 0.05 to prevent insulin stacking."
    )
    kd: float = Field(
        ge=0.0, le=2.0, 
        description="Derivative gain. Must be strictly between 0.0 and 2.0 to prevent pump jitter."
    )

def plan_experiment(hypothesis: str, current_belief: str) -> ExperimentDesign:
    client = genai.Client()
    
    prompt = f"""
    You are an autonomous AI Control Systems Engineer tuning an Artificial Pancreas (PID controller).
    Current engineering notebook: {current_belief}
    User Hypothesis to test: {hypothesis}
    
    Design the next PID tuning parameters (Kp, Ki, Kd) to test this hypothesis and improve Time in Range after a meal disturbance. 
    Provide your reasoning, then specify the exact parameters. Do NOT exceed the safety limits defined in the schema.
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ExperimentDesign,
            temperature=0.2, 
        ),
    )
    
    return ExperimentDesign.model_validate_json(response.text)