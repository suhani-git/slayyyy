def detect_leakages(df):
    leaks = []

    # Micro transactions
    micro = df[df["amount"] < 200]
    if len(micro) >= 5:
        leaks.append(("Micro Transactions", micro["amount"].sum()))

    # Subscriptions
    subs = df[df["category"] == "subscription"]
    for name, group in subs.groupby("description"):
        if len(group) >= 2:
            leaks.append((f"Recurring Subscription: {name}", group["amount"].sum()))

    # Impulse purchases
    impulse = df[df["amount"] > 800]
    if not impulse.empty:
        leaks.append(("Impulse Purchases", impulse["amount"].sum()))

    return leaks
