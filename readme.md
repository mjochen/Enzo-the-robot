# Enzo

The repo that combines all effort into Enzo, a home-assistant-robot.


## 🦿 1. **Robot Base: Arduino + DC Motors + Tracks**

* Arduino reads MQTT commands over serial from the Pi
* Drives motors (via an H-bridge like L298N or TB6612FNG)
* Optional: wheel encoders for odometry feedback
* Also reads battery voltage or bump sensors

* Keeps real-time control tight (PWM, interrupts stay smooth)
* Pi doesn't need to micro-manage every pulse

🔧 **Tip**: Define a clean serial protocol, e.g.

```text
CMD MOVE 100 -80   # Left motor 100 PWM, right motor -80 PWM
CMD STOP
SENSOR BATTERY 7.8
```

## 👀 2. **Animated Eyes: Another Arduino + MQTT over Serial**

* Control eye servos (pan/tilt), eyelids, LED pupils, whatever you imagine
* Receive mood/state from ROS over serial via MQTT-style command
* Optionally respond with expressions, “blinks,” curiosity, etc.

This keeps your “expressive subsystem” isolated and easy to tinker with. It could even run pre-programmed animations based on high-level triggers.

🔧 Example:

```text
CMD EYES TRACK LEFT
CMD MOOD CURIOUS
```

## 🧠 3. **Pi 4: The Robot Brain with ROS 2**

* Runs ROS 2
* Has two serial ports open:

  * `/dev/ttyUSB0` for motion Arduino
  * `/dev/ttyUSB1` for eyes Arduino
* Publishes/subscribes to ROS topics like `/cmd_vel`, `/mood`, `/battery`
* Has two ROS nodes acting as MQTT bridges:

  * `ros2_serial_bridge_motion`
  * `ros2_serial_bridge_eyes`

ROS 2 handles logic, reasoning, LLM interaction, sensor fusion, etc.
Your Pi becomes the brain that connects to the LLM server and decides what to do, while the Arduinos simply act.

## 📡 4. **Use MQTT Between Nodes if Needed**

* Optional, but nice if you also want to:
  * Monitor robot status from another device
  * Control the bot remotely from your PC/phone
* You can have ROS ↔ MQTT bridge (like [`ros2_mqtt_bridge`](https://github.com/ros2-bridge/ros2_mqtt_bridge))


## 🧠 Advanced Thoughts for Later

| Feature   | Suggestion                                               |
| --------- | -------------------------------------------------------- |
| Odometry  | Add wheel encoders → send pulses over serial to Pi       |
| Auto-dock | Mark charger with AprilTag, use camera to localize       |
| Voice I/O | Add USB mic + speaker, run Vosk or TTS                   |
| Emotions  | Use `/mood` to trigger animations, sounds, or LED states |
| Logging   | Use MQTT + InfluxDB + Grafana (fun dashboard)            |

# Coms


| Purpose                                      | Best Tool          | Why                                        |
| -------------------------------------------- | ------------------ | ------------------------------------------ |
| **ROS ↔ ROS nodes**                          | 🔷 ROS 2 pub/sub   | Built-in, efficient, structured            |
| **ROS ↔ external systems (e.g. LLM server)** | ✅ REST API or MQTT | Depends on the use case                    |
| **Sensors/microcontrollers ↔ ROS**           | ✅ MQTT or serial   | Lightweight, easy integration (ESP32 etc.) |


## ✅ Use ROS 2 Pub/Sub for Internal Comms

If all your components speak ROS (e.g., camera node, battery monitor node, docking behavior node), then:

* **Use ROS 2 topics and services** — it’s efficient and standardized
* ROS 2 handles message types, namespaces, and timing for you
* You get tools like `rqt_graph`, `ros2 topic echo`, `rosbag`, etc.

Example:

```bash
ros2 topic echo /battery/status
```

---

## 🟡 When to Use MQTT

**MQTT is great when you want to connect non-ROS devices**, especially small microcontrollers like:

* ESP32, Arduino, Pi Pico
* IR sensors, ultrasonic, battery monitor, temperature

It’s:

* Super lightweight
* Pub-sub like ROS, but much simpler
* Easy to run an `mqtt_bridge` node in ROS that listens to `/sensor/battery` and republishes it as a ROS topic

Typical use:

* ESP32 reads battery voltage → publishes to MQTT topic `robot/battery`
* ROS node subscribes to `robot/battery` → republishes as `/battery/status`

## 🟢 When to Use an API (HTTP/REST or WebSocket)

Use an API if you're talking to a **non-robotic system** like:

* Your **LLM server** (e.g., Ollama or llama.cpp running on your main server)
* A **remote cloud service**
* A **web interface** or logging dashboard

Example:

Your robot notices you're nearby → sends this to your LLM via HTTP:

```http
POST /chat
{ "prompt": "Jochen walked into the room. What should I say?" }
```

LLM responds:

```json
{ "reply": "Hi Jochen! I was just thinking about you 🐾" }
```

Then your robot speaks that out loud using text-to-speech.

## 🧠 Practical Architecture Suggestion

Here’s how it could look:

```
[ ESP32 ] --> MQTT --> [ ROS 2 MQTT Bridge Node ] --> /battery/status
                                                 ↘
                                                /human_detected

[ LLM Bridge Node ] <--> HTTP API <--> [ LLM Server on your main PC ]

[ Behavior Node ] ← subscribes to all sensors
               → sends text to speech node or motor command node
```

---

## ✅ Recommendations for You

| Need                             | Best Option           |
| -------------------------------- | --------------------- |
| Microcontrollers/sensors         | MQTT → ROS bridge     |
| Intra-robot logic                | ROS 2 native pub/sub  |
| Talking to the LLM               | REST API or WebSocket |
| Voice / Web interface (optional) | HTTP                  |

---

Let me know if you'd like:

* A concrete example MQTT + ROS bridge setup
* A Python snippet to call your local LLM API from ROS
* Help choosing how to structure ROS nodes for sensors vs behavior vs personality


