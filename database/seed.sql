-- Seed data for VoiceCRM database
-- This populates the database with example data for testing

-- Insert demo users
INSERT INTO users (email, password_hash, name, role) VALUES
-- Password for all demo users: "demo1234"
-- Hash generated with: bcrypt.hashpw("demo1234", bcrypt.gensalt(rounds=12))
('demo@voicecrm.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewYWk/FqZ5T6FXQK', 'Demo User', 'user'),
('admin@voicecrm.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewYWk/FqZ5T6FXQK', 'Admin User', 'admin'),
('comercial@voicecrm.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewYWk/FqZ5T6FXQK', 'Juan Comercial', 'user');

-- Insert companies
INSERT INTO companies (name, sector, size, employees, revenue, website, country, city) VALUES
('Acme Corporation', 'Technology', 'Large', 500, 15000000, 'https://acmecorp.com', 'España', 'Madrid'),
('TechStart Solutions', 'Software', 'Medium', 120, 3500000, 'https://techstart.io', 'España', 'Barcelona'),
('Global Consulting Group', 'Consulting', 'Large', 800, 25000000, 'https://globalconsult.com', 'España', 'Madrid'),
('Innovatech', 'Technology', 'Small', 35, 800000, 'https://innovatech.es', 'España', 'Valencia'),
('Digital Marketing Pro', 'Marketing', 'Medium', 90, 2100000, 'https://digitalmp.com', 'España', 'Sevilla'),
('Cloud Services SA', 'Cloud Computing', 'Large', 450, 12000000, 'https://cloudservices.com', 'España', 'Madrid'),
('StartupHub', 'Incubadora', 'Small', 25, 500000, 'https://startuphub.es', 'España', 'Bilbao'),
('Retail Excellence', 'Retail', 'Large', 1200, 35000000, 'https://retailex.com', 'España', 'Barcelona'),
('FinTech Innovations', 'Finanzas', 'Medium', 180, 5500000, 'https://fintechinn.com', 'España', 'Madrid'),
('EduTech Platform', 'Educación', 'Small', 45, 950000, 'https://edutech.es', 'España', 'Granada');

-- Insert contacts
INSERT INTO contacts (company_id, name, surname, position, email, phone_mobile, lead_type, lead_status, lead_source) VALUES
-- Acme Corporation
(1, 'Germán', 'Palomares', 'CTO', 'german.palomares@acmecorp.com', '+34 600 111 222', 'client', 'qualified', 'referral'),
(1, 'Laura', 'Martínez', 'CEO', 'laura.martinez@acmecorp.com', '+34 600 111 223', 'client', 'qualified', 'web'),
(1, 'Carlos', 'Rodríguez', 'Product Manager', 'carlos.rodriguez@acmecorp.com', '+34 600 111 224', 'client', 'contacted', 'event'),

-- TechStart Solutions
(2, 'María', 'González', 'Founder & CEO', 'maria.gonzalez@techstart.io', '+34 611 222 333', 'prospect', 'qualified', 'web'),
(2, 'Javier', 'López', 'CTO', 'javier.lopez@techstart.io', '+34 611 222 334', 'prospect', 'contacted', 'web'),

-- Global Consulting
(3, 'Ana', 'Fernández', 'Directora de Operaciones', 'ana.fernandez@globalconsult.com', '+34 622 333 444', 'client', 'qualified', 'referral'),
(3, 'Roberto', 'Sánchez', 'Consultor Senior', 'roberto.sanchez@globalconsult.com', '+34 622 333 445', 'client', 'contacted', 'email'),

-- Innovatech
(4, 'Elena', 'Torres', 'CEO', 'elena.torres@innovatech.es', '+34 633 444 555', 'lead', 'new', 'social_media'),
(4, 'Diego', 'Ramírez', 'Desarrollador Lead', 'diego.ramirez@innovatech.es', '+34 633 444 556', 'lead', 'contacted', 'web'),

-- Digital Marketing Pro
(5, 'Sofía', 'Moreno', 'CMO', 'sofia.moreno@digitalmp.com', '+34 644 555 666', 'prospect', 'qualified', 'event'),
(5, 'Miguel', 'Jiménez', 'Account Manager', 'miguel.jimenez@digitalmp.com', '+34 644 555 667', 'prospect', 'contacted', 'referral'),

