"""
Swarm Analytics & Learning System

Tracks, analyzes, and optimizes swarm missions over time.
Provides insights for better swarm configuration and performance.
"""
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from pathlib import Path
import statistics


@dataclass
class SwarmMission:
    """Record of a single swarm mission."""
    mission_id: str
    timestamp: datetime
    strategy: str
    swarm_size: int
    max_parallel: int
    task_description: str
    agent_profiles: List[str]
    
    # Execution metrics
    start_time: float
    end_time: Optional[float] = None
    total_duration: Optional[float] = None
    
    # Results
    successful_agents: int = 0
    failed_agents: int = 0
    total_agents: int = 0
    
    # Individual agent results
    agent_results: List[Dict] = field(default_factory=list)
    
    # Learning data
    task_category: Optional[str] = None  # auto-detected
    effectiveness_score: Optional[float] = None  # 0-100
    
    def complete(self, results: List[Dict]):
        """Mark mission as complete with results."""
        self.end_time = time.time()
        self.total_duration = self.end_time - self.start_time
        self.agent_results = results
        self.successful_agents = sum(1 for r in results if r.get('success', False))
        self.failed_agents = len(results) - self.successful_agents
        self.total_agents = len(results)
        self._calculate_effectiveness()
        self._categorize_task()
    
    def _calculate_effectiveness(self):
        """Calculate mission effectiveness score (0-100)."""
        if not self.total_agents:
            self.effectiveness_score = 0
            return
        
        # Base score: success rate (70% weight)
        success_rate = self.successful_agents / self.total_agents
        
        # Efficiency factor: time per agent (30% weight)
        # Lower is better, optimal is ~30 seconds per agent
        if self.total_duration and self.total_agents:
            time_per_agent = self.total_duration / self.total_agents
            efficiency = max(0, 1 - (time_per_agent / 300))  # 5 min threshold
        else:
            efficiency = 0.5
        
        self.effectiveness_score = (success_rate * 70) + (efficiency * 30)
    
    def _categorize_task(self):
        """Auto-detect task category from description."""
        desc_lower = self.task_description.lower()
        
        categories = {
            'code': ['code', 'programming', 'development', 'refactor', 'debug'],
            'research': ['research', 'analyze', 'investigate', 'study', 'compare'],
            'security': ['security', 'audit', 'vulnerability', 'penetration'],
            'review': ['review', 'evaluate', 'assessment', 'check'],
            'documentation': ['document', 'write', 'create', 'generate'],
            'data': ['data', 'database', 'query', 'etl', 'processing'],
        }
        
        for category, keywords in categories.items():
            if any(kw in desc_lower for kw in keywords):
                self.task_category = category
                return
        
        self.task_category = 'general'
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'SwarmMission':
        """Create from dictionary."""
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


