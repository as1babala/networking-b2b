import pytz
from django.utils.translation import gettext_lazy as _
import uuid, base64


def jwt_payload_handler(user):
    """Custom payload handler
    Token encrypts the dictionary returned by this function, and can be
    decoded by rest_framework_jwt.utils.jwt_decode_handler
    """
    return {
        "id": user.pk,
        # 'name': user.name,
        "email": user.email,
        # "role": user.role,
        # "has_sales_access": user.has_sales_access,
        # "has_marketing_access": user.has_marketing_access,
        "file_prepend": user.file_prepend,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_active": user.is_active,
        # "is_admin": user.is_admin,
        "is_staff": user.is_staff,
        # "date_joined"
    }
    
def generate_code():
    code = str(uuid.uuid4()).replace('-', '').upper()[:12]
    return code

SEX = (
    ("Masculin", "Masculin"),
    ("Feminin","Feminin"),
    
)

TOGO_REGION = (
    ("Maritime","Maritime"),
    ("Plateaux","Plateaux"),
    ("Centrale", "Centrale"),
    ("Kara", "Kara"),
    ("Savane", "Savane"),
    
)

JOB_GRADES = (
    ("CS", "Cadre Superieur"),
    ("CM", "Cadre Moyen"),
    
)

Departments = (
    ("ACC", "Accounting"),
    ("FNS", "Financial Services"),
    
)
TOGO_VILLE = (
    ("Grand Lome", "Grand Lome"),
    ("Baguida","Baguida"),
    ("Aneho", "Aneho"),
    ("Agoe", "Agoe"),
    ("Tsevie", "Tsevie"),
    ("Agbelouve", "Agbelouve"),
    ("Kpalime", "Kpalime"),
    ("Atapkame", "Atapkame"),
    ("Sotouboua", "Sotouboua"),
    ("Blitta", "Blitta"),
    ("Bafilo", "Bafilo"),
    ("Sokode", "Sokode"),
    ("Kara", "Kara"),
    ("Mango", "Mango"),
    ("Dapaong", "Dapaong"),
    ("Pya", "Pya"),
    ("Pya", "Pya"),
    
)

INDCHOICES = (
    ("ADVERTISING", "ADVERTISING"),
    ("AGRICULTURE", "AGRICULTURE"),
    ("APPAREL & ACCESSORIES", "APPAREL & ACCESSORIES"),
    ("AUTOMOTIVE", "AUTOMOTIVE"),
    ("BANKING", "BANKING"),
    ("BIOTECHNOLOGY", "BIOTECHNOLOGY"),
    ("BUILDING MATERIALS & EQUIPMENT", "BUILDING MATERIALS & EQUIPMENT"),
    ("CHEMICAL", "CHEMICAL"),
    ("COMPUTER", "COMPUTER"),
    ("EDUCATION", "EDUCATION"),
    ("ELECTRONICS", "ELECTRONICS"),
    ("ENERGY", "ENERGY"),
    ("ENTERTAINMENT & LEISURE", "ENTERTAINMENT & LEISURE"),
    ("FINANCE", "FINANCE"),
    ("FOOD & BEVERAGE", "FOOD & BEVERAGE"),
    ("GROCERY", "GROCERY"),
    ("HEALTHCARE", "HEALTHCARE"),
    ("INSURANCE", "INSURANCE"),
    ("LEGAL", "LEGAL"),
    ("MANUFACTURING", "MANUFACTURING"),
    ("PUBLISHING", "PUBLISHING"),
    ("REAL ESTATE", "REAL ESTATE"),
    ("SERVICE", "SERVICE"),
    ("SOFTWARE", "SOFTWARE"),
    ("SPORTS", "SPORTS"),
    ("TECHNOLOGY", "TECHNOLOGY"),
    ("TELECOMMUNICATIONS", "TELECOMMUNICATIONS"),
    ("TELEVISION", "TELEVISION"),
    ("TRANSPORTATION", "TRANSPORTATION"),
    ("VENTURE CAPITAL", "VENTURE CAPITAL"),
)

    

TYPECHOICES = (
    ("CUSTOMER", "CUSTOMER"),
    ("INVESTOR", "INVESTOR"),
    ("PARTNER", "PARTNER"),
    ("RESELLER", "RESELLER"),
)

CSAT = (
    ("0", 0),
    ("1", 1),
    ("2", 2),
    ("3", 3),
    ("4", 4),
    ("5", 5),
    ("6", 6),
    ("7", 7),
    ("8", 8),
    ("9", 9),
    ("10", 10),
    
    
)

ORG = (
    ("call center","Call Center"),
    ("FIN ","Finance"),
    ("CAO ","Administration Office"),
    ("news","News center"),
    
)
ROLES = (
    ("ADMIN", "ADMIN"),
    ("USER", "USER"),
)

LEAD_STATUS = (
    ("assigned", "Assigned"),
    ("in process", "In Process"),
    ("converted", "Converted"),
    ("recycled", "Recycled"),
    ("closed", "Closed"),
)


LEAD_SOURCE = (
    ("call", "Call"),
    ("email", "Email"),
    ("existing customer", "Existing Customer"),
    ("partner", "Partner"),
    ("public relations", "Public Relations"),
    ("compaign", "Campaign"),
    ("other", "Other"),
)

STATUS_CHOICE = (
    ("New", "New"),
    ("Assigned", "Assigned"),
    ("Pending", "Pending"),
    ("Closed", "Closed"),
    ("Rejected", "Rejected"),
    ("Duplicate", "Duplicate"),
)

PRIORITY_CHOICE = (
    ("Low", "Low"),
    ("Normal", "Normal"),
    ("High", "High"),
    ("Urgent", "Urgent"),
)

CASE_TYPE = (("Question", "Question"), ("Incident", "Incident"), ("Problem", "Problem"))

STAGES = (
    ("QUALIFICATION", "QUALIFICATION"),
    ("NEEDS ANALYSIS", "NEEDS ANALYSIS"),
    ("VALUE PROPOSITION", "VALUE PROPOSITION"),
    ("ID.DECISION MAKERS", "ID.DECISION MAKERS"),
    ("PERCEPTION ANALYSIS", "PERCEPTION ANALYSIS"),
    ("PROPOSAL/PRICE QUOTE", "PROPOSAL/PRICE QUOTE"),
    ("NEGOTIATION/REVIEW", "NEGOTIATION/REVIEW"),
    ("CLOSED WON", "CLOSED WON"),
    ("CLOSED LOST", "CLOSED LOST"),
)