-- Cloud Services SA
(6, 'Patricia', 'Ruiz', 'Directora Comercial', 'patricia.ruiz@cloudservices.com', '+34 655 666 777', 'client', 'qualified', 'web'),
(6, 'Alberto', 'Navarro', 'Arquitecto Cloud', 'alberto.navarro@cloudservices.com', '+34 655 666 778', 'client', 'qualified', 'referral'),

-- StartupHub
(7, 'Carmen', 'Díaz', 'Community Manager', 'carmen.diaz@startuphub.es', '+34 666 777 888', 'lead', 'contacted', 'event'),

-- Retail Excellence
(8, 'Fernando', 'Gutiérrez', 'Director de Expansión', 'fernando.gutierrez@retailex.com', '+34 677 888 999', 'prospect', 'qualified', 'email'),
(8, 'Isabel', 'Castro', 'CFO', 'isabel.castro@retailex.com', '+34 677 888 990', 'prospect', 'contacted', 'web'),

-- FinTech Innovations
(9, 'Andrés', 'Vega', 'CEO', 'andres.vega@fintechinn.com', '+34 688 999 000', 'client', 'qualified', 'referral'),
(9, 'Beatriz', 'Romero', 'Head of Product', 'beatriz.romero@fintechinn.com', '+34 688 999 001', 'client', 'contacted', 'web'),

-- EduTech Platform
(10, 'Luis', 'Herrera', 'Fundador', 'luis.herrera@edutech.es', '+34 699 000 111', 'lead', 'new', 'social_media'),
(10, 'Marta', 'Iglesias', 'Directora Pedagógica', 'marta.iglesias@edutech.es', '+34 699 000 112', 'lead', 'contacted', 'event');

-- Insert sample interactions (assumes user_id = 1 for demo user)
INSERT INTO interactions (user_id, contact_id, type, interaction_date, transcript, notes) VALUES
(1, 1, 'meeting', '2025-11-15 10:00:00', 'Reunión con Germán Palomares para revisar propuesta de migración cloud', 'Muy interesado en la solución. Presupuesto aprox. 50K€. Decisión en 2 semanas.'),
(1, 1, 'call', '2025-11-10 15:30:00', 'Llamada de seguimiento sobre el proyecto', 'Aclaradas dudas técnicas. Solicita demo técnica.'),
(1, 4, 'meeting', '2025-11-12 11:00:00', 'Primera reunión con María González de TechStart', 'Buscan solución de CRM integrada. Budget 20K€.'),
(1, 6, 'call', '2025-11-08 09:00:00', 'Llamada con Ana Fernández', 'Interés en servicios de consultoría. Programar reunión presencial.'),
(1, 10, 'email', '2025-11-05 14:00:00', 'Email de presentación a Sofía Moreno', 'Enviada propuesta inicial de marketing automation.'),
(1, 12, 'meeting', '2025-11-14 16:00:00', 'Reunión con Patricia Ruiz de Cloud Services', 'Discutimos integración con sus sistemas actuales. Muy positiva.'),
(1, 17, 'call', '2025-11-11 12:00:00', 'Llamada con Andrés Vega', 'Confirma interés. Quiere propuesta formal esta semana.');

-- Insert sample opportunities
INSERT INTO opportunities (contact_id, title, value, probability, stage, close_date) VALUES
(1, 'Migración Cloud Acme Corp', 50000, 75, 'negotiation', '2025-12-01'),
(4, 'Implementación CRM TechStart', 20000, 60, 'proposal', '2025-12-15'),
(6, 'Consultoría Digital Transformation', 35000, 50, 'qualification', '2026-01-10'),
(10, 'Marketing Automation Platform', 15000, 40, 'prospecting', '2026-01-20'),
(12, 'Cloud Infrastructure Upgrade', 80000, 80, 'negotiation', '2025-11-30'),
(17, 'FinTech Integration Project', 45000, 70, 'proposal', '2025-12-10');

-- Summary
SELECT 'Database seeded successfully!' as message;
SELECT COUNT(*) as user_count FROM users;
SELECT COUNT(*) as company_count FROM companies;
SELECT COUNT(*) as contact_count FROM contacts;
SELECT COUNT(*) as interaction_count FROM interactions;
SELECT COUNT(*) as opportunity_count FROM opportunities;
