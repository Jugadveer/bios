"""
Management command to import scenarios from scenarios.json
Run: python manage.py import_scenarios
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
import json
import os
from django.conf import settings


class Command(BaseCommand):
    help = 'Imports scenarios from scenarios.json file'

    def handle(self, *args, **options):
        self.stdout.write('Importing scenarios from scenarios.json...')
        
        # Get the JSON file path
        json_path = os.path.join(settings.BASE_DIR, 'scenarios.json')
        
        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f'File not found: {json_path}'))
            return
        
        # Read and parse JSON
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Separate scenarios and decision options
        scenarios_data = [item for item in data if item['model'] == 'simulator.scenario']
        options_data = [item for item in data if item['model'] == 'simulator.decisionoption']
        
        self.stdout.write(f'Found {len(scenarios_data)} scenarios and {len(options_data)} decision options')
        
        # Import using Django's loaddata
        # Create a temporary fixture file
        temp_fixture = os.path.join(settings.BASE_DIR, 'temp_scenarios_fixture.json')
        
        try:
            # Write only scenarios and options (skip user logs)
            fixture_data = scenarios_data + options_data
            
            with open(temp_fixture, 'w', encoding='utf-8') as f:
                json.dump(fixture_data, f, indent=4, ensure_ascii=False)
            
            # Use loaddata to import
            call_command('loaddata', temp_fixture, verbosity=0)
            
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(scenarios_data)} scenarios'))
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(options_data)} decision options'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing: {str(e)}'))
        finally:
            # Clean up temp file
            if os.path.exists(temp_fixture):
                os.remove(temp_fixture)