SOURCES = (
    ("NONE", "NONE"),
    ("CALL", "CALL"),
    ("EMAIL", " EMAIL"),
    ("EXISTING CUSTOMER", "EXISTING CUSTOMER"),
    ("PARTNER", "PARTNER"),
    ("PUBLIC RELATIONS", "PUBLIC RELATIONS"),
    ("CAMPAIGN", "CAMPAIGN"),
    ("WEBSITE", "WEBSITE"),
    ("OTHER", "OTHER"),
)

EVENT_PARENT_TYPE = ((10, "Account"), (13, "Lead"), (14, "Opportunity"), (11, "Case"))

EVENT_STATUS = (
    ("Planned", "Planned"),
    ("Held", "Held"),
    ("Not Held", "Not Held"),
    ("Not Started", "Not Started"),
    ("Started", "Started"),
    ("Completed", "Completed"),
    ("Canceled", "Canceled"),
    ("Deferred", "Deferred"),
)


COUNTRIES = (
    ("GB", _("United Kingdom")),
    ("AF", _("Afghanistan")),
    ("AX", _("Aland Islands")),
    ("AL", _("Albania")),
    ("DZ", _("Algeria")),
    ("AS", _("American Samoa")),
    ("AD", _("Andorra")),
    ("AO", _("Angola")),
    ("AI", _("Anguilla")),
    ("AQ", _("Antarctica")),
    ("AG", _("Antigua and Barbuda")),
    ("AR", _("Argentina")),
    ("AM", _("Armenia")),
    ("AW", _("Aruba")),
    ("AU", _("Australia")),
    ("AT", _("Austria")),
    ("AZ", _("Azerbaijan")),
    ("BS", _("Bahamas")),
    ("BH", _("Bahrain")),
    ("BD", _("Bangladesh")),
    ("BB", _("Barbados")),
    ("BY", _("Belarus")),
    ("BE", _("Belgium")),
    ("BZ", _("Belize")),
    ("BJ", _("Benin")),
    ("BM", _("Bermuda")),
    ("BT", _("Bhutan")),
    ("BO", _("Bolivia")),
    ("BA", _("Bosnia and Herzegovina")),
    ("BW", _("Botswana")),
    ("BV", _("Bouvet Island")),
    ("BR", _("Brazil")),
    ("IO", _("British Indian Ocean Territory")),
    ("BN", _("Brunei Darussalam")),
    ("BG", _("Bulgaria")),
    ("BF", _("Burkina Faso")),
    ("BI", _("Burundi")),
    ("KH", _("Cambodia")),
    ("CM", _("Cameroon")),
    ("CA", _("Canada")),
    ("CV", _("Cape Verde")),
    ("KY", _("Cayman Islands")),
    ("CF", _("Central African Republic")),
    ("TD", _("Chad")),
    ("CL", _("Chile")),
    ("CN", _("China")),
    ("CX", _("Christmas Island")),
    ("CC", _("Cocos (Keeling) Islands")),
    ("CO", _("Colombia")),
    ("KM", _("Comoros")),
    ("CG", _("Congo")),
    ("CD", _("Congo, The Democratic Republic of the")),
    ("CK", _("Cook Islands")),
    ("CR", _("Costa Rica")),
    ("CI", _("Cote d'Ivoire")),
    ("HR", _("Croatia")),
    ("CU", _("Cuba")),
    ("CY", _("Cyprus")),
    ("CZ", _("Czech Republic")),
    ("DK", _("Denmark")),
    ("DJ", _("Djibouti")),
    ("DM", _("Dominica")),
    ("DO", _("Dominican Republic")),
    ("EC", _("Ecuador")),
    ("EG", _("Egypt")),
    ("SV", _("El Salvador")),
    ("GQ", _("Equatorial Guinea")),
    ("ER", _("Eritrea")),
    ("EE", _("Estonia")),
    ("ET", _("Ethiopia")),
    ("FK", _("Falkland Islands (Malvinas)")),
    ("FO", _("Faroe Islands")),
    ("FJ", _("Fiji")),
    ("FI", _("Finland")),
    ("FR", _("France")),
    ("GF", _("French Guiana")),
    ("PF", _("French Polynesia")),
    ("TF", _("French Southern Territories")),
    ("GA", _("Gabon")),
    ("GM", _("Gambia")),
    ("GE", _("Georgia")),
    ("DE", _("Germany")),
    ("GH", _("Ghana")),
    ("GI", _("Gibraltar")),
    ("GR", _("Greece")),
    ("GL", _("Greenland")),
    ("GD", _("Grenada")),
    ("GP", _("Guadeloupe")),
    ("GU", _("Guam")),
    ("GT", _("Guatemala")),
    ("GG", _("Guernsey")),
    ("GN", _("Guinea")),
    ("GW", _("Guinea-Bissau")),
    ("GY", _("Guyana")),
    ("HT", _("Haiti")),
    ("HM", _("Heard Island and McDonald Islands")),
    ("VA", _("Holy See (Vatican City State)")),
    ("HN", _("Honduras")),
    ("HK", _("Hong Kong")),
    ("HU", _("Hungary")),
    ("IS", _("Iceland")),
    ("IN", _("India")),
    ("ID", _("Indonesia")),
    ("IR", _("Iran, Islamic Republic of")),
    ("IQ", _("Iraq")),
    ("IE", _("Ireland")),
    ("IM", _("Isle of Man")),
    ("IL", _("Israel")),
    ("IT", _("Italy")),
    ("JM", _("Jamaica")),
    ("JP", _("Japan")),
    ("JE", _("Jersey")),
    ("JO", _("Jordan")),
    ("KZ", _("Kazakhstan")),
    ("KE", _("Kenya")),
    ("KI", _("Kiribati")),
    ("KP", _("Korea, Democratic People's Republic of")),
    ("KR", _("Korea, Republic of")),
    ("KW", _("Kuwait")),
    ("KG", _("Kyrgyzstan")),
    ("LA", _("Lao People's Democratic Republic")),
    ("LV", _("Latvia")),
    ("LB", _("Lebanon")),
    ("LS", _("Lesotho")),
    ("LR", _("Liberia")),
    ("LY", _("Libyan Arab Jamahiriya")),
    ("LI", _("Liechtenstein")),
    ("LT", _("Lithuania")),
    ("LU", _("Luxembourg")),
    ("MO", _("Macao")),
    ("MK", _("Macedonia, The Former Yugoslav Republic of")),
    ("MG", _("Madagascar")),
    ("MW", _("Malawi")),
    ("MY", _("Malaysia")),
    ("MV", _("Maldives")),
    ("ML", _("Mali")),
    ("MT", _("Malta")),
    ("MH", _("Marshall Islands")),
    ("MQ", _("Martinique")),
    ("MR", _("Mauritania")),
    ("MU", _("Mauritius")),
    ("YT", _("Mayotte")),
    ("MX", _("Mexico")),
    ("FM", _("Micronesia, Federated States of")),
    ("MD", _("Moldova")),
    ("MC", _("Monaco")),
    ("MN", _("Mongolia")),
    ("ME", _("Montenegro")),
    ("MS", _("Montserrat")),
    ("MA", _("Morocco")),
    ("MZ", _("Mozambique")),
    ("MM", _("Myanmar")),
    ("NA", _("Namibia")),
    ("NR", _("Nauru")),
    ("NP", _("Nepal")),
    ("NL", _("Netherlands")),
    ("AN", _("Netherlands Antilles")),
    ("NC", _("New Caledonia")),
    ("NZ", _("New Zealand")),
    ("NI", _("Nicaragua")),
    ("NE", _("Niger")),
    ("NG", _("Nigeria")),
    ("NU", _("Niue")),
    ("NF", _("Norfolk Island")),
    ("MP", _("Northern Mariana Islands")),
    ("NO", _("Norway")),
    ("OM", _("Oman")),
    ("PK", _("Pakistan")),
    ("PW", _("Palau")),
    ("PS", _("Palestinian Territory, Occupied")),
    ("PA", _("Panama")),
    ("PG", _("Papua New Guinea")),
    ("PY", _("Paraguay")),
    ("PE", _("Peru")),
    ("PH", _("Philippines")),
    ("PN", _("Pitcairn")),
    ("PL", _("Poland")),
    ("PT", _("Portugal")),
    ("PR", _("Puerto Rico")),
    ("QA", _("Qatar")),
    ("RE", _("Reunion")),
    ("RO", _("Romania")),
    ("RU", _("Russian Federation")),
    ("RW", _("Rwanda")),
    ("BL", _("Saint Barthelemy")),
    ("SH", _("Saint Helena")),
    ("KN", _("Saint Kitts and Nevis")),
    ("LC", _("Saint Lucia")),
    ("MF", _("Saint Martin")),
    ("PM", _("Saint Pierre and Miquelon")),
    ("VC", _("Saint Vincent and the Grenadines")),
    ("WS", _("Samoa")),
    ("SM", _("San Marino")),
    ("ST", _("Sao Tome and Principe")),
    ("SA", _("Saudi Arabia")),
    ("SN", _("Senegal")),
    ("RS", _("Serbia")),
    ("SC", _("Seychelles")),
    ("SL", _("Sierra Leone")),
    ("SG", _("Singapore")),
    ("SK", _("Slovakia")),
    ("SI", _("Slovenia")),
    ("SB", _("Solomon Islands")),
    ("SO", _("Somalia")),
    ("ZA", _("South Africa")),
    ("GS", _("South Georgia and the South Sandwich Islands")),
    ("ES", _("Spain")),
    ("LK", _("Sri Lanka")),
    ("SD", _("Sudan")),
    ("SR", _("Suriname")),
    ("SJ", _("Svalbard and Jan Mayen")),
    ("SZ", _("Swaziland")),
    ("SE", _("Sweden")),
    ("CH", _("Switzerland")),
    ("SY", _("Syrian Arab Republic")),
    ("TW", _("Taiwan, Province of China")),
    ("TJ", _("Tajikistan")),
    ("TZ", _("Tanzania, United Republic of")),
    ("TH", _("Thailand")),
    ("TL", _("Timor-Leste")),
    ("TG", _("Togo")),
    ("TK", _("Tokelau")),
    ("TO", _("Tonga")),
    ("TT", _("Trinidad and Tobago")),
    ("TN", _("Tunisia")),
    ("TR", _("Turkey")),
    ("TM", _("Turkmenistan")),
    ("TC", _("Turks and Caicos Islands")),
    ("TV", _("Tuvalu")),
    ("UG", _("Uganda")),
    ("UA", _("Ukraine")),
    ("AE", _("United Arab Emirates")),
    ("US", _("United States")),
    ("UM", _("United States Minor Outlying Islands")),
    ("UY", _("Uruguay")),
    ("UZ", _("Uzbekistan")),
    ("VU", _("Vanuatu")),
    ("VE", _("Venezuela")),
    ("VN", _("Viet Nam")),
    ("VG", _("Virgin Islands, British")),
    ("VI", _("Virgin Islands, U.S.")),
    ("WF", _("Wallis and Futuna")),
    ("EH", _("Western Sahara")),
    ("YE", _("Yemen")),
    ("ZM", _("Zambia")),
    ("ZW", _("Zimbabwe")),
)

