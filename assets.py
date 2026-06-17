def get_custom_css():
    """
    Returns custom CSS for a 'Google Light Theme' aesthetic.
    Features white background, clean borders, and Google colors for accents.
    """
    return """
    <style>
        /* Base Google Light Theme */
        .stApp {
            background-color: #FFFFFF; 
            color: #202124; /* Dark grey for readability */
            font-family: 'Google Sans', 'Roboto', 'Segoe UI', sans-serif;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: #000000; /* black */
            font-weight: 600;
        }
        
        /* Headers specific styling */
        h1 { text-shadow: 0 1px 2px rgba(66,133,244,0.1); }

        /* Google Styled Buttons */
        .stButton > button {
            background-color: #FFFFFF !important;
            color: #4285F4 !important;
            border: 1px solid #4285F4 !important;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            transition: all 0.3s ease-in-out;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .stButton > button:hover {
            background-color: #F8F9FA !important;
            color: #174EA6 !important; /* Darker blue on hover */
            border-color: #174EA6 !important;
            box-shadow: 0 4px 8px rgba(66, 133, 244, 0.2) !important;
            transform: translateY(-1px);
        }

        /* --- ACCESSIBILITY FIXES --- */
        
        /* High Contrast Focus Rings for Keyboard Navigation */
        button:focus, input:focus, textarea:focus, select:focus, a:focus {
            outline: 3px solid #005fcc !important; /* High contrast blue against white background */
            outline-offset: 2px !important;
            box-shadow: 0 0 0 4px rgba(0, 95, 204, 0.4) !important;
        }

        /* Strict requirement from user */
        *:focus-visible { 
            outline: 3px solid #005fcc !important; 
            outline-offset: 2px !important; 
        }

        /* Ensure main body text maintains high contrast (4.5:1 ratio) against white background */
        p, span, div, label {
            color: #202124; /* Dark grey ensures WCAG AA compliance on #FFFFFF background */
        }
        
        /* Specific Button for the main action (Red accent) */
        .stButton > button[key="diagnostic_btn"] {
            border-color: #EA4335 !important;
            color: #EA4335 !important;
        }
        .stButton > button[key="diagnostic_btn"]:hover {
            background-color: #FCE8E6 !important;
            color: #C5221F !important;
            box-shadow: 0 4px 8px rgba(234, 67, 53, 0.2) !important;
        }

        /* Input Fields */
        .stTextInput > div > div > input, .stChatInput > div > div > textarea {
            background-color: #FFFFFF !important;
            color: #202124 !important;
            border: 1px solid #DADCE0 !important;
            border-radius: 8px;
        }

        .stTextInput > div > div > input:focus, .stChatInput > div > div > textarea:focus {
            border-color: #005fcc !important;
        }

        /* Chat Messages */
        .stChatMessage {
            background-color: #F8F9FA;
            border: 1px solid #E8EAED;
            border-radius: 12px;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        
        .stChatMessage[data-testid="chatAvatarIcon-user"] {
            border-left: 4px solid #34A853; /* Google Green for user */
            background-color: #F1F8F4;
        }
        
        .stChatMessage[data-testid="chatAvatarIcon-assistant"] {
            border-left: 4px solid #4285F4; /* Google Blue for AI */
            background-color: #E8F0FE;
        }
        
        /* Metric Cards */
        [data-testid="stMetric"] {
            background-color: #FFFFFF;
            border: 1px solid #DADCE0;
            border-radius: 12px;
            padding: 1.2rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: box-shadow 0.2s ease-in-out;
        }
        
        [data-testid="stMetric"]:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        [data-testid="stMetricValue"] {
            color: #202124 !important;
            font-weight: 700;
        }
        
        [data-testid="stMetricDelta"] {
            color: #34A853 !important; /* Green */
        }
        
        /* Dataframes */
        .stDataFrame {
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid #DADCE0;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #F8F9FA;
            border-right: 1px solid #E8EAED;
        }
    </style>
    """


def get_threejs_html():
    """
    Returns HTML string containing a pure CSS glowing text with a grey-to-black gradient.
    Refactored with ARIA labels and semantic wrappers for accessibility.
    """
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Carbon 0 Header</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@900&display=swap');
            
            body { 
                margin: 0; 
                display: flex; 
                justify-content: center; 
                align-items: center; 
                height: 100vh; 
                background-color: #FFFFFF; 
                overflow: hidden;
            }
            .glowing-text {
                font-family: 'Roboto', sans-serif;
                font-size: 90px;
                font-weight: 900;
                letter-spacing: 4px;
                margin: 0;
                
                /* Black and Grey Gradient */
                background: linear-gradient(to bottom, #AAAAAA 0%, #000000 80%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                
                /* Glowing Grey effect */
                filter: drop-shadow(0px 10px 25px rgba(170, 170, 170, 0.8));
                
                /* Simple floating animation */
                animation: float 4s ease-in-out infinite;
            }
            
            @keyframes float {
                0% { transform: translateY(0px); }
                50% { transform: translateY(-10px); }
                100% { transform: translateY(0px); }
            }
            
            header {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <header role="banner" aria-label="Carbon 0 Platform Banner">
            <h1 class="glowing-text" aria-label="CARBON 0 Title">CARBON 0</h1>
            <!-- Hidden decorative element to satisfy aria-hidden requirements if needed -->
            <div aria-hidden="true" class="decorative-glow"></div>
            <p style="position: absolute; bottom: 20px; font-family: 'Roboto', sans-serif; color: #202124;">Daily Carbon Tracker</p>
            <p style="position: absolute; bottom: 5px; font-family: 'Roboto', sans-serif; font-size: 7px; color: #202124;">[2026] | Himanshu Jain</p>
        </header>
    </body>
    </html>
    """
