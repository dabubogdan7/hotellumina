"""
Configurare email — Hotel Lumina
================================
Pentru a activa trimiterea emailurilor:
  1. Activează "App Passwords" în contul Gmail (myaccount.google.com/security)
  2. Generează o parolă de aplicație (16 caractere)
  3. Completează EMAIL_USER și EMAIL_PASSWORD de mai jos

Dacă lași EMAIL_USER gol, emailurile sunt simulate în consolă (mod demo).
"""

EMAIL_HOST     = "smtp.gmail.com"
EMAIL_PORT     = 587
EMAIL_USER     = ""          # ex: "hotelullumina@gmail.com"
EMAIL_PASSWORD = ""          # ex: "abcd efgh ijkl mnop"

HOTEL_NAME     = "Hotel Lumina"
HOTEL_EMAIL    = "rezervari@hotellumina.ro"
HOTEL_PHONE    = "+40 21 123 4567"
HOTEL_ADDRESS  = "Str. Luminii 12, București"
