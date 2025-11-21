from django.contrib import admin
from .models import Scenario, DecisionOption, UserScenarioLog, UserScenarioCustomization, UserScenarioProgress


@admin.register(Scenario)
class ScenarioAdmin(admin.ModelAdmin):
    list_display = ['title', 'starting_balance']
    search_fields = ['title']


@admin.register(DecisionOption)
class DecisionOptionAdmin(admin.ModelAdmin):
    list_display = ['text', 'scenario', 'decision_type']
    list_filter = ['decision_type', 'scenario']
    search_fields = ['text']


@admin.register(UserScenarioLog)
class UserScenarioLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'scenario', 'final_balance', 'date_played']
    list_filter = ['date_played']
    search_fields = ['user__username']


@admin.register(UserScenarioCustomization)
class UserScenarioCustomizationAdmin(admin.ModelAdmin):
    list_display = ['user', 'scenario', 'is_active', 'created_at']
    search_fields = ['user__username']
    list_filter = ['is_active', 'created_at']


@admin.register(UserScenarioProgress)
class UserScenarioProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'scenario', 'times_played', 'best_score', 'last_played']
    search_fields = ['user__username']
    list_filter = ['times_played', 'last_played']
