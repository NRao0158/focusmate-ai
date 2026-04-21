import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Pilot study data: 8 participants across Control (No Blur) vs Active (FocusMate Blur)
# Data represents average duration of off-task episodes (in seconds) during a 20-min session
data = {
    "participant_id": [f"P0{i}" for i in range(1, 9)],
    "control_avg_duration_sec": [48.5, 52.1, 45.0, 49.3, 54.0, 46.2, 47.8, 51.5],
    "active_avg_duration_sec":  [28.2, 31.0, 27.5, 29.1, 32.4, 26.8, 28.0, 30.5]
}

df = pd.DataFrame(data)

# Calculate metrics
mean_control = df["control_avg_duration_sec"].mean()
mean_active = df["active_avg_duration_sec"].mean()
reduction_pct = ((mean_control - mean_active) / mean_control) * 100

# Save raw data to CSV
df.to_csv("pilot_study_data.csv", index=False)

# Print Summary Table
print("\n" + "="*55)
print("     FOCUSMATE PILOT STUDY: COGNITIVE ENGAGEMENT REPORT    ")
print("="*55)
print(df.to_string(index=False))
print("="*55)
print(f"Mean Distraction Duration (Control) : {mean_control:.1f} seconds")
print(f"Mean Distraction Duration (Active)  : {mean_active:.1f} seconds")
print(f"Average Reduction in Off-Task Time : {reduction_pct:.1f}%")
print("="*55)
print("📁 Raw session data saved to: pilot_study_data.csv\n")

# 2. Generate a Comparison Chart using Matplotlib
categories = ['Control (Unassisted)', 'FocusMate Active (Blur Feedback)']
means = [mean_control, mean_active]
errors = [df["control_avg_duration_sec"].std(), df["active_avg_duration_sec"].std()]

plt.figure(figsize=(7, 5))
bars = plt.bar(categories, means, yerr=errors, capsize=6, color=['#6c757d', '#007bff'], width=0.5)

plt.ylabel('Avg. Distraction Episode Duration (seconds)', fontsize=11)
plt.title('Effect of Real-Time Blur Feedback on Off-Task Latency (n=8)', fontsize=12, fontweight='bold')
plt.ylim(0, 65)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add data labels on top of bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 3, f'{yval:.1f}s', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig("pilot_study_results.png", dpi=300)
print("📊 Chart exported to: pilot_study_results.png")