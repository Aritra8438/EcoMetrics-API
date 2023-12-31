from thefuzz import process

countries = [
    "Afghanistan",
    "Albania",
    "Algeria",
    "Andorra",
    "Angola",
    "Antigua and Barbuda",
    "Argentina",
    "Armenia",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Bahamas",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Belgium",
    "Belize",
    "Benin",
    "Bhutan",
    "Bolivia",
    "Bosnia and Herzegovina",
    "Botswana",
    "Brazil",
    "Brunei",
    "Bulgaria",
    "Burkina Faso",
    "Burundi",
    "Cabo Verde",
    "Cambodia",
    "Cameroon",
    "Canada",
    "Central African Republic",
    "Chad",
    "Chile",
    "China",
    "Colombia",
    "Comoros",
    "Congo, Democratic Republic of the",
    "Congo, Republic of the",
    "Costa Rica",
    "Cote d'Ivoire",
    "Croatia",
    "Cuba",
    "Cyprus",
    "Czech Republic",
    "Denmark",
    "Djibouti",
    "Dominica",
    "Dominican Republic",
    "Ecuador",
    "Egypt",
    "El Salvador",
    "Equatorial Guinea",
    "Eritrea",
    "Estonia",
    "Eswatini",
    "Ethiopia",
    "Fiji",
    "Finland",
    "France",
    "Gabon",
    "Gambia",
    "Georgia",
    "Germany",
    "Ghana",
    "Greece",
    "Grenada",
    "Guatemala",
    "Guinea",
    "Guinea-Bissau",
    "Guyana",
    "Haiti",
    "Honduras",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Iran",
    "Iraq",
    "Ireland",
    "Israel",
    "Italy",
    "Jamaica",
    "Japan",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Kiribati",
    "Korea, North",
    "Korea, South",
    "Kosovo",
    "Kuwait",
    "Kyrgyzstan",
    "Laos",
    "Latvia",
    "Lebanon",
    "Lesotho",
    "Liberia",
    "Libya",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Madagascar",
    "Malawi",
    "Malaysia",
    "Maldives",
    "Mali",
    "Malta",
    "Marshall Islands",
    "Mauritania",
    "Mauritius",
    "Mexico",
    "Micronesia",
    "Moldova",
    "Monaco",
    "Mongolia",
    "Montenegro",
    "Morocco",
    "Mozambique",
    "Myanmar",
    "Namibia",
    "Nauru",
    "Nepal",
    "Netherlands",
    "New Zealand",
    "Nicaragua",
    "Niger",
    "Nigeria",
    "North Macedonia",
    "Norway",
    "Oman",
    "Pakistan",
    "Palau",
    "Panama",
    "Papua New Guinea",
    "Paraguay",
    "Peru",
    "Philippines",
    "Poland",
    "Portugal",
    "Qatar",
    "Romania",
    "Russia",
    "Rwanda",
    "Saint Kitts and Nevis",
    "Saint Lucia",
    "Saint Vincent and the Grenadines",
    "Samoa",
    "San Marino",
    "Sao Tome and Principe",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Seychelles",
    "Sierra Leone",
    "Singapore",
    "Slovakia",
    "Slovenia",
    "Solomon Islands",
    "Somalia",
    "South Africa",
    "South Sudan",
    "Spain",
    "Sri Lanka",
    "Sudan",
    "Sudan, South",
    "Suriname",
    "Sweden",
    "Switzerland",
    "Syria",
    "Taiwan",
    "Tajikistan",
    "Tanzania",
    "Thailand",
    "Timor-Leste",
    "Togo",
    "Tonga",
    "Trinidad and Tobago",
    "Tunisia",
    "Turkey",
    "Turkmenistan",
    "Tuvalu",
    "Uganda",
    "Ukraine",
    "United Arab Emirates",
    "United Kingdom",
    "United States",
    "Uruguay",
    "Uzbekistan",
    "Vanuatu",
    "Vatican City",
    "Venezuela",
    "Vietnam",
    "Yemen",
    "Zambia",
    "Zimbabwe",
]
cities = [
    "Abidjan",
    "Abu Dhabi",
    "Abuja",
    "Accra",
    "Addis Ababa",
    "Adelaide",
    "Agra",
    "Ahmedabad",
    "Albuquerque",
    "Alexandria",
    "Algiers",
    "Almaty",
    "Amman",
    "Amsterdam",
    "Ankara",
    "Antananarivo",
    "Apia",
    "Ashgabat",
    "Asmara",
    "Astana",
    "Asunción",
    "Athens",
    "Atlanta",
    "Auckland",
    "Austin",
    "Baghdad",
    "Baku",
    "Baltimore",
    "Bamako",
    "Bandar Seri Begawan",
    "Bangkok",
    "Bangui",
    "Banjul",
    "Barcelona",
    "Barranquilla",
    "Basra",
    "Beijing",
    "Beirut",
    "Belfast",
    "Belgrade",
    "Belize City",
    "Bengaluru",
    "Berlin",
    "Bern",
    "Bishkek",
    "Bissau",
    "Bogotá",
    "Bologna",
    "Bordeaux",
    "Boston",
    "Brasília",
    "Bratislava",
    "Brazzaville",
    "Brisbane",
    "Bristol",
    "Brussels",
    "Bucharest",
    "Budapest",
    "Buenos Aires",
    "Bujumbura",
    "Cairo",
    "Calgary",
    "Cali",
    "Cape Town",
    "Caracas",
    "Cardiff",
    "Casablanca",
    "Chennai",
    "Chicago",
    "Chisinau",
    "Christchurch",
    "Cincinnati",
    "Cleveland",
    "Colombo",
    "Conakry",
    "Copenhagen",
    "Córdoba",
    "Dakar",
    "Dallas",
    "Damascus",
    "Dar es Salaam",
    "Darwin",
    "Davao City",
    "Delhi",
    "Denver",
    "Detroit",
    "Dhaka",
    "Djibouti City",
    "Doha",
    "Douala",
    "Dubai",
    "Dublin",
    "Dushanbe",
    "Edinburgh",
    "Edmonton",
    "Frankfurt",
    "Freetown",
    "Funafuti",
    "Gaborone",
    "Geneva",
    "Georgetown",
    "Glasgow",
    "Guatemala City",
    "Hanoi",
    "Harare",
    "Havana",
    "Helsinki",
    "Hobart",
    "Hong Kong",
    "Honolulu",
    "Houston",
    "Hyderabad",
    "Islamabad",
    "Istanbul",
    "Jacksonville",
    "Jakarta",
    "Jeddah",
    "Jerusalem",
    "Johannesburg",
    "Kabul",
    "Kampala",
    "Kathmandu",
    "Khartoum",
    "Kiev",
    "Kigali",
    "Kingston",
    "Kinshasa",
    "Kuala Lumpur",
    "Kuwait City",
    "La Paz",
    "Lagos",
    "Lahore",
    "Las Vegas",
    "Leeds",
    "Leipzig",
    "Lima",
    "Lisbon",
    "Ljubljana",
    "London",
    "Los Angeles",
    "Louisville",
    "Luanda",
    "Lusaka",
    "Luxembourg City",
    "Macau",
    "Machakos",
    "Madrid",
    "Majuro",
    "Malmö",
    "Managua",
    "Manama",
    "Manila",
    "Maputo",
    "Marrakech",
    "Marseille",
    "Maseru",
    "Mazatlán",
    "Mecca",
    "Medan",
    "Medellín",
    "Melbourne",
    "Memphis",
    "Mendoza",
    "Minsk",
    "Monaco",
    "Monrovia",
    "Montevideo",
    "Montreal",
    "Moscow",
    "Mumbai",
    "Munich",
    "Muscat",
    "Nairobi",
    "Nassau",
    "Naypyidaw",
    "Ndola",
    "New Delhi",
    "New Orleans",
    "New York City",
    "Niamey",
    "Nicosia",
    "Nouakchott",
    "Nukuʻalofa",
    "Osaka",
    "Oslo",
    "Ottawa",
    "Ouagadougou",
    "Palikir",
    "Panama City",
    "Paramaribo",
    "Paris",
    "Perth",
    "Phnom Penh",
    "Phoenix",
    "Podgorica",
    "Port Louis",
    "Port Moresby",
    "Port-au-Prince",
    "Porto",
    "Prague",
    "Praia",
    "Pretoria",
    "Puerto Vallarta",
    "Pyongyang",
    "Quebec City",
    "Quito",
    "Rabat",
    "Rarotonga",
    "Reykjavik",
    "Richmond",
    "Riga",
    "Rio de Janeiro",
    "Riyadh",
    "Rome",
    "Roseau",
    "Sacramento",
    "Saint John's",
    "Salvador",
    "San Diego",
    "San Francisco",
    "San José",
    "San Juan",
    "San Marino",
    "San Salvador",
    "Sana'a",
    "Santiago",
    "Santo Domingo",
    "São Paulo",
    "Sarajevo",
    "Seattle",
    "Seoul",
    "Shanghai",
    "Shenzhen",
    "Singapore",
    "Skopje",
    "Sofia",
    "St. George's",
    "St. Petersburg",
    "Stockholm",
    "Sucre",
    "Suva",
    "Sydney",
    "T'aipei",
    "Tallinn",
    "Tashkent",
    "Tbilisi",
    "Tegucigalpa",
    "Tehran",
    "Tel Aviv",
    "Thimphu",
    "Tirana",
    "Tokyo",
    "Toronto",
    "Tórshavn",
    "Tripoli",
    "Tunis",
    "Ulaanbaatar",
    "Vaduz",
    "Valletta",
    "Vancouver",
    "Varanasi",
    "Venice",
    "Vienna",
    "Vientiane",
    "Vilnius",
    "Warsaw",
    "Washington, D.C.",
    "Wellington",
    "Windhoek",
    "Winnipeg",
    "Yaoundé",
    "Yerevan",
    "Zagreb",
    "Zurich",
]


def infer_region(region):
    """
    Infer the type (country or city) of a given region name.

    This function takes a region name as input and uses fuzzy string matching to determine
    whether the region is more likely to be a country or a city. It returns a tuple
    containing the inferred type and the matched region name.

    :param region: The region name to be inferred (e.g., a country or a city).
    :return: A tuple with two elements:
            - The inferred type ('country' or 'city').
            - The matched region name.
    """
    country = process.extract(region, countries, limit=1)
    city = process.extract(region, cities, limit=1)
    if country[0][1] >= city[0][1]:
        return "country", country[0][0]
    return "city", city[0][0]