CURRENCY_CODES = (
    ("AED", _("AED, Dirham")),
    ("AFN", _("AFN, Afghani")),
    ("ALL", _("ALL, Lek")),
    ("AMD", _("AMD, Dram")),
    ("ANG", _("ANG, Guilder")),
    ("AOA", _("AOA, Kwanza")),
    ("ARS", _("ARS, Peso")),
    ("AUD", _("AUD, Dollar")),
    ("AWG", _("AWG, Guilder")),
    ("AZN", _("AZN, Manat")),
    ("BAM", _("BAM, Marka")),
    ("BBD", _("BBD, Dollar")),
    ("BDT", _("BDT, Taka")),
    ("BGN", _("BGN, Lev")),
    ("BHD", _("BHD, Dinar")),
    ("BIF", _("BIF, Franc")),
    ("BMD", _("BMD, Dollar")),
    ("BND", _("BND, Dollar")),
    ("BOB", _("BOB, Boliviano")),
    ("BRL", _("BRL, Real")),
    ("BSD", _("BSD, Dollar")),
    ("BTN", _("BTN, Ngultrum")),
    ("BWP", _("BWP, Pula")),
    ("BYR", _("BYR, Ruble")),
    ("BZD", _("BZD, Dollar")),
    ("CAD", _("CAD, Dollar")),
    ("CDF", _("CDF, Franc")),
    ("CHF", _("CHF, Franc")),
    ("CLP", _("CLP, Peso")),
    ("CNY", _("CNY, Yuan Renminbi")),
    ("COP", _("COP, Peso")),
    ("CRC", _("CRC, Colon")),
    ("CUP", _("CUP, Peso")),
    ("CVE", _("CVE, Escudo")),
    ("CZK", _("CZK, Koruna")),
    ("DJF", _("DJF, Franc")),
    ("DKK", _("DKK, Krone")),
    ("DOP", _("DOP, Peso")),
    ("DZD", _("DZD, Dinar")),
    ("EGP", _("EGP, Pound")),
    ("ERN", _("ERN, Nakfa")),
    ("ETB", _("ETB, Birr")),
    ("EUR", _("EUR, Euro")),
    ("FJD", _("FJD, Dollar")),
    ("FKP", _("FKP, Pound")),
    ("GBP", _("GBP, Pound")),
    ("GEL", _("GEL, Lari")),
    ("GHS", _("GHS, Cedi")),
    ("GIP", _("GIP, Pound")),
    ("GMD", _("GMD, Dalasi")),
    ("GNF", _("GNF, Franc")),
    ("GTQ", _("GTQ, Quetzal")),
    ("GYD", _("GYD, Dollar")),
    ("HKD", _("HKD, Dollar")),
    ("HNL", _("HNL, Lempira")),
    ("HRK", _("HRK, Kuna")),
    ("HTG", _("HTG, Gourde")),
    ("HUF", _("HUF, Forint")),
    ("IDR", _("IDR, Rupiah")),
    ("ILS", _("ILS, Shekel")),
    ("INR", _("INR, Rupee")),
    ("IQD", _("IQD, Dinar")),
    ("IRR", _("IRR, Rial")),
    ("ISK", _("ISK, Krona")),
    ("JMD", _("JMD, Dollar")),
    ("JOD", _("JOD, Dinar")),
    ("JPY", _("JPY, Yen")),
    ("KES", _("KES, Shilling")),
    ("KGS", _("KGS, Som")),
    ("KHR", _("KHR, Riels")),
    ("KMF", _("KMF, Franc")),
    ("KPW", _("KPW, Won")),
    ("KRW", _("KRW, Won")),
    ("KWD", _("KWD, Dinar")),
    ("KYD", _("KYD, Dollar")),
    ("KZT", _("KZT, Tenge")),
    ("LAK", _("LAK, Kip")),
    ("LBP", _("LBP, Pound")),
    ("LKR", _("LKR, Rupee")),
    ("LRD", _("LRD, Dollar")),
    ("LSL", _("LSL, Loti")),
    ("LTL", _("LTL, Litas")),
    ("LVL", _("LVL, Lat")),
    ("LYD", _("LYD, Dinar")),
    ("MAD", _("MAD, Dirham")),
    ("MDL", _("MDL, Leu")),
    ("MGA", _("MGA, Ariary")),
    ("MKD", _("MKD, Denar")),
    ("MMK", _("MMK, Kyat")),
    ("MNT", _("MNT, Tugrik")),
    ("MOP", _("MOP, Pataca")),
    ("MRO", _("MRO, Ouguiya")),
    ("MUR", _("MUR, Rupee")),
    ("MVR", _("MVR, Rufiyaa")),
    ("MWK", _("MWK, Kwacha")),
    ("MXN", _("MXN, Peso")),
    ("MYR", _("MYR, Ringgit")),
    ("MZN", _("MZN, Metical")),
    ("NAD", _("NAD, Dollar")),
    ("NGN", _("NGN, Naira")),
    ("NIO", _("NIO, Cordoba")),
    ("NOK", _("NOK, Krone")),
    ("NPR", _("NPR, Rupee")),
    ("NZD", _("NZD, Dollar")),
    ("OMR", _("OMR, Rial")),
    ("PAB", _("PAB, Balboa")),
    ("PEN", _("PEN, Sol")),
    ("PGK", _("PGK, Kina")),
    ("PHP", _("PHP, Peso")),
    ("PKR", _("PKR, Rupee")),
    ("PLN", _("PLN, Zloty")),
    ("PYG", _("PYG, Guarani")),
    ("QAR", _("QAR, Rial")),
    ("RON", _("RON, Leu")),
    ("RSD", _("RSD, Dinar")),
    ("RUB", _("RUB, Ruble")),
    ("RWF", _("RWF, Franc")),
    ("SAR", _("SAR, Rial")),
    ("SBD", _("SBD, Dollar")),
    ("SCR", _("SCR, Rupee")),
    ("SDG", _("SDG, Pound")),
    ("SEK", _("SEK, Krona")),
    ("SGD", _("SGD, Dollar")),
    ("SHP", _("SHP, Pound")),
    ("SLL", _("SLL, Leone")),
    ("SOS", _("SOS, Shilling")),
    ("SRD", _("SRD, Dollar")),
    ("SSP", _("SSP, Pound")),
    ("STD", _("STD, Dobra")),
    ("SYP", _("SYP, Pound")),
    ("SZL", _("SZL, Lilangeni")),
    ("THB", _("THB, Baht")),
    ("TJS", _("TJS, Somoni")),
    ("TMT", _("TMT, Manat")),
    ("TND", _("TND, Dinar")),
    ("TOP", _("TOP, Paanga")),
    ("TRY", _("TRY, Lira")),
    ("TTD", _("TTD, Dollar")),
    ("TWD", _("TWD, Dollar")),
    ("TZS", _("TZS, Shilling")),
    ("UAH", _("UAH, Hryvnia")),
    ("UGX", _("UGX, Shilling")),
    ("USD", _("$, Dollar")),
    ("UYU", _("UYU, Peso")),
    ("UZS", _("UZS, Som")),
    ("VEF", _("VEF, Bolivar")),
    ("VND", _("VND, Dong")),
    ("VUV", _("VUV, Vatu")),
    ("WST", _("WST, Tala")),
    ("XAF", _("XAF, Franc")),
    ("XCD", _("XCD, Dollar")),
    ("XOF", _("XOF, Franc")),
    ("XPF", _("XPF, Franc")),
    ("YER", _("YER, Rial")),
    ("ZAR", _("ZAR, Rand")),
    ("ZMK", _("ZMK, Kwacha")),
    ("ZWL", _("ZWL, Dollar")),
)


