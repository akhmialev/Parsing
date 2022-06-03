Task: 

Write a Python script that will collect the address from the site in all cities
(city, street, house number, etc.), coordinates, working hours (if any)
(decomposed by days) and telephones (general and additional, if indicated).

Description:

Description:
The script must generate a json file that will store the array
objects
Exclude use of selenium,json file format:

{

    "address": "Москва, проспект Мира, 91к3",
    "latlon": [55.876279, 37.331549],
    "name": "KFC Ленинградское Москва",
    "phones": [ "+74952120000"],
    "working_hours": ["пн - пт 10:00 до 20:00", "сб-вс 10:00-20:00»]
}