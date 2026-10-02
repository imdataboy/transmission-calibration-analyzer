from asammdf import MDF


mdf = MDF("demo_data/city_B.mf4")


# basic info
print(f"version: {mdf.version}")

print("===== available channels =====")
print(list(mdf.channels_db.keys()))


# extract Vehicle speed

# initialize vars
speed = mdf.get("VehicleSpeed")
rpm = mdf.get("EngineSpeed")
gear = mdf.get("CurrentGear")
target_gear = mdf.get("TargetGear")


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

print("==== TargetGear ====")
print(f"samples: {target_gear.samples[:20]}")


throttle = mdf.get("ThrottlePosition")

print("==== ThrottlePosition ====")
print(f"unit: {throttle.unit}")
print(f"samples: {throttle.samples[:20]}")


torque = mdf.get("EngineTorque")

print("==== EngineTorque ====")
print(f"unit: {torque.unit}")
print(f"samples: {torque.samples[:20]}")


input_speed = mdf.get("TransmissionInputSpeed")
output_speed = mdf.get("TransmissionOutputSpeed")

print("==== Transmission speeds ====")
print(f"input:  {input_speed.samples[:10]}")
print(f"output: {output_speed.samples[:10]}")

print("==== gear changes ====")
previous_gear = gear.samples[0]

for t,g in zip(gear.timestamps, gear.samples):
    if g != previous_gear:
        print(
            f"{previous_gear} -> {g} "
            f"at {t:.1f} s"
        )

    previous_gear = g


print("==== Target vs Current Gear ====")

for timestamp, target, current in zip(
    gear.timestamps,
    target_gear.samples,
    gear.samples
):
    if target != current:
        print(
            f"{timestamp:.1f}s | "
            f"TargetGear={target} | "
            f"CurrentGear={current}"
        )