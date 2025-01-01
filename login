<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Tasty Treats</title>
    <link rel="stylesheet" href="styles.css">
    <style>
        body {
            font-family: 'Francois One ', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f4cae4 0%, #eeffa8 100%);
            margin: 0;
            min-height: 100vh;
            position: relative;
            overflow: hidden;
        }

        .floating-food {
            position: absolute;
            opacity: 0.4;
            animation: float 15s infinite linear;
            z-index: -1;
            font-size: 5rem;
        }

        .food-1 { top: 20%; left: 5%; animation-delay: 0s; }
        .food-2 { top: 30%; right: 10%; animation-delay: -3s; }
        .food-3 { bottom: 20%; left: 15%; animation-delay: -6s; }
        .food-4 { bottom: 40%; right: 20%; animation-delay: -9s; }
        .food-5 { top: 50%; left: 50%; animation-delay: -12s; }
        .food-6 { top: 15%; left: 30%; animation-delay: -15s; }
        .food-7 { bottom: 30%; right: 35%; animation-delay: -18s; }
        .food-8 { top: 60%; right: 45%; animation-delay: -21s; }

        @keyframes float {
            0% {
                transform: translate(0, 0) rotate(0deg);
            }
            25% {
                transform: translate(50px, 50px) rotate(90deg);
            }
            50% {
                transform: translate(0, 100px) rotate(180deg);
            }
            75% {
                transform: translate(-50px, 50px) rotate(270deg);
            }
            100% {
                transform: translate(0, 0) rotate(360deg);
            }
        }

        header {
            background-color: #ffe4ed;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            padding: 1rem;
            font-family:'shadows into light';
        }

        .logo {
            font-size: 2rem;
            font-weight: bold;
            color: #ff6b6b;
            text-align: center;
            margin-bottom: 1rem;
            font-family:'shadows into light';
        }

        nav ul {
            display: flex;
            justify-content: center;
            list-style: none;
            padding: 0;
            margin: 0;
            font-family:'shadows into light';   
            font-weight: 700;
        }

        nav ul li {
            margin: 0 1rem;
            
        }

        nav ul li a {
            text-decoration: none;
            color: #4a4a4a;
            font-weight: 500;
            transition: color 0.3s ease;
        }

        nav ul li a:hover {
            color: #ff6b6b;
        }

        .login-container {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 2rem;
            max-width: 400px;
            margin: 4rem auto;
            text-align: center;
            position: relative;
            z-index: 1;
            font-family: 'Francois One';
        }

        .login-container h2 {
            color: #333;
            margin-bottom: 2rem;
            font-size: 1.8rem;
            font-family:Georgia, 'Times New Roman', Times, serif;


        }

        #loginForm input {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1rem;
            transition: border-color 0.3s ease;
        }

        #loginForm input:focus {
            outline: none;
            border-color: #ff6b6b;
            box-shadow: 0 0 5px rgba(255,107,107,0.2);
        }

        #loginForm button {
            background-color: #ff6b6b;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 12px 30px;
            font-size: 1rem;
            cursor: pointer;
            transition: background-color 0.3s ease;
            width: 100%;
            margin-top: 1rem;
        }

        #loginForm button:hover {
            background-color: #ff5252;
        }

        #loginForm p {
            margin-top: 1rem;
            color: #666;
        }

        #loginForm a {
            color: #ff6b6b;
            text-decoration: none;
            font-weight: 500;
        }

        #loginForm a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="floating-food food-1">🍕</div>
    <div class="floating-food food-2">🍔</div>
    <div class="floating-food food-3">🥗</div>
    <div class="floating-food food-4">🍰</div>
    <div class="floating-food food-5">🍝</div>
    <div class="floating-food food-6">🍣</div>
    <div class="floating-food food-7">🌮</div>
    <div class="floating-food food-8">🍜</div>

    <header>
        <div class="logo">TASTY TREATS</div>
        <nav>
            <ul>
                <li><a href=landingpage.html>HOME</a></li>
                <li class="dropdown">
                    <a href="#">RECIPES</a>
                    <ul class="dropdown-menu">
                        <li><a href=breakfast.html>Breakfast</a></li>
                        <li><a href=lunch.html>Lunch</a></li>
                        <li><a href=dinner.html>Dinner</a></li>
                        <li><a href=cholesterol.html>Cholesterol</a></li>
                        <li><a href=heart-disease.html>Heart Disease</a></li>
                        <li><a href=high-blood-pressure.html>High Blood Pressure</a></li>
                        <li><a href=diabetes.html>Diabetes</a></li>
                    </ul>
                </li>
                <li><a href=login.html>LOGIN/SIGN UP</a></li>
            </ul>
        </nav>
    </header>

    <div class="login-container">
        <h2>Welcome Back!</h2>
        <form id="loginForm">
            <input type="email" id="email" placeholder="Enter your email" required>
            <input type="password" id="password" placeholder="Enter your password" required>
            <button type="submit">Sign In</button>
            <p>Don't have an account? <a href="signup.html">Create Account</a></p>
        </form>
    </div>

    <script>
        const loginForm = document.getElementById('loginForm');
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch('http://127.0.0.1:5000/login', {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Accept': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                const result = await response.json();

                if (response.ok) {
                    // Store user info in localStorage
                    localStorage.setItem('user', JSON.stringify({
                        username: result.username,
                        email: result.email,
                        id: result.id  // Make sure backend sends this
                    }));
                    window.location.href = 'dashboard.html';
                } else {
                    alert(result.message);
                }
            } catch (error) {
                console.error('Error during login:', error);
                alert('An error occurred. Please try again later.');
            }
        });
    </script>
</body>
</html>
