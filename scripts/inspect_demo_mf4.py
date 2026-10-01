from asammdf import MDF


mdf = MDF("demo_data/city_01.mf4")


# basic info
print(f"version: {mdf.version}")

print("===== available channels =====")
print(list(mdf.channels_db.keys()))


# extract Vehicle speed

# initialize vars
speed = mdf.get("VehicleSpeed")
rpm = mdf.get("EngineSpeed")
gear = mdf.get("CurrentGear")


print("==== VehicleSpeed ====")
print(f"unit: {speed.unit[:10]}")
print(f"samples: {speed.samples[:10]}")
print(f"timestamps: {speed.timestamps[:10]}")


print("==== EngineSpeed ====")
print(f"unit: {rpm.unit[:10]}")
print(f"samples: {rpm.samples[:10]}")
print(f"timestamps: {rpm.timestamps[:10]}")



print("==== CurrentGear ====")
print(f"samples: {gear.samples[:20]}")


print("==== gear changes ====")
previous_gear = gear.samples[0]

for t,g in zip(gear.timestamps, gear.samples):
    if g != previous_gear:
        print(
            f"{previous_gear} -> {g} "
            f"at {t:.1f} s"
        )

    previous_gear = g