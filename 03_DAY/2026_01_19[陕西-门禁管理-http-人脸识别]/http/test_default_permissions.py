import json
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.person_service import person_service

# Test data without permission values (should use defaults)
test_data = json.dumps({
    'id': 'test_default_1',
    'name': 'Test Default'
})

print('Testing default permission values...')
result = person_service.create_person(test_data)
print(f'Result: {result}\n')

if result['success']:
    person = result['data']
    print('Verifying default permission values:')
    print(f'  facePermission: {person.get("facePermission")} (expected: 1)')
    print(f'  idCardPermission: {person.get("idCardPermission")} (expected: 1)')
    print(f'  faceAndCardPermission: {person.get("faceAndCardPermission")} (expected: 1)')
    
    # Check if all permissions are set to 1
    if (person.get('facePermission') == 1 and 
        person.get('idCardPermission') == 1 and 
        person.get('faceAndCardPermission') == 1):
        print('\n✅ All permissions correctly set to default value 1!')
    else:
        print('\n❌ Some permissions not set to default value 1!')
else:
    print('❌ Person creation failed!')