def return_complete_address(self):
    address = ""
    if self.address_line:
        address += self.address_line
    if self.street:
        if address:
            address += ", " + self.street
        else:
            address += self.street
    if self.city:
        if address:
            address += ", " + self.city
        else:
            address += self.city
    if self.state:
        if address:
            address += ", " + self.state
        else:
            address += self.state
    if self.postcode:
        if address:
            address += ", " + self.postcode
        else:
            address += self.postcode
    if self.country:
        if address:
            address += ", " + self.get_country_display()
        else:
            address += self.get_country_display()
    return address


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def convert_to_custom_timezone(custom_date, custom_timezone, to_utc=False):
    user_time_zone = pytz.timezone(custom_timezone)
    if to_utc:
        custom_date = user_time_zone.localize(custom_date.replace(tzinfo=None))
        user_time_zone = pytz.UTC
    return custom_date.astimezone(user_time_zone)


def append_str_to(append_to: str, *args, sep=", ", **kwargs):
    """Concatenate to a string.
    Args:
        append_to(str): The string to append to.
        args(list): list of string characters to concatenate.
        sep(str): Seperator to use between concatenated strings.
        kwargs(dict): Mapping of variables with intended string values.
    Returns:
        str, joined strings seperated
    """
    append_to = append_to or ""
    result_list = [append_to] + list(args) + list(kwargs.values())
    data = False
    for item in result_list:
        if item:
            data = True
            break
    return f"{sep}".join(filter(len, result_list)) if data else ""


