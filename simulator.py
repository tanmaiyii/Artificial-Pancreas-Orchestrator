import numpy as np
import pandas as pd

def run_simulation(kp: float, ki: float, kd: float, time_steps: int = 240, noise_level: float = 2.0) -> pd.DataFrame:
    # Simulating 4 hours (240 minutes) of blood glucose dynamics
    t = np.arange(0, time_steps, 1.0)
    
    G = np.zeros(len(t)) # Blood Glucose (mg/dL)
    I = np.zeros(len(t)) # Active Insulin
    
    # Initial steady state
    G_target = 100.0
    G[0] = G_target 
    I[0] = 0.0
    
    # PID Controller State
    integral = 0.0
    prev_error = 0.0
    
    # Disturbance: Patient eats a meal at t=30 minutes
    meal_absorption = np.zeros(len(t))
    meal_absorption[30:90] = 3.0 # Carbs entering bloodstream
    
    for i in range(1, len(t)):
        # 1. PID Controller calculates insulin delivery based on glucose error
        error = G[i-1] - G_target
        integral += error
        derivative = error - prev_error
        
        # Insulin delivery cannot be negative (can't suck insulin out of the body)
        insulin_delivery = max(0, (kp * error) + (ki * integral) + (kd * derivative))
        prev_error = error
        
        # 2. Metabolic Plant Model (Highly simplified)
        # Insulin clears from blood slowly, but increases with delivery
        dI = -0.05 * I[i-1] + 0.1 * insulin_delivery
        
        # Glucose increases from meal, decreases from insulin, naturally reverts to target
        dG = -0.01 * (G[i-1] - G_target) - 0.1 * I[i-1] + meal_absorption[i-1]
        
        G[i] = G[i-1] + dG
        I[i] = I[i-1] + dI
        
    # Add realistic Continuous Glucose Monitor (CGM) sensor noise
    noise = np.random.normal(0, noise_level, len(t))
    G_noisy = np.clip(G + noise, 40, 400) # Bounded to realistic human levels
    
    return pd.DataFrame({'time': t, 'glucose': G_noisy, 'insulin': I})