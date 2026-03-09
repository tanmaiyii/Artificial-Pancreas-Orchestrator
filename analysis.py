import numpy as np
import pandas as pd

def analyze_results(df_control: pd.DataFrame, df_experiment: pd.DataFrame) -> dict:
    # Mean Absolute Error from target (100 mg/dL)
    mae_control = np.mean(np.abs(df_control['glucose'] - 100))
    mae_exp = np.mean(np.abs(df_experiment['glucose'] - 100))
    
    # Time in Range (70-180 mg/dL)
    tir_control = np.mean((df_control['glucose'] >= 70) & (df_control['glucose'] <= 180)) * 100
    tir_exp = np.mean((df_experiment['glucose'] >= 70) & (df_experiment['glucose'] <= 180)) * 100
    
    improvement = mae_control - mae_exp # Positive means experiment had lower error
    
    return {
        "control_TIR": float(tir_control),
        "experiment_TIR": float(tir_exp),
        "mae_improvement": float(improvement),
        "significant": bool(improvement > 2.0) # Considered clinically significant
    }