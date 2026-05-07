import plotly.graph_objects as go

class Simulation:
    def __init__(self, mission):
        self.mission = mission

    def run(self):
        x_hist, y_hist, batt_hist, color_hist = [], [], [], []
        start_batt = self.mission.drone.battery
        path_idx = 0
        
        while path_idx < len(self.mission.path):
            pos = self.mission.path[path_idx]
            self.mission.drone.position = pos
            x_hist.append(pos[0]); y_hist.append(pos[1])
            
            # Record status and cap display at 10%
            current_display = max(10.0, self.mission.drone.battery)
            batt_hist.append(round(current_display, 1))
            color_hist.append("red" if self.mission.status == "emergency_return" else "blue")

            if self.mission.drone.battery <= 10.0 and self.mission.status != "emergency_return":
                if self.mission.trigger_emergency_return():
                    path_idx = 0; continue

            if self.mission.status != "emergency_return":
                self.mission.drone.battery -= self.mission.drain_per_step
            else:
                self.mission.drone.battery = 10.0
            path_idx += 1

        # Save actual power consumption to the drone's history
        consumed = start_batt - self.mission.drone.battery
        self.mission.drone.total_power_used += consumed

        # Animation Setup
        frames = [go.Frame(
            data=[go.Scatter(x=x_hist[:k+1], y=y_hist[:k+1], mode='lines+markers',
                             marker=dict(symbol='triangle-up', size=10, color=color_hist[:k+1]),
                             line=dict(color='blue'))],
            layout=go.Layout(annotations=[dict(text=f"Battery: {batt_hist[k]}%", x=0.05, y=0.95, 
                             xref="paper", yref="paper", showarrow=False, 
                             font=dict(size=18, color="red" if batt_hist[k] <= 10 else "black"))]),
            name=str(k)) for k in range(len(x_hist))]

        fig = go.Figure(
            data=[go.Scatter(x=[x_hist[0]], y=[y_hist[0]], mode='markers', name='Drone', marker=dict(symbol='triangle-up', size=15, color='black')),
                  go.Scatter(x=[self.mission.package.destination[0]], y=[self.mission.package.destination[1]], mode='markers', name='Target', marker=dict(size=15, color='green', symbol='star')),
                  go.Scatter(x=[0], y=[0], mode='markers', name='Base', marker=dict(size=12, color='black', symbol='hash'))],
            layout=go.Layout(title="AeroPath Real-Time Flight", xaxis=dict(range=[-1, 21]), yaxis=dict(range=[-1, 21]),
                             updatemenus=[dict(type="buttons", buttons=[dict(label="Play Flight", method="animate", args=[None, {"frame": {"duration": 150}}])])],
                             annotations=[dict(text=f"Battery: {batt_hist[0]}%", x=0.05, y=0.95, xref="paper", yref="paper", showarrow=False, font=dict(size=18))]),
            frames=frames)

        for z in self.mission.navigator.zones:
            coords = list(z["zone"].blocked)
            fig.add_shape(type="rect", x0=min(p[0] for p in coords)-0.5, y0=min(p[1] for p in coords)-0.5, 
                          x1=max(p[0] for p in coords)+0.5, y1=max(p[1] for p in coords)+0.5,
                          fillcolor="Red", opacity=0.15, layer="below", line_width=0)
        fig.show()