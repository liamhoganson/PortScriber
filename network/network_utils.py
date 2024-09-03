def cisco_mac_address_formatter(mac_address):
    formatter = [
        mac_address.replace(":", "")[i : i + 4]
        for i in range(0, len(mac_address), 4)
    ]
    formatter = [element + "." for element in formatter]
    formatted_mac_address = "".join(formatter)[:-3]
    return formatted_mac_address
