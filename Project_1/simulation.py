import plotly.graph_objects as go

class Simulation:
    def __init__(self, mission):
        self.mission = mission

    def run(self):
        x_history, y_history, color_history, battery_history = [], [], [], []
        path_index = 0
        
        while path_index < len(self.mission.path):
            current_pos = self.mission.path[path_index]
            self.mission.drone.position = current_pos
            x_history.append(current_pos[0]); y_history.append(current_pos[1])
            
            # --- Battery Capping Logic ---
            # We strictly prevent the recorded battery from dropping below 10.0
            if self.mission.drone.battery < 10.0:
                self.mission.drone.battery = 10.0
            
            battery_history.append(round(self.mission.drone.battery, 1))
            color_history.append("red" if self.mission.status == "emergency_return" else "blue")

            # Trigger emergency if we hit 10%
            if self.mission.drone.battery <= 10.0 and self.mission.status != "emergency_return":
                if self.mission.trigger_emergency_return():
                    path_index = 0; continue

            # Apply drain only if not in emergency mode
            if self.mission.status != "emergency_return":
                self.mission.drone.battery -= self.mission.drain_per_step
            else:
                # Keep battery at exactly 10% during return
                self.mission.drone.battery = 10.0
            
            path_index += 1

        # Build Animation Frames
        frames = [go.Frame(
            data=[go.Scatter(x=x_history[:k+1], y=y_history[:k+1], mode='lines+markers',
                             marker=dict(symbol='triangle-up', size=10, color=color_history[:k+1]),
                             line=dict(color='blue'))],
            layout=go.Layout(annotations=[dict(text=f"Battery: {battery_history[k]}%", x=0.05, y=0.95, 
                             xref="paper", yref="paper", showarrow=False, 
                             font=dict(size=18, color="red" if battery_history[k] <= 10 else "black"))]),
            name=str(k)) for k in range(len(x_history))]

        fig = go.Figure(
            data=[go.Scatter(x=[x_history[0]], y=[y_history[0]], mode='markers', name='Drone', marker=dict(symbol='triangle-up', size=15, color='black')),
                  go.Scatter(x=[self.mission.package.destination[0]], y=[self.mission.package.destination[1]], mode='markers', name='Target', marker=dict(size=15, color='green', symbol='star')),
                  go.Scatter(x=[0], y=[0], mode='markers', name='Base', marker=dict(size=12, color='black', symbol='hash'))],
            layout=go.Layout(title="🚁 Drone Simulation with Areas Team E ☝🏼☝🏼🔥",
                             xaxis=dict(range=[-1, 21], dtick=1), yaxis=dict(range=[-1, 21], dtick=1),
                             updatemenus=[dict(type="buttons", buttons=[dict(label="Play Flight", method="animate", args=[None, {"frame": {"duration": 150}}])])],
                             annotations=[dict(text=f"Battery: {battery_history[0]}%", x=0.05, y=0.95, xref="paper", yref="paper", showarrow=False, font=dict(size=18))]),
            frames=frames)

        # Draw No-Fly Zones
        for z in self.mission.navigator.zones:
            coords = list(z["zone"].blocked)
            fig.add_shape(type="rect", x0=min(p[0] for p in coords)-0.5, y0=min(p[1] for p in coords)-0.5, 
                          x1=max(p[0] for p in coords)+0.5, y1=max(p[1] for p in coords)+0.5,
                          fillcolor="Red", opacity=0.15, layer="below", line_width=0)
        fig.show()