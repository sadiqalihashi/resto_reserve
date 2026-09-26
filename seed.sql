INSERT INTO tables (table_number, capacity, status) VALUES
('1', 2, 'available'),
('2', 2, 'occupied'),
('3', 4, 'available'),
('4', 4, 'reserved'),
('5', 6, 'available'),
('6', 6, 'occupied'),
('7', 8, 'available'),
('8', 4, 'reserved');

INSERT INTO reservations (customer_name, phone_number, party_size, table_id, reservation_time, status)
SELECT 'Grace Wanjiru', '0722123456', 4, id, NOW() + INTERVAL '2 hours', 'confirmed'
FROM tables WHERE table_number = '4';

INSERT INTO reservations (customer_name, phone_number, party_size, table_id, reservation_time, status)
SELECT 'Brian Otieno', '0733987654', 3, id, NOW() + INTERVAL '4 hours', 'confirmed'
FROM tables WHERE table_number = '8';

INSERT INTO reservations (customer_name, phone_number, party_size, table_id, reservation_time, status)
SELECT 'Amina Yusuf', '0700111222', 2, id, NOW() + INTERVAL '1 day', 'confirmed'
FROM tables WHERE table_number = '1';