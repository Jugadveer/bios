from django.db import models
from django.contrib.auth.models import User

class Scenario(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    starting_balance = models.DecimalField(max_digits=10, decimal_places=2, default=50000)
    
    def __str__(self):
        return self.title

class DecisionOption(models.Model):
    scenario = models.ForeignKey(Scenario, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=100)  # e.g. "Invest 50% in SIP"
    
    TYPE_CHOICES = [
        ('INVEST', 'Invest'),
        ('SAVE', 'Save'),
        ('SPEND', 'Spend'),
    ]
    decision_type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    # Game Logic Data
    balance_impact = models.DecimalField(max_digits=10, decimal_places=2, help_text="Negative for spending, positive for income")
    confidence_delta = models.IntegerField(default=0, help_text="e.g. +10 or -5")
    risk_score_delta = models.IntegerField(default=0, help_text="0-100 scale impact")
    future_growth_rate = models.DecimalField(max_digits=5, decimal_places=4, default=0.0, help_text="Annual return rate (e.g. 0.12 for 12%)")
    
    # Narrative Data
    why_it_matters = models.TextField(help_text="Educational context text")
    mentor_feedback = models.CharField(max_length=255, help_text="Short snappy feedback")

    def __str__(self):
        return self.text

class UserScenarioLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, null=True, blank=True)
    final_balance = models.DecimalField(max_digits=12, decimal_places=2)
    date_played = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_played']


# User-specific scenario customization (for future use)
class UserScenarioCustomization(models.Model):
    """Store user-specific customizations for scenarios (different questions, options, etc.)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scenario_customizations')
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name='user_customizations', null=True, blank=True)
    custom_scenario_id = models.IntegerField(null=True, blank=True, help_text="For JSON-based scenarios")  # Renamed to avoid conflict
    custom_content = models.JSONField(default=dict, blank=True)  # Store custom options, questions, etc.
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'scenario']
        indexes = [
            models.Index(fields=['user', 'scenario']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.scenario.title if self.scenario else self.custom_scenario_id}"


# User-specific scenario progress/state
class UserScenarioProgress(models.Model):
    """Track user progress and state for scenarios"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scenario_progress')
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE, related_name='user_progress', null=True, blank=True)
    custom_scenario_id = models.IntegerField(null=True, blank=True, help_text="For JSON-based scenarios")  # Renamed to avoid conflict
    current_state = models.JSONField(default=dict, blank=True)  # Store current game state
    best_score = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    times_played = models.IntegerField(default=0)
    last_played = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'scenario']
        indexes = [
            models.Index(fields=['user', 'scenario']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.scenario.title if self.scenario else self.custom_scenario_id} - {self.times_played} plays"
