from flask import Flask, render_template, request, flash, redirect, url_for, session
from datetime import datetime
import database
import email_service

app = Flask(__name__)
app.secret_key = "hotel_lumina_secret_2026"

database.init_db()

# ─── DATE ────────────────────────────────────────────────────────────────────

ROOMS = [
    {
        "id": 1, "name": "Camera Deluxe", "price": 350,
        "size": "32 m²", "guests": 2,
        "image": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=800&q=80",
        "description": "O cameră elegantă cu vedere la grădină, pat king-size și baie de lux.",
        "features": ["Wi-Fi gratuit", "Aer condiționat", "TV Smart", "Mic dejun inclus"],
    },
    {
        "id": 2, "name": "Suite Panoramică", "price": 580,
        "size": "55 m²", "guests": 2,
        "image": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800&q=80",
        "description": "Suite spațioasă cu balcon privat și priveliște panoramică asupra orașului.",
        "features": ["Wi-Fi gratuit", "Jacuzzi privat", "Salon separat", "Serviciu la cameră 24/7"],
    },
    {
        "id": 3, "name": "Camera Junior Suite", "price": 450,
        "size": "42 m²", "guests": 3,
        "image": "https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800&q=80",
        "description": "Perfectă pentru familii, cu zonă de living separată și două băi.",
        "features": ["Wi-Fi gratuit", "Aer condiționat", "Pat suplimentar", "Frigider minibar"],
    },
    {
        "id": 4, "name": "Camera Standard", "price": 220,
        "size": "24 m²", "guests": 2,
        "image": "https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=800&q=80",
        "description": "Confort esențial într-un design modern și curat, ideal pentru călătorii de afaceri.",
        "features": ["Wi-Fi gratuit", "Aer condiționat", "TV 42\"", "Duș cu efect ploaie"],
    },
    {
        "id": 5, "name": "Suite Prezidențială", "price": 1200,
        "size": "110 m²", "guests": 4,
        "image": "https://images.unsplash.com/photo-1618773928121-c32242e63f39?w=800&q=80",
        "description": "Cel mai luxos spațiu al hotelului, cu terasă privată, living și dining room.",
        "features": ["Concierge privat", "Jacuzzi panoramic", "Bucătărie complet utilată", "Transfer aeroport inclus"],
    },
    {
        "id": 6, "name": "Camera Twin", "price": 280,
        "size": "30 m²", "guests": 2,
        "image": "https://images.unsplash.com/photo-1595576508898-0ad5c879a061?w=800&q=80",
        "description": "Două paturi single confortabile, ideală pentru prieteni sau colegi de călătorie.",
        "features": ["Wi-Fi gratuit", "Aer condiționat", "Birou de lucru", "Seif electronic"],
    },
]

GALLERY = [
    {"url": "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80",  "title": "Hol principal"},
    {"url": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&q=80", "title": "Piscina exterioară"},
    {"url": "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&q=80", "title": "Restaurant"},
    {"url": "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?w=800&q=80",   "title": "Spa & Wellness"},
    {"url": "https://images.unsplash.com/photo-1563911302283-d2bc129e7570?w=800&q=80", "title": "Bar lounge"},
    {"url": "https://images.unsplash.com/photo-1540541338287-41700207dee6?w=800&q=80", "title": "Grădina hotelului"},
    {"url": "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=800&q=80",   "title": "Sala de conferințe"},
    {"url": "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=800&q=80", "title": "Terasă panoramică"},
]

OFFERS = [
    {
        "id": "romantic",
        "name": "Romantik Weekend",
        "emoji": "🌹",
        "tagline": "O escapadă romantică de neuitat",
        "image": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=900&q=80",
        "description": "Surprinde-ți partenerul cu un weekend perfect. Totul e pregătit pentru voi.",
        "inclusions": [
            "Cameră Deluxe cu rose petals",
            "Cină romantică pentru 2 persoane",
            "Masaj duo la spa (60 min)",
            "Șampanie la sosire",
            "Mic dejun în cameră",
            "Late check-out gratuit (ora 14:00)",
        ],
        "original_price": 1400,
        "price": 999,
        "discount": 29,
        "expires": "2026-06-14",
        "room_id": 1,
        "color": "#B5451B",
        "badge": "Cel mai popular",
    },
    {
        "id": "corporate",
        "name": "Corporate Stay",
        "emoji": "💼",
        "tagline": "Productivitate și confort pentru oamenii de afaceri",
        "image": "https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=900&q=80",
        "description": "Totul de care ai nevoie pentru un sejur de afaceri eficient și confortabil.",
        "inclusions": [
            "Camera la alegere (Standard sau Deluxe)",
            "Mic dejun buffet inclus zilnic",
            "Acces sala de conferințe (2h/zi)",
            "Wi-Fi dedicat 1 Gbps",
            "Transfer aeroport dus-întors",
            "Parcare gratuită",
        ],
        "original_price": 980,
        "price": 720,
        "discount": 27,
        "expires": "2026-06-28",
        "room_id": 4,
        "color": "#1B3A5C",
        "badge": "Business",
    },
    {
        "id": "family",
        "name": "Vacanță în Familie",
        "emoji": "👨‍👩‍👧‍👦",
        "tagline": "Amintiri de neuitat pentru întreaga familie",
        "image": "https://images.unsplash.com/photo-1590490360182-c33d57733427?w=900&q=80",
        "description": "Pachetul perfect pentru familii cu copii — activități, relaxare și distracție.",
        "inclusions": [
            "Junior Suite sau cameră cu pat suplimentar",
            "Mic dejun buffet pentru toată familia",
            "Intrare gratuită la piscina exterioară",
            "1 tratament spa pentru adulți",
            "Activități pentru copii (weekend)",
            "Parcare gratuită",
        ],
        "original_price": 1600,
        "price": 1190,
        "discount": 26,
        "expires": "2026-07-31",
        "room_id": 3,
        "color": "#2D6A4F",
        "badge": "Familie",
    },
]

# ─── RUTE PRINCIPALE ─────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/camere")
def rooms():
    return render_template("rooms.html", rooms=ROOMS)


@app.route("/galerie")
def gallery():
    return render_template("gallery.html", images=GALLERY)


@app.route("/despre")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name    = request.form.get("name", "").strip()
        email   = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        if name and email and message:
            flash("Mesajul tău a fost trimis cu succes! Te vom contacta în curând.", "success")
        else:
            flash("Te rugăm să completezi toate câmpurile.", "error")
        return redirect(url_for("contact"))
    return render_template("contact.html")


# ─── OFERTE ──────────────────────────────────────────────────────────────────

@app.route("/oferte")
def offers():
    return render_template("offers.html", offers=OFFERS)


# ─── REZERVARE ───────────────────────────────────────────────────────────────

@app.route("/rezervare/<int:room_id>", methods=["GET", "POST"])
def booking(room_id):
    room = next((r for r in ROOMS if r["id"] == room_id), None)
    if not room:
        return redirect(url_for("rooms"))

    if request.method == "POST":
        check_in   = request.form.get("check_in", "").strip()
        check_out  = request.form.get("check_out", "").strip()
        guest_name = request.form.get("guest_name", "").strip()
        guest_email= request.form.get("guest_email", "").strip()
        guest_phone= request.form.get("guest_phone", "").strip()
        num_guests = request.form.get("num_guests", "1")
        special    = request.form.get("special_requests", "").strip()

        # Validare câmpuri
        if not all([check_in, check_out, guest_name, guest_email]):
            flash("Completați toate câmpurile obligatorii.", "error")
            return redirect(url_for("booking", room_id=room_id))

        # Validare date
        try:
            d1 = datetime.strptime(check_in, "%Y-%m-%d")
            d2 = datetime.strptime(check_out, "%Y-%m-%d")
            nights = (d2 - d1).days
            if nights < 1:
                flash("Data de check-out trebuie să fie după check-in.", "error")
                return redirect(url_for("booking", room_id=room_id))
        except ValueError:
            flash("Format de dată invalid.", "error")
            return redirect(url_for("booking", room_id=room_id))

        # Verificare disponibilitate
        if not database.is_available(room_id, check_in, check_out):
            flash("Ne pare rău, camera nu este disponibilă în perioada selectată. Alege alte date.", "error")
            return redirect(url_for("booking", room_id=room_id))

        total_price = nights * room["price"]

        booking_id = database.create_booking({
            "room_id":          room_id,
            "room_name":        room["name"],
            "guest_name":       guest_name,
            "guest_email":      guest_email,
            "guest_phone":      guest_phone,
            "check_in":         check_in,
            "check_out":        check_out,
            "num_guests":       int(num_guests),
            "nights":           nights,
            "total_price":      total_price,
            "special_requests": special,
        })

        booking_data = {
            "id":          booking_id,
            "room_name":   room["name"],
            "room_image":  room["image"],
            "guest_name":  guest_name,
            "guest_email": guest_email,
            "guest_phone": guest_phone,
            "check_in":    check_in,
            "check_out":   check_out,
            "num_guests":  int(num_guests),
            "nights":      nights,
            "total_price": total_price,
        }

        email_service.send_confirmation(booking_data)
        session["last_booking"] = booking_data
        return redirect(url_for("booking_success"))

    occupied = database.get_occupied_ranges(room_id)
    today = datetime.now().strftime("%Y-%m-%d")
    return render_template("booking.html", room=room, occupied_ranges=occupied, today=today)


@app.route("/rezervare/succes")
def booking_success():
    booking_data = session.pop("last_booking", None)
    if not booking_data:
        return redirect(url_for("index"))
    return render_template("booking_success.html", booking=booking_data)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
