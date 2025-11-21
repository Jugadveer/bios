import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Scenario, UserScenarioLog

# 1. HOMEPAGE: Redirects straight to the first scenario
@login_required(login_url='/')
def home(request):
    # Tries to find the first scenario ID (usually 1)
    first_scenario = Scenario.objects.first()
    if first_scenario:
        return redirect(f'/scenario/play/{first_scenario.id}/')
    else:
        return HttpResponse("No scenarios found. Please add them in Admin.")

# 2. GAME ENGINE
@login_required(login_url='/')
def scenario_play(request, scenario_id):
    scenario = get_object_or_404(Scenario, id=scenario_id)
    
    # Logic to find the Next Scenario button
    next_scenario = Scenario.objects.filter(id__gt=scenario.id).order_by('id').first()
    next_id = next_scenario.id if next_scenario else None

    options_data = []
    for option in scenario.options.all():
        options_data.append({
            'id': option.id,
            'text': option.text,
            'type': option.decision_type,
            'impact': {
                'balance': float(option.balance_impact),
                'confidence': option.confidence_delta,
                'risk': option.risk_score_delta,
                'growth_rate': float(option.future_growth_rate)
            },
            'content': {
                'why_matters': option.why_it_matters,
                'mentor': option.mentor_feedback
            }
        })

    game_config = {
        'scenario_id': scenario.id,
        'start_balance': float(scenario.starting_balance),
        'next_scenario_id': next_id,
        'choices': options_data
    }

    return render(request, 'scenario_play.html', {
        'scenario': scenario,
        'game_config_json': game_config
    })

@login_required(login_url='/')
@csrf_exempt
def save_scenario_result(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            scenario_id = data.get('scenario_id')
            scenario = None
            if scenario_id:
                try:
                    scenario = Scenario.objects.get(id=scenario_id)
                except Scenario.DoesNotExist:
                    pass
            
            UserScenarioLog.objects.create(
                user=request.user,
                scenario=scenario,
                final_balance=data.get('final_balance', 0)
            )
            return JsonResponse({'status': 'success'})
        except Exception:
            return JsonResponse({'status': 'error'}, status=500)
    return JsonResponse({'status': 'error'}, status=400)