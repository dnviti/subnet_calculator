import argparse
import json

def ip_to_str(ip):
    return ".".join(map(str, ip))


def increment_ip_address(ip, increment=1):
    new_ip = ip.copy()
    for i in range(3, -1, -1):
        new_ip[i] += increment
        increment, new_ip[i] = divmod(new_ip[i], 256)
    return new_ip


def convert_to_decimal_mask(host_bits):
    mask_bits = 32 - host_bits
    mask = [0, 0, 0, 0]
    for i in range(mask_bits):
        mask[i // 8] += 1 << (7 - i % 8)
    return ip_to_str(mask)


def calculate_subnet(base_ip, host_bits, subnet_number, output_file):
    total_hosts_by_subnet = 2**host_bits
    network_address = base_ip
    first_host = increment_ip_address(network_address)
    broadcast = increment_ip_address(network_address, total_hosts_by_subnet - 1)
    last_host = increment_ip_address(broadcast, -1)
    subnet_mask_decimal = convert_to_decimal_mask(host_bits)
    
    output = (
        f"----------------------------\n"
        f"Sottorete {subnet_number}:\n"
        f"Rete: {ip_to_str(network_address)}\n"
        f"Primo: {ip_to_str(first_host)}\n"
        f"Ultimo: {ip_to_str(last_host)}\n"
        f"Broadcast: {ip_to_str(broadcast)}\n"
        f"Subnet Mask: /{32 - host_bits} ({subnet_mask_decimal})\n"
        f"Numero di hosts per sottorete: {total_hosts_by_subnet}\n"
    )
    print(output, file=output_file)

    spiegazioni = (
        "Spiegazione dei calcoli:\n"
        f"1. Calcolo della Subnet Mask: Per {total_hosts_by_subnet} indirizzi (inclusi rete e broadcast), "
        f"sono necessari {host_bits} bit. La Subnet Mask quindi /{32 - host_bits} ({subnet_mask_decimal}).\n"
        f"2. Indirizzo di Rete: {ip_to_str(network_address)}. Gli ultimi {host_bits} bit sono 0.\n"
        f"3. Primo Host: {ip_to_str(first_host)}. L'indirizzo di rete + 1.\n"
        f"4. Ultimo Host: {ip_to_str(last_host)}. L'indirizzo di broadcast - 1.\n"
        f"5. Indirizzo di Broadcast: {ip_to_str(broadcast)}. Gli ultimi {host_bits} bit sono 1.\n"
    )
    print(spiegazioni, file=output_file)
    return broadcast

def calculate_subnets(args, output_file):
    base_ip = list(map(int, args.ip.split(".")))
    subnet_type = "FLSM"  # Default a FLSM
    subnet_count = 0

    if isinstance(args.hosts, list):
        subnet_type = "VLSM"
        for hosts in args.hosts:
            host_bits = 0
            while (2**host_bits) < (hosts + 2):
                host_bits += 1
            subnet_count += 1
            base_ip = increment_ip_address(
                calculate_subnet(base_ip, host_bits, subnet_count, output_file)
            )
            if base_ip[3] == 0:
                break
    else:
        host_bits = 0
        while (2**host_bits) < (args.hosts + 2):
            host_bits += 1
        while args.subnets is None or subnet_count < args.subnets:
            subnet_count += 1
            base_ip = increment_ip_address(
                calculate_subnet(base_ip, host_bits, subnet_count, output_file)
            )
            if base_ip[3] == 0:
                break

    return subnet_type

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calcola sottoreti usando FLSM o VLSM."
    )
    parser.add_argument(
        "--ip", type=str, help="Indirizzo IP di base della rete."
    )
    parser.add_argument(
        "--hosts",
        nargs="+",
        type=int,
        help="Numero di hosts richiesto per sottorete o lista di host per ogni sottorete per VLSM.",
    )
    parser.add_argument(
        "--subnets",
        type=int,
        help="Numero di sottoreti da visualizzare (opzionale per FLSM).",
    )
    parser.add_argument(
        "--config",
        type=str,
        default="config.json",
        help="File JSON con la configurazione (opzionale).",
    )
    parser.add_argument(
        "--output", type=str, help="Percorso del file di output (opzionale)."
    )

    args = parser.parse_args(args=[])

    # Carica la configurazione dal file JSON
    if args.config:
        try:
            with open(args.config, "r") as config_file:
                config = json.load(config_file)
                args.ip = config.get("ip", args.ip)
                args.hosts = config.get("hosts", args.hosts)
                args.subnets = config.get("subnets", args.subnets)
        except FileNotFoundError:
            print(
                f"File di configurazione {args.config} non trovato. Utilizzo valori di default."
            )

    # Imposta il nome del file di output basato sull'indirizzo IP, se non specificato
    output_filename = (
        args.output if args.output else f"{args.ip.replace('.', '_')}_output.txt"
    )
    output_file = open(output_filename, "w")

    info = (
        f"\nIndirizzo IP di base: {args.ip}\n"
        f"Numero di hosts richiesto: {args.hosts}\n"
        f"Numero di sottoreti: {args.subnets}\n"
    )
    print(info, file=output_file)

    subnet_type = calculate_subnets(args, output_file)
    print(f"\nApproccio utilizzato: {subnet_type}", file=output_file)

    output_file.close()
