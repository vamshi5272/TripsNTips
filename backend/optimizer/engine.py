"""Small, explainable route optimizer for the TripsNTips demo.

Uses bounded simple-path enumeration over a directed transport graph. The demo graph
is intentionally small. For larger graphs, replace this with a time-aware DP or a
Branch-and-Bound implementation with proven lower bounds.
"""
from collections import defaultdict

STRATEGIES = {"pocket_saver", "time_saver", "smart_balance"}


def build_adjacency(edges, allowed_modes=None):
    adjacency = defaultdict(list)
    allowed = set(allowed_modes or [])
    for edge in edges:
        if allowed and edge["mode"] not in allowed:
            continue
        adjacency[edge["from"]].append(edge)
    return adjacency


def enumerate_paths(adjacency, origin, destination, required_stops=None, max_edges=8, max_paths=5000):
    """Enumerate simple paths, requiring all required stop IDs to be visited."""
    required = set(required_stops or [])
    paths, explored = [], 0

    def dfs(node, visited, path):
        nonlocal explored
        if len(paths) >= max_paths or explored >= max_paths * 20:
            return
        explored += 1
        if node == destination:
            nodes = {path[0]["from"]} if path else {origin}
            nodes.update(edge["to"] for edge in path)
            if required.issubset(nodes):
                paths.append(list(path))
            return
        if len(path) >= max_edges:
            return
        for edge in adjacency.get(node, []):
            nxt = edge["to"]
            if nxt in visited:
                continue
            dfs(nxt, visited | {nxt}, path + [edge])

    dfs(origin, {origin}, [])
    return paths


def evaluate_path(path, locations, sightseeing, origin, destination, required_stops=None):
    by_id = {loc["id"]: loc for loc in locations}
    required = set(required_stops or [])
    node_ids = [origin] + [edge["to"] for edge in path]
    cost = sum(float(edge["cost"]) for edge in path)
    duration = sum(int(edge["duration_min"]) for edge in path)
    stages = []
    for edge in path:
        stages.append({
            "from": edge["from"], "to": edge["to"],
            "from_name": by_id.get(edge["from"], {}).get("name", edge["from"]),
            "to_name": by_id.get(edge["to"], {}).get("name", edge["to"]),
            "mode": edge["mode"], "label": edge.get("label", edge["mode"]),
            "cost": float(edge["cost"]), "duration_min": int(edge["duration_min"]),
            "kind": edge.get("kind", "main"), "data_status": "demo"
        })
    seen_sightseeing = set()
    for node_id in node_ids:
        if node_id in sightseeing and node_id not in seen_sightseeing:
            info = sightseeing[node_id]
            cost += float(info.get("stop_cost", 0))
            duration += int(info.get("stop_duration_min", 0))
            seen_sightseeing.add(node_id)
            stages.append({
                "from": node_id, "to": node_id,
                "from_name": by_id.get(node_id, {}).get("name", node_id),
                "to_name": by_id.get(node_id, {}).get("name", node_id),
                "mode": "Sightseeing stop", "label": "Planned sightseeing time and expense",
                "cost": float(info.get("stop_cost", 0)),
                "duration_min": int(info.get("stop_duration_min", 0)),
                "kind": "sightseeing", "data_status": "demo"
            })
    return {
        "origin": origin, "destination": destination,
        "nodes": node_ids, "stages": stages,
        "cost": round(cost, 2), "duration_min": duration,
        "transfers": max(0, len(path) - 1),
        "modes": list(dict.fromkeys(edge["mode"] for edge in path)),
        "required_stops": sorted(required),
        "data_status": "demo"
    }


