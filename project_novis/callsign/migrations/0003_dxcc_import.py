# Generated by Django 2.1b1 on 2018-06-27 15:20

from django.db import migrations


# Based on http://www.adif.org/308/ADIF_308.htm
DXCC_ENTIRES = [
    {'deleted': False,
     'id': 1,
     'name': 'Canada',
     'numeric_3': '124'},
    {'deleted': True,
     'id': 2,
     'name': 'Abu Ail Is.',
     'numeric_3': "887"},
    {'deleted': False,
     'id': 3,
     'name': 'Afghanistan',
     'numeric_3': '004'},
    {'deleted': False,
     'id': 4,
     'name': 'Agalega & St. Brandon Is.',
     'numeric_3': '028'},
    {'deleted': False,
     'id': 5,
     'name': 'Aland Is.',
     'numeric_3': '246'},
    {'deleted': False,
     'id': 6,
     'name': 'Alaska',
     'numeric_3': '840'},
    {'deleted': False,
     'id': 7,
     'name': 'Albania',
     'numeric_3': '008'},
    {'deleted': True,
     'id': 8,
     'name': 'Aldabra',
     'numeric_3': "690"},
    {'deleted': False,
     'id': 9,
     'name': 'American Samoa',
     'numeric_3': '840'},
    {'deleted': False,
     'id': 10,
     'name': 'Amsterdam & St. Paul Is.',
     'numeric_3': "250"},
    {'deleted': False,
     'id': 11,
     'name': 'Andaman & Nicobar Is.',
     'numeric_3': "356"},
    {'deleted': False,
     'id': 12,
     'name': 'Anguilla',
     'numeric_3': '826'},
    {'deleted': False,
     'id': 13,
     'name': 'Antarctica',
     'numeric_3': '010'},
    {'deleted': False,
     'id': 14,
     'name': 'Armenia',
     'numeric_3': '051'},
    {'deleted': False,
     'id': 15,
     'name': 'Asiatic Russia',
     'numeric_3': "643"},
    {'deleted': False,
     'id': 16,
     'name': 'New Zealand Subantarctic Islands',
     'numeric_3': "554"},
    {'deleted': False,
     'id': 17,
     'name': 'Aves I.',
     'numeric_3': "862"},
    {'deleted': False,
     'id': 18,
     'name': 'Azerbaijan',
     'numeric_3': '031'},
    {'deleted': True,
     'id': 19,
     'name': 'Bajo Nuevo',
     'numeric_3': "170"},
    {'deleted': False,
     'id': 20,
     'name': 'Baker & Howland Is.',
     'numeric_3': '840'},
    {'deleted': False,
     'id': 21,
     'name': 'Balearic Is.',
     'numeric_3': "724"},
    {'deleted': False,
     'id': 22,
     'name': 'Palau',
     'numeric_3': '585'},
    {'deleted': True,
     'id': 23,
     'name': 'Blenheim Reef',
     'numeric_3': "826"},
    {'deleted': False,
     'id': 24,
     'name': 'Bouvet',
     'numeric_3': '578'},
    {'deleted': True,
     'id': 25,
     'name': 'British North Borneo',
     'numeric_3': '458'},
    {'deleted': True,
     'id': 26,
     'name': 'British Somaliland',
     'numeric_3': '826'},
    {'deleted': False,
     'id': 27,
     'name': 'Belarus',
     'numeric_3': '112'},
    {'deleted': True,
     'id': 28,
     'name': 'Canal Zone',
     'numeric_3': '591'},
    {'deleted': False,
     'id': 29,
     'name': 'Canary Is.',
     'numeric_3': "724"},
    {'deleted': True,
     'id': 30,
     'name': 'Celebe & Molucca Is.',
     'numeric_3': '360'},
    {'deleted': False,
     'id': 31,
     'name': 'C. Kiribati (British Phoenix Is.)',
     'numeric_3': "296"},
    {'deleted': False,
     'id': 32,
     'name': 'Ceuta & Melilla',
     'numeric_3': "724"},
    {'deleted': False,
     'id': 33,
     'name': 'Chagos Is.',
     'numeric_3': "826"},
    {'deleted': False,
     'id': 34,
     'name': 'Chatham Is.',
     'numeric_3': "554"},
    {'deleted': False,
     'id': 35,
     'name': 'Christmas I.',
     'numeric_3': '036'},
    {'deleted': False,
     'id': 36,
     'name': 'Clipperton I.',
     'numeric_3': '250'},
    {'deleted': False,
     'id': 37,
     'name': 'Cocos I.',
     'numeric_3': "036"},
    {'deleted': False,
     'id': 38,
     'name': 'Cocos (Keeling) Is.',
     'numeric_3': '036'},
    {'deleted': True,
     'id': 39,
     'name': 'Comoros',
     'numeric_3': "174"},
    {'deleted': False,
     'id': 40,
     'name': 'Crete',
     'numeric_3': "300"},
    {'deleted': False,
     'id': 41,
     'name': 'Crozet I.',
     'numeric_3': "250"},
    {'deleted': True,
     'id': 42,
     'name': 'Damao, Diu',
     'numeric_3': "356"},
    {'deleted': False,
     'id': 43,
     'name': 'Desecheo I.',
     'numeric_3': "840"},
    {'deleted': True,
     'id': 44,
     'name': 'Desroches',
     'numeric_3': "690"},
    {'deleted': False,
     'id': 45,
     'name': 'Dodecanese',
     'numeric_3': "300"},
    {'deleted': False,
     'id': 46,
     'name': 'East Malaysia',
     'numeric_3': "458"},
    {'deleted': False,
     'id': 47,
     'name': 'Easter I.',
     'numeric_3': "152"},
    {'deleted': False,
     'id': 48,
     'name': 'E. Kiribati (Line Is.)',
     'numeric_3': '296'},
    {'deleted': False,
     'id': 49,
     'name': 'Equatorial Guinea',
     'numeric_3': '226'},
    {'deleted': False,
     'id': 50,
     'name': 'Mexico',
     'numeric_3': '484'},
    {'deleted': False,
     'id': 51,
     'name': 'Eritrea',
     'numeric_3': '232'},
    {'deleted': False,
     'id': 52,
     'name': 'Estonia',
     'numeric_3': '233'},
    {'deleted': False,
     'id': 53,
     'name': 'Ethiopia',
     'numeric_3': '231'},
    {'deleted': False,
     'id': 54,
     'name': 'European Russia',
     'numeric_3': '643'},
    {'deleted': True,
     'id': 55,
     'name': 'Farquhar',
     'numeric_3': '690'},
    {'deleted': False,
     'id': 56,
     'name': 'Fernando De Noronha',
     'numeric_3': '076'},
    {'deleted': True,
     'id': 57,
     'name': 'French Equatorial Africa',
     'numeric_3': '250'},
    {'deleted': True,
     'id': 58,
     'name': 'French Indo-China',
     'numeric_3': '250'},
    {'deleted': True,
     'id': 59,
     'name': 'French West Africa',
     'numeric_3': '250'},
    {'deleted': False,
     'id': 60,
     'name': 'Bahamas',
     'numeric_3': '044'},
    {'deleted': False,
     'id': 61,
     'name': 'Franz Josef Land',
     'numeric_3': '643'},
    {'deleted': False,
     'id': 62,
     'name': 'Barbados',
     'numeric_3': '052'},
    {'deleted': False,
     'id': 63,
     'name': 'French Guiana',
     'numeric_3': '250'},
    {'deleted': False,
     'id': 64,
     'name': 'Bermuda',
     'numeric_3': '826'},
    {'deleted': False,
     'id': 65,
     'name': 'British Virgin Is.',
     'numeric_3': '826'},
    {'deleted': False,
     'id': 66,
     'name': 'Belize',
     'numeric_3': '084'},
    {'deleted': True,
     'id': 67,
     'name': 'French India',
     'numeric_3': "356"},
    {'deleted': True,
     'id': 68,
     'name': 'Kuwait/saudi Arabia Neutral Zone',
     'numeric_3': '414'},
    {'deleted': False,
     'id': 69,
     'name': 'Cayman Is.',
     'numeric_3': '826'},
    {'deleted': False,
     'id': 70,
     'name': 'Cuba',
     'numeric_3': '192'},
    {'deleted': False,
     'id': 71,
     'name': 'Galapagos Is.',
     'numeric_3': '218'},
    {'deleted': False,
     'id': 72,
     'name': 'Dominican Republic',
     'numeric_3': '214'},
    {'deleted': False,
     'id': 74,
     'name': 'El Salvador',
     'numeric_3': '222'},
    {'deleted': False,
     'id': 75,
     'name': 'Georgia',
     'numeric_3': '268'},
    {'deleted': False,
     'id': 76,
     'name': 'Guatemala',
     'numeric_3': '320'},
    {'deleted': False,
     'id': 77,
     'name': 'Grenada',
     'numeric_3': '308'},
    {'deleted': False,
     'id': 78,
     'name': 'Haiti',
     'numeric_3': '332'},
    {'deleted': False,
     'id': 79,
     'name': 'Guadeloupe',
     'numeric_3': '250'},
    {'deleted': False,
     'id': 80,
     'name': 'Honduras',
     'numeric_3': '340'},
    {'deleted': True,
     'id': 81,
     'name': 'Germany',
     'numeric_3': '276'},
    {'deleted': False,
     'id': 82,
     'name': 'Jamaica',
     'numeric_3': '388'},
    {'deleted': False,
     'id': 84,
     'name': 'Martinique',
     'numeric_3': '250'},
    {'deleted': True,
     'id': 85,
     'name': 'Bonaire, Curacao',
     'numeric_3': '528'},
    {'deleted': False,
     'id': 86,
     'name': 'Nicaragua',
     'numeric_3': '558'},
    {'deleted': False,
     'id': 88,
     'name': 'Panama',
     'numeric_3': '591'},
    {'deleted': False,
     'id': 89,
     'name': 'Turks & Caicos Is.',
     'numeric_3': '826'},
    {'deleted': False,
     'id': 90,
     'name': 'Trinidad & Tobago',
     'numeric_3': '780'},
    {'deleted': False,
     'id': 91,
     'name': 'Aruba',
     'numeric_3': '528'},
    {'deleted': True,
     'id': 93,
     'name': 'Geyser Reef',
     'numeric_3': '250'},
    {'deleted': False,
     'id': 94,
     'name': 'Antigua & Barbuda',
     'numeric_3': '028'},
    {'deleted': False,
     'id': 95,
     'name': 'Dominica',
     'numeric_3': '212'},
    {'deleted': False,
     'id': 96,
     'name': 'Montserrat',
     'numeric_3': '826'},
    {'deleted': False,
     'id': 97,
     'name': 'St. Lucia',
     'numeric_3': '826'},
    {'deleted': False,
     'id': 98,
     'name': 'St. Vincent',
     'numeric_3': '670'},
    {'deleted': False,
     'id': 99,
     'name': 'Glorioso Is.',
     'numeric_3': '250'},
    {'deleted': False,
     'id': 100,
     'name': 'Argentina',
     'numeric_3': '032'},
    {'deleted': True,
     'id': 101,
     'name': 'Goa',
     'numeric_3': '356'},
    {'deleted': True,
     'id': 102,
     'name': 'Gold Coast, Togoland',
     'numeric_3': '826'},
    {'deleted': False,
     'id': 103,
     'name': 'Guam',
     'numeric_3': '840'},
    {'deleted': False,
     'id': 104,
     'name': 'Bolivia',
     'numeric_3': '068'},
    {'deleted': False,
     'id': 105,
     'name': 'Guantanamo Bay',
     'numeric_3': '192'},
    {'deleted': False,
     'id': 106,
     'name': 'Guernsey',
     'numeric_3': '831'},
    {'deleted': False,
     'id': 107,
     'name': 'Guinea',
     'numeric_3': '324'},
    {'deleted': False,
     'id': 108,
     'name': 'Brazil',
     'numeric_3': '076'},
    {'deleted': False,
     'id': 109,
     'name': 'Guinea-Bissau',
     'numeric_3': '624'},
    {'deleted': False,
     'id': 110,
     'name': 'Hawaii',
     'numeric_3': '840'},
    {'deleted': False,
     'id': 111,
     'name': 'Heard I.',
     'numeric_3': '036'},
    {'deleted': False,
     'id': 112,
     'name': 'Chile',
     'numeric_3': '152'},
    {'deleted': True,
     'id': 113,
     'name': 'Ifni',
     'numeric_3': '504'},
    {'deleted': False,
     'id': 114,
     'name': 'Isle of Man',
     'numeric_3': '826'},
    {'deleted': True,
     'id': 115,
     'name': 'Italian Somaliland',
     'numeric_3': '706'},
    {'deleted': False,
     'id': 116,
     'name': 'Colombia',
     'numeric_3': '170'},
    {'deleted': False,
     'id': 117,
     'name': 'Itu Hq',
     # None ok
     'numeric_3': None},
    {'deleted': False,
     'id': 118,
     'name': 'Jan Mayen',
     'numeric_3': '578'},
    {'deleted': True,
     'id': 119,
     'name': 'Java',
     'numeric_3': '360'},
    {'deleted': False,
     'id': 120,
     'name': 'Ecuador',
     'numeric_3': '218'},
    {'deleted': False,
     'id': 122,
     'name': 'Jersey',
     'numeric_3': '826'},
    {'deleted': False,
     'id': 123,
     'name': 'Johnston I.',
     'numeric_3': '840'},
    {'deleted': False,
     'id': 124,
     'name': 'Juan De Nova, Europa',
     'numeric_3': '250'},
    {'deleted': False,
     'id': 125,
     'name': 'Juan Fernandez Is.',
     'numeric_3': '152'},
    {'deleted': False,
     'id': 126,
     'name': 'Kaliningrad',
     'numeric_3': '643'},
    {'deleted': True,
     'id': 127,
     'name': 'Kamaran Is.',
     'numeric_3': '887'},
    {'deleted': True,
     'id': 128,
     'name': 'Karelo-Finnish Republic',
     'numeric_3': '643'},
    {'deleted': False,
     'id': 129,
     'name': 'Guyana',
     'numeric_3': '328'},
    {'deleted': False,
     'id': 130,
     'name': 'Kazakhstan',
     'numeric_3': '398'},
    {'deleted': False,
     'id': 131,
     'name': 'Kerguelen Is.',
     'numeric_3': '250'},
    {'deleted': False,
     'id': 132,
     'name': 'Paraguay',
     'numeric_3': '600'},
    {'deleted': False,
     'id': 133,
     'name': 'Kermadec Is.',
     'numeric_3': '554'},
    {'deleted': True,
     'id': 134,
     'name': 'Kingman Reef',
     'numeric_3': '840'},
    {'deleted': False,
     'id': 135,
     'name': 'Kyrgyzstan',
     'numeric_3': '417'},
    {'deleted': False,
     'id': 136,
     'name': 'Peru',
     'numeric_3': '604'},
    {'deleted': False,
     'id': 137,
     'name': 'Republic of Korea',
     'numeric_3': '410'},
    {'deleted': False,
     'id': 138,
     'name': 'Kure I.',
     'numeric_3': '840'},
    {'deleted': True,
     'id': 139,
     'name': 'Kuria Muria I.',
     'numeric_3': '512'},
    {'deleted': False,
     'id': 140,
     'name': 'Suriname',
     'numeric_3': '740'},
    {'deleted': False,
     'id': 141,
     'name': 'Falkland Is.',
     'numeric_3': '826'},
    {'deleted': False,
     'id': 142,
     'name': 'Lakshadweep Is.',
     'numeric_3': '356'},
    {'deleted': False,
     'id': 143,
     'name': 'Laos',
     'numeric_3': '418'},
    {'deleted': False,
     'id': 144,
     'name': 'Uruguay',
     'numeric_3': '858'},
    {'deleted': False,
     'id': 145,
     'name': 'Latvia',
     'numeric_3': '428'},
    {'deleted': False,
     'id': 146,
     'name': 'Lithuania',
     'numeric_3': '440'},
    {'deleted': False,
     'id': 147,
     'name': 'Lord Howe I.',
     'numeric_3': '036'},
    {'deleted': False,
     'id': 148,
     'name': 'Venezuela',
     'numeric_3': '862'},
    {'deleted': False,
     'id': 149,
     'name': 'Azores',
     'numeric_3': '620'},
    {'deleted': False,
     'id': 150,
     'name': 'Australia',
     'numeric_3': '036'},
    {'deleted': True,
     'id': 151,
     'name': 'Malyj Vysotskij I.',
     'numeric_3': '643'},
    {'deleted': False,
     'id': 152,
     'name': 'Macao',
     'numeric_3': '156'},
    {'deleted': False,
     'id': 153,
     'name': 'Macquarie I.',
     'numeric_3': '036'},
    {'deleted': True,
     'id': 154,
     'name': 'Yemen Arab Republic',
     'numeric_3': '887'},
    {'deleted': True,
     'id': 155,
     'name': 'Malaya',
     'numeric_3': '458'},
    {'deleted': False,
     'id': 157,
     'name': 'Nauru',
     'numeric_3': '520'},
    {'deleted': False,
     'id': 158,
     'name': 'Vanuatu',
     'numeric_3': '548'},
    {'deleted': False,
     'id': 159,
     'name': 'Maldives',
     'numeric_3': '462'},
    {'deleted': False,
     'id': 160,
     'name': 'Tonga',
     'numeric_3': '776'},
    {'deleted': False,
     'id': 161,
     'name': 'Malpelo I.',
     'numeric_3': '170'},
    {'deleted': False,
     'id': 162,
     'name': 'New Caledonia',
     'numeric_3': '250'},
    {'deleted': False,
     'id': 163,
     'name': 'Papua New Guinea',
     'numeric_3': '598'},
    {'deleted': True,
     'id': 164,
     'name': 'Manchuria',
     'numeric_3': '156'},
    {'deleted': False,
     'id': 165,
     'name': 'Mauritius',
     'numeric_3': '480'},
    {'deleted': False,
     'id': 166,
     'name': 'Mariana Is.',
     'numeric_3': '840'},
    {'deleted': False,
     'id': 167,
     'name': 'Market Reef',
     'numeric_3': '246'},
    {'deleted': False,
     'id': 168,
     'name': 'Marshall Is.',
     'numeric_3': '584'},
    {'deleted': False,
     'id': 169,
     'name': 'Mayotte',
     'numeric_3': '250'},
    {'deleted': False,
     'id': 170,
     'name': 'New Zealand',
     'numeric_3': '554'},
    {'deleted': False,
     'id': 171,
     'name': 'Mellish Reef',
     'numeric_3': '036'},
    {'deleted': False,
     'id': 172,
     'name': 'Pitcairn I.',
     'numeric_3': '826'},
    {'deleted': False,
     'id': 173,
     'name': 'Micronesia',
     'numeric_3': '583'},
    {'deleted': False,
     'id': 174,
     'name': 'Midway I.',
     'numeric_3': '840'},
    {'deleted': False,
     'id': 175,
     'name': 'French Polynesia',
     'numeric_3': '250'},
    {'deleted': False,
     'id': 176,
     'name': 'Fiji',
     'numeric_3': '242'},
    {'deleted': False,
     'id': 177,
     'name': 'Minami Torishima',
     'numeric_3': '392'},
    {'deleted': True,
     'id': 178,
     'name': 'Minerva Reef',
     'numeric_3': '776'},
    {'deleted': False,
     'id': 179,
     'name': 'Moldova',
     'numeric_3': '498'},
    {'deleted': False,
     'id': 180,
     'name': 'Mount Athos',
     'numeric_3': '300'},
    {'deleted': False,
     'id': 181,
     'name': 'Mozambique',
     'numeric_3': '508'},
    {'deleted': False,
     'id': 182,
     'name': 'Navassa I.',
     'numeric_3': '840'},
    {'deleted': True,
     'id': 183,
     'name': 'Netherlands Borneo',
     'numeric_3': '360'},
    {'deleted': True,
     'id': 184,
     'name': 'Netherlands New Guinea',
     'numeric_3': '360'},
    {'deleted': False,
     'id': 185,
     'name': 'Solomon Is.',
     'numeric_3': '090'},
    {'deleted': True,
     'id': 186,
     'name': 'Newfoundland, Labrador',
     'numeric_3': '124'},
    {'deleted': False,
     'id': 187,
     'name': 'Niger',
     'numeric_3': '562'},
    {'deleted': False,
     'id': 188,
     'name': 'Niue',
     'numeric_3': '570'},
    {'deleted': False,
     'id': 189,
     'name': 'Norfolk I.',
     'numeric_3': '036'},
    {'deleted': False,
     'id': 190,
     'name': 'Samoa',
     'numeric_3': '882'},
    {'deleted': False,
     'id': 191,
     'name': 'North Cook Is.',
     'numeric_3': '554'},
    {'deleted': False,
     'id': 192,
     'name': 'Ogasawara',
     'numeric_3': '392'},
    {'deleted': True,
     'id': 193,
     'name': 'Okinawa (Ryukyu Is.)',
     'numeric_3': '392'},
    {'deleted': True,
     'id': 194,
     'name': 'Okino Tori-Shima',
     'numeric_3': '392'},
    {'deleted': False,
     'id': 195,
     'name': 'Annobon I.',
     'numeric_3': '226'},
    {'deleted': True,
     'id': 196,
     'name': 'Palestine',
     'numeric_3': '840'},
    {'deleted': False,
     'id': 197,
     'name': 'Palmyra & Jarvis Is.',
     'numeric_3': '840'},
    {'deleted': True,
     'id': 198,
     'name': 'Papua Territory',
     'numeric_3': '598'},
    {'deleted': False,
     'id': 199,
     'name': 'Peter 1 I.',
     # None okay
     'numeric_3': None},
    {'deleted': True,
     'id': 200,
     'name': 'Portuguese Timor',
     'numeric_3': '626'},
    {'deleted': False,
     'id': 201,
     'name': 'Prince Edward & Marion Is.',
     'numeric_3': '710'},
    {'deleted': False,
     'id': 202,
     'name': 'Puerto Rico',
     'numeric_3': '840'},
    {'deleted': False,
     'id': 203,
     'name': 'Andorra',
     'numeric_3': '020'},
    {'deleted': False,
     'id': 204,
     'name': 'Revillagigedo',
     'numeric_3': '484'},
    {'deleted': False,
     'id': 205,
     'name': 'Ascension I.',
     'numeric_3': '826'},
    {'deleted': False,
     'id': 206,
     'name': 'Austria',
     'numeric_3': '040'},
    {'deleted': False,
     'id': 207,
     'name': 'Rodriguez I.',
     'numeric_3': '480'},
    {'deleted': True,
     'id': 208,
     'name': 'Ruanda-Urundi',
     # None okay
     'numeric_3': None},
    {'deleted': False,
     'id': 209,
     'name': 'Belgium',
     'numeric_3': '056'},
    {'deleted': True,
     'id': 210,
     'name': 'Saar',
     'numeric_3': '276'},
    {'deleted': False,
     'id': 211,
     'name': 'Sable I.',
     'numeric_3': '124'},
    {'deleted': False,
     'id': 212,
     'name': 'Bulgaria',
     'numeric_3': '100'},
    {'deleted': False,
     'id': 213,
     'name': 'Saint Martin',
     'numeric_3': '250'},
    {'deleted': False,
     'id': 214,
     'name': 'Corsica',
     'numeric_3': '250'},
    {'deleted': False,
     'id': 215,
     'name': 'Cyprus',
     'numeric_3': '196'},
    {'deleted': False,
     'id': 216,
     'name': 'San Andres & Providencia',
     'numeric_3': '170'},
    {'deleted': False,
     'id': 217,
     'name': 'San Felix & San Ambrosio',
     'numeric_3': '152'},
    {'deleted': True,
     'id': 218,
     'name': 'Czechoslovakia',
     'numeric_3': '203'},
    {'deleted': False,
     'id': 219,
     'name': 'Sao Tome & Principe',
     'numeric_3': '678'},
    {'deleted': True,
     'id': 220,
     'name': 'Sarawak',
     'numeric_3': '458'},
    {'deleted': False,
     'id': 221,
     'name': 'Denmark',
     'numeric_3': '208'},
    {'deleted': False,
     'id': 222,
     'name': 'Faroe Is.',
     'numeric_3': '208'},
    {'deleted': False,
     'id': 223,
     'name': 'England',
     'numeric_3': '826'},
    {'deleted': False,
     'id': 224,
     'name': 'Finland',
     'numeric_3': '246'},
    {'deleted': False,
     'id': 225,
     'name': 'Sardinia',
     'numeric_3': '380'},
    {'deleted': True,
     'id': 226,
     'name': 'Saudi Arabia/iraq Neutral Zone',
     # None okay
     'numeric_3': None},
    {'deleted': False,
     'id': 227,
     'name': 'France',
     'numeric_3': '250'},
    {'deleted': True,
     'id': 228,
     'name': 'Serrana Bank & Roncador Cay',
     'numeric_3': '170'},
    {'deleted': True,
     'id': 229,
     'name': 'German Democratic Republic',
     'numeric_3': '276'},
    {'deleted': False,
     'id': 230,
     'name': 'Federal Republic of Germany',
     'numeric_3': '276'},
    {'deleted': True,
     'id': 231,
     'name': 'Sikkim',
     'numeric_3': '356'},
    {'deleted': False,
     'id': 232,
     'name': 'Somalia',
     'numeric_3': '706'},
    {'deleted': False,
     'id': 233,
     'name': 'Gibraltar',
     'numeric_3': '826'},
    {'deleted': False,
     'id': 234,
     'name': 'South Cook Is.',
     'numeric_3': '554'},
    {'deleted': False,
     'id': 235,
     'name': 'South Georgia I.',
     'numeric_3': '826'},
    {'deleted': False,
     'id': 236,
     'name': 'Greece',
     'numeric_3': '300'},
    {'deleted': False,
     'id': 237,
     'name': 'Greenland',
     'numeric_3': '208'},
    {'deleted': False,
     'id': 238,
     'name': 'South Orkney Is.',
     'numeric_3': '010'},
    {'deleted': False,
     'id': 239,
     'name': 'Hungary',
     'numeric_3': '348'},
    {'deleted': False,
     'id': 240,
     'name': 'South Sandwich Is.',
     'numeric_3': '826'},
    {'deleted': False,
     'id': 241,
     'name': 'South Shetland Is.',
     'numeric_3': '010'},
    {'deleted': False,
     'id': 242,
     'name': 'Iceland',
     'numeric_3': '352'},
    {'deleted': True,
     'id': 243,
     'name': "People's Democratic Rep. of Yemen",
     'numeric_3': '887'},
    {'deleted': True,
     'id': 244,
     'name': 'Southern Sudan',
     'numeric_3': '728'},
    {'deleted': False,
     'id': 245,
     'name': 'Ireland',
     'numeric_3': '372'},
    {'deleted': False,
     'id': 246,
     'name': 'Sovereign Military Order of Malta',
     # None okay
     'numeric_3': None},
    {'deleted': False,
     'id': 247,
     'name': 'Spratly Is.',
     # None okay
     'numeric_3': None},
    {'deleted': False,
     'id': 248,
     'name': 'Italy',
     'numeric_3': '380'},
    {'deleted': False,
     'id': 249,
     'name': 'St. Kitts & Nevis',
     'numeric_3': '659'},
    {'deleted': False,
     'id': 250,
     'name': 'St. Helena',
     'numeric_3': '826'},
    {'deleted': False,
     'id': 251,
     'name': 'Liechtenstein',
     'numeric_3': '438'},
    {'deleted': False,
     'id': 252,
     'name': 'St. Paul I.',
     'numeric_3': '840'},
    {'deleted': False,
     'id': 253,
     'name': 'St. Peter & St. Paul Rocks',
     'numeric_3': '076'},
    {'deleted': False,
     'id': 254,
     'name': 'Luxembourg',
     'numeric_3': '442'},
    {'deleted': True,
     'id': 255,
     'name': 'St. Maarten, Saba, St. Eustatius',
     'numeric_3': '528'},
    {'deleted': False,
     'id': 256,
     'name': 'Madeira Is.',
     'numeric_3': '620'},
    {'deleted': False,
     'id': 257,
     'name': 'Malta',
     'numeric_3': '470'},
    {'deleted': True,
     'id': 258,
     'name': 'Sumatra',
     'numeric_3': '360'},
    {'deleted': False,
     'id': 259,
     'name': 'Svalbard',
     'numeric_3': '578'},
    {'deleted': False,
     'id': 260,
     'name': 'Monaco',
     'numeric_3': '492'},
    {'deleted': True,
     'id': 261,
     'name': 'Swan Is.',
     'numeric_3': '840'},
    {'deleted': False,
     'id': 262,
     'name': 'Tajikistan',
     'numeric_3': '762'},
    {'deleted': False,
     'id': 263,
     'name': 'Netherlands',
     'numeric_3': '528'},
    {'deleted': True,
     'id': 264,
     'name': 'Tangier',
     'numeric_3': '504'},
    {'deleted': False,
     'id': 265,
     'name': 'Northern Ireland',
     'numeric_3': '826'},
    {'deleted': False,
     'id': 266,
     'name': 'Norway',
     'numeric_3': '578'},
    {'deleted': True,
     'id': 267,
     'name': 'Territory of New Guinea',
     'numeric_3': '598'},
    {'deleted': True,
     'id': 268,
     'name': 'Tibet',
     'numeric_3': '156'},
    {'deleted': False,
     'id': 269,
     'name': 'Poland',
     'numeric_3': '616'},
    {'deleted': False,
     'id': 270,
     'name': 'Tokelau Is.',
     'numeric_3': '554'},
    {'deleted': True,
     'id': 271,
     'name': 'Trieste',
     'numeric_3': '380'},
    {'deleted': False,
     'id': 272,
     'name': 'Portugal',
     'numeric_3': '620'},
    {'deleted': False,
     'id': 273,
     'name': 'Trindade & Martim Vaz Is.',
     'numeric_3': '076'},
    {'deleted': False,
     'id': 274,
     'name': 'Tristan Da Cunha & Gough I.',
     'numeric_3': '826'},
    {'deleted': False,
     'id': 275,
     'name': 'Romania',
     'numeric_3': '642'},
    {'deleted': False,
     'id': 276,
     'name': 'Tromelin I.',
     'numeric_3': '250'},
    {'deleted': False,
     'id': 277,
     'name': 'St. Pierre & Miquelon',
     'numeric_3': '250'},
    {'deleted': False,
     'id': 278,
     'name': 'San Marino',
     'numeric_3': '674'},
    {'deleted': False,
     'id': 279,
     'name': 'Scotland',
     'numeric_3': '826'},
    {'deleted': False,
     'id': 280,
     'name': 'Turkmenistan',
     'numeric_3': '795'},
    {'deleted': False,
     'id': 281,
     'name': 'Spain',
     'numeric_3': '724'},
    {'deleted': False,
     'id': 282,
     'name': 'Tuvalu',
     'numeric_3': '798'},
    {'deleted': False,
     'id': 283,
     'name': 'Uk Sovereign Base Areas On Cyprus',
     'numeric_3': '826'},
    {'deleted': False,
     'id': 284,
     'name': 'Sweden',
     'numeric_3': '752'},
    {'deleted': False,
     'id': 285,
     'name': 'Virgin Is.',
     'numeric_3': '840'},
    {'deleted': False,
     'id': 286,
     'name': 'Uganda',
     'numeric_3': '800'},
    {'deleted': False,
     'id': 287,
     'name': 'Switzerland',
     'numeric_3': '756'},
    {'deleted': False,
     'id': 288,
     'name': 'Ukraine',
     'numeric_3': '804'},
    {'deleted': False,
     'id': 289,
     'name': 'United Nations Hq',
     # None okay
     'numeric_3': None},
    {'deleted': False,
     'id': 291,
     'name': 'United States of America',
     'numeric_3': '840'},
    {'deleted': False,
     'id': 292,
     'name': 'Uzbekistan',
     'numeric_3': '860'},
    {'deleted': False,
     'id': 293,
     'name': 'Viet Nam',
     'numeric_3': '704'},
    {'deleted': False,
     'id': 294,
     'name': 'Wales',
     'numeric_3': '826'},
    {'deleted': False,
     'id': 295,
     'name': 'Vatican',
     'numeric_3': '336'},
    {'deleted': False,
     'id': 296,
     'name': 'Serbia',
     'numeric_3': '688'},
    {'deleted': False,
     'id': 297,
     'name': 'Wake I.',
     'numeric_3': '840'},
    {'deleted': False,
     'id': 298,
     'name': 'Wallis & Futuna Is.',
     'numeric_3': '250'},
    {'deleted': False,
     'id': 299,
     'name': 'West Malaysia',
     'numeric_3': '458'},
    {'deleted': False,
     'id': 301,
     'name': 'W. Kiribati (Gilbert Is. )',
     'numeric_3': '296'},
    {'deleted': False,
     'id': 302,
     'name': 'Western Sahara',
     'numeric_3': '504'},
    {'deleted': False,
     'id': 303,
     'name': 'Willis I.',
     'numeric_3': '036'},
    {'deleted': False,
     'id': 304,
     'name': 'Bahrain',
     'numeric_3': '048'},
    {'deleted': False,
     'id': 305,
     'name': 'Bangladesh',
     'numeric_3': '050'},
    {'deleted': False,
     'id': 306,
     'name': 'Bhutan',
     'numeric_3': '064'},
    {'deleted': True,
     'id': 307,
     'name': 'Zanzibar',
     'numeric_3': '834'},
    {'deleted': False,
     'id': 308,
     'name': 'Costa Rica',
     'numeric_3': '188'},
    {'deleted': False,
     'id': 309,
     'name': 'Myanmar',
     'numeric_3': '104'},
    {'deleted': False,
     'id': 312,
     'name': 'Cambodia',
     'numeric_3': '116'},
    {'deleted': False,
     'id': 315,
     'name': 'Sri Lanka',
     'numeric_3': '144'},
    {'deleted': False,
     'id': 318,
     'name': 'China',
     'numeric_3': '156'},
    {'deleted': False,
     'id': 321,
     'name': 'Hong Kong',
     'numeric_3': '156'},
    {'deleted': False,
     'id': 324,
     'name': 'India',
     'numeric_3': '356'},
    {'deleted': False,
     'id': 327,
     'name': 'Indonesia',
     'numeric_3': '360'},
    {'deleted': False,
     'id': 330,
     'name': 'Iran',
     'numeric_3': '364'},
    {'deleted': False,
     'id': 333,
     'name': 'Iraq',
     'numeric_3': '368'},
    {'deleted': False,
     'id': 336,
     'name': 'Israel',
     'numeric_3': '376'},
    {'deleted': False,
     'id': 339,
     'name': 'Japan',
     'numeric_3': '392'},
    {'deleted': False,
     'id': 342,
     'name': 'Jordan',
     'numeric_3': '400'},
    {'deleted': False,
     'id': 344,
     'name': "Democratic People's Rep. of Korea",
     'numeric_3': '408'},
    {'deleted': False,
     'id': 345,
     'name': 'Brunei Darussalam',
     'numeric_3': '096'},
    {'deleted': False,
     'id': 348,
     'name': 'Kuwait',
     'numeric_3': '414'},
    {'deleted': False,
     'id': 354,
     'name': 'Lebanon',
     'numeric_3': '422'},
    {'deleted': False,
     'id': 363,
     'name': 'Mongolia',
     'numeric_3': '496'},
    {'deleted': False,
     'id': 369,
     'name': 'Nepal',
     'numeric_3': '524'},
    {'deleted': False,
     'id': 370,
     'name': 'Oman',
     'numeric_3': '512'},
    {'deleted': False,
     'id': 372,
     'name': 'Pakistan',
     'numeric_3': '586'},
    {'deleted': False,
     'id': 375,
     'name': 'Philippines',
     'numeric_3': '608'},
    {'deleted': False,
     'id': 376,
     'name': 'Qatar',
     'numeric_3': '634'},
    {'deleted': False,
     'id': 378,
     'name': 'Saudi Arabia',
     'numeric_3': '682'},
    {'deleted': False,
     'id': 379,
     'name': 'Seychelles',
     'numeric_3': '690'},
    {'deleted': False,
     'id': 381,
     'name': 'Singapore',
     'numeric_3': '702'},
    {'deleted': False,
     'id': 382,
     'name': 'Djibouti',
     'numeric_3': '262'},
    {'deleted': False,
     'id': 384,
     'name': 'Syria',
     'numeric_3': '760'},
    {'deleted': False,
     'id': 386,
     'name': 'Taiwan',
     'numeric_3': '158'},
    {'deleted': False,
     'id': 387,
     'name': 'Thailand',
     'numeric_3': '764'},
    {'deleted': False,
     'id': 390,
     'name': 'Turkey',
     'numeric_3': '792'},
    {'deleted': False,
     'id': 391,
     'name': 'United Arab Emirates',
     'numeric_3': '784'},
    {'deleted': False,
     'id': 400,
     'name': 'Algeria',
     'numeric_3': '012'},
    {'deleted': False,
     'id': 401,
     'name': 'Angola',
     'numeric_3': '024'},
    {'deleted': False,
     'id': 402,
     'name': 'Botswana',
     'numeric_3': '072'},
    {'deleted': False,
     'id': 404,
     'name': 'Burundi',
     'numeric_3': '108'},
    {'deleted': False,
     'id': 406,
     'name': 'Cameroon',
     'numeric_3': '120'},
    {'deleted': False,
     'id': 408,
     'name': 'Central Africa',
     'numeric_3': '140'},
    {'deleted': False,
     'id': 409,
     'name': 'Cape Verde',
     'numeric_3': '132'},
    {'deleted': False,
     'id': 410,
     'name': 'Chad',
     'numeric_3': '148'},
    {'deleted': False,
     'id': 411,
     'name': 'Comoros',
     'numeric_3': '174'},
    {'deleted': False,
     'id': 412,
     'name': 'Republic of the Congo',
     'numeric_3': '178'},
    {'deleted': False,
     'id': 414,
     'name': 'Democratic Republic of the Congo',
     'numeric_3': '180'},
    {'deleted': False,
     'id': 416,
     'name': 'Benin',
     'numeric_3': '204'},
    {'deleted': False,
     'id': 420,
     'name': 'Gabon',
     'numeric_3': '266'},
    {'deleted': False,
     'id': 422,
     'name': 'the Gambia',
     'numeric_3': '270'},
    {'deleted': False,
     'id': 424,
     'name': 'Ghana',
     'numeric_3': '288'},
    {'deleted': False,
     'id': 428,
     'name': "Cote D'ivoire",
     'numeric_3': '384'},
    {'deleted': False,
     'id': 430,
     'name': 'Kenya',
     'numeric_3': '404'},
    {'deleted': False,
     'id': 432,
     'name': 'Lesotho',
     'numeric_3': '426'},
    {'deleted': False,
     'id': 434,
     'name': 'Liberia',
     'numeric_3': '430'},
    {'deleted': False,
     'id': 436,
     'name': 'Libya',
     'numeric_3': '434'},
    {'deleted': False,
     'id': 438,
     'name': 'Madagascar',
     'numeric_3': '450'},
    {'deleted': False,
     'id': 440,
     'name': 'Malawi',
     'numeric_3': '454'},
    {'deleted': False,
     'id': 442,
     'name': 'Mali',
     'numeric_3': '466'},
    {'deleted': False,
     'id': 444,
     'name': 'Mauritania',
     'numeric_3': '478'},
    {'deleted': False,
     'id': 446,
     'name': 'Morocco',
     'numeric_3': '504'},
    {'deleted': False,
     'id': 450,
     'name': 'Nigeria',
     'numeric_3': '566'},
    {'deleted': False,
     'id': 452,
     'name': 'Zimbabwe',
     'numeric_3': '716'},
    {'deleted': False,
     'id': 453,
     'name': 'Reunion I.',
     'numeric_3': '250'},
    {'deleted': False,
     'id': 454,
     'name': 'Rwanda',
     'numeric_3': '646'},
    {'deleted': False,
     'id': 456,
     'name': 'Senegal',
     'numeric_3': '686'},
    {'deleted': False,
     'id': 458,
     'name': 'Sierra Leone',
     'numeric_3': '694'},
    {'deleted': False,
     'id': 460,
     'name': 'Rotuma I.',
     'numeric_3': '242'},
    {'deleted': False,
     'id': 462,
     'name': 'South Africa',
     'numeric_3': '710'},
    {'deleted': False,
     'id': 464,
     'name': 'Namibia',
     'numeric_3': '516'},
    {'deleted': False,
     'id': 466,
     'name': 'Sudan',
     'numeric_3': '729'},
    {'deleted': False,
     'id': 468,
     'name': 'Swaziland',
     'numeric_3': '748'},
    {'deleted': False,
     'id': 470,
     'name': 'Tanzania',
     'numeric_3': '834'},
    {'deleted': False,
     'id': 474,
     'name': 'Tunisia',
     'numeric_3': '788'},
    {'deleted': False,
     'id': 478,
     'name': 'Egypt',
     'numeric_3': '818'},
    {'deleted': False,
     'id': 480,
     'name': 'Burkina Faso',
     'numeric_3': '854'},
    {'deleted': False,
     'id': 482,
     'name': 'Zambia',
     'numeric_3': '894'},
    {'deleted': False,
     'id': 483,
     'name': 'Togo',
     'numeric_3': '768'},
    {'deleted': True,
     'id': 488,
     'name': 'Walvis Bay',
     'numeric_3': "516"},
    {'deleted': False,
     'id': 489,
     'name': 'Conway Reef',
     'numeric_3': "242"},
    {'deleted': False,
     'id': 490,
     'name': 'Banaba I. (Ocean I.)',
     'numeric_3': "296"},
    {'deleted': False,
     'id': 492,
     'name': 'Yemen',
     'numeric_3': '887'},
    {'deleted': True,
     'id': 493,
     'name': 'Penguin Is.',
     'numeric_3': "036"},
    {'deleted': False,
     'id': 497,
     'name': 'Croatia',
     'numeric_3': '191'},
    {'deleted': False,
     'id': 499,
     'name': 'Slovenia',
     'numeric_3': '705'},
    {'deleted': False,
     'id': 501,
     'name': 'Bosnia-Herzegovina',
     'numeric_3': '070'},
    {'deleted': False,
     'id': 502,
     'name': 'Macedonia',
     'numeric_3': '807'},
    {'deleted': False,
     'id': 503,
     'name': 'Czech Republic',
     'numeric_3': '203'},
    {'deleted': False,
     'id': 504,
     'name': 'Slovak Republic',
     'numeric_3': '703'},
    {'deleted': False,
     'id': 505,
     'name': 'Pratas I.',
     'numeric_3': "158"},
    {'deleted': False,
     'id': 506,
     'name': 'Scarborough Reef',
     # None okay
     'numeric_3': None},
    {'deleted': False,
     'id': 507,
     'name': 'Temotu Province',
     'numeric_3': "090"},
    {'deleted': False,
     'id': 508,
     'name': 'Austral I.',
     'numeric_3': "250"},
    {'deleted': False,
     'id': 509,
     'name': 'Marquesas Is.',
     'numeric_3': "250"},
    {'deleted': False,
     'id': 510,
     'name': 'Palestine',
     'numeric_3': '275'},
    {'deleted': False,
     'id': 511,
     'name': 'Timor-Leste',
     'numeric_3': '626'},
    {'deleted': False,
     'id': 512,
     'name': 'Chesterfield Is.',
     'numeric_3': "250"},
    {'deleted': False,
     'id': 513,
     'name': 'Ducie I.',
     'numeric_3': "826"},
    {'deleted': False,
     'id': 514,
     'name': 'Montenegro',
     'numeric_3': '499'},
    {'deleted': False,
     'id': 515,
     'name': 'Swains I.',
     'numeric_3': "840"},
    {'deleted': False,
     'id': 516,
     'name': 'Saint Barthelemy',
     'numeric_3': '250'},
    {'deleted': False,
     'id': 517,
     'name': 'Curacao',
     'numeric_3': '528'},
    {'deleted': False,
     'id': 518,
     'name': 'St Maarten',
     'numeric_3': '528'},
    {'deleted': False,
     'id': 519,
     'name': 'Saba & St. Eustatius',
     'numeric_3': "528"},
    {'deleted': False,
     'id': 520,
     'name': 'Bonaire',
     'numeric_3': '528'},
    {'deleted': False,
     'id': 521,
     'name': 'South Sudan (Republic of)',
     'numeric_3': '728'},
    {'deleted': False,
     'id': 522,
     'name': 'Republic of Kosovo',
     'numeric_3': '000'}
]


def forwards(apps, schema_editor):
    DXCCEntry = apps.get_model('callsign', 'DXCCEntry')
    Country = apps.get_model('callsign', 'Country')
    db_alias = schema_editor.connection.alias

    for dxcc_entry in DXCC_ENTIRES:
        country_numeric_3 = dxcc_entry.pop("numeric_3", None)
        if country_numeric_3:
            dxcc_entry["country"] = Country.objects.using(db_alias).get(numeric_3=country_numeric_3)
        DXCCEntry.objects.using(db_alias).create(**dxcc_entry)


class Migration(migrations.Migration):
    dependencies = [
        ('callsign', '0002_country_import'),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]
