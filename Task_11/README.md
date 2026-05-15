Synchronization

The two incoming data streams, position and priority, arrive on separate topics. A shared dictionary called fleet stores the latest value of each stream per robot. A 10Hz timer runs the yielding logic and only processes a robot when both its pose and priority have been received.

---

Yielding Logic

Every 0.1 seconds the traffic manager checks every robot in the fleet. It calculates the straight line distance using the Euclidean formula. A DANGER warning is triggered only when the robot is within 2.0 meters and has a higher priority than robot_0. Both conditions must be true at the same time, otherwise the path is CLEAR.