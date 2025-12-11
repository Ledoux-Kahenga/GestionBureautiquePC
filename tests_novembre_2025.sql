-- Données de test pour novembre 2025
-- Structure: transactions(id, type, montant, description, date, created_at, type_depense)
-- type: 'recette', 'depense', 'apport'
-- type_depense: 'normale', 'speciale'

-- Novembre 2025: 30 jours (du 2025-11-01 au 2025-11-29)

-- Jour 1: 2025-11-01 (Samedi)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 45000, 'Impression affiches publicitaires', '2025-11-01', '2025-11-01 08:15:23', 'normale'),
('recette', 12500, 'Photocopies documents', '2025-11-01', '2025-11-01 09:30:45', 'normale'),
('recette', 28000, 'Impression cartes de visite', '2025-11-01', '2025-11-01 11:20:12', 'normale'),
('depense', 8500, 'Achat papier A4', '2025-11-01', '2025-11-01 14:00:00', 'normale'),
('depense', 3000, 'Transport marchandises', '2025-11-01', '2025-11-01 16:30:00', 'normale');

-- Jour 2: 2025-11-02 (Dimanche)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 18500, 'Reliure documents', '2025-11-02', '2025-11-02 09:00:00', 'normale'),
('recette', 52000, 'Impression calendriers 2026', '2025-11-02', '2025-11-02 10:45:30', 'normale'),
('depense', 15000, 'Achat encre imprimante', '2025-11-02', '2025-11-02 15:20:00', 'normale');

-- Jour 3: 2025-11-03 (Lundi)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 38000, 'Impression brochures', '2025-11-03', '2025-11-03 08:30:15', 'normale'),
('recette', 22000, 'Plastification documents', '2025-11-03', '2025-11-03 10:15:40', 'normale'),
('recette', 15000, 'Photocopies couleur', '2025-11-03', '2025-11-03 12:00:00', 'normale'),
('depense', 5500, 'Électricité', '2025-11-03', '2025-11-03 14:30:00', 'normale'),
('depense', 12000, 'Maintenance machine', '2025-11-03', '2025-11-03 16:00:00', 'normale'),
('apport', 100000, 'Apport capital pour expansion', '2025-11-03', '2025-11-03 17:00:00', 'speciale');

-- Jour 4: 2025-11-04 (Mardi)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 48000, 'Impression flyers événement', '2025-11-04', '2025-11-04 08:00:00', 'normale'),
('recette', 31000, 'Cartes de vœux personnalisées', '2025-11-04', '2025-11-04 10:30:00', 'normale'),
('recette', 19500, 'Scan et impression photos', '2025-11-04', '2025-11-04 13:45:00', 'normale'),
('depense', 7000, 'Fournitures bureau', '2025-11-04', '2025-11-04 15:00:00', 'normale'),
('depense', 25000, 'Achat nouvel ordinateur', '2025-11-04', '2025-11-04 16:30:00', 'speciale');

-- Jour 5: 2025-11-05 (Mercredi)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 55000, 'Impression banderoles grand format', '2025-11-05', '2025-11-05 08:45:00', 'normale'),
('recette', 26000, 'Reliure thèses universitaires', '2025-11-05', '2025-11-05 11:00:00', 'normale'),
('recette', 14000, 'Photocopies N&B', '2025-11-05', '2025-11-05 14:30:00', 'normale'),
('depense', 6500, 'Internet mensuel', '2025-11-05', '2025-11-05 16:00:00', 'normale'),
('depense', 4000, 'Eau', '2025-11-05', '2025-11-05 16:15:00', 'normale');

-- Jour 6: 2025-11-06 (Jeudi)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 42000, 'Impression menus restaurant', '2025-11-06', '2025-11-06 09:15:00', 'normale'),
('recette', 17500, 'Badges événement', '2025-11-06', '2025-11-06 11:45:00', 'normale'),
('recette', 33000, 'Impression dépliants touristiques', '2025-11-06', '2025-11-06 14:00:00', 'normale'),
('depense', 9000, 'Achat papier photo', '2025-11-06', '2025-11-06 15:30:00', 'normale');

