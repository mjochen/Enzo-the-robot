# Links

https://www.instructables.com/Droid-Style-RC-Animatronics-Using-Bottango-and-ESP

# Robot motors

Great practical question — and yes, **NEMA17 stepper motors** are *easy to control accurately*, but they come with some real power and efficiency drawbacks for mobile robots.

Let’s compare the three common drive setups you’re considering:

---

## ⚙️ 1. **NEMA17 Stepper Motors with Tracks**

| Feature       | Notes                                                              |
| ------------- | ------------------------------------------------------------------ |
| ✅ Precision   | Excellent — perfect for accurate turns, odometry, repeatable paths |
| ❌ Efficiency  | Low — **they draw power even when holding position**               |
| ❌ Power usage | High — easily **1-2 amps per motor** at 12V (12–24W per motor)     |
| ⚠️ Complexity | Needs proper driver (e.g. TMC2209 or DRV8825) + good power supply  |
| ⚠️ Weight     | Heavy compared to DC motors                                        |

### 🔋 Battery Life Impact

* Idle or stationary: still drawing current unless you disable the coils
* On a battery-driven robot, **expect much lower runtime**

🔧 Some people use a trick: **disable holding torque** when the robot is idle, but this can lead to drift or slippage.

---

## ⚙️ 2. **DC Motors with Tracks or Wheels (e.g. TT gear motors or brushed DC)**

(We'll take these)

| Feature       | Notes                                           |
| ------------- | ----------------------------------------------- |
| ✅ Efficiency  | Much better — **power only when moving**        |
| ⚠️ Precision  | Worse — may require encoders for odometry       |
| ✅ Cost        | Cheap and easy to find                          |
| ✅ Power usage | 0.2–1 A typical; much better runtime on battery |

🔋 Best for mobile, battery-powered bots.

* Pair with **quadrature encoders** for speed and distance measurement
* Use a motor driver like L298N or DRV8833

---

## ⚙️ 3. **DC Motor + Servo (like an RC car)**

| Feature             | Notes                                                   |
| ------------------- | ------------------------------------------------------- |
| ✅ Simple control    | One motor for speed, one for steering                   |
| ❌ Less maneuverable | Can't turn in place, no "tank turn" like tracked robots |
| ✅ Power efficient   | Often better than steppers; only active when moving     |
| ✅ Fast              | Great if your bot is more pet-like and playful          |

🔧 Requires a bit more planning for path planning and navigation (no differential drive).

---

## 🧠 Summary Comparison

| Feature                 | Stepper (NEMA17)    | DC Motors           | DC + Servo              |
| ----------------------- | ------------------- | ------------------- | ----------------------- |
| Power usage             | 🔴 High             | 🟢 Low to Moderate  | 🟢 Low to Moderate      |
| Precision (no encoders) | 🟢 Excellent        | 🔴 Poor             | ⚠️ Steering only        |
| Maneuverability         | 🟢 In-place turning | 🟢 In-place turning | 🔴 Needs turning radius |
| Battery runtime         | 🔴 Short            | 🟢 Long             | 🟢 Long                 |
| Simplicity              | ⚠️ Medium           | 🟢 Easy             | ⚠️ Medium               |

---

## ✅ My Recommendation (for a robot-pet on battery)

* If you want **long battery life, simplicity, and sufficient control** → go with **DC motors with encoders**
* If you want **RC-style movement (playful, wheeled)** → DC + servo is great
* Use **NEMA17 steppers only if**:

  * You really need **precise repeatable motion**
  * You don’t mind power drain or are always plugged in
  * You're doing SLAM or camera-based nav where position accuracy matters

That’s a **fantastic plan** — modular, expandable, and nicely layered. You’ve basically nailed the architecture used in many professional robots. Let me validate and expand on each piece with just enough detail to help you start building with confidence:

---
