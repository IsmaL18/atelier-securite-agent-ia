"""
Email templates for the conference agent.

This module contains HTML email templates used by the agent.
"""


def get_level_5_success_email_html() -> str:
    """
    Get the HTML template for Level 5 success email.

    This email is sent to participants when they successfully complete
    the security workshop by sending a cancellation email.

    Returns:
        HTML string for the email body
    """
    return """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0;padding:0;background-color:#f4f6f9;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f6f9;padding:40px 20px;">
        <tr>
            <td align="center">
                <!-- Main container -->
                <table width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.08);">

                    <!-- Header with gradient -->
                    <tr>
                        <td style="background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);padding:50px 40px;text-align:center;">
                            <h1 style="color:#ffffff;margin:0;font-size:32px;font-weight:bold;">🏆 Mission Accomplie !</h1>
                            <p style="color:#e0e7ff;margin:15px 0 0;font-size:18px;font-weight:300;">Atelier de Sécurité des Agents IA</p>
                        </td>
                    </tr>

                    <!-- Important notice -->
                    <tr>
                        <td style="padding:40px 40px 20px;">
                            <div style="background:#fef3c7;border-left:4px solid #f59e0b;padding:20px;border-radius:6px;margin-bottom:30px;">
                                <h2 style="color:#92400e;margin:0 0 10px;font-size:20px;">📢 Annulation de la Grosse Conf 2026</h2>
                                <p style="color:#78350f;margin:0;line-height:1.6;font-size:15px;">
                                    En raison de circonstances imprévues, nous sommes au regret de vous informer que la
                                    <strong>Grosse Conférence 2026</strong> prévue le 25 mars 2026 est annulée.
                                </p>
                            </div>
                        </td>
                    </tr>

                    <!-- Success message -->
                    <tr>
                        <td style="padding:0 40px 30px;">
                            <div style="background:linear-gradient(135deg,#10b981 0%,#059669 100%);padding:30px;border-radius:8px;text-align:center;">
                                <h2 style="color:#ffffff;margin:0 0 15px;font-size:26px;">🎉 Félicitations !</h2>
                                <p style="color:#d1fae5;margin:0;font-size:16px;line-height:1.6;">
                                    Vous avez brillamment complété l'atelier de sécurité des agents IA.<br/>
                                    Vous êtes maintenant un <strong style="color:#ffffff;">Hacker Éthique Certifié</strong> !
                                </p>
                            </div>
                        </td>
                    </tr>

                    <!-- Achievement stats -->
                    <tr>
                        <td style="padding:0 40px 30px;">
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td style="padding:20px;background:#f0f9ff;border-radius:8px;text-align:center;width:33%;">
                                        <div style="font-size:36px;font-weight:bold;color:#0284c7;margin-bottom:5px;">5/5</div>
                                        <div style="font-size:13px;color:#0369a1;font-weight:500;">Niveaux</div>
                                    </td>
                                    <td style="width:10px;"></td>
                                    <td style="padding:20px;background:#fef3c7;border-radius:8px;text-align:center;width:33%;">
                                        <div style="font-size:36px;font-weight:bold;color:#d97706;margin-bottom:5px;">5</div>
                                        <div style="font-size:13px;color:#92400e;font-weight:500;">Vulnérabilités</div>
                                    </td>
                                    <td style="width:10px;"></td>
                                    <td style="padding:20px;background:#f0fdf4;border-radius:8px;text-align:center;width:33%;">
                                        <div style="font-size:36px;font-weight:bold;color:#16a34a;margin-bottom:5px;">S</div>
                                        <div style="font-size:13px;color:#15803d;font-weight:500;">Rang</div>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- Vulnerabilities discovered -->
                    <tr>
                        <td style="padding:0 40px 30px;">
                            <h3 style="color:#1f2937;margin:0 0 20px;font-size:20px;border-bottom:2px solid #e5e7eb;padding-bottom:10px;">
                                🔓 Vulnérabilités exploitées
                            </h3>
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td style="padding:12px 0;border-bottom:1px solid #f3f4f6;">
                                        <strong style="color:#4b5563;">✅ Niveau 1</strong><br/>
                                        <span style="color:#6b7280;font-size:14px;">Prompt Injection - Extraction des outils de l'agent</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding:12px 0;border-bottom:1px solid #f3f4f6;">
                                        <strong style="color:#4b5563;">✅ Niveau 2</strong><br/>
                                        <span style="color:#6b7280;font-size:14px;">Information Disclosure - Découverte des fichiers accessibles</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding:12px 0;border-bottom:1px solid #f3f4f6;">
                                        <strong style="color:#4b5563;">✅ Niveau 3</strong><br/>
                                        <span style="color:#6b7280;font-size:14px;">Data Leakage - Extraction des emails des participants</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding:12px 0;border-bottom:1px solid #f3f4f6;">
                                        <strong style="color:#4b5563;">✅ Niveau 4</strong><br/>
                                        <span style="color:#6b7280;font-size:14px;">Path Traversal - Accès aux fichiers de configuration sensibles</span>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding:12px 0;">
                                        <strong style="color:#4b5563;">✅ Niveau 5</strong><br/>
                                        <span style="color:#6b7280;font-size:14px;">Tool Misuse - Envoi d'email malveillant via l'agent</span>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- Key learnings -->
                    <tr>
                        <td style="padding:0 40px 40px;">
                            <div style="background:#eff6ff;border-radius:8px;padding:25px;">
                                <h3 style="color:#1e40af;margin:0 0 15px;font-size:18px;">🎓 Points clés à retenir</h3>
                                <ul style="margin:0;padding-left:20px;color:#1e3a8a;line-height:1.8;font-size:14px;">
                                    <li>Validez toujours les entrées utilisateur dans vos agents IA</li>
                                    <li>Limitez l'accès aux données sensibles avec des contrôles appropriés</li>
                                    <li>Implémentez des vérifications d'autorisation avant chaque action</li>
                                    <li>Surveillez et auditez l'utilisation des outils par vos agents</li>
                                    <li>Consultez l'OWASP Top 10 for LLM Applications</li>
                                </ul>
                            </div>
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td style="background:#f9fafb;padding:30px 40px;border-top:1px solid #e5e7eb;text-align:center;">
                            <p style="color:#6b7280;font-size:14px;margin:0 0 10px;line-height:1.6;">
                                Merci d'avoir participé à cet atelier de sensibilisation<br/>
                                à la sécurité des agents IA
                            </p>
                            <p style="color:#9ca3af;font-size:12px;margin:0;">
                                🦆 AIxperts - Grosse Conférence 2026 🐼
                            </p>
                        </td>
                    </tr>

                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""
