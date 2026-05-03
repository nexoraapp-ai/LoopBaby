<!DOCTYPE html>
<html lang="it">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Progetto Ecommerce</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <link rel="stylesheet" href="styles.css">
</head>

<body>
    <!-- Header with Hamburger Menu -->
    <header>
        <div class="logo">
            <h1>La Mia Vetrina</h1>
        </div>
        <nav class="navbar">
            <ul>
                <li><a href="#home">Home</a></li>
                <li><a href="#box">Box</a></li>
                <li><a href="#vetrina">Vetrina</a></li>
                <li><a href="#info">Chi Siamo</a></li>
                <li><a href="#carrello">Carrello</a></li>
                <li><a href="#login">Login</a></li>
            </ul>
        </nav>
        <div class="hamburger-menu" onclick="toggleMenu()">
            <i class="fas fa-bars"></i>
        </div>
    </header>

    <!-- Main Section -->
    <main>
        <!-- Home Section -->
        <section id="home" class="section-home">
            <div class="welcome-message">
                <h2>Benvenuto nella nostra piattaforma</h2>
                <p>Scopri i nostri box personalizzati e acquista i tuoi capi di abbigliamento preferiti.</p>
            </div>
        </section>

        <!-- Box Section -->
        <section id="box" class="section-box">
            <h2>Personalizza il tuo Box</h2>
            <p>Seleziona i capi che desideri ricevere a casa.</p>
            <!-- Add dynamic content here (e.g., products) -->
            <button class="box-button">Aggiungi al tuo Box</button>
        </section>

        <!-- Vetrina Section -->
        <section id="vetrina" class="section-vetrina">
            <h2>Vetrina</h2>
            <div class="product-display">
                <div class="product-item">
                    <img src="product1.jpg" alt="Prodotto 1">
                    <p>Maglietta Uomo</p>
                    <button>Aggiungi al Carrello</button>
                </div>
                <div class="product-item">
                    <img src="product2.jpg" alt="Prodotto 2">
                    <p>Pantaloni Donna</p>
                    <button>Aggiungi al Carrello</button>
                </div>
                <!-- Add more products here -->
            </div>
        </section>

        <!-- Info Section -->
        <section id="info" class="section-info">
            <h2>Chi Siamo</h2>
            <p>Offriamo un servizio di box personalizzati per abbigliamento, pensato per chi ama lo shopping comodamente da casa.</p>
        </section>

        <!-- Carrello Section -->
        <section id="carrello" class="section-carrello">
            <h2>Il Tuo Carrello</h2>
            <div class="carrello-item">
                <p>Maglietta Uomo - €25</p>
                <button>Rimuovi</button>
            </div>
            <div class="carrello-item">
                <p>Pantaloni Donna - €40</p>
                <button>Rimuovi</button>
            </div>
            <p><strong>Totale: €65</strong></p>
            <button class="checkout-btn">Checkout</button>
        </section>

        <!-- Login Section -->
        <section id="login" class="section-login">
            <h2>Accedi al Tuo Account</h2>
            <form id="loginForm">
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required>
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" required>
                <button type="submit">Accedi</button>
            </form>
            <p><a href="#">Registrati</a> | <a href="#">Recupera Password</a></p>
        </section>
    </main>

    <!-- Footer -->
    <footer>
        <p>&copy; 2023 La Mia Vetrina. Tutti i diritti riservati.</p>
    </footer>

    <script src="scripts.js"></script>
</body>

</html>

<style>
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
    }

    header {
        background-color: #333;
        color: white;
        padding: 10px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .logo h1 {
        margin: 0;
    }

    .navbar ul {
        list-style: none;
        margin: 0;
        padding: 0;
        display: flex;
    }

    .navbar ul li {
        margin: 0 15px;
    }

    .navbar ul li a {
        color: white;
        text-decoration: none;
        font-size: 18px;
    }

    .hamburger-menu {
        display: none;
        cursor: pointer;
    }

    .hamburger-menu i {
        color: white;
        font-size: 24px;
    }

    .section-home,
    .section-box,
    .section-vetrina,
    .section-info,
    .section-carrello,
    .section-login {
        padding: 40px;
    }

    .product-display {
        display: flex;
        justify-content: space-between;
    }

    .product-item {
        text-align: center;
        width: 45%;
    }

    .box-button,
    .checkout-btn {
        background-color: #f0a500;
        border: none;
        padding: 10px 20px;
        color: white;
        cursor: pointer;
    }

    footer {
        background-color: #333;
        color: white;
        text-align: center;
        padding: 20px;
    }

    @media (max-width: 768px) {
        .navbar ul {
            display: none;
            flex-direction: column;
            width: 100%;
        }

        .navbar ul li {
            margin: 10px 0;
        }

        .hamburger-menu {
            display: block;
        }

        .navbar.active {
            display: block;
        }
    }
</style>

<script>
    function toggleMenu() {
        document.querySelector('.navbar').classList.toggle('active');
    }
</script>
