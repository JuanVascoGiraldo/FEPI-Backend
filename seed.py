"""
Script de seed: crea 5 mesas y 100 platillos via API REST.
Uso: uv run python seed.py <JWT>
"""
import asyncio
import sys
import httpx

BASE_URL = "http://localhost:8000"

TABLES = [
    {"number": "1", "description": "Terraza norte"},
    {"number": "2", "description": "Terraza sur"},
    {"number": "3", "description": "Salón principal"},
    {"number": "4", "description": "Salón VIP"},
    {"number": "5", "description": "Barra"},
]

# category: 1=Entrada 2=Plato principal 3=Bebida 4=Postre 5=Otro
DISHES = [
    # Entradas (1)
    {"name": "Guacamole con totopos", "description": "Aguacate fresco, jitomate, cebolla y cilantro", "price": 95.00, "category": 1},
    {"name": "Elotes asados", "description": "Con mayonesa, queso cotija y chile piquín", "price": 75.00, "category": 1},
    {"name": "Quesadillas de flor de calabaza", "description": "Tortilla de maíz, queso Oaxaca y flor de calabaza", "price": 110.00, "category": 1},
    {"name": "Sopa azteca", "description": "Caldo de jitomate, chile pasilla, crema y queso fresco", "price": 90.00, "category": 1},
    {"name": "Tostadas de tinga", "description": "Pollo deshebrado en salsa de chipotle sobre tostada crujiente", "price": 100.00, "category": 1},
    {"name": "Ceviche de camarón", "description": "Camarón marinado en limón, pepino, cebolla morada y aguacate", "price": 130.00, "category": 1},
    {"name": "Ensalada César", "description": "Lechuga romana, crutones, parmesano y aderezo César casero", "price": 105.00, "category": 1},
    {"name": "Flautas de papa", "description": "Tortillas fritas rellenas de papa, crema y salsa verde", "price": 85.00, "category": 1},
    {"name": "Chorizo con nopales", "description": "Chorizo artesanal salteado con nopales y cebolla", "price": 115.00, "category": 1},
    {"name": "Sopa de lima", "description": "Caldo yucateco con pollo, tortilla frita y limón", "price": 95.00, "category": 1},

    # Platos principales (2)
    {"name": "Tacos de pastor", "description": "Con piña, cebolla, cilantro y salsa roja", "price": 175.00, "category": 2},
    {"name": "Enchiladas verdes", "description": "Rellenas de pollo, bañadas en salsa verde con crema y queso", "price": 160.00, "category": 2},
    {"name": "Mole negro con pollo", "description": "Pollo en mole negro oaxaqueño, acompañado de arroz y frijoles", "price": 195.00, "category": 2},
    {"name": "Chiles en nogada", "description": "Chile poblano relleno de picadillo, cubierto de nogada y granada", "price": 220.00, "category": 2},
    {"name": "Camarones al ajillo", "description": "Camarones salteados en mantequilla, ajo y chile de árbol", "price": 210.00, "category": 2},
    {"name": "Bistec a la mexicana", "description": "Con jitomate, cebolla, chile serrano, arroz y frijoles", "price": 185.00, "category": 2},
    {"name": "Pozole rojo", "description": "Con carne de cerdo, maíz cacahuazintle y guarniciones", "price": 170.00, "category": 2},
    {"name": "Cochinita pibil", "description": "Cerdo marinado en achiote, con cebollas encurtidas y tortillas", "price": 180.00, "category": 2},
    {"name": "Arrachera a la parrilla", "description": "Con guacamole, pico de gallo, tortillas y arroz", "price": 240.00, "category": 2},
    {"name": "Tamales de rajas", "description": "Con crema, elote y queso, en salsa verde", "price": 145.00, "category": 2},
    {"name": "Chilaquiles rojos", "description": "Con pollo, crema, queso fresco y cebolla morada", "price": 155.00, "category": 2},
    {"name": "Pescado a la veracruzana", "description": "Filete de huachinango en salsa de jitomate, aceitunas y alcaparras", "price": 225.00, "category": 2},
    {"name": "Tacos de canasta", "description": "Papa, frijoles y chicharrón prensado, tres piezas", "price": 120.00, "category": 2},
    {"name": "Gorditas de chicharrón", "description": "Masa gruesa con chicharrón prensado y salsa de tu elección", "price": 135.00, "category": 2},
    {"name": "Huarache de nopales", "description": "Base de maíz con nopal, queso, frijoles y salsa verde", "price": 150.00, "category": 2},
    {"name": "Mixiote de borrego", "description": "Carne de borrego marinada en chile guajillo, envuelta en maguey", "price": 205.00, "category": 2},
    {"name": "Sopes de tinga", "description": "Tres sopes con tinga de pollo, crema y lechuga", "price": 165.00, "category": 2},
    {"name": "Arroz con leche de mariscos", "description": "Arroz cremoso con camarones, mejillones y vieiras", "price": 230.00, "category": 2},
    {"name": "Torta de milanesa", "description": "Pan telera con milanesa de res, aguacate, jitomate y chile jalapeño", "price": 145.00, "category": 2},
    {"name": "Caldo de res", "description": "Con verduras de temporada, epazote y limón al gusto", "price": 160.00, "category": 2},

    # Bebidas (3)
    {"name": "Agua de horchata", "description": "Arroz, canela y azúcar al gusto — 500 ml", "price": 45.00, "category": 3},
    {"name": "Agua de Jamaica", "description": "Flor de Jamaica fría con azúcar al gusto — 500 ml", "price": 45.00, "category": 3},
    {"name": "Agua de tamarindo", "description": "Tamarindo natural con piloncillo — 500 ml", "price": 45.00, "category": 3},
    {"name": "Michelada clásica", "description": "Cerveza con jugo de limón, clamato, chile y sal en vaso escarc", "price": 95.00, "category": 3},
    {"name": "Margarita de tamarindo", "description": "Tequila, tamarindo, triple sec y sal de gusano", "price": 110.00, "category": 3},
    {"name": "Paloma", "description": "Tequila, jugo de toronja, limón y sal", "price": 100.00, "category": 3},
    {"name": "Tepache artesanal", "description": "Bebida fermentada de piña con clavo y canela — 400 ml", "price": 65.00, "category": 3},
    {"name": "Café de olla", "description": "Café negro con canela y piloncillo — 300 ml", "price": 55.00, "category": 3},
    {"name": "Chocolate caliente", "description": "Cacao puro batido con leche entera — 300 ml", "price": 60.00, "category": 3},
    {"name": "Refresco", "description": "Coca-Cola, Sprite o Fanta — 355 ml", "price": 35.00, "category": 3},
    {"name": "Jugo de naranja natural", "description": "Tres naranjas exprimidas al momento — 300 ml", "price": 55.00, "category": 3},
    {"name": "Agua mineral", "description": "San Pellegrino o Topo Chico — 500 ml", "price": 40.00, "category": 3},
    {"name": "Limonada natural", "description": "Limón exprimido, agua y azúcar — 400 ml", "price": 50.00, "category": 3},
    {"name": "Cerveza artesanal IPA", "description": "De grifo local, 500 ml, lupulada y aromática", "price": 90.00, "category": 3},
    {"name": "Mezcal joven", "description": "Shot de mezcal artesanal con sal de gusano y naranja", "price": 120.00, "category": 3},

    # Postres (4)
    {"name": "Churros con cajeta", "description": "Churros fritos con cajeta artesanal y chocolate", "price": 85.00, "category": 4},
    {"name": "Flan napolitano", "description": "Flan cremoso con caramelo y crema chantilly", "price": 75.00, "category": 4},
    {"name": "Pastel de tres leches", "description": "Bizcocho empapado en tres leches con merengue", "price": 90.00, "category": 4},
    {"name": "Helado de mamey", "description": "Dos bolas de helado artesanal de mamey con galleta", "price": 70.00, "category": 4},
    {"name": "Buñuelos con piloncillo", "description": "Masa frita crujiente bañada en miel de piloncillo", "price": 80.00, "category": 4},
    {"name": "Arroz con leche", "description": "Con canela, pasas y ralladura de naranja", "price": 65.00, "category": 4},
    {"name": "Nieves de leche quemada", "description": "Nieve artesanal de leche quemada con toque de vainilla", "price": 60.00, "category": 4},
    {"name": "Capirotada", "description": "Pan de yema con pasas, cacahuate, queso y piloncillo", "price": 75.00, "category": 4},
    {"name": "Gelatina de guayaba", "description": "Guayaba natural en gelatina con leche condensada", "price": 55.00, "category": 4},
    {"name": "Brownie de chocolate mexicano", "description": "Con nuez y helado de vainilla, chocolate Abuelita", "price": 95.00, "category": 4},

    # Otros (5)
    {"name": "Pan de la casa", "description": "Telera o bolillo recién horneado con mantequilla", "price": 30.00, "category": 5},
    {"name": "Tortillas de maíz", "description": "Orden de 10 tortillas hechas a mano", "price": 35.00, "category": 5},
    {"name": "Salsa verde", "description": "Tomatillo, serrano y cilantro — porción extra", "price": 20.00, "category": 5},
    {"name": "Salsa roja", "description": "Chile guajillo tatemado — porción extra", "price": 20.00, "category": 5},
    {"name": "Crema ácida", "description": "Porción de crema ácida de rancho — 60 ml", "price": 25.00, "category": 5},
    {"name": "Frijoles de olla", "description": "Frijoles negros con epazote — taza", "price": 45.00, "category": 5},
    {"name": "Arroz rojo", "description": "Arroz con jitomate, zanahoria y chícharo — porción", "price": 45.00, "category": 5},
    {"name": "Limones", "description": "Orden de 6 limones partidos", "price": 15.00, "category": 5},
    {"name": "Queso fresco", "description": "Porción de queso fresco desmoronado — 50 g", "price": 30.00, "category": 5},
    {"name": "Chile jalapeño en escabeche", "description": "Rajas de jalapeño con zanahoria y cebolla — porción", "price": 25.00, "category": 5},

    # Entradas extra (1)
    {"name": "Tacos de cangrejo", "description": "Cangrejo desmenuzado con aguacate y mayonesa de chipotle", "price": 145.00, "category": 1},
    {"name": "Brochetas de camarón", "description": "Tres brochetas de camarón con pimiento y cebolla a la parrilla", "price": 135.00, "category": 1},
    {"name": "Carpaccio de res", "description": "Res cruda en láminas con alcaparras, parmesano y aceite de oliva", "price": 150.00, "category": 1},
    {"name": "Empanadas de tinga", "description": "Tres empanadas de pollo en salsa chipotle, horneadas", "price": 120.00, "category": 1},
    {"name": "Quesillo fundido", "description": "Queso Oaxaca fundido con chorizo y nopales", "price": 125.00, "category": 1},

    # Platos principales extra (2)
    {"name": "Pollo a la plancha", "description": "Pechuga marinada en limón y hierbas, con ensalada y papas", "price": 175.00, "category": 2},
    {"name": "Filete de res al carbón", "description": "200 g de filete con salsa de champiñones y papas al horno", "price": 280.00, "category": 2},
    {"name": "Tacos de barbacoa", "description": "Tres tacos de barbacoa de res con consomé y limón", "price": 165.00, "category": 2},
    {"name": "Enchiladas rojas", "description": "Rellenas de queso, bañadas en salsa roja con frijoles", "price": 155.00, "category": 2},
    {"name": "Tostadas de atún", "description": "Atún sellado sobre tostada con aguacate y mayonesa de wasabi", "price": 185.00, "category": 2},
    {"name": "Costillas BBQ", "description": "Costillas de cerdo en salsa barbecue ahumada con coleslaw", "price": 260.00, "category": 2},
    {"name": "Pasta al pesto", "description": "Linguine con pesto de albahaca, nuez y queso parmesano", "price": 165.00, "category": 2},
    {"name": "Hamburguesa artesanal", "description": "200 g de res, cheddar, tocino, lechuga, jitomate y papas fritas", "price": 190.00, "category": 2},
    {"name": "Risotto de hongos", "description": "Arroz cremoso con portobello, shiitake y parmesano", "price": 195.00, "category": 2},
    {"name": "Tacos de suadero", "description": "Cuatro tacos de suadero con cilantro, cebolla y salsa", "price": 150.00, "category": 2},

    # Bebidas extra (3)
    {"name": "Smoothie de mango", "description": "Mango, leche de coco y jengibre — 400 ml", "price": 70.00, "category": 3},
    {"name": "Agua de pepino con limón", "description": "Pepino, limón, menta y hielo — 500 ml", "price": 45.00, "category": 3},
    {"name": "Mojito sin alcohol", "description": "Lima, menta, agua mineral y azúcar morena — 400 ml", "price": 65.00, "category": 3},
    {"name": "Té helado de hibisco", "description": "Jamaica fría con menta y limón — 500 ml", "price": 50.00, "category": 3},
    {"name": "Cerveza artesanal Stout", "description": "De grifo local, oscura y cremosa — 500 ml", "price": 95.00, "category": 3},

    # Postres extra (4)
    {"name": "Crepas de cajeta", "description": "Crepas con cajeta artesanal, nuez y helado de vainilla", "price": 100.00, "category": 4},
    {"name": "Tarta de limón", "description": "Base de galleta con crema de limón y merengue tatemado", "price": 90.00, "category": 4},
    {"name": "Volcán de chocolate", "description": "Bizcocho de chocolate fundido con helado de vainilla", "price": 110.00, "category": 4},
    {"name": "Paletas de fruta", "description": "Dos paletas artesanales: tamarindo picoso y mango con chamoy", "price": 60.00, "category": 4},
    {"name": "Empanadas de guayaba", "description": "Tres empanadas de pasta hojaldrada rellenas de guayaba con azúcar", "price": 75.00, "category": 4},

    # Ronda final para completar 100
    {"name": "Tacos de pescado", "description": "Filete de mahi-mahi empanizado con coleslaw y salsa de chipotle", "price": 170.00, "category": 2},
    {"name": "Caldo tlalpeño", "description": "Caldo con pollo, garbanzo, chile chipotle y epazote", "price": 105.00, "category": 1},
    {"name": "Agua de melón", "description": "Melón fresco licuado con azúcar al gusto — 500 ml", "price": 45.00, "category": 3},
    {"name": "Nieve de limón", "description": "Nieve artesanal de limón con ralladura — una bola", "price": 50.00, "category": 4},
    {"name": "Quesadillas de huitlacoche", "description": "Tortilla de maíz con huitlacoche y queso Oaxaca", "price": 130.00, "category": 1},
    {"name": "Pambazos de papa y chorizo", "description": "Pan mojado en salsa guajillo con relleno de papa y chorizo", "price": 140.00, "category": 2},
    {"name": "Atole de guayaba", "description": "Bebida caliente de maíz con guayaba y piloncillo — 300 ml", "price": 55.00, "category": 3},
    {"name": "Gelatina de leche", "description": "Gelatina cremosa de leche con cajeta y nuez", "price": 60.00, "category": 4},
    {"name": "Tostadas de picadillo", "description": "Con picadillo de res, crema, queso y lechuga", "price": 115.00, "category": 1},
    {"name": "Pipián verde con pollo", "description": "Pollo en salsa de pepita, chile serrano y hierbas, con arroz", "price": 185.00, "category": 2},
]


