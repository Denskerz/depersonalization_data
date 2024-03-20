import os
import re
import hashlib
import logging
import time
from re import Match
from pathlib import Path


def time_ms():
    return round(time.time() * 1000)


def hashing(line: str, personal_data: str) -> str:
    coincidence: Match[str] | None = re.search(personal_data, line)
    if coincidence is not None:
        tmp = hashlib.md5(str(coincidence).encode())
        return tmp.hexdigest()
    return None


file_log = logging.FileHandler('Log.log')
console_out = logging.StreamHandler()
logging.basicConfig(level=logging.DEBUG, handlers=(file_log, console_out), format="[%(asctime)s | %(levelname)s]: %(message)s", datefmt='%m.%d.%Y %H:%M:%S')

ROOT_PATH = Path(__file__).resolve().parents[0]
DOTENV_PATH = os.path.join(ROOT_PATH, ".env")

REGEXP_EXAMPLE='(?i)(?<=<EXAMPLE>).+?(?=</EXAMPLE>)|(?<=\"EXAMPLE\":\").+?(?=\")|(?i)(?<=<tns:EXAMPLE>).+?(?=</tns:EXAMPLE>)|(?<=\"tns:EXAMPLE\":\").+?(?=\")'

ATTRIBUTES='CRMID,CRMApplicationID,ClientCRMID,LastName,FirstName,MiddleName,Email,ForProblZone,ReplacementFlag,BirthDate,Sex,Citizenship,RelationMilitary,EndDateDeferment,InfoResourcesAgree,InfoResourcesAgreeNumber,UNP,IBSO_ID,RegistrationNumber,RegistrationDate,StreetAddress,StreetAddressTypeCode,House,ApartmentNumber,Number,PartyDisplayName,PersonalNumber,IssueAuthority,IssueDate,ExpiryDate,City,Building,CategoryRelationship,CompanyNameFull'

pattern_list: list = ATTRIBUTES.split(',')
for pattern_number in range(len(pattern_list)):
    pattern_list[pattern_number] = re.sub(pattern="(?i)EXAMPLE", repl=pattern_list[pattern_number], string=REGEXP_EXAMPLE)

source = []

#listdir = os.listdir(f'{ROOT_PATH}/input_data')