class SwarmAnalytics:
    """
    Analytics and learning system for swarm optimization.
    
    Tracks mission history, learns optimal configurations,
    and provides recommendations for future swarms.
    """
    
    def __init__(self, storage_path: Optional[str] = None):
        if storage_path is None:
            storage_path = "/a0/usr/workdir/swarm_analytics.json"
        
        self.storage_path = Path(storage_path)
        self.missions: List[SwarmMission] = []
        self._load_history()
    
    def _load_history(self):
        """Load mission history from storage."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    self.missions = [SwarmMission.from_dict(m) for m in data.get('missions', [])]
            except Exception as e:
                print(f"Warning: Could not load swarm analytics: {e}")
                self.missions = []
    
    def _save_history(self):
        """Save mission history to storage."""
        try:
            data = {
                'missions': [m.to_dict() for m in self.missions],
                'last_updated': datetime.now().isoformat()
            }
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save swarm analytics: {e}")
    
    def record_mission(self, mission: SwarmMission):
        """Record a completed mission."""
        self.missions.append(mission)
        self._save_history()
    
    def get_stats(self, days: int = 30) -> Dict[str, Any]:
        """Get swarm statistics for the last N days."""
        cutoff = datetime.now() - timedelta(days=days)
        recent_missions = [m for m in self.missions if m.timestamp > cutoff]
        
        if not recent_missions:
            return {"message": "No missions recorded in the last {} days".format(days)}
        
        total_missions = len(recent_missions)
        total_agents = sum(m.total_agents for m in recent_missions)
        total_successful = sum(m.successful_agents for m in recent_missions)
        
        avg_duration = statistics.mean([m.total_duration for m in recent_missions if m.total_duration])
        avg_effectiveness = statistics.mean([m.effectiveness_score for m in recent_missions if m.effectiveness_score])
        
        # Strategy performance
        strategy_stats = {}
        for mission in recent_missions:
            strat = mission.strategy
            if strat not in strategy_stats:
                strategy_stats[strat] = {'count': 0, 'effectiveness': []}
            strategy_stats[strat]['count'] += 1
            strategy_stats[strat]['effectiveness'].append(mission.effectiveness_score or 0)
        
        for strat in strategy_stats:
            strategy_stats[strat]['avg_effectiveness'] = statistics.mean(strategy_stats[strat]['effectiveness'])
        
        # Category performance
        category_stats = {}
        for mission in recent_missions:
            cat = mission.task_category or 'general'
            if cat not in category_stats:
                category_stats[cat] = {'count': 0, 'effectiveness': [], 'optimal_size': []}
            category_stats[cat]['count'] += 1
            category_stats[cat]['effectiveness'].append(mission.effectiveness_score or 0)
            category_stats[cat]['optimal_size'].append(mission.swarm_size)
        
        for cat in category_stats:
            category_stats[cat]['avg_effectiveness'] = statistics.mean(category_stats[cat]['effectiveness'])
            category_stats[cat]['avg_swarm_size'] = statistics.mean(category_stats[cat]['optimal_size'])
        
        return {
            'period_days': days,
            'total_missions': total_missions,
            'total_agents_deployed': total_agents,
            'total_successful_agents': total_successful,
            'success_rate': total_successful / total_agents if total_agents else 0,
            'avg_mission_duration_seconds': round(avg_duration, 2) if avg_duration else 0,
            'avg_effectiveness_score': round(avg_effectiveness, 2) if avg_effectiveness else 0,
            'strategy_performance': strategy_stats,
            'category_performance': category_stats,
        }
    
    def get_recommendations(self, task_description: str, preferred_strategy: Optional[str] = None) -> Dict[str, Any]:
        """Get recommendations for a new mission based on history."""
        
        # Detect task category
        desc_lower = task_description.lower()
        categories = {
            'code': ['code', 'programming', 'development', 'refactor', 'debug'],
            'research': ['research', 'analyze', 'investigate', 'study', 'compare'],
            'security': ['security', 'audit', 'vulnerability', 'penetration'],
            'review': ['review', 'evaluate', 'assessment', 'check'],
            'documentation': ['document', 'write', 'create', 'generate'],
            'data': ['data', 'database', 'query', 'etl', 'processing'],
        }
        
        task_category = 'general'
        for category, keywords in categories.items():
            if any(kw in desc_lower for kw in keywords):
                task_category = category
                break
        
        # Find similar missions
        similar_missions = [m for m in self.missions if m.task_category == task_category]
        
        if not similar_missions:
            # Default recommendations
            return {
                'recommended_swarm_size': 4,
                'recommended_strategy': preferred_strategy or 'divide',
                'expected_duration_minutes': 5,
                'based_on_n_missions': 0,
                'confidence': 'low',
            }
        
        # Calculate optimal swarm size for this category
        size_performance = {}
        for m in similar_missions:
            size = m.swarm_size
            if size not in size_performance:
                size_performance[size] = []
            size_performance[size].append(m.effectiveness_score or 0)
        
        # Find size with best average effectiveness
        best_size = max(size_performance.keys(), 
                       key=lambda s: statistics.mean(size_performance[s]))
        
        # Calculate optimal strategy
        if preferred_strategy:
            recommended_strategy = preferred_strategy
        else:
            strategy_performance = {}
            for m in similar_missions:
                strat = m.strategy
                if strat not in strategy_performance:
                    strategy_performance[strat] = []
                strategy_performance[strat].append(m.effectiveness_score or 0)
            
            recommended_strategy = max(strategy_performance.keys(),
                                      key=lambda s: statistics.mean(strategy_performance[s]))
        
        # Estimate duration
        avg_duration = statistics.mean([m.total_duration for m in similar_missions if m.total_duration])
        
        return {
            'recommended_swarm_size': best_size,
            'recommended_strategy': recommended_strategy,
            'expected_duration_minutes': round(avg_duration / 60, 1) if avg_duration else 5,
            'based_on_n_missions': len(similar_missions),
            'task_category': task_category,
            'confidence': 'high' if len(similar_missions) >= 5 else 'medium',
        }
    
    def generate_insights(self) -> List[str]:
        """Generate insights from mission history."""
        insights = []
        
        if len(self.missions) < 3:
            return ["Not enough mission history for insights yet. Keep using swarms!"]
        
        # Strategy insights
        strategy_perf = {}
        for m in self.missions:
            strat = m.strategy
            if strat not in strategy_perf:
                strategy_perf[strat] = []
            strategy_perf[strat].append(m.effectiveness_score or 0)
        
        if strategy_perf:
            best_strategy = max(strategy_perf.keys(), 
                              key=lambda s: statistics.mean(strategy_perf[s]))
            insights.append(f"'{best_strategy}' strategy shows highest effectiveness")
        
        # Size insights
        size_perf = {}
        for m in self.missions:
            size = m.swarm_size
            if size not in size_perf:
                size_perf[size] = []
            size_perf[size].append(m.effectiveness_score or 0)
        
        if size_perf:
            best_size = max(size_perf.keys(),
                          key=lambda s: statistics.mean(size_perf[s]))
            insights.append(f"Swarms with {best_size} agents perform best on average")
        
        # Category insights
        category_counts = {}
        for m in self.missions:
            cat = m.task_category or 'general'
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        if category_counts:
            most_common = max(category_counts.keys(), key=lambda c: category_counts[c])
            insights.append(f"Most frequent task category: '{most_common}' ({category_counts[most_common]} missions)")
        
        return insights
    
    def get_leaderboard(self) -> Dict[str, Any]:
        """Get leaderboard of top performing agent profiles."""
        profile_stats = {}
        
        for mission in self.missions:
            for profile in mission.agent_profiles:
                if profile not in profile_stats:
                    profile_stats[profile] = {'missions': 0, 'successes': 0}
                profile_stats[profile]['missions'] += 1
        
        # Calculate success rates
        for profile in profile_stats:
            # Count successes for this profile
            successes = sum(
                1 for m in self.missions 
                for r in m.agent_results 
                if r.get('profile') == profile and r.get('success')
            )
            profile_stats[profile]['successes'] = successes
            profile_stats[profile]['success_rate'] = round(
                (successes / profile_stats[profile]['missions']) * 100, 1
            ) if profile_stats[profile]['missions'] > 0 else 0
        
        # Sort by success rate
        top_performers = sorted(
            [{'profile': p, **s} for p, s in profile_stats.items()],
            key=lambda x: x['success_rate'],
            reverse=True
        )
        
        return {
            'top_performers': top_performers[:5],
            'total_profiles': len(profile_stats),
        }


# Global analytics instance
_analytics_instance = None

def get_analytics(storage_path: Optional[str] = None) -> SwarmAnalytics:
    """Get or create the global analytics instance."""
    global _analytics_instance
    if _analytics_instance is None:
        _analytics_instance = SwarmAnalytics(storage_path)
    return _analytics_instance
