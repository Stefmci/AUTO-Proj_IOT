from tinydb import TinyDB, Query


db = TinyDB("bottles.json")
Bottle = Query()

def update_bottle(bottle_id, new_data):
    existing = db.get(Bottle.bottle == bottle_id)
    if existing:
        # Dispenser ergänzen statt überschreiben
        if "dispenser" in new_data:
            if "dispenser" not in existing:
                existing["dispenser"] = {}
            for disp, disp_data in new_data["dispenser"].items():
                existing["dispenser"][disp] = disp_data
            db.update({"dispenser": existing["dispenser"]}, Bottle.bottle == bottle_id)
        else:
            updated = {**existing, **new_data}
            db.update(updated, Bottle.bottle == bottle_id)
    else:
        db.insert({"bottle": bottle_id, **new_data})

def update_dispenser_temperature(bottle_id, dispenser, temperature):
    existing = db.get(Bottle.bottle == bottle_id)
    if existing and "dispenser" in existing and dispenser in existing["dispenser"]:
        existing["dispenser"][dispenser]["temperature_C"] = temperature
        db.update(existing, Bottle.bottle == bottle_id)
    else:
        update_bottle(bottle_id, {"dispenser": {dispenser: {"temperature_C": temperature}}})
