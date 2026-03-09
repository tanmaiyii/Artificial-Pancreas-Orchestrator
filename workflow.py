from prefect import flow, task
from simulator import run_simulation
from analysis import analyze_results

@task(retries=2)
def simulate_task(params: dict):
    return run_simulation(**params)

@task
def analyze_task(control_df, experiment_df):
    return analyze_results(control_df, experiment_df)

@flow(name="PID-Tuning-Loop")
def scientific_workflow(experiment_design):
    # Base parameters (A poorly tuned control baseline)
    control_params = {"kp": 0.05, "ki": 0.001, "kd": 0.0}
    control_data = simulate_task(control_params)
    
    # Experimental parameters (from Gemini)
    exp_params = {
        "kp": experiment_design.kp,
        "ki": experiment_design.ki,
        "kd": experiment_design.kd
    }
    experiment_data = simulate_task(exp_params)
    
    stats = analyze_task(control_data, experiment_data)
    return control_data, experiment_data, stats