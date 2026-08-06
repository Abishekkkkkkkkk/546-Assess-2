
import json
import os

machine_data = [
    {
        "Machine ID": "M-101",
        "Plant Name": "Plant Alpha",
        "Operating Hours": 500.0,
        "Downtime": 25.0,
        "Energy Consumption": 12000.0,  # kWh
        "Units Produced": 45000,
        "Maintenance Cost": 3500.0
    },
    {
        "Machine ID": "M-102",
        "Plant Name": "Plant Alpha",
        "Operating Hours": 500.0,
        "Downtime": 120.0,
        "Energy Consumption": 15000.0,
        "Units Produced": 28000,
        "Maintenance Cost": 8200.0
    },
    {
        "Machine ID": "M-201",
        "Plant Name": "Plant Beta",
        "Operating Hours": 480.0,
        "Downtime": 15.0,
        "Energy Consumption": 10500.0,
        "Units Produced": 46000,
        "Maintenance Cost": 2100.0
    },
    {
        "Machine ID": "M-202",
        "Plant Name": "Plant Beta",
        "Operating Hours": 480.0,
        "Downtime": 90.0,
        "Energy Consumption": 13000.0,
        "Units Produced": 31000,
        "Maintenance Cost": 6500.0
    },
    {
        "Machine ID": "M-301",
        "Plant Name": "Plant Gamma",
        "Operating Hours": 500.0,
        "Downtime": 5.0,
        "Energy Consumption": 11000.0,
        "Units Produced": 52000,
        "Maintenance Cost": 1500.0
    }
]

def process_iot_monitoring(data):
    processed_machines = []
    
    for mach in data:
        op_hours = mach["Operating Hours"]
        downtime = mach["Downtime"]
        effective_hours = op_hours - downtime
        
       
        if effective_hours > 0:
            efficiency = mach["Units Produced"] / effective_hours
        else:
            efficiency = 0.0
        mach["Efficiency (Units/Hr)"] = round(efficiency, 2)
        
        
        # (Using Energy Consumption cost estimated at $0.12/kWh + Maintenance Cost apportioned)
        total_cost = (mach["Energy Consumption"] * 0.12) + mach["Maintenance Cost"]
        cost_per_unit = total_cost / mach["Units Produced"] if mach["Units Produced"] > 0 else 0.0
        mach["Cost Per Unit"] = round(cost_per_unit, 2)
        
        processed_machines.append(mach)

    
    sorted_machines = sorted(processed_machines, key=lambda x: x["Efficiency (Units/Hr)"], reverse=True)

    print("--- 7. MACHINES SORTED BY EFFICIENCY ---")
    for m in sorted_machines:
        print(f"Machine: {m['Machine ID']} ({m['Plant Name']}) - Efficiency: {m['Efficiency (Units/Hr)']} units/hr")

   
    print("\n--- 3. INEFFICIENT MACHINES ---")
    inefficient_machines = [m for m in sorted_machines if m["Efficiency (Units/Hr)"] < 80.0]
    if inefficient_machines:
        for m in inefficient_machines:
            print(f"- {m['Machine ID']} in {m['Plant Name']} (Efficiency: {m['Efficiency (Units/Hr)']})")
    else:
        print("No inefficient machines identified.")

    
    highest_maint = max(processed_machines, key=lambda x: x["Maintenance Cost"])
    print(f"\n--- 4. HIGHEST MAINTENANCE COST MACHINE ---")
    print(f"Machine ID: {highest_maint['Machine ID']} | Plant: {highest_maint['Plant Name']} | Cost: ${highest_maint['Maintenance Cost']:,.2f}")

    
    plant_stats = {}
    for m in processed_machines:
        plant = m["Plant Name"]
        if plant not in plant_stats:
            plant_stats[plant] = {"total_eff": 0.0, "count": 0}
        plant_stats[plant]["total_eff"] += m["Efficiency (Units/Hr)"]
        plant_stats[plant]["count"] += 1

    print(f"\n--- 5. PLANT-WISE AVERAGE EFFICIENCY ---")
    plant_avg_efficiency = {}
    for plant, stats in plant_stats.items():
        avg_eff = stats["total_eff"] / stats["count"]
        plant_avg_efficiency[plant] = round(avg_eff, 2)
        print(f"Plant: {plant} - Average Efficiency: {plant_avg_efficiency[plant]} units/hr")

    
    print(f"\n--- 6. MACHINES REQUIRING PREVENTIVE MAINTENANCE ---")
    pm_required = [m for m in processed_machines if (m["Downtime"] / m["Operating Hours"]) > 0.15 or m["Maintenance Cost"] > 6000]
    if pm_required:
        for m in pm_required:
            print(f"- {m['Machine ID']} ({m['Plant Name']}) requires inspection due to excessive downtime/costs.")
    else:
        print("All machines operate within optimal wear parameters.")

   
    report_data = {
        "plant_summary": plant_avg_efficiency,
        "machines": sorted_machines
    }
    filename = "maintenance_report.json"
    with open(filename, "w") as f:
        json.dump(report_data, f, indent=4)
    print(f"\n--- 8 & 9. REPORT GENERATION & STORAGE ---")
    print(f"Maintenance report successfully generated and saved to {filename}")

  
    print(f"\n--- 10. READ MAINTENANCE REPORT BACK ---")
    if os.path.exists(filename):
        with open(filename, "r") as f:
            loaded_report = json.load(f)
            print(f"Successfully read report. Total monitored machines loaded: {len(loaded_report['machines'])}")
            print(f"Sample Read Check -> Top Efficient Machine: {loaded_report['machines'][0]['Machine ID']}")

if __name__ == "__main__":
    process_iot_monitoring(machine_data)
