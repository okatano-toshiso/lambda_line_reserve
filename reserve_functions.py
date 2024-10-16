import xmlrpc.client
import re
from datetime import datetime, timedelta

def create_tentative_reserve_info(hotel_code, line_reserve_data, line_user_data):
    processDiv = "0"
    arrivalTime = "160000"
    departureTime = "100000"
    man = "1"
    female = "0"
    child = "0"
    copNmKanji = ""
    copTel = ""
    guestSex1 = "1"
    guestPointDiv1 = "0"
    ntnltyCode1 = "JPN"
    freeTicket = "0"
    rooms1 = "1"
    roomChg1 = "10000"
    vcntType1 = "0001"
    rsvRecptTime = "100000"
    payWayCd1 = "1"
    claimAhCd1 = "1"
    payWayCd2 = "1"
    centerPsnCd = "99999"
    rsvRecptPlace = "LINE"
    rsvRecptPsn = "予約JPN"
    arrivalDay = line_reserve_data["check_in"].strftime("%Y%m%d")
    stays = (line_reserve_data["check_out"] - line_reserve_data["check_in"]).days
    departureDay = line_reserve_data["check_out"].strftime("%Y%m%d")
    rsvNmKanji = line_reserve_data["name"]
    rsvNmKana = line_user_data["name_kana"]
    rsvTel = line_reserve_data["phone_number"]
    guestNmKanji1 = line_reserve_data["name"]
    guestNmKana1 = line_user_data["name_kana"]
    guestTel1 = line_reserve_data["phone_number"]
    roomTypeCd1 = re.search(r'\((.*?)\)', line_reserve_data["room_type"]).group(1) if re.search(r'\((.*?)\)', line_reserve_data["room_type"]) else None
    people1 = line_reserve_data["count_of_person"]
    rsvRecptDay = line_reserve_data["reservation_date"].strftime("%Y%m%d")
    # each_day_room_charge_info
    roomTypeDiv = "1"
    cstWebRoomChg = "10000"
    gnrWebRoomChg = "10000"
    ecoFlag = "0"
    dscntRate = "20"
    netCstWebRoomChg = "10000"
    netGnrWebRoomChg = "10000"
    dscntWebChg = "20"
    stayTaxFlag = "0"
    stayTax = "0"

    room_days = [(line_reserve_data["check_in"] + timedelta(days=i)).strftime('%Y%m%d') for i in range(stays)]
    print(room_days)

    def create_each_day_room_charge_info(
            roomTypeDiv,
            date,
            cstWebRoomChg,
            gnrWebRoomChg,
            ecoFlag,
            dscntRate,
            netCstWebRoomChg,
            netGnrWebRoomChg,
            dscntWebChg,
            stayTaxFlag,
            stayTax
        ):
        each_day_room_charge_info = {
            "roomTypeDiv": roomTypeDiv,
            "stayingDay": date,
            "cstWebRoomChg": cstWebRoomChg,
            "gnrWebRoomChg": gnrWebRoomChg,
            "ecoFlag": ecoFlag,
            "dscntRate": dscntRate,
            "netCstWebRoomChg": netCstWebRoomChg,
            "netGnrWebRoomChg": netGnrWebRoomChg,
            "dscntWebChg": dscntWebChg,
            "stayTaxFlag": stayTaxFlag,
            "stayTax": stayTax,
            "cpnCode": "",
            "cpnName": "",
            "cpnAmnt": "",
            "cpnIssClssfctn": "",
            "cpnClssfctn": ""
        }
        return each_day_room_charge_info

    tentative_reserve_info = {
        "hotelCd": hotel_code,
        "reserveNo": str(line_reserve_data["reservation_id"]),
        "processDiv": processDiv,
        "arrivalDay": arrivalDay,
        "arrivalTime": arrivalTime,
        "stays": str(stays),
        "departureDay": departureDay,
        "departureTime": departureTime,
        "man": man,
        "female": female,
        "child": child,
        "rsvNmKanji": rsvNmKanji,
        "rsvNmKana": rsvNmKana,
        "rsvTel": rsvTel,
        "copNmKanji": copNmKanji,
        "copTel": copTel,
        "guestNmKanji1": guestNmKanji1,
        "guestNmKana1": guestNmKana1,
        "guestSex1": guestSex1,
        "guestTel1": guestTel1,
        "guestPointDiv1": guestPointDiv1,
        "ntnltyCode1": ntnltyCode1,
        "freeTicket": freeTicket,
        "roomTypeCd1": roomTypeCd1,
        "people1": str(people1),
        "rooms1": rooms1,
        "roomChg1": roomChg1,
        "vcntType1": vcntType1,
        "people2": "",
        "rooms2": "",
        "roomChg2": "",
        "people3": "",
        "rooms3": "",
        "roomChg3": "",
        "lodDivCd": "",
        "dsctDivCd": "",
        "rsvRecptDay": rsvRecptDay,
        "rsvRecptTime": rsvRecptTime,
        "payWayCd1": payWayCd1,
        "claimAhCd1": claimAhCd1,
        "payWayCd2": payWayCd2,
        "centerPsnCd": centerPsnCd,
        "rsvRecptPlace": rsvRecptPlace,
        "rsvRecptPsn": rsvRecptPsn
    }

    tentative_reserve_info["edRoomChgInfo"] = [
        create_each_day_room_charge_info(
            roomTypeDiv,
            date,
            cstWebRoomChg,
            gnrWebRoomChg,
            ecoFlag,
            dscntRate,
            netCstWebRoomChg,
            netGnrWebRoomChg,
            dscntWebChg,
            stayTaxFlag,
            stayTax
        )
        for date in room_days
    ]
    return tentative_reserve_info

def create_tentative_reserve(hotel_code, line_reserve_data, line_user_data):
    info_list = [create_tentative_reserve_info(hotel_code, line_reserve_data, line_user_data)]
    return {
        "hotelCd": hotel_code,
        "trsvInfoList": info_list
    }

def send_reservation_request(url, tentative_reserve):
    try:
        with xmlrpc.client.ServerProxy(url) as server:
            method = server.__getattr__(
                "com.toyokoinn.api.hns.service.WebReserveService.entryTentativeReserve"
            )
            xml_result = method.__call__(tentative_reserve)
        print(f"Response from server: {xml_result}")

    except Exception as e:
        print(f"Failed to connect or communicate with the server: {str(e)}")