-- Jour 7: 2025-11-07 (Vendredi)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 61000, 'Impression packagings produits', '2025-11-07', '2025-11-07 08:00:00', 'normale'),
('recette', 29000, 'Tampons personnalisés', '2025-11-07', '2025-11-07 10:30:00', 'normale'),
('recette', 18000, 'Plastification menus', '2025-11-07', '2025-11-07 13:00:00', 'normale'),
('depense', 11000, 'Salaire employé 1', '2025-11-07', '2025-11-07 17:00:00', 'normale'),
('depense', 11000, 'Salaire employé 2', '2025-11-07', '2025-11-07 17:05:00', 'normale');

-- Jour 8: 2025-11-08 (Samedi)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 37000, 'Impression invitations mariage', '2025-11-08', '2025-11-08 09:00:00', 'normale'),
('recette', 23000, 'Cartes de remerciement', '2025-11-08', '2025-11-08 11:30:00', 'normale'),
('recette', 16500, 'Photocopies couleur A3', '2025-11-08', '2025-11-08 14:45:00', 'normale'),
('depense', 8000, 'Réparation imprimante', '2025-11-08', '2025-11-08 16:00:00', 'normale');

-- Jour 9: 2025-11-09 (Dimanche)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 28000, 'Impression certificats', '2025-11-09', '2025-11-09 10:00:00', 'normale'),
('recette', 41000, 'Brochures entreprise', '2025-11-09', '2025-11-09 12:30:00', 'normale'),
('depense', 5000, 'Nettoyage local', '2025-11-09', '2025-11-09 15:00:00', 'normale');

-- Jour 10: 2025-11-10 (Lundi)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 53000, 'Impression étiquettes produits', '2025-11-10', '2025-11-10 08:30:00', 'normale'),
('recette', 24000, 'Cartes de membre association', '2025-11-10', '2025-11-10 10:45:00', 'normale'),
('recette', 19000, 'Reliure rapports annuels', '2025-11-10', '2025-11-10 13:15:00', 'normale'),
('depense', 13000, 'Achat toner laser', '2025-11-10', '2025-11-10 15:00:00', 'normale'),
('depense', 6000, 'Transport livraison', '2025-11-10', '2025-11-10 16:30:00', 'normale'),
('depense', 35000, 'Paiement loyer mensuel', '2025-11-10', '2025-11-10 17:00:00', 'speciale');

-- Jour 11: 2025-11-11 (Mardi)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 46000, 'Impression posters cinéma', '2025-11-11', '2025-11-11 08:15:00', 'normale'),
('recette', 32000, 'Faire-part naissance', '2025-11-11', '2025-11-11 11:00:00', 'normale'),
('recette', 21000, 'Photocopies documents juridiques', '2025-11-11', '2025-11-11 14:30:00', 'normale'),
('depense', 7500, 'Achat agrafeuses professionnelles', '2025-11-11', '2025-11-11 16:00:00', 'normale');

-- Jour 12: 2025-11-12 (Mercredi)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 58000, 'Impression catalogues produits', '2025-11-12', '2025-11-12 08:00:00', 'normale'),
('recette', 27000, 'Badges employés entreprise', '2025-11-12', '2025-11-12 10:30:00', 'normale'),
('recette', 15500, 'Plastification cartes', '2025-11-12', '2025-11-12 13:45:00', 'normale'),
('depense', 10000, 'Maintenance climatisation', '2025-11-12', '2025-11-12 15:30:00', 'normale'),
('depense', 4500, 'Fournitures diverses', '2025-11-12', '2025-11-12 16:45:00', 'normale');

-- Jour 13: 2025-11-13 (Jeudi)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 39000, 'Impression dossiers présentation', '2025-11-13', '2025-11-13 09:00:00', 'normale'),
('recette', 25000, 'Cartes de fidélité commerce', '2025-11-13', '2025-11-13 11:30:00', 'normale'),
('recette', 17000, 'Reliure mémoires', '2025-11-13', '2025-11-13 14:00:00', 'normale'),
('depense', 8500, 'Achat papier cartonné', '2025-11-13', '2025-11-13 16:00:00', 'normale');

