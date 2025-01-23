from http.client import HTTPConnection

add_pet = open('add_pet.json').read()
add_vet = open('add_vet.json').read()

update_appointment = open('update_appointment.json').read()
update_pet = open('update_pet.json').read()
update_resource = open('update_resource.json').read()
update_vet = open('update_vet.json').read()

conn = HTTPConnection("127.0.0.1:5000")

req = conn.request("POST", "/api/pets?key=1234", add_pet,
                        {"Content-type": "application/json"})
resp = conn.getresponse()
print(resp.read())

req = conn.request("PATCH", "/api/appointments/1?key=1234",
                   update_appointment, {"Content-type": "application/json"})

resp = conn.getresponse()
print(resp.read())
