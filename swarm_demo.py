#!/usr/bin/env python3
"""
🐝 SWARM MODE DEMO 🐝
Demonstrates the power of Agent Zero Swarm Mode

Run this to see how swarms work without needing to set up a full Agent Zero instance.
"""

import asyncio
import random
import time
from datetime import datetime
from typing import List, Dict


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


class SimulatedSubordinate:
    """Simulates a subordinate agent in the swarm"""
    
    def __init__(self, agent_id: str, specialty: str):
        self.agent_id = agent_id
        self.specialty = specialty
        self.status = "idle"
        
    async def execute_task(self, task: str) -> Dict:
        self.status = "working"
        processing_time = random.uniform(1.0, 3.0)
        
        print(f"{Colors.CYAN}    ├─ Agent {self.agent_id} [{self.specialty}] starting...{Colors.END}")
        
        for i in range(3):
            await asyncio.sleep(processing_time / 3)
            print(f"{Colors.CYAN}    ├─ Agent {self.agent_id} processing{'.' * (i + 1)}{Colors.END}")
        
        self.status = "complete"
        
        print(f"{Colors.GREEN}    ├─ Agent {self.agent_id} completed! ({processing_time:.1f}s){Colors.END}")
        
        return {
            "agent_id": self.agent_id,
            "specialty": self.specialty,
            "processing_time": processing_time
        }


class SwarmDemo:
    """Interactive Swarm Mode Demo"""
    
    def __init__(self):
        self.mission = None
        self.swarm_size = 0
        self.strategy = None
        
    def print_banner(self):
        print(f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║              🐝  AGENT ZERO SWARM MODE DEMO  🐝                  ║
║                                                                  ║
║     Watch how multiple AI agents work together in parallel!      ║
╚══════════════════════════════════════════════════════════════════╝
{Colors.END}
        """)
        
    def select_mission(self):
        print(f"\n{Colors.YELLOW}{Colors.BOLD}=== SELECT DEMO MISSION ==={Colors.END}\n")
        
        missions = [
            ("Codebase Analysis", "review", 4, ["analyzer", "reviewer", "tester", "researcher"]),
            ("Web App Development", "implement", 5, ["designer", "coder", "coder", "tester", "reviewer"]),
            ("Research Report", "research", 3, ["researcher", "researcher", "analyzer"]),
            ("System Design", "divide", 4, ["designer", "designer", "analyzer", "implementer"]),
        ]
        
        for i, (name, strategy, size, _) in enumerate(missions, 1):
            print(f"  {i}. {Colors.BOLD}{name}{Colors.END}")
            print(f"     Strategy: {Colors.CYAN}{strategy}{Colors.END} | Agents: {size}")
            print()
            
        choice = int(input(f"{Colors.CYAN}Select mission (1-4): {Colors.END}"))
        selected = missions[choice - 1]
        
        self.mission = selected[0]
        self.strategy = selected[1]
        self.swarm_size = selected[2]
        self.specialties = selected[3]
                
    async def run_swarm(self):
        print(f"\n{Colors.YELLOW}{Colors.BOLD}🐝 SWARM ACTIVATED 🐝{Colors.END}\n")
        print(f"{Colors.CYAN}📋 Mission:{Colors.END} {self.mission}")
        print(f"{Colors.CYAN}🎯 Strategy:{Colors.END} {self.strategy}")
        print(f"{Colors.CYAN}👥 Swarm Size:{Colors.END} {self.swarm_size} agents")
        print()
        
        print(f"{Colors.YELLOW}🧠 Step 1: Task Decomposition{Colors.END}")
        await asyncio.sleep(1)
        for i in range(self.swarm_size):
            print(f"{Colors.GREEN}   ✓ Subtask {i+1} assigned{Colors.END}")
            await asyncio.sleep(0.3)
        print()
        
        print(f"{Colors.YELLOW}🚀 Step 2: Spawning Agents{Colors.END}")
        subordinates = []
        for i, specialty in enumerate(self.specialties[:self.swarm_size]):
            agent_id = f"A-{i+1:03d}"
            agent = SimulatedSubordinate(agent_id, specialty)
            subordinates.append(agent)
            print(f"{Colors.CYAN}   ✓ Spawned Agent {agent_id} [{specialty}]{Colors.END}")
            await asyncio.sleep(0.2)
        print()
        
        print(f"{Colors.YELLOW}⚡ Step 3: Parallel Execution{Colors.END}")
        print(f"{Colors.CYAN}   All {self.swarm_size} agents working simultaneously...{Colors.END}\n")
        
        start_time = time.time()
        tasks = [agent.execute_task(f"Task {i+1}") for i, agent in enumerate(subordinates)]
        results = await asyncio.gather(*tasks)
        
        elapsed = time.time() - start_time
        print(f"\n{Colors.GREEN}   ✓ All agents completed in {elapsed:.1f} seconds{Colors.END}")
        print()
        
        print(f"{Colors.YELLOW}🔄 Step 4: Result Synthesis{Colors.END}")
        await asyncio.sleep(1)
        print(f"{Colors.GREEN}   ✓ Results combined into final deliverable{Colors.END}")
        print()
        
        print(f"{Colors.YELLOW}{Colors.BOLD}=== MISSION COMPLETE ==={Colors.END}")
        print(f"  Duration: {elapsed:.1f}s")
        print(f"  Speedup: ~{self.swarm_size * 0.8:.1f}x faster than sequential")
        
    def main_menu(self):
        while True:
            print("\n" * 3)
            self.print_banner()
            
            print(f"\n{Colors.YELLOW}{Colors.BOLD}=== MAIN MENU ==={Colors.END}\n")
            print(f"  1. 🚀 Run Swarm Demo")
            print(f"  2. 🚪 Exit")
            
            choice = input(f"\n{Colors.CYAN}Select option (1-2): {Colors.END}")
            
            if choice == "1":
                print("\n" * 3)
                self.print_banner()
                self.select_mission()
                asyncio.run(self.run_swarm())
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.END}")
            elif choice == "2":
                print(f"\n{Colors.GREEN}Thanks for exploring Swarm Mode! 🐝{Colors.END}\n")
                break


def main():
    demo = SwarmDemo()
    demo.main_menu()


if __name__ == "__main__":
    main()
