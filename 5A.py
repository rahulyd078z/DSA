import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import random
import math
from typing import List, Dict, Tuple

# Simple tourist spots data - Nepali Places
TOURIST_SPOTS = [
    {"name": "Swayambhunath", "cost": 300, "time": 2, "interests": ["temples", "views"]},
    {"name": "Boudhanath", "cost": 200, "time": 1.5, "interests": ["temples", "spiritual"]},
    {"name": "Pashupatinath", "cost": 150, "time": 2, "interests": ["temples", "spiritual"]},
    {"name": "Durbar Square", "cost": 400, "time": 2.5, "interests": ["historical", "architecture"]},
    {"name": "Thamel", "cost": 800, "time": 2, "interests": ["shopping", "dining"]},
    {"name": "Patan", "cost": 350, "time": 2, "interests": ["historical", "temples"]},
    {"name": "Bhaktapur", "cost": 300, "time": 2.5, "interests": ["historical", "culture"]},
    {"name": "Kathmandu Valley", "cost": 500, "time": 3, "interests": ["nature", "views"]},
    {"name": "Pokhara", "cost": 1200, "time": 4, "interests": ["nature", "relaxation"]},
    {"name": "Nagarkot", "cost": 400, "time": 2, "interests": ["nature", "views", "hiking"]},
]


class SimulatedAnnealing:
    """Simple Simulated Annealing for itinerary optimization"""
    
    def __init__(self, spots: List[Dict], budget: float, time_limit: float, interests: List[str]):
        self.spots = spots
        self.budget = budget
        self.time_limit = time_limit
        self.interests = [i.lower().strip() for i in interests]
        self.explanation = ""
    
    def calculate_score(self, path: List[int]) -> float:
        """Calculate fitness score for a path"""
        if not path:
            return float('-inf')
        
        total_cost = sum(self.spots[i]["cost"] for i in path)
        total_time = sum(self.spots[i]["time"] for i in path)
        
        # Count interest matches
        interest_matches = 0
        for idx in path:
            for spot_interest in self.spots[idx]["interests"]:
                if spot_interest in self.interests:
                    interest_matches += 1
        
        # Score = interest matches - penalties
        score = interest_matches * 10
        
        # Budget penalty
        if total_cost > self.budget:
            score -= (total_cost - self.budget) * 2
        
        # Time penalty
        if total_time > self.time_limit:
            score -= (total_time - self.time_limit) * 5
        
        return score
    
    def optimize(self, iterations: int = 500) -> Tuple[List[int], float]:
        """Run simulated annealing"""
        # Start with random selection
        num_spots = min(4, len(self.spots))
        current = random.sample(range(len(self.spots)), num_spots)
        best = current.copy()
        best_score = self.calculate_score(best)
        
        temp = 50.0
        cooling_rate = 0.995
        
        for iteration in range(iterations):
            # Create neighbor by swapping two spots
            neighbor = current.copy()
            if len(neighbor) > 1:
                i, j = random.sample(range(len(neighbor)), 2)
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            
            current_score = self.calculate_score(current)
            neighbor_score = self.calculate_score(neighbor)
            delta = neighbor_score - current_score
            
            # Accept or reject
            if delta > 0 or random.random() < math.exp(delta / temp):
                current = neighbor
            
            # Update best
            current_score = self.calculate_score(current)
            if current_score > best_score:
                best = current.copy()
                best_score = current_score
            
            temp *= cooling_rate
        
        self._create_explanation(best, best_score)
        return best, best_score
    
    def _create_explanation(self, path: List[int], score: float):
        """Create simple explanation"""
        total_cost = sum(self.spots[i]["cost"] for i in path)
        total_time = sum(self.spots[i]["time"] for i in path)
        
        self.explanation = f"""Simulated Annealing Results:

Algorithm: Swapped spots randomly, accepted better solutions always, 
and worse solutions with decreasing probability as temperature cooled.

Parameters:
- Initial Temperature: 50
- Cooling Rate: 0.995
- Iterations: 500

Final Result:
- Spots Selected: {len(path)}
- Total Cost: ${total_cost}
- Total Time: {total_time:.1f} hours
- Interest Matches: Optimized for your interests
- Score: {score:.2f}"""


class TouristOptimizerApp:
    """Simple GUI Application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Tourist Spot Optimizer")
        self.root.geometry("700x600")
        ctk.set_appearance_mode("dark")
        
        self.sa = None
        self.best_path = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI"""
        # Title
        title = ctk.CTkLabel(self.root, text="Tourist Spot Optimizer", font=("Arial", 24, "bold"))
        title.pack(pady=20)
        
        # Input frame
        input_frame = ctk.CTkFrame(self.root)
        input_frame.pack(padx=20, pady=10, fill="x")
        
        # Budget
        ctk.CTkLabel(input_frame, text="Budget ($):", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.budget_var = ctk.StringVar(value="3000")
        ctk.CTkEntry(input_frame, textvariable=self.budget_var).grid(row=0, column=1, padx=10, sticky="ew")
        
        # Time
        ctk.CTkLabel(input_frame, text="Time (hours):", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.time_var = ctk.StringVar(value="6")
        ctk.CTkEntry(input_frame, textvariable=self.time_var).grid(row=1, column=1, padx=10, sticky="ew")
        
        # Interests
        ctk.CTkLabel(input_frame, text="Interests:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
        self.interests_var = ctk.StringVar(value="landmarks, art")
        ctk.CTkEntry(input_frame, textvariable=self.interests_var).grid(row=2, column=1, padx=10, sticky="ew")
        
        input_frame.grid_columnconfigure(1, weight=1)
        
        # Button
        btn = ctk.CTkButton(self.root, text="Generate Itinerary", command=self.optimize, font=("Arial", 14, "bold"))
        btn.pack(pady=15)
        
        # Results
        ctk.CTkLabel(self.root, text="Results:", font=("Arial", 12, "bold")).pack(anchor="w", padx=20, pady=(10, 5))
        
        self.result_text = ctk.CTkTextbox(self.root, height=300, font=("Courier", 10))
        self.result_text.pack(padx=20, pady=10, fill="both", expand=True)
        self.result_text.insert("0.0", "Click 'Generate Itinerary' to start...")
    
    def optimize(self):
        """Run optimization"""
        try:
            budget = float(self.budget_var.get())
            time_limit = float(self.time_var.get())
            interests = self.interests_var.get().split(",")
            
            if budget <= 0 or time_limit <= 0:
                raise ValueError("Budget and time must be positive")
            if not interests[0].strip():
                raise ValueError("Please enter interests")
            
            self.sa = SimulatedAnnealing(TOURIST_SPOTS, budget, time_limit, interests)
            self.best_path, score = self.sa.optimize()
            
            self.display_results()
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def display_results(self):
        """Display results"""
        if not self.best_path:
            return
        
        output = "OPTIMIZED ITINERARY:\n" + "="*50 + "\n\n"
        total_cost = 0
        total_time = 0
        
        for idx, spot_idx in enumerate(self.best_path, 1):
            spot = TOURIST_SPOTS[spot_idx]
            output += f"{idx}. {spot['name']}\n"
            output += f"   Cost: ${spot['cost']}\n"
            output += f"   Time: {spot['time']} hours\n"
            output += f"   Interests: {', '.join(spot['interests'])}\n\n"
            total_cost += spot['cost']
            total_time += spot['time']
        
        output += "="*50 + "\n"
        output += f"Total Cost: ${total_cost}\n"
        output += f"Total Time: {total_time} hours\n\n"
        output += self.sa.explanation
        
        self.result_text.delete("0.0", "end")
        self.result_text.insert("0.0", output)


def main():
    root = ctk.CTk()
    app = TouristOptimizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
