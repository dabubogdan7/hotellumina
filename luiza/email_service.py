import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config


def send_confirmation(b: dict) -> bool:
    """Trimite email de confirmare rezervare. Returnează True dacă a reușit."""
    if not config.EMAIL_USER:
        print(f"[EMAIL DEMO] Rezervare #{b['id']} pentru {b['guest_email']} "
              f"({b['check_in']} - {b['check_out']}, {b['nights']} nopti, {b['total_price']:.0f} lei)")
        return True

    nights_label = "noapte" if b["nights"] == 1 else "nopți"
    html = f"""<!DOCTYPE html>
<html lang="ro">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#FAF7F0;font-family:'Helvetica Neue',Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#FAF7F0;padding:40px 16px;">
<tr><td align="center">
<table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;background:#fff;border-radius:20px;overflow:hidden;box-shadow:0 8px 32px rgba(27,67,50,.12);">

  <!-- HEADER -->
  <tr><td style="background:linear-gradient(135deg,#1B4332 0%,#2D6A4F 100%);padding:44px 40px;text-align:center;">
    <p style="color:#C9A84C;font-size:10px;letter-spacing:4px;text-transform:uppercase;margin:0 0 10px 0;">Confirmare rezervare</p>
    <h1 style="color:#fff;font-size:36px;margin:0;font-weight:300;font-family:Georgia,serif;">Hotel <em style="color:#E8C96D;font-style:italic;">Lumina</em></h1>
    <p style="color:rgba(255,255,255,.6);font-size:13px;margin:12px 0 0;">✓ Rezervarea ta a fost înregistrată cu succes</p>
  </td></tr>

  <!-- GREETING -->
  <tr><td style="padding:40px 40px 24px;">
    <p style="font-size:18px;color:#1C1C1E;margin:0 0 10px 0;">Dragă <strong>{b['guest_name']}</strong>,</p>
    <p style="color:#6C6C6E;line-height:1.8;margin:0;font-size:15px;">Îți mulțumim pentru că ai ales <strong>Hotel Lumina</strong>! Suntem încântați să te primim și ne vom asigura că sejurul tău va fi de neuitat.</p>
  </td></tr>

  <!-- BOOKING CARD -->
  <tr><td style="padding:0 40px 32px;">
    <table width="100%" cellpadding="0" cellspacing="0" style="border-radius:14px;overflow:hidden;border:1.5px solid #E8DCC8;">
      <tr><td colspan="2" style="background:#2D6A4F;padding:14px 24px;">
        <p style="color:#fff;font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin:0;">
          Rezervare #{b['id']}
        </p>
      </td></tr>
      <tr>
        <td style="padding:20px 24px;border-bottom:1px solid #E8DCC8;width:50%;">
          <p style="color:#6C6C6E;font-size:10px;text-transform:uppercase;letter-spacing:1.5px;margin:0 0 6px;">Cameră</p>
          <p style="color:#1C1C1E;font-size:16px;font-weight:700;margin:0;">{b['room_name']}</p>
        </td>
        <td style="padding:20px 24px;border-bottom:1px solid #E8DCC8;border-left:1px solid #E8DCC8;">
          <p style="color:#6C6C6E;font-size:10px;text-transform:uppercase;letter-spacing:1.5px;margin:0 0 6px;">Persoane</p>
          <p style="color:#1C1C1E;font-size:16px;font-weight:700;margin:0;">{b['num_guests']}</p>
        </td>
      </tr>
      <tr>
        <td style="padding:20px 24px;border-bottom:1px solid #E8DCC8;">
          <p style="color:#6C6C6E;font-size:10px;text-transform:uppercase;letter-spacing:1.5px;margin:0 0 6px;">Check-in</p>
          <p style="color:#1C1C1E;font-size:16px;font-weight:700;margin:0;">{b['check_in']}</p>
          <p style="color:#6C6C6E;font-size:12px;margin:2px 0 0;">după ora 15:00</p>
        </td>
        <td style="padding:20px 24px;border-bottom:1px solid #E8DCC8;border-left:1px solid #E8DCC8;">
          <p style="color:#6C6C6E;font-size:10px;text-transform:uppercase;letter-spacing:1.5px;margin:0 0 6px;">Check-out</p>
          <p style="color:#1C1C1E;font-size:16px;font-weight:700;margin:0;">{b['check_out']}</p>
          <p style="color:#6C6C6E;font-size:12px;margin:2px 0 0;">până la ora 12:00</p>
        </td>
      </tr>
      <tr>
        <td style="padding:20px 24px;">
          <p style="color:#6C6C6E;font-size:10px;text-transform:uppercase;letter-spacing:1.5px;margin:0 0 6px;">Durata sejurului</p>
          <p style="color:#1C1C1E;font-size:16px;font-weight:700;margin:0;">{b['nights']} {nights_label}</p>
        </td>
        <td style="padding:20px 24px;border-left:1px solid #E8DCC8;background:#1B4332;">
          <p style="color:rgba(255,255,255,.7);font-size:10px;text-transform:uppercase;letter-spacing:1.5px;margin:0 0 6px;">Total de plată</p>
          <p style="color:#E8C96D;font-size:26px;font-weight:800;margin:0;">{b['total_price']:.0f} lei</p>
          <p style="color:rgba(255,255,255,.5);font-size:11px;margin:2px 0 0;">plată la recepție</p>
        </td>
      </tr>
    </table>
  </td></tr>

  <!-- REMINDERS -->
  <tr><td style="padding:0 40px 32px;">
    <table width="100%" cellpadding="14" cellspacing="0" style="background:#FAF7F0;border-radius:12px;">
      <tr><td colspan="2" style="padding:16px 20px 8px;">
        <p style="color:#1B4332;font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin:0;">Informații utile</p>
      </td></tr>
      <tr>
        <td style="padding:8px 20px;font-size:13px;color:#2C2C2E;">📍 {config.HOTEL_ADDRESS}</td>
        <td style="padding:8px 20px;font-size:13px;color:#2C2C2E;">📞 {config.HOTEL_PHONE}</td>
      </tr>
      <tr>
        <td style="padding:8px 20px 16px;font-size:13px;color:#2C2C2E;">🅿️ Parcare gratuită disponibilă</td>
        <td style="padding:8px 20px 16px;font-size:13px;color:#2C2C2E;">🛎️ Recepție 24/7</td>
      </tr>
    </table>
  </td></tr>

  <!-- FOOTER -->
  <tr><td style="background:#1C1C1E;padding:28px 40px;text-align:center;">
    <p style="color:rgba(255,255,255,.4);font-size:12px;margin:0 0 6px;">{config.HOTEL_NAME} · {config.HOTEL_ADDRESS}</p>
    <p style="color:rgba(255,255,255,.4);font-size:12px;margin:0;">{config.HOTEL_EMAIL} · {config.HOTEL_PHONE}</p>
  </td></tr>

</table>
</td></tr>
</table>
</body>
</html>"""

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"✓ Confirmare rezervare #{b['id']} — {config.HOTEL_NAME}"
        msg["From"]    = f"{config.HOTEL_NAME} <{config.EMAIL_USER}>"
        msg["To"]      = b["guest_email"]
        msg.attach(MIMEText(html, "html", "utf-8"))

        with smtplib.SMTP(config.EMAIL_HOST, config.EMAIL_PORT) as srv:
            srv.ehlo()
            srv.starttls()
            srv.login(config.EMAIL_USER, config.EMAIL_PASSWORD)
            srv.sendmail(config.EMAIL_USER, b["guest_email"], msg.as_string())
        print(f"[EMAIL OK] Trimis la {b['guest_email']}")
        return True
    except Exception as exc:
        print(f"[EMAIL ERROR] {exc}")
        return False
