import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "E-commerence analysis"


def test_web_dashboard_assets_exist():
    for name in ("index.html", "styles.css", "app.js", "dashboard_data.json", "README.md"):
        assert (WEB / name).exists()


def test_web_dashboard_uses_validated_scope():
    payload = json.loads((WEB / "dashboard_data.json").read_text(encoding="utf-8"))
    assert payload["scope"]["amazon_lines"] == 128969
    assert payload["scope"]["amazon_orders"] == 120378
    assert payload["scope"]["mixed_status_orders"] == 0
    assert payload["monthly"]
    assert payload["category"]
    assert payload["sku"]
    assert payload["category_price"]


def test_web_dashboard_is_not_a_pbix_or_unsupported_analysis():
    html = (WEB / "index.html").read_text(encoding="utf-8")
    assert ".pbix" not in html.lower()
    assert "Profit by" not in html
    assert "Margin by" not in html
    assert "Product &amp; Pricing" in html
    assert "Status composition proxy" in html
