import json
from pyscript import document, window, when

PRODUCTS = {
    "essentials": {"name": "Velora Essentials", "price": 299, "image": "images/essentials.svg",
                   "short": "Everyday basics made to last.",
                   "long": "Velora Essentials covers the basics you use every day. Simple, reliable and priced for everyone."},
    "premium": {"name": "Velora Premium", "price": 499, "image": "images/premium.svg",
                "short": "Upgraded materials and finish.",
                "long": "Velora Premium adds better materials and a refined finish for customers who want a little more."},
    "deluxe": {"name": "Velora Deluxe", "price": 799, "image": "images/deluxe.svg",
               "short": "Our complete, high-quality set.",
               "long": "Velora Deluxe is our complete set, made with high-quality materials and built to impress."},
    "signature": {"name": "Velora Signature", "price": 999, "image": "images/signature.svg",
                  "short": "Our finest, limited collection.",
                  "long": "Velora Signature is our finest product, crafted with the best materials in the Velora range."},
}


def q(selector):
    return document.querySelector(selector)


def peso(amount):
    return f"₱{amount:,.2f}"


def load_cart():
    raw = window.localStorage.getItem("velora_cart")
    return json.loads(raw) if raw else {}   


def save_cart(cart):
    window.localStorage.setItem("velora_cart", json.dumps(cart))
    update_cart_count()


def update_cart_count():
    total = sum(load_cart().values())
    for badge in document.querySelectorAll(".cart-count"):
        badge.innerText = str(total)


def say(text):
    box = q("#cart-message")
    if box is not None:
        box.innerText = text


def calculate_total():
    """Subtotal, 10% discount at P1,000+, P50 delivery below P1,500."""
    cart = load_cart()
    subtotal = sum(PRODUCTS[pid]["price"] * qty for pid, qty in cart.items())
    discount = subtotal * 0.10 if subtotal >= 1000 else 0
    delivery = 0 if (subtotal >= 1500 or subtotal == 0) else 50
    return {"subtotal": subtotal, "discount": discount, "delivery": delivery,
            "total": subtotal - discount + delivery}


def show_totals():
    t = calculate_total()
    for key, el_id in [("subtotal", "#subtotal"), ("discount", "#discount"),
                       ("delivery", "#delivery"), ("total", "#grand-total")]:
        el = q(el_id)
        if el is not None:
            el.innerText = ("-" if key == "discount" and t[key] else "") + peso(t[key])


def add_to_cart(pid, qty=1, quiet=False):
    cart = load_cart()
    cart[pid] = cart.get(pid, 0) + qty      
    save_cart(cart)
    if not quiet:
        say(f"{PRODUCTS[pid]['name']} has been added to your cart.")


def remove_from_cart(pid):
    cart = load_cart()
    cart.pop(pid, None)
    save_cart(cart)
    render_cart()


def increase_quantity(pid):
    cart = load_cart()
    cart[pid] = cart.get(pid, 0) + 1
    save_cart(cart)
    render_cart()


def decrease_quantity(pid):
    cart = load_cart()
    if cart.get(pid, 1) > 1:               
        cart[pid] -= 1
    save_cart(cart)
    render_cart()


def product_card(pid, view_label):
    p = PRODUCTS[pid]
    return (f'<article class="card product-card"><img src="{p["image"]}" alt="{p["name"]}">'
            f'<h3>{p["name"]}</h3><p>{p["short"]}</p><p class="price">₱{p["price"]:,}</p>'
            f'<div class="card-buttons"><a class="btn btn-outline" href="product.html?id={pid}">{view_label}</a>'
            f'<button type="button" class="btn" data-action="add" data-id="{pid}">Add to Cart</button></div></article>')


def render_product_lists():
    featured = q("#featured-grid")
    if featured is not None:
        featured.innerHTML = "".join(product_card(pid, "View Product") for pid in list(PRODUCTS)[:3])
    catalog = q("#product-grid")
    if catalog is not None:
        catalog.innerHTML = "".join(product_card(pid, "View Details") for pid in PRODUCTS)


def current_product_id():
    pid = window.URLSearchParams.new(window.location.search).get("id")
    return pid if pid in PRODUCTS else "essentials"


def render_product_detail():
    if q("#detail-name") is None:
        return
    p = PRODUCTS[current_product_id()]
    q("#detail-img").src = p["image"]
    q("#detail-img").alt = p["name"]
    q("#detail-name").innerText = p["name"]
    q("#detail-price").innerText = f"₱{p['price']:,}"
    q("#detail-desc").innerText = p["long"]
    document.title = p["name"] + " - Velora Online"
