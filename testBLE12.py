import Penguin_scanner as p_scanner

input_address = "f4:e7:24:45:42:b1"
MAC, PN, SoC, Temperature = p_scanner.run_scanner(input_address)
print(f'MAC: {MAC} | PN: {PN} | SoC: {SoC}% | Temperature: {Temperature}F')