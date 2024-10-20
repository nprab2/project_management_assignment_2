import pulp as lp

tasks = {
    "A": {"predecessors": [], "duration": (4, 6, 10), "projectm": 47},
    "B": {"predecessors": [], "duration": (8, 12, 16), "projectm": 47},
    "C": {"predecessors": ["A"], "duration": (6, 8, 12), "projectm": 47, "frontend": 55},
    "D": {"predecessors": [], "duration": (40, 60, 80), "projectm": 47, "frontend": 55, "backend": 57, "data_sci": 49, "data_eng": 50},
    "D1": {"predecessors": ["A"], "duration": (8, 10, 12), "projectm": 47, "data_sci": 49},
    "D2": {"predecessors": ["D1"], "duration": (12, 16, 24), "projectm": 47, "frontend": 55, "backend": 57},
    "D3": {"predecessors": ["D1"], "duration": (12, 16, 24), "projectm": 47, "backend": 57},
    "D4": {"predecessors": ["D2", "D3"], "duration": (40, 60, 80), "projectm": 47, "backend": 57},
    "D5": {"predecessors": ["D4"], "duration": (8, 12, 16), "projectm": 47},
    "D6": {"predecessors": ["D4"], "duration": (10, 14, 20), "projectm": 47},
    "D7": {"predecessors": ["D6"], "duration": (12, 18, 24), "projectm": 47},
    "D8": {"predecessors": ["D5", "D7"], "duration": (6, 8, 12), "projectm": 47},
    "E": {"predecessors": ["B", "C"], "duration": (10, 14, 20), "projectm": 47},
    "F": {"predecessors": ["D8", "E"], "duration": (6, 8, 12), "projectm": 47},
    "G": {"predecessors": ["A", "D8"], "duration": (8, 10, 14), "projectm": 47, "backend": 57},
    "H": {"predecessors": ["F", "G"], "duration": (8, 12, 16), "projectm": 47},
}

def scenario(duration_type="expected"):

    lp_problem = lp.LpProblem(f"Scheduling_{duration_type.capitalize()}", lp.LpMinimize)


    start_times = {task: lp.LpVariable(f"start_{task}", lowBound=0) for task in tasks}
    end_times = {task: lp.LpVariable(f"end_{task}") for task in tasks}


    total_cost = lp.lpSum(
        [
            (end_times[task] - start_times[task]) * tasks[task]["projectm"]
            for task in tasks
        ]
    )
    
    for role in ["frontend", "backend", "data_sci", "data_eng"]:
        total_cost += lp.lpSum(
            [
                (end_times[task] - start_times[task]) * tasks[task].get(role, 0)
                for task in tasks if role in tasks[task]
            ]
        )
    lp_problem += total_cost

    for task, data in tasks.items():
        if duration_type == "best":
            duration = data["duration"][0]
        elif duration_type == "worst":
            duration = data["duration"][2]
        else: 
            duration = data["duration"][1]
        lp_problem += end_times[task] == start_times[task] + duration

    for task, data in tasks.items():
        for predecessor in data["predecessors"]:
            lp_problem += start_times[task] >= end_times[predecessor]

    lp_problem.solve()
    print(f"Status: {lp.LpStatus[lp_problem.status]}")
    total_cost_value = lp.value(lp_problem.objective)
    print(f"Total project cost for {duration_type} case: ${total_cost_value:.2f}")
    for task in tasks:
        print(f"Task {task}: Start at {lp.value(start_times[task])}, End at {lp.value(end_times[task])}")



scenario("best")
scenario("expected")
scenario("worst")