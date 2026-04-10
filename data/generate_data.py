"""Generate sample EMEIA sales data with region-specific margins."""
import csv
import random
from pathlib import Path

random.seed(42)

REGIONS = ["EMEIA - Europe", "EMEIA - Middle East", "EMEIA - India", "EMEIA - Africa"]
CATEGORIES = ["iPhone", "Mac", "iPad", "Services", "Wearables"]
CHANNELS = ["Retail", "Online"]
MONTHS = [f"2024-{m:02d}-01" for m in range(1, 7)]

# Base revenue per region+category (Jan 2024)
BASE_REVENUE = {
    "EMEIA - Europe":      {"iPhone": 1250000, "Mac": 980000, "iPad": 620000, "Services": 450000, "Wearables": 380000},
    "EMEIA - Middle East": {"iPhone": 420000,  "Mac": 310000, "iPad": 195000, "Services": 140000, "Wearables": 125000},
    "EMEIA - India":       {"iPhone": 580000,  "Mac": 290000, "iPad": 210000, "Services": 180000, "Wearables": 155000},
    "EMEIA - Africa":      {"iPhone": 195000,  "Mac": 98000,  "iPad": 72000,  "Services": 55000,  "Wearables": 48000},
}

# Cost as % of revenue — varies by BOTH region AND category
COST_RATIO = {
    "EMEIA - Europe": {
        "iPhone": 0.68, "Mac": 0.72, "iPad": 0.71, "Services": 0.38, "Wearables": 0.65,
    },
    "EMEIA - Middle East": {
        "iPhone": 0.62, "Mac": 0.67, "iPad": 0.66, "Services": 0.42, "Wearables": 0.60,
    },
    "EMEIA - India": {
        "iPhone": 0.74, "Mac": 0.76, "iPad": 0.73, "Services": 0.35, "Wearables": 0.70,
    },
    "EMEIA - Africa": {
        "iPhone": 0.78, "Mac": 0.80, "iPad": 0.77, "Services": 0.48, "Wearables": 0.75,
    },
}

# Monthly growth jitter per region (some grow faster)
REGION_GROWTH = {
    "EMEIA - Europe": 0.025,
    "EMEIA - Middle East": 0.035,
    "EMEIA - India": 0.045,
    "EMEIA - Africa": 0.030,
}

rows = []
for month_idx, date in enumerate(MONTHS):
    for region in REGIONS:
        for category in CATEGORIES:
            base = BASE_REVENUE[region][category]
            growth = 1 + REGION_GROWTH[region] * month_idx
            noise = random.uniform(0.92, 1.08)
            revenue = int(base * growth * noise)

            cost_ratio = COST_RATIO[region][category]
            cost_noise = random.uniform(-0.03, 0.03)
            cost = int(revenue * max(0.25, min(0.85, cost_ratio + cost_noise)))

            avg_price = revenue / max(1, (revenue // (base // random.randint(200, 600))))
            units = max(100, int(revenue / max(1, random.randint(150, 400))))

            channel = random.choice(CHANNELS)
            rows.append([date, region, category, revenue, units, cost, channel])

out = Path(__file__).resolve().parent / "sales_data.csv"
with open(out, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["date", "region", "product_category", "revenue", "units_sold", "cost", "channel"])
    w.writerows(rows)

print(f"Wrote {len(rows)} rows to {out}")