TYPE_COMPANIES = (("Sole proprietorship", "Sole proprietorship"),
                  ("Partnership", "Partnership"),
                  ("Limited liability company (LLC)", "Limited liability company (LLC)"),
                  ("Corporation","Corporation"),
                  ("Cooperative", "Cooperative"),
                  ("Publicly traded company", "Publicly traded company"),
                  ("Privately held company", "Privately held company"),
                  ("Non-profit", "Non-profit"),
                 
)

PARTENERSHIP_TYPE = (
    ("PARTENAIRE COMMERCIAL", "PARTENAIRE COMMERCIAL"),
    ("PARTENAIRE TECHNIQUE ", "PARTENAIRE TECHNIQUE "),
    ("PARTENAIRE FINANCIER ", "PARTENAIRE FINANCIER "),
    ("PARTENAIR MANAGEMENT ","PARTENAIR MANAGEMENT "),
    
)

PHONE_CODE = (
('+1','+1'),
('+7','+7'),
('+20','+20'),
('+27','+27'),
('+30','+30'),
('+31','+31'),
('+32','+32'),
('+33','+33'),
('+34','+34'),
('+36','+36'),
('+39','+39'),
('+40','+40'),
('+41','+41'),
('+43','+43'),
('+44','+44'),
('+45','+45'),
('+46','+46'),
('+47','+47'),
('+48','+48'),
('+49','+49'),
('+51','+51'),
('+52','+52'),
('+53','+53'),
('+54','+54'),
('+55','+55'),
('+56','+56'),
('+57','+57'),
('+58','+58'),
('+60','+60'),


('+61','+61'),
('+62','+62'),
('+63','+63'),
('+64','+64'),
('+64','+64'),
('+65','+65'),
('+66','+66'),
('+81','+81'),
('+82','+82'),
('+84','+84'),
('+86','+86'),
('+90','+90'),
('+91','+91'),
('+92','+92'),
('+93','+93'),
('+94','+94'),
('+95','+95'),
('+98','+98'),
('+211','+211'),
('+212','+212'),
('+212','+212'),
('+213','+213'),
('+216','+216'),
('+218','+218'),
('+220','+220'),
('+221','+221'),
('+222','+222'),
('+223','+223'),
('+224','+224'),
('+225','+225'),
('+226','+226'),
('+227','+227'),
('+228','+228'),
('+229','+229'),
('+230','+230'),
('+231','+231'),
('+232','+232'),
('+233','+233'),
('+234','+234'),
('+235','+235'),
('+236','+236'),
('+237','+237'),
('+238','+238'),
('+239','+239'),
('+240','+240'),
('+241','+241'),
('+242','+242'),
('+243','+243'),
('+244','+244'),
('+245','+245'),
('+246','+246'),
('+248','+248'),
('+249','+249'),
('+250','+250'),
('+251','+251'),
('+252','+252'),
('+253','+253'),
('+254','+254'),
('+255','+255'),
('+256','+256'),
('+257','+257'),
('+258','+258'),
('+260','+260'),
('+261','+261'),
('+262','+262'),
('+262','+262'),
('+263','+263'),
('+264','+264'),
('+265','+265'),
('+266','+266'),
('+267','+267'),
('+268','+268'),
('+269','+269'),
('+290','+290'),
('+291','+291'),
('+297','+297'),
('+298','+298'),
('+299','+299'),
('+350','+350'),
('+351','+351'),
('+352','+352'),
('+353','+353'),
('+354','+354'),
('+355','+355'),
('+356','+356'),
('+357','+357'),
('+358','+358'),
('+359','+359'),
('+370','+370'),
('+371','+371'),
('+372','+372'),
('+373','+373'),
('+374','+374'),
('+375','+375'),
('+376','+376'),
('+377','+377'),
('+378','+378'),
('+379','+379'),
('+380','+380'),
('+381','+381'),
('+382','+382'),
('+383','+383'),
('+385','+385'),
('+386','+386'),
('+387','+387'),
('+389','+389'),
('+420','+420'),
('+421','+421'),
('+423','+423'),
('+500','+500'),
('+501','+501'),
('+502','+502'),
('+503','+503'),
('+504','+504'),
('+505','+505'),
('+506','+506'),
('+507','+507'),
('+508','+508'),
('+509','+509'),
('+590','+590'),
('+590','+590'),
('+591','+591'),
('+592','+592'),
('+593','+593'),
('+595','+595'),
('+597','+597'),
('+598','+598'),
('+599','+599'),
('+599','+599'),
('+670','+670'),
('+672','+672'),
('+673','+673'),
('+674','+674'),
('+675','+675'),
('+676','+676'),
('+677','+677'),
('+678','+678'),
('+679','+679'),
('+680','+680'),
('+681','+681'),
('+682','+682'),
('+683','+683'),
('+685','+685'),
('+686','+686'),
('+687','+687'),
('+688','+688'),
('+689','+689'),
('+690','+690'),
('+691','+691'),
('+692','+692'),
('+850','+850'),
('+852','+852'),
('+853','+853'),
('+855','+855'),
('+856','+856'),
('+880','+880'),
('+886','+886'),
('+960','+960'),
('+961','+961'),
('+962','+962'),
('+963','+963'),
('+964','+964'),
('+965','+965'),
('+966','+966'),
('+967','+967'),
('+968','+968'),
('+970','+970'),
('+971','+971'),
('+972','+972'),
('+973','+973'),
('+974','+974'),
('+975','+975'),
('+976','+976'),
('+977','+977'),
('+992','+992'),
('+993','+993'),
('+994','+994'),
('+995','+995'),
('+996','+996'),
('+998','+998'),
('+1242','+1242'),
('+1246','+1246'),
('+1264','+1264'),
('+1268','+1268'),
('+1284','+1284'),
('+1340','+1340'),
('+1345','+1345'),
('+1441','+1441'),
('+1473','+1473'),
('+1649','+1649'),
('+1664','+1664'),
('+1670','+1670'),
('+1671','+1671'),
('+1684','+1684'),
('+1721','+1721'),
('+1758','+1758'),
('+1767','+1767'),
('+1784','+1784'),
('+1868','+1868'),
('+1869','+1869'),
('+1876','+1876'),
('+4779','+4779'),
('+441481','+441481'),
('+441534','+441534'),
('+441624','+441624'),
)

EMP_NUMBER = [('1','Less than 10 employees'),
              ('2','11 - 25 employees'), ('3', '26 - 50 employees'), ('4', '51 - 100 employees'), 
          ('5', '101 - 250 employees '),('6','More than 250 employees')]

REVENUE = [('1','Less than 150 000 000'),
              ('2','150 000 000 -  500 000 000'), ('3', '500 000 001 - 1 000 000 000'), 
          ('4', 'More 1 000 000 000 ')]

PARTNERSHIP_TYPE = (('PARTENAIRE COMMERCIAL', 'PARTENAIRE COMMERCIAL'),
                     ('PARTENAIRE TECHNIQUE', 'PARTENAIRE TECHNIQUE'),
                     ('PARTENAIRE FINANCIER', 'PARTENAIRE FINANCIER'),
                     ('PARTENAIR MANAGEMENT', 'PARTENAIR MANAGEMENT'))

FICHE_CAT = (('Agriculture', 'Agriculture'), ('Elevage', 'Elevage'), ('Pisciculture', 'Pisciculture'))

EXPERTISE_LEVEL = (('No Expertise needed', 'No Expertise Needed'),('Minimum Level', 'Minimum Level'),
                   ('Medium Level', 'Medium Level'), ('High Level', "high level")
                   )

JOB_TYPE = (("FT", "Full Time"), ("PT", "Part Time"), ("IN", "Intern"))

BLOG_STATUS = (("DRAFT", "DRAFT"), ("PUBLISHED", "PUBLISHED"), ("ARCHIVED", "ARCHIVED"),)

      
OPPORTUNITY_TYPES = (('Looking for Financing Provider', 'Looking for Financing Provider'),
                    ('Offering Services','Offering Services'),
                    ('In Search of Services Provider','In Search of Services Provider'),
                     ('Offering Financing', 'Offering Financing'),
                     #('Looking for a Buyer', 'Looking for a Buyer'),
                     #('Looking for a Seller', 'Looking for a Seller'),
                     ('Offering Leadership Services', 'Offering Leadership Services'),
                     ('In Search of Leadership Services Provider', 'In Search of Leadership Services Provider'),
                     ('Offering Management Services', 'Offering Management Services'),
                     ('In Search of Management Services Provider', 'In Search of Management Services Provider'),
                     ('In Search of Technical Partner', 'In Search of Technical Partner'),
                    ('Offering Technical Services', 'Offering Technical Services'), 
)
OPP_CAT = (('Services', 'Services'), ('Products','Products'))

REVIEWERS = (('Blessing','Blessing'), ('Babala','Bbala'))
APPROVERS = (('Hannah','Hannah'), ('Elizam','Elizam'))
PROJECT_DECISION = (('APPROVED', 'APPROVED'), ('REJECTED', 'REJECTED'),)

APPLICATION_STATUS_CHOICES = (
        ('Applied', 'Applied'),
        ('Under Review', 'Under Review'),
        ('Rejected', 'Rejected'),
        ('Hired', 'Hired')
    )

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    #('O', 'Other')
]

BLOOD_GROUPS = [
    ('O-', 'O-'),
    ('O+', 'O+'),
    ('A-', 'A-'),
    ('A+', 'A+'),
    ('B-', 'B-'),
    ('B+', 'B+'),
    ('AB-', 'AB-'),
    ('AB+', 'AB+'),
]


DEGREE_CHOICES = (("BS", 'Bachelors Science'),
                 ("BA", 'Bachelors Arts'),
                 ("MBA", 'Master Business Administration'),
                 ("M", 'Masters'),
                 ("HS", 'High School'),
                  ("PhD", 'Doctorate'),
                  ("CR", "CERTIFICATE"),
)


 
SEX = (("F", "Female"), ("M", "Male"))
CONTRACT = (("DD", "Duree Determinee"), ("DI", "Duree Indeterminee"))


DEPARTMENTS = (
     ('F', 'Finance'),
     ('S', 'Sales'),
     ('CC', 'Contact Center'),
     ('ACC', 'Accounting'),
     ('IT', 'Information Technology'),
     ('RM', 'Risk Management')
     
)

EMP_TITLE = (
    ('OF', 'OFFICER'),
    ('MG', 'MANAGER'),
    ('SP', 'SUPERVISOR'),
    ('SG', 'SENIOR MG'),
    ('DT', 'DIRECTOR'),
    ('MD', 'MANAGING DIRECTOR'),
    ('CEO', 'CHIEF EXECUTIVE OFFICER')
)

DEGREE_CHOICES = (("BS", 'Bachelors Science'),
                 ("BA", 'Bachelors Arts'),
                 ("MBA", 'Master Business Administration'),
                 ("M", 'Masters'),
                 ("HS", 'High School'),
                  ("PhD", 'Doctorate'),
)

SEX = (("F", "Female"), ("M", "Male"))
CONTRACT = (("DD", "Duree Determinee"), ("DI", "Duree Indeterminee"))


DEPARTMENTS = (
     ('F', 'Finance'),
     ('S', 'Sales'),
     ('CC', 'Contact Center'),
     ('ACC', 'Accounting'),
     ('IT', 'Information Technology'),
     ('RM', 'Risk Management')
)

EMP_TITLE = (
    ('OF', 'OFFICER'),
    ('MG', 'MANAGER'),
    ('SP', 'SUPERVISOR'),
    ('SG', 'SENIOR MG'),
    ('DT', 'DIRECTOR'),
    ('MD', 'MANAGING DIRECTOR'),
    ('CEO', 'CHIEF EXECUTIVE OFFICER'),
    
)

RATING_CHOICES = (
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    ) 
TRAININGS = [('TECHNOLOGY','TECHNOLOGY'),
             ('INFORMATION TECHNOLOGY','INFORMATION TECHNOLOGY'),
     ('FINANCE','FINANCE'), ('FINANCIAL MODELING', 'FINANCIAL MODELING'),
     ('DATA ANALYSIS', 'DATA ANALYSIS')
]

TRAININGS_DOMAIN = [('FINANCE','FINANCE')]  
REQUIREMENTS = [('BACHELORS','BACHELORS')] 

POSITIONS = [('OFFICER', 'OFFICER'), ('ASSISTANT VICE PRESIDENT', 'ASSISTANT VICE PRESIDENT'), 
         ('VICE PRESIDENT', 'VICE PRESIDENT'), ('OTHER', 'OTHER')] 

