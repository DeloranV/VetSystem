from http.client import HTTPConnection

add_pet = open('data/add_pet.json').read()
add_vet = open('data/add_vet.json').read()
add_appointment = open('data/add_appointment.json').read()

update_appointment = open('data/update_appointment.json').read()
update_pet = open('data/update_pet.json').read()
update_resource = open('data/update_resource.json').read()
update_vet = open('data/update_vet.json').read()

conn = HTTPConnection("127.0.0.1:5000")

req = conn.request("POST", "/api/appointments?key=1111", add_appointment,
                        {"Content-type": "application/json"})

resp = conn.getresponse()
print(resp.read())


#(TODO) TESTING WITH ASSERT
