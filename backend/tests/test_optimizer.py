import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from optimizer.engine import optimize

DATA = json.loads((Path(__file__).resolve().parents[1] / "data" / "demo_routes.json").read_text())


def test_returns_feasible_routes_for_demo_trip():
    result = optimize(DATA, {"origin": "HYD_HOME", "destination": "GOA_CENTER", "budget": 5000,
                            "max_duration_hours": 24, "strategy": "smart_balance"})
    assert result["feasible"] is True
    assert result["routes"]
    assert all(r["cost"] <= 5000 and r["duration_min"] <= 24 * 60 for r in result["routes"])


def test_no_feasible_route_when_budget_too_low():
    result = optimize(DATA, {"origin": "HYD_HOME", "destination": "GOA_CENTER", "budget": 1,
                            "max_duration_hours": 24, "strategy": "pocket_saver"})
    assert result["feasible"] is False
    assert result["routes"] == []


def test_rejects_unknown_location():
    try:
        optimize(DATA, {"origin": "UNKNOWN", "destination": "GOA_CENTER"})
    except ValueError as exc:
        assert "supported demo dataset" in str(exc)
    else:
        assert False, "Expected ValueError"