TRAINING_DAYS = [('MONDAY', 'MONDAY'),
                 ('TUESDAY', 'TUESDAY'),
                 ('WEDNESDAY', 'WEDNESDAY'),
                 ('THURSDAY', 'THURSDAY'),
                 ('FRIDAY', 'FRIDAY'),
                 ('SATURDAY', 'SATURDAY')
             ]

TRAININGS_DURATION = [("0:30 PER DAY","0:30 PER DAY"), ("0:45 PER DAY","0:45 PER DAY"),("1:00 PER DAY","1:00 PER DAY"),
                  ("1:30 PER DAY","1:30 PER DAY"), ("1:45 PER DAY","1:45 PER DAY"), ("2:00 PER DAY","2:00 PER DAY"),
              ("2:30 PER DAY","2:30 PER DAY"), ("2:45 PER DAY","2:45 PER DAY"), ("3:00 PER DAY","3:00 PER DAY")]

TRAININGS_MODE = [("ONLINE", "ONLINE"), ("IN PERSON", "IN PERSON"), ("HYBRID", "HYBRID")]

PROJECT_CATEGORY = [("Industrial", "Industrial"), ("Fishing","Fishing"), ("Manufacturing", "Manufacturing")]

BLOG_CATEGORIES = [("Finance","Finance"), ("Entrepreneurship", "Entrepreneurship")]

SERVICES_CATEGORIES = [
  ('Healthcare Services', 'Healthcare Services'),
('Educational Services:', 'Educational Services:'),
('Professional Consulting', 'Professional Consulting'),
('Financial Services', 'Financial Services'),
('Information Technology (IT) Services', 'Information Technology (IT) Services'),
('Real Estate Services', 'Real Estate Services'),
('Hospitality Services', 'Hospitality Services'),
('Transportation Services', 'Transportation Services'),
('Entertainment Services', 'Entertainment Services'),
('Marketing & Advertising Services:', 'Marketing & Advertising Services:'),
('Home Maintenance and Repair', 'Home Maintenance and Repair'),
('Beauty & Personal Care Services', 'Beauty & Personal Care Services'),
('Legal Services', 'Legal Services'),
('Creative Services', 'Creative Services'),
('Retail & E-commerce Services', 'Retail & E-commerce Services'),
('Environmental Services', 'Environmental Services'),
('Agricultural Services', 'Agricultural Services'),
('Human Resources (HR) & Recruitment', 'Human Resources (HR) & Recruitment'),
('Construction & Architecture', 'Construction & Architecture'),
('Security Services:', 'Security Services:')
]

PRODUCTS_CATEGORIES = [
    ('Electronics', 'Electronics'),
('Fashion & Apparel', 'Fashion & Apparel'),
('Home & Furniture', 'Home & Furniture'),
('Beauty & Personal Care', 'Beauty & Personal Care'),
('Automobiles & Vehicles', 'Automobiles & Vehicles'),
('Books & Stationery', 'Books & Stationery'),
('Food & Beverages', 'Food & Beverages'),
('Health & Wellness', 'Health & Wellness'),
('Toys & Games', 'Toys & Games'),
('Home Appliances', 'Home Appliances'),
('Sports & Outdoors:', 'Sports & Outdoors:'),
('Gardening & Landscaping', 'Gardening & Landscaping'),
('DIY & Home Improvement', 'DIY & Home Improvement'),
('Music & Entertainment', 'Music & Entertainment'),
('Pet Supplies & Products', 'Pet Supplies & Products'),
('Software & Apps', 'Software & Apps'),
('Industrial & B2B Products', 'Industrial & B2B Products'),
('Art & Crafts', 'Art & Crafts'),
('Travel & Leisure Products', 'Travel & Leisure Products'),
('Real Estate:', 'Real Estate:'),
('Agriculture Products','Agriculture Products')
    
]

PRODUCTS_OPPORTUNITIES = [
    ('Looking for a seller', 'Looking for a Seller'),
    ('Looking for a Buyer', 'Looking for a Buyer'),
]

MEASUREMENT_UNIT = [
    ('Unit', 'Unit'),
   ('Meter (m) - length','Meter (m) - length'),
('foot (ft) - length ','foot (ft) - length '),
('yard (yd) - length ','yard (yd) - length '),
('mile (mi) - length ','mile (mi) - length '),
('Inch (in) - length  ','Inch (in) - length  '),
('Kilogram (kg) - weight/mass','Kilogram (kg) - weight/mass'),
('Tonne (t) - weight/mass','Tonne (t) - weight/mass'),
('Pound (lb) - weight/mass','Pound (lb) - weight/mass'),
('ounce (oz) - weight/mass','ounce (oz) - weight/mass'),
('ounce (oz) - volume ','ounce (oz) - volume '),
('Square inches (in²) - area','Square inches (in²) - area'),
('Square meter (m²) - area','Square meter (m²) - area'),
('hectares - area','hectares - area'),
('acres - area','acres - area'),
('square feet (ft²) - area','square feet (ft²) - area'),
('Gallon (gal) - volume ','Gallon (gal) - volume '),
('Liter (L) - volume','Liter (L) - volume'),
('pint (pt) - volume ','pint (pt) - volume '),
]