-- Jour 14: 2025-11-14 (Vendredi)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 64000, 'Impression panneaux publicitaires', '2025-11-14', '2025-11-14 08:30:00', 'normale'),
('recette', 30000, 'Impression T-shirts événement', '2025-11-14', '2025-11-14 11:00:00', 'normale'),
('recette', 22000, 'Photocopies plans architecture', '2025-11-14', '2025-11-14 14:30:00', 'normale'),
('depense', 11000, 'Salaire employé 1', '2025-11-14', '2025-11-14 17:00:00', 'normale'),
('depense', 11000, 'Salaire employé 2', '2025-11-14', '2025-11-14 17:05:00', 'normale'),
('depense', 9000, 'Charges sociales', '2025-11-14', '2025-11-14 17:15:00', 'normale');

-- Jour 15: 2025-11-15 (Samedi)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 43000, 'Impression menus carte', '2025-11-15', '2025-11-15 09:15:00', 'normale'),
('recette', 26500, 'Invitations événement corporate', '2025-11-15', '2025-11-15 12:00:00', 'normale'),
('recette', 18500, 'Scan documents anciens', '2025-11-15', '2025-11-15 15:00:00', 'normale'),
('depense', 6500, 'Réparation perforeuse', '2025-11-15', '2025-11-15 16:30:00', 'normale'),
('apport', 50000, 'Injection de capital', '2025-11-15', '2025-11-15 17:30:00', 'speciale');

-- Jour 16: 2025-11-16 (Dimanche)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 35000, 'Impression flyers concert', '2025-11-16', '2025-11-16 10:00:00', 'normale'),
('recette', 20000, 'Reliure documents officiels', '2025-11-16', '2025-11-16 13:00:00', 'normale'),
('depense', 4000, 'Achat papier couleur', '2025-11-16', '2025-11-16 15:00:00', 'normale');

-- Jour 17: 2025-11-17 (Lundi)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 51000, 'Impression livrets formation', '2025-11-17', '2025-11-17 08:00:00', 'normale'),
('recette', 28500, 'Cartes postales touristiques', '2025-11-17', '2025-11-17 10:30:00', 'normale'),
('recette', 16000, 'Photocopies N&B A4', '2025-11-17', '2025-11-17 13:45:00', 'normale'),
('depense', 12000, 'Achat plastifieuse neuve', '2025-11-17', '2025-11-17 15:00:00', 'speciale'),
('depense', 7000, 'Électricité', '2025-11-17', '2025-11-17 16:00:00', 'normale');

-- Jour 18: 2025-11-18 (Mardi)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 47000, 'Impression programmes événement', '2025-11-18', '2025-11-18 08:45:00', 'normale'),
('recette', 33000, 'Badges conférence', '2025-11-18', '2025-11-18 11:15:00', 'normale'),
('recette', 19500, 'Plastification certificats', '2025-11-18', '2025-11-18 14:00:00', 'normale'),
('depense', 8000, 'Maintenance ordinateurs', '2025-11-18', '2025-11-18 16:00:00', 'normale');

-- Jour 19: 2025-11-19 (Mercredi)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 56000, 'Impression brochures hôtel', '2025-11-19', '2025-11-19 08:30:00', 'normale'),
('recette', 29000, 'Cartes de visite luxe', '2025-11-19', '2025-11-19 11:00:00', 'normale'),
('recette', 21000, 'Reliure présentation projet', '2025-11-19', '2025-11-19 14:30:00', 'normale'),
('depense', 9500, 'Achat encre couleur premium', '2025-11-19', '2025-11-19 16:00:00', 'normale'),
('depense', 5000, 'Internet', '2025-11-19', '2025-11-19 16:30:00', 'normale');

-- Jour 20: 2025-11-20 (Jeudi)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 41000, 'Impression affiches scolaires', '2025-11-20', '2025-11-20 09:00:00', 'normale'),
('recette', 24000, 'Photocopies examens', '2025-11-20', '2025-11-20 11:45:00', 'normale'),
('recette', 17500, 'Reliure cahiers personnalisés', '2025-11-20', '2025-11-20 14:15:00', 'normale'),
('depense', 6000, 'Transport matériel', '2025-11-20', '2025-11-20 16:00:00', 'normale');

