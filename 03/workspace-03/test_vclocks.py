from vector_clock import VectorClock

# Simulate a system with 3 processes
vc0 = VectorClock(num_processes=3, process_id=0)
vc1 = VectorClock(num_processes=3, process_id=1)
vc2 = VectorClock(num_processes=3, process_id=2)

print("Inisialisasi Awal:")
print(vc0)
print(vc1)
print(vc2)

print("\n--- Event 1: P0 Melakukan Local Event ---")
vc0.increment()
print(vc0)

print("\n--- Event 2: P0 Mengirim Pesan ke P1 ---")
message_from_p0 = vc0.send_message()
vc1.receive_message(message_from_p0)
print(vc0)
print(vc1)

print("\n--- Event 3: P2 Melakukan Local Event ---")
vc2.increment()
print(vc2)

print("\n--- Event 4: P1 Mengirim Pesan ke P2 ---")
message_from_p1 = vc1.send_message()
vc2.receive_message(message_from_p1)
print(vc1)
print(vc2)

print("\n--- Cek Kausalitas (Causality Check) ---")
print(f"vc0 happens before vc1: {vc0.happens_before(vc1)}")
print(f"vc1 happens before vc0: {vc1.happens_before(vc0)}")
print(f"vc0 is concurrent with vc2: {vc0.is_concurrent(vc2)}")