CURRENCIES_SYMBOLS = [
    ('AED (United Arab Emirates Dirham) - د.إ','AED (United Arab Emirates Dirham) - د.إ'),
('Algerian Dinar (DZD) - د.ج','Algerian Dinar (DZD) - د.ج'),
('Angolan Kwanza (AOA) - Kz','Angolan Kwanza (AOA) - Kz'),
('ARS (Argentine Peso) - $','ARS (Argentine Peso) - $'),
('AUD (Australian Dollar) - A$','AUD (Australian Dollar) - A$'),
('BDT (Bangladeshi Taka) - ৳','BDT (Bangladeshi Taka) - ৳'),
('Botswana Pula (BWP) - P','Botswana Pula (BWP) - P'),
('BRL (Brazilian Real) - R$','BRL (Brazilian Real) - R$'),
('Burundian Franc (BIF)','Burundian Franc (BIF)'),
('CAD (Canadian Dollar) - C$','CAD (Canadian Dollar) - C$'),
('Cape Verdean Escudo (CVE) - $ or Esc','Cape Verdean Escudo (CVE) - $ or Esc'),
('Central African CFA Franc (XAF) - FCFA','Central African CFA Franc (XAF) - FCFA'),
('CHF (Swiss Franc) - CHF','CHF (Swiss Franc) - CHF'),
('CLP (Chilean Peso) - $','CLP (Chilean Peso) - $'),
('CNY (Chinese Yuan Renminbi) - ¥ or 元','CNY (Chinese Yuan Renminbi) - ¥ or 元'),
('Comorian Franc (KMF)','Comorian Franc (KMF)'),
('Congolese Franc (CDF) - FC','Congolese Franc (CDF) - FC'),
('COP (Colombian Peso) - $','COP (Colombian Peso) - $'),
('CZK (Czech Koruna) - Kč','CZK (Czech Koruna) - Kč'),
('Djiboutian Franc (DJF)','Djiboutian Franc (DJF)'),
('DKK (Danish Krone) - kr','DKK (Danish Krone) - kr'),
('EGP (Egyptian Pound) - £ or ج.م','EGP (Egyptian Pound) - £ or ج.م'),
('Egyptian Pound (EGP) - £ or ج.م','Egyptian Pound (EGP) - £ or ج.م'),
('Eritrean Nakfa (ERN) - Nfk','Eritrean Nakfa (ERN) - Nfk'),
('Ethiopian Birr (ETB) - Br','Ethiopian Birr (ETB) - Br'),
('EUR (Euro) - €','EUR (Euro) - €'),
('Gambian Dalasi (GMD) - D','Gambian Dalasi (GMD) - D'),
('GBP (British Pound Sterling) - £','GBP (British Pound Sterling) - £'),
('Ghanaian Cedi (GHS) - GH₵','Ghanaian Cedi (GHS) - GH₵'),
('Guinean Franc (GNF) - GFr','Guinean Franc (GNF) - GFr'),
('HKD (Hong Kong Dollar) - HK$','HKD (Hong Kong Dollar) - HK$'),
('HUF (Hungarian Forint) - Ft','HUF (Hungarian Forint) - Ft'),
('IDR (Indonesian Rupiah) - Rp','IDR (Indonesian Rupiah) - Rp'),
('ILS (Israeli New Shekel) - ₪','ILS (Israeli New Shekel) - ₪'),
('INR (Indian Rupee) - ₹','INR (Indian Rupee) - ₹'),
('IQD (Iraqi Dinar) - ع.د','IQD (Iraqi Dinar) - ع.د'),
('JPY (Japanese Yen) - ¥','JPY (Japanese Yen) - ¥'),
('Kenyan Shilling (KES) - KSh','Kenyan Shilling (KES) - KSh'),
('KRW (South Korean Won) - ₩','KRW (South Korean Won) - ₩'),
('Lesotho Loti (LSL) - L','Lesotho Loti (LSL) - L'),
('Liberian Dollar (LRD) - $','Liberian Dollar (LRD) - $'),
('Libyan Dinar (LYD) - ل.د','Libyan Dinar (LYD) - ل.د'),
('Malagasy Ariary (MGA)','Malagasy Ariary (MGA)'),
('Malawian Kwacha (MWK) - MK','Malawian Kwacha (MWK) - MK'),
('Mauritanian Ouguiya (MRU) - UM','Mauritanian Ouguiya (MRU) - UM'),
('Mauritian Rupee (MUR) - ₨','Mauritian Rupee (MUR) - ₨'),
('Moroccan Dirham (MAD) - د.م.','Moroccan Dirham (MAD) - د.م.'),
('Mozambican Metical (MZN) - MT','Mozambican Metical (MZN) - MT'),
('MXN (Mexican Peso) - $','MXN (Mexican Peso) - $'),
('MYR (Malaysian Ringgit) - RM','MYR (Malaysian Ringgit) - RM'),
('Namibian Dollar (NAD) - $','Namibian Dollar (NAD) - $'),
('NGN (Nigerian Naira) - ₦','NGN (Nigerian Naira) - ₦'),
('NOK (Norwegian Krone) - kr','NOK (Norwegian Krone) - kr'),
('NZD (New Zealand Dollar) - NZ$','NZD (New Zealand Dollar) - NZ$'),
('PHP (Philippine Peso) - ₱','PHP (Philippine Peso) - ₱'),
('PKR (Pakistani Rupee) - ₨','PKR (Pakistani Rupee) - ₨'),
('PLN (Polish Zloty) - zł','PLN (Polish Zloty) - zł'),
('RON (Romanian Leu) - lei','RON (Romanian Leu) - lei'),
('RUB (Russian Ruble) - ₽','RUB (Russian Ruble) - ₽'),
('Rwandan Franc (RWF)','Rwandan Franc (RWF)'),
('São Tomé and Príncipe Dobra (STN) - Db','São Tomé and Príncipe Dobra (STN) - Db'),
('SAR (Saudi Riyal) - ﷼','SAR (Saudi Riyal) - ﷼'),
('SEK (Swedish Krona) - kr','SEK (Swedish Krona) - kr'),
('Seychellois Rupee (SCR) - ₨','Seychellois Rupee (SCR) - ₨'),
('SGD (Singapore Dollar) - S$','SGD (Singapore Dollar) - S$'),
('Sierra Leonean Leone (SLL) - Le','Sierra Leonean Leone (SLL) - Le'),
('Somali Shilling (SOS) - Sh.So.','Somali Shilling (SOS) - Sh.So.'),
('South African Rand (ZAR) - R','South African Rand (ZAR) - R'),
('South Sudanese Pound (SSP)','South Sudanese Pound (SSP)'),
('Sudanese Pound (SDG) - ج.س','Sudanese Pound (SDG) - ج.س'),
('Swazi Lilangeni (SZL) - L','Swazi Lilangeni (SZL) - L'),
('SYP (Syrian Pound) - £ or ل.س','SYP (Syrian Pound) - £ or ل.س'),
('Tanzanian Shilling (TZS) - Sh','Tanzanian Shilling (TZS) - Sh'),
('THB (Thai Baht) - ฿','THB (Thai Baht) - ฿'),
('TRY (Turkish Lira) - ₺','TRY (Turkish Lira) - ₺'),
('Tunisian Dinar (TND) - د.ت','Tunisian Dinar (TND) - د.ت'),
('TWD (New Taiwan Dollar) - NT$','TWD (New Taiwan Dollar) - NT$'),
('Ugandan Shilling (UGX) - USh','Ugandan Shilling (UGX) - USh'),
('USD (United States Dollar) - $','USD (United States Dollar) - $'),
('West African CFA Franc (XOF) - CFA','West African CFA Franc (XOF) - CFA'),
('Zambian Kwacha (ZMW) - ZK','Zambian Kwacha (ZMW) - ZK'),
('ZAR (South African Rand) - R','ZAR (South African Rand) - R'),
('Zimbabwean Dollar (ZWL) - $','Zimbabwean Dollar (ZWL) - $'),
]

DISCOUNTS = [
    ('5%','5%'),
    ('10%','10%'),
    ('15%','15%'),
    ('20%','20%'),
   
]