-- Jour 21: 2025-11-21 (Vendredi)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 62000, 'Impression packaging luxe', '2025-11-21', '2025-11-21 08:00:00', 'normale'),
('recette', 31000, 'Étiquettes autocollantes', '2025-11-21', '2025-11-21 10:45:00', 'normale'),
('recette', 23000, 'Impression dépliants promotion', '2025-11-21', '2025-11-21 13:30:00', 'normale'),
('depense', 11000, 'Salaire employé 1', '2025-11-21', '2025-11-21 17:00:00', 'normale'),
('depense', 11000, 'Salaire employé 2', '2025-11-21', '2025-11-21 17:05:00', 'normale'),
('depense', 10000, 'Achat papier en gros', '2025-11-21', '2025-11-21 17:30:00', 'normale');

-- Jour 22: 2025-11-22 (Samedi)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 38000, 'Impression cartes fidélité', '2025-11-22', '2025-11-22 09:30:00', 'normale'),
('recette', 25000, 'Faire-part communion', '2025-11-22', '2025-11-22 12:00:00', 'normale'),
('recette', 16500, 'Photocopies dossiers', '2025-11-22', '2025-11-22 15:00:00', 'normale'),
('depense', 7500, 'Réparation massicot', '2025-11-22', '2025-11-22 16:30:00', 'normale');

-- Jour 23: 2025-11-23 (Dimanche)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 30000, 'Impression calendriers muraux', '2025-11-23', '2025-11-23 10:30:00', 'normale'),
('recette', 44000, 'Brochures immobilières', '2025-11-23', '2025-11-23 13:00:00', 'normale'),
('depense', 5500, 'Nettoyage équipements', '2025-11-23', '2025-11-23 15:30:00', 'normale');

-- Jour 24: 2025-11-24 (Lundi)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 54000, 'Impression bannières publicitaires', '2025-11-24', '2025-11-24 08:15:00', 'normale'),
('recette', 27500, 'Cartes menu restaurant gastronomique', '2025-11-24', '2025-11-24 10:45:00', 'normale'),
('recette', 18000, 'Reliure dossiers juridiques', '2025-11-24', '2025-11-24 13:30:00', 'normale'),
('depense', 14000, 'Achat consommables divers', '2025-11-24', '2025-11-24 15:30:00', 'normale'),
('depense', 8000, 'Électricité', '2025-11-24', '2025-11-24 16:00:00', 'normale');

-- Jour 25: 2025-11-25 (Mardi)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 49000, 'Impression flyers promotionnels', '2025-11-25', '2025-11-25 08:30:00', 'normale'),
('recette', 34000, 'Badges sécurité entreprise', '2025-11-25', '2025-11-25 11:00:00', 'normale'),
('recette', 20000, 'Plastification photos grand format', '2025-11-25', '2025-11-25 14:00:00', 'normale'),
('depense', 9000, 'Maintenance imprimantes offset', '2025-11-25', '2025-11-25 16:00:00', 'normale'),
('depense', 20000, 'Achat nouvelle découpeuse', '2025-11-25', '2025-11-25 17:00:00', 'speciale');

-- Jour 26: 2025-11-26 (Mercredi)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 59000, 'Impression plaquettes commerciales', '2025-11-26', '2025-11-26 08:00:00', 'normale'),
('recette', 28000, 'Invitations gala', '2025-11-26', '2025-11-26 10:30:00', 'normale'),
('recette', 22000, 'Photocopies plans techniques', '2025-11-26', '2025-11-26 13:45:00', 'normale'),
('depense', 11000, 'Achat toner multifonction', '2025-11-26', '2025-11-26 15:30:00', 'normale'),
('depense', 6000, 'Internet et téléphonie', '2025-11-26', '2025-11-26 16:15:00', 'normale');

-- Jour 27: 2025-11-27 (Jeudi)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 42000, 'Impression programmes spectacle', '2025-11-27', '2025-11-27 09:00:00', 'normale'),
('recette', 26000, 'Cartes de vœux entreprise', '2025-11-27', '2025-11-27 11:30:00', 'normale'),
('recette', 17500, 'Reliure rapports financiers', '2025-11-27', '2025-11-27 14:30:00', 'normale'),
('depense', 8500, 'Fournitures bureau', '2025-11-27', '2025-11-27 16:00:00', 'normale');

-- Jour 28: 2025-11-28 (Vendredi)
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 65000, 'Impression catalogues mode', '2025-11-28', '2025-11-28 08:30:00', 'normale'),
('recette', 32000, 'Tampons officiels personnalisés', '2025-11-28', '2025-11-28 11:00:00', 'normale'),
('recette', 24000, 'Plastification menus luxe', '2025-11-28', '2025-11-28 14:00:00', 'normale'),
('depense', 11000, 'Salaire employé 1', '2025-11-28', '2025-11-28 17:00:00', 'normale'),
('depense', 11000, 'Salaire employé 2', '2025-11-28', '2025-11-28 17:05:00', 'normale'),
('depense', 12000, 'Prime employés', '2025-11-28', '2025-11-28 17:15:00', 'normale');

-- Jour 29: 2025-11-29 (Samedi) - Jour actuel
INSERT INTO transactions (type, montant, description, date, created_at, type_depense) VALUES 
('recette', 40000, 'Impression affiches cinéma', '2025-11-29', '2025-11-29 09:00:00', 'normale'),
('recette', 27000, 'Cartes événement sportif', '2025-11-29', '2025-11-29 12:00:00', 'normale'),
('depense', 7000, 'Achat papier spécial', '2025-11-29', '2025-11-29 15:00:00', 'normale');

-- Clôture de certains jours (rapports journaliers clôturés)
-- Utiliser INSERT OR REPLACE pour éviter les conflits avec les données existantes
INSERT OR REPLACE INTO rapports_journaliers (date, cloture, cloture_at) VALUES
('2025-11-01', 1, '2025-11-01 18:00:00'),
('2025-11-02', 1, '2025-11-02 18:00:00'),
('2025-11-03', 1, '2025-11-03 18:00:00'),
('2025-11-04', 1, '2025-11-04 18:00:00'),
('2025-11-05', 1, '2025-11-05 18:00:00'),
('2025-11-06', 1, '2025-11-06 18:00:00'),
('2025-11-07', 1, '2025-11-07 18:00:00'),
('2025-11-08', 1, '2025-11-08 18:00:00'),
('2025-11-09', 1, '2025-11-09 18:00:00'),
('2025-11-10', 1, '2025-11-10 18:00:00'),
('2025-11-11', 1, '2025-11-11 18:00:00'),
('2025-11-12', 1, '2025-11-12 18:00:00'),
('2025-11-13', 1, '2025-11-13 18:00:00'),
('2025-11-14', 1, '2025-11-14 18:00:00'),
('2025-11-15', 1, '2025-11-15 18:00:00'),
('2025-11-16', 1, '2025-11-16 18:00:00'),
('2025-11-17', 1, '2025-11-17 18:00:00'),
('2025-11-18', 1, '2025-11-18 18:00:00'),
('2025-11-19', 1, '2025-11-19 18:00:00'),  
('2025-11-20', 1, '2025-11-20 18:00:00'),
('2025-11-21', 1, '2025-11-21 18:00:00'),
('2025-11-22', 1, '2025-11-22 18:00:00'),
('2025-11-23', 1, '2025-11-23 18:00:00'),
('2025-11-24', 1, '2025-11-24 18:00:00'),
('2025-11-25', 1, '2025-11-25 18:00:00'),
('2025-11-26', 1, '2025-11-26 18:00:00'),
('2025-11-27', 1, '2025-11-27 18:00:00'),
('2025-11-28', 1, '2025-11-28 18:00:00');

-- Statistiques du mois de novembre 2025:
-- - 29 jours de données
-- - Environ 3-5 transactions par jour
-- - Mélange de recettes (impression, photocopies, reliure, etc.)
-- - Dépenses normales (fournitures, électricité, salaires, maintenance)
-- - Dépenses spéciales/caisse (équipements, loyer)
-- - Apports de capital (3 apports répartis dans le mois)
-- - 28 jours clôturés (jour 29 reste ouvert)
