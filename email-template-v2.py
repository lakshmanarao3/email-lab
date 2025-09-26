<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lumen Service Renewal</title>
    <style>
        /* Reset and base styles */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; 
            line-height: 1.6; 
            color: #333; 
            background-color: #f8f8f8; 
        }
        
        /* Email container */
        .email-container {
            max-width: 600px;
            margin: 20px auto;
            background: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        /* Header - Official Lumen Blue with subtle gradient */
        .header {
            background: linear-gradient(135deg, #0C9ED9, #0a87c2);
            padding: 30px 20px;
            text-align: center;
        }
        .header img {
            max-width: 150px;
            height: auto;
        }
        .header-text {
            color: white;
            font-size: 18px;
            margin-top: 10px;
            font-weight: 300;
        }
        
        /* Main content */
        .content {
            padding: 40px 30px;
        }
        .greeting {
            font-size: 24px;
            font-weight: 300;
            margin-bottom: 20px;
            color: #333;
        }
        .message {
            font-size: 16px;
            margin-bottom: 25px;
            line-height: 1.5;
        }
        .account-info {
            background: #f0f9ff;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 30px;
            border-left: 4px solid #0C9ED9;
        }
        .account-number {
            font-weight: bold;
            color: #0C9ED9;
            font-size: 18px;
        }
        
        /* Services Table */
        .services-section {
            margin: 30px 0;
        }
        .services-title {
            font-size: 20px;
            font-weight: 600;
            color: #0C9ED9;
            margin-bottom: 15px;
        }
        .services-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 25px;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            overflow: hidden;
        }
        .services-table th {
            background: #0C9ED9;
            color: white;
            padding: 12px 15px;
            text-align: left;
            font-weight: 600;
            font-size: 14px;
        }
        .services-table td {
            padding: 12px 15px;
            border-bottom: 1px solid #f0f0f0;
            font-size: 14px;
        }
        .services-table tr:last-child td {
            border-bottom: none;
        }
        .services-table tr:nth-child(even) {
            background: #f9f9f9;
        }
        .services-table tr:hover {
            background: #f0f7ff;
        }
        .service-name {
            font-weight: 600;
            color: #0C9ED9;
        }
        .service-status {
            color: #28a745;
            font-weight: 500;
        }
        
        /* CTA Button - Official Lumen Blue */
        .cta-container {
            text-align: center;
            margin: 30px 0;
        }
        .cta-button {
            display: inline-block;
            background: #0C9ED9;
            color: white !important;
            padding: 15px 40px;
            text-decoration: none;
            border-radius: 4px;
            font-size: 16px;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: background 0.3s ease;
        }
        .cta-button:hover {
            background: #0a87c2;
        }
        
        /* Fallback link */
        .fallback-link {
            font-size: 14px;
            color: #666;
            text-align: center;
            margin-top: 20px;
            line-height: 1.4;
        }
        .fallback-link a {
            color: #0C9ED9;
            word-break: break-all;
        }
        
        /* Address section */
        .address-section {
            margin-top: 20px;
            padding: 15px;
            background: #f9f9f9;
            border-radius: 4px;
            font-size: 14px;
            color: #666;
        }
        
        /* Footer - Dark Blue with Lumen styling */
        .footer {
            background: linear-gradient(135deg, #0C9ED9, #0a87c2);
            color: #b3d1ff;
            padding: 30px 20px;
            text-align: center;
            font-size: 12px;
        }
        .footer img {
            max-width: 150px;
            height: auto;
        }
        .footer-text {
            color: white;
            font-size: 18px;
            margin-top: 10px;
            font-weight: 300;
        }
        .footer-links {
            margin: 15px 0;
        }
        .footer-links a {
            color: #b3d1ff;
            text-decoration: none;
            margin: 0 15px;
            font-size: 13px;
        }
        .footer-links a:hover {
            color: #ffffff;
        }
        .copyright {
            margin-top: 15px;
            font-size: 11px;
            color: #8bb3ff;
        }
        
        /* Responsive */
        @media (max-width: 600px) {
            .email-container { margin: 10px; border-radius: 0; }
            .content { padding: 30px 20px; }
            .greeting { font-size: 20px; }
            .cta-button { padding: 12px 30px; font-size: 14px; }
            .footer-links a { margin: 0 8px; }
            .services-table th, .services-table td {
                padding: 8px 10px;
                font-size: 12px;
            }
        }
    </style>
</head>
<body>
    <div class="email-container">
        <!-- Header with Lumen Logo -->
        <div class="header">
            <img src="https://www.lumen.com/content/dam/lumen/share/lumen_thumbnail.png" 
                 alt="Lumen Technologies Logo" aria-label="Lumen Technologies">
            <div class="header-text">The trusted network for AI</div>
        </div>
        
        <!-- Main Content -->
        <div class="content">
            <h1 class="greeting">Hi {{ customer_name }},</h1>
            
            <p class="message">
                It's time to renew your Lumen services! Continue enjoying our enterprise-grade connectivity, 
                cloud solutions, and security services without interruption.
            </p>
            
            <div class="account-info">
                <p>Account Number: <span class="account-number">{{ account_number }}</span></p>
            </div>
            
            <!-- Services Table -->
            <div class="services-section">
                <h3 class="services-title">Your Lumen Services</h3>
                <table class="services-table">
                    <thead>
                        <tr>
                            <th>Service</th>
                            <th>Contract End Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for product in products %}
                        <tr>
                            <td class="service-name">{{ product.name }}</td>
                            <td>{{ product.contract_end_date }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            
            {% if physical_address %}
            <div class="address-section">
                <strong>Billing Address:</strong><br>
                {{ physical_address }}
            </div>
            {% endif %}
            
            <!-- Call to Action -->
            <div class="cta-container">
                <a href="{{ renewal_link }}" class="cta-button" target="_blank" rel="noopener">
                    Renew Services
                </a>
            </div>
            
            <div class="fallback-link">
                If the button doesn't work, copy and paste this link into your browser:<br>
                <a href="{{ renewal_link }}" target="_blank" rel="noopener">{{ renewal_link }}</a>
            </div>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            <img src="https://www.lumen.com/content/dam/lumen/share/lumen_thumbnail.png" 
                 alt="Lumen Technologies Logo" aria-label="Lumen Technologies">
            
            <div class="footer-links">
                <a href="https://www.lumen.com/help.html" target="_blank">Support Center</a>
                <a href="https://www.lumen.com/legal.html" target="_blank">Terms of Service</a>
                <a href="https://www.lumen.com/legal/privacy-notice.html" target="_blank">Privacy Policy</a>
                <a href="#" target="_blank">Unsubscribe</a>
            </div>
            
            <div class="copyright">
                All information is confidential.<br>
                © 2025 Lumen Technologies, Inc. All rights reserved.
            </div>
        </div>
    </div>
</body>
</html>