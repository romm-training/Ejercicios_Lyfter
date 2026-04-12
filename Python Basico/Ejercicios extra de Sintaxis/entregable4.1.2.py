seconds_threshold = 600
seconds_to_threshold = 0
result = "Mayor"
seconds = int(input("Ingrese los segundos: "))

if seconds < seconds_threshold:
    seconds_to_threshold = seconds_threshold - seconds
    result = f"Faltan {seconds_to_threshold} segundos para {seconds_threshold}"
elif seconds == seconds_threshold:
    result = "Igual"

print(result)