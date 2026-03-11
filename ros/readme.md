# Running

docker-compose up -d

Open the Web Interface:
Go to studio.foxglove.dev in your browser.

Connect to your Container:

    Click "Open Connection".

    Select "Foxglove WebSocket".

    Enter ws://localhost:8765 and click Connect.

# Testing

## Seeing "What Happens" (Your First Test)

Now that the bridge is running, let’s generate some data to see if it shows up in the web interface.

    Exec into the running container:
    Bash

    docker exec -it ros_dev bash

    Run a demo publisher:
    Inside that terminal, run:
    Bash

    source /opt/ros/humble/setup.bash
    ros2 run demo_nodes_cpp talker

    Check the Dashboard:
    In Foxglove, add a "Raw Messages" or "Teleplot" panel. You should see the "Hello World" messages appearing in real-time.

## Important Config: The Workspace

In the docker-compose file above, I included a volume mapping: ./my_workspace:/ros_ws.

    src/: This is where you put your Python or C++ code.

    colcon build: You run this inside the container to compile your code.

    Persistent Storage: Because of the volume mapping, even if you stop the container, your code remains safe on your laptop’s hard drive in the my_workspace folder.


# Robot software


https://blog.robotair.io/the-complete-beginners-guide-to-using-docker-for-ros-2-deployment-2025-edition-0f259ca8b378


## ROS?

### 🧩 1. **Scalable Sensor Architecture**

* ROS lets you add sensors (distance, temperature, battery, GPS, etc.) as **modular nodes**.
* You don’t have to rewrite your logic each time — you just subscribe to new topics like `/battery_level`, `/proximity`, etc.
* Debugging and monitoring via tools like `rqt_graph` and `ros2 topic echo` becomes incredibly useful.

### 🔋 2. **Battery Monitoring & Charging Logic**

* ROS doesn’t come with a “battery module” out of the box, but:

  * You can run a **battery monitor node** that reads from ADC, I2C, or smart battery interfaces.
  * It can publish data to a topic like `/battery/status`.
  * Another node (your behavior controller or decision logic) **subscribes** and decides: "Am I low? Should I say something? Should I drive to my charger?"

* Later you could add:

  * A `/charger_locator` service that uses camera + AR marker
  * A `/docking` node that runs a path planner

ROS even has some **existing packages** for autonomous docking (like from TurtleBot).

### 🤖 3. **LLM as a Sidecar**

* Your LLM logic can live **outside ROS** (on your main server) and expose a local API.
* A ROS node can then:

  * Subscribe to events (`/seen_human`, `/bored`, `/battery_low`)
  * Send a query to the LLM
  * Publish LLM responses to `/speech_output` or `/intent_action`

That keeps your AI logic and hardware decoupled — a major benefit in the long run.


## 🚀 Next Steps (if you go with ROS)

1. **Start small** with:
   * A `battery_monitor` node
   * A `sensor_manager` node
   * A `llm_bridge` node (talks to your server)
2. Structure the bot’s logic using **event-based triggers** (e.g., when `/battery/status` < 20%, trigger alert).
3. Let the LLM be a *flavor* on top — the robot is a robot first, a quirky companion second.


## 🧱 Suggested ROS Node Architecture

| ROS Node               | Purpose                                    |
| ---------------------- | ------------------------------------------ |
| `/cmd_vel` publisher   | Sends movement commands (linear/angular)   |
| `serial_motion_bridge` | Translates `/cmd_vel` to Arduino serial    |
| `serial_eyes_bridge`   | Publishes `/mood`, `/eyes/track`           |
| `battery_monitor`      | Reads voltage from motion Arduino          |
| `navigation_core`      | Decides where to go (goal, idle, charging) |
| `llm_bridge`           | Talks to your LLM server                   |