async def seed(jwt: str) -> None:
    headers = {"Authorization": jwt, "Content-Type": "application/json"}

    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        # --- Mesas (solo si no se especifica offset) ---
        if len(sys.argv) <= 2:
            print("\n[MESAS] Creando 5 mesas...")
        for table in TABLES if len(sys.argv) <= 2 else []:
            r = await client.post("/api/tables/", json=table, headers=headers)
            if r.status_code == 201:
                data = r.json()
                print(f"  OK  Mesa #{data['number']} - {data.get('description', '')}")
            else:
                print(f"  ERR Mesa #{table['number']} - {r.status_code}: {r.text}")

        # --- Platillos ---
        offset = int(sys.argv[2]) if len(sys.argv) > 2 else 0
        batch = DISHES[offset:]
        print(f"\n[PLATILLOS] Creando {len(batch)} platillos (desde #{offset+1})...")
        ok = 0
        for dish in batch:
            r = await client.post("/api/dishes/", json=dish, headers=headers)
            if r.status_code == 201:
                data = r.json()
                print(f"  OK  {data['name']} - ${float(data['price']):.2f} + IVA ${float(data['tax']):.2f} = ${float(data['total_price']):.2f}")
                ok += 1
            else:
                print(f"  ERR {dish['name']} - {r.status_code}: {r.text}")

        print(f"\nSeed completo: {ok}/{len(batch)} platillos creados.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: uv run python seed.py <JWT>")
        sys.exit(1)
    asyncio.run(seed(sys.argv[1]))
