import json
import sys
sys.path.insert(0, '.')
from services.person_service import person_service

# Test data with integer values
person_data1 = json.dumps({
    'id': 'test001',
    'name': 'test1',
    'facePermission': 1,
    'idCardPermission': 2,
    'faceAndCardPermission': 1
})

# Test data with string values
person_data2 = json.dumps({
    'id': 'test002',
    'name': 'test2',
    'facePermission': '1',
    'idCardPermission': '2',
    'faceAndCardPermission': '1'
})

# Test creating person with integer values
print('Test 1: Creating person with integer permission values')
result1 = person_service.create_person(person_data1)
print(f'Result: {result1}\n')

# Test creating person with string values  
print('Test 2: Creating person with string permission values')
result2 = person_service.create_person(person_data2)
print(f'Result: {result2}\n')

# Test updating person with missing permissions (should keep existing values)
update_data = json.dumps({
    'id': 'test001',
    'name': 'updated_test1'
})
print('Test 3: Updating person without permission values (should keep existing)')
result3 = person_service.update_person(update_data)
print(f'Result: {result3}\n')