def optimize(data, request):
    locations = data["locations"]
    edges = data["edges"]
    origin, destination = request.get("origin"), request.get("destination")
    if not origin or not destination:
        raise ValueError("Origin and destination are required.")
    location_ids = {loc["id"] for loc in locations}
    if origin not in location_ids or destination not in location_ids:
        raise ValueError("Origin or destination is not in the supported demo dataset.")
    if origin == destination:
        raise ValueError("Origin and destination must be different.")

    budget = float(request.get("budget", 5000))
    max_duration = int(float(request.get("max_duration_hours", 24)) * 60)
    strategy = request.get("strategy", "smart_balance")
    if strategy not in STRATEGIES:
        raise ValueError("Strategy must be pocket_saver, time_saver, or smart_balance.")
    required_stops = request.get("required_stops", [])
    if not isinstance(required_stops, list) or any(stop not in location_ids for stop in required_stops):
        raise ValueError("Required stops must be valid location IDs.")
    if origin in required_stops or destination in required_stops:
        required_stops = [s for s in required_stops if s not in {origin, destination}]

    allowed_modes = request.get("allowed_modes") or []
    adjacency = build_adjacency(edges, allowed_modes)
    paths = enumerate_paths(adjacency, origin, destination, required_stops, max_edges=8)
    sightseeing = data.get("sightseeing", {})
    candidates = [evaluate_path(p, locations, sightseeing, origin, destination, required_stops) for p in paths]
    feasible = [r for r in candidates if r["cost"] <= budget and r["duration_min"] <= max_duration]

    # Pareto-style route set: remove routes dominated in both cost and duration.
    nondominated = []
    for route in sorted(feasible, key=lambda r: (r["cost"], r["duration_min"])):
        if not any(other["cost"] <= route["cost"] and other["duration_min"] <= route["duration_min"] and
                   (other["cost"] < route["cost"] or other["duration_min"] < route["duration_min"])
                   for other in feasible):
            nondominated.append(route)
    if not nondominated and feasible:
        nondominated = feasible[:]

    if nondominated:
        min_cost = min(r["cost"] for r in nondominated)
        min_time = min(r["duration_min"] for r in nondominated)
        max_cost = max(r["cost"] for r in nondominated)
        max_time = max(r["duration_min"] for r in nondominated)
        def score(route):
            cost_term = (route["cost"] - min_cost) / max(1, max_cost - min_cost)
            time_term = (route["duration_min"] - min_time) / max(1, max_time - min_time)
            return (cost_term + time_term) / 2
        pocket = min(nondominated, key=lambda r: (r["cost"], r["duration_min"]))
        fastest = min(nondominated, key=lambda r: (r["duration_min"], r["cost"]))
        balanced = min(nondominated, key=score)
        selected = {"pocket_saver": pocket, "time_saver": fastest, "smart_balance": balanced}[strategy]
        # Return all nondominated routes plus strategy selections, with stable IDs.
        unique = []
        seen = set()
        for route in [pocket, fastest, balanced] + sorted(nondominated, key=lambda r: (r["cost"], r["duration_min"])):
            signature = tuple(route["nodes"]) + (route["cost"], route["duration_min"])
            if signature not in seen:
                seen.add(signature)
                route["id"] = f"route-{len(unique)+1}"
                route["duration_hours"] = round(route["duration_min"] / 60, 1)
                route["cost_breakdown"] = {"transport_and_access": round(sum(s["cost"] for s in route["stages"] if s["kind"] != "sightseeing"), 2),
                                            "sightseeing": round(sum(s["cost"] for s in route["stages"] if s["kind"] == "sightseeing"), 2),
                                            "total": route["cost"]}
                unique.append(route)
        selected_signature = tuple(selected["nodes"]) + (selected["cost"], selected["duration_min"])
        selected_id = next(r["id"] for r in unique if tuple(r["nodes"]) + (r["cost"], r["duration_min"]) == selected_signature)
        return {"feasible": True, "strategy": strategy, "selected_route_id": selected_id,
                "routes": unique, "candidates_evaluated": len(candidates),
                "data_notice": data.get("notice", "Demo data"),
                "explanation": "Routes are calculated from the configured demo graph. Values are not live fares or schedules."}
    return {"feasible": False, "strategy": strategy, "routes": [], "candidates_evaluated": len(candidates),
            "data_notice": data.get("notice", "Demo data"),
            "message": "No route in the current dataset meets both your budget and maximum duration.",
            "suggestions": ["Increase your budget", "Allow more travel time", "Allow more transport modes", "Remove an optional stop"]}
