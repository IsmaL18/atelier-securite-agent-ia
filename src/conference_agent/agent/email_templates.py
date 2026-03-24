"""
Email templates for the conference agent.

This module contains HTML email templates used by the agent.
"""


def get_final_level_success_email_html() -> str:
    """
    Get the HTML template for the final level success email.

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
                                    <strong>Grosse Conf 2026</strong> prévue le 25 mars 2026 est annulée.
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
                                        <div style="font-size:36px;font-weight:bold;color:#0284c7;margin-bottom:5px;">4/4</div>
                                        <div style="font-size:13px;color:#0369a1;font-weight:500;">Niveaux</div>
                                    </td>
                                    <td style="width:10px;"></td>
                                    <td style="padding:20px;background:#fef3c7;border-radius:8px;text-align:center;width:33%;">
                                        <div style="font-size:36px;font-weight:bold;color:#d97706;margin-bottom:5px;">4</div>
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

                    <!-- Vulnérabilités exploitées par niveau -->
                    <tr>
                        <td style="padding:0 40px 30px;">
                            <h3 style="color:#1f2937;margin:0 0 20px;font-size:20px;border-bottom:2px solid #e5e7eb;padding-bottom:10px;">
                                🎯 Vulnérabilités exploitées dans l'atelier
                            </h3>
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td style="padding:10px;background:#f0f9ff;border-radius:6px;margin-bottom:8px;">
                                        <strong style="color:#0284c7;">✅ Niveau 1 — Reconnaissance</strong><br/>
                                        <span style="font-size:13px;color:#0369a1;">LLM01 Prompt Injection · LLM07 System Prompt Leakage</span><br/>
                                        <span style="font-size:12px;color:#6b7280;">Extraction des outils internes de l'agent</span>
                                    </td>
                                </tr>
                                <tr><td style="height:8px;"></td></tr>
                                <tr>
                                    <td style="padding:10px;background:#fef3c7;border-radius:6px;">
                                        <strong style="color:#d97706;">✅ Niveau 2 — Data Leakage</strong><br/>
                                        <span style="font-size:13px;color:#92400e;">LLM02 Sensitive Information Disclosure · LLM06 Excessive Agency</span><br/>
                                        <span style="font-size:12px;color:#6b7280;">Extraction des emails des participants</span>
                                    </td>
                                </tr>
                                <tr><td style="height:8px;"></td></tr>
                                <tr>
                                    <td style="padding:10px;background:#fee2e2;border-radius:6px;">
                                        <strong style="color:#dc2626;">✅ Niveau 3 — Indirect Prompt Injection</strong><br/>
                                        <span style="font-size:13px;color:#991b1b;">LLM01 Prompt Injection (indirect) · LLM05 Improper Output Handling · LLM07 System Prompt Leakage</span><br/>
                                        <span style="font-size:12px;color:#6b7280;">Modification des instructions de l'agent</span>
                                    </td>
                                </tr>
                                <tr><td style="height:8px;"></td></tr>
                                <tr>
                                    <td style="padding:10px;background:#ede9fe;border-radius:6px;">
                                        <strong style="color:#7c3aed;">✅ Niveau 4 — Tool Misuse</strong><br/>
                                        <span style="font-size:13px;color:#5b21b6;">LLM06 Excessive Agency · LLM01 Prompt Injection · LLM05 Improper Output Handling</span><br/>
                                        <span style="font-size:12px;color:#6b7280;">Envoi d'email malveillant via l'agent</span>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- OWASP Top 10 LLM Applications 2025 -->
                    <tr>
                        <td style="padding:0 40px 30px;">
                            <h3 style="color:#1f2937;margin:0 0 20px;font-size:20px;border-bottom:2px solid #e5e7eb;padding-bottom:10px;">
                                🔓 OWASP Top 10 LLM Applications (2025)
                            </h3>
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr><td style="padding:8px 0;border-bottom:1px solid #f3f4f6;font-size:14px;"><strong style="color:#4b5563;">LLM01</strong> <span style="color:#6b7280;">Prompt Injection — Des entrées malveillantes détournent le comportement du modèle</span></td></tr>
                                <tr><td style="padding:8px 0;border-bottom:1px solid #f3f4f6;font-size:14px;"><strong style="color:#4b5563;">LLM02</strong> <span style="color:#6b7280;">Sensitive Information Disclosure — Exposition de PII, credentials ou secrets</span></td></tr>
                                <tr><td style="padding:8px 0;border-bottom:1px solid #f3f4f6;font-size:14px;"><strong style="color:#4b5563;">LLM03</strong> <span style="color:#6b7280;">Supply Chain — Composants compromis en amont (modèles, plugins, datasets)</span></td></tr>
                                <tr><td style="padding:8px 0;border-bottom:1px solid #f3f4f6;font-size:14px;"><strong style="color:#4b5563;">LLM04</strong> <span style="color:#6b7280;">Data and Model Poisoning — Corruption des données d'entraînement</span></td></tr>
                                <tr><td style="padding:8px 0;border-bottom:1px solid #f3f4f6;font-size:14px;"><strong style="color:#4b5563;">LLM05</strong> <span style="color:#6b7280;">Improper Output Handling — Sorties injectées sans validation dans d'autres systèmes</span></td></tr>
                                <tr><td style="padding:8px 0;border-bottom:1px solid #f3f4f6;font-size:14px;"><strong style="color:#4b5563;">LLM06</strong> <span style="color:#6b7280;">Excessive Agency — Permissions et autonomie au-delà des besoins réels</span></td></tr>
                                <tr><td style="padding:8px 0;border-bottom:1px solid #f3f4f6;font-size:14px;"><strong style="color:#4b5563;">LLM07</strong> <span style="color:#6b7280;">System Prompt Leakage — Extraction du prompt système et de la logique métier</span></td></tr>
                                <tr><td style="padding:8px 0;border-bottom:1px solid #f3f4f6;font-size:14px;"><strong style="color:#4b5563;">LLM08</strong> <span style="color:#6b7280;">Vector and Embedding Weaknesses — Bases vectorielles RAG vulnérables</span></td></tr>
                                <tr><td style="padding:8px 0;border-bottom:1px solid #f3f4f6;font-size:14px;"><strong style="color:#4b5563;">LLM09</strong> <span style="color:#6b7280;">Misinformation — Hallucinations propagées en cascade dans les décisions</span></td></tr>
                                <tr><td style="padding:8px 0;font-size:14px;"><strong style="color:#4b5563;">LLM10</strong> <span style="color:#6b7280;">Unbounded Consumption — Saturation des ressources et explosion des coûts</span></td></tr>
                            </table>
                        </td>
                    </tr>

                    <!-- 4 Messages clés -->
                    <tr>
                        <td style="padding:0 40px 30px;">
                            <div style="background:linear-gradient(135deg,#1e3a5f 0%,#2d1b69 100%);border-radius:8px;padding:25px;color:#ffffff;">
                                <h3 style="color:#fbbf24;margin:0 0 15px;font-size:18px;">⚡ Messages clés</h3>
                                <div style="margin-bottom:10px;padding:10px;background:rgba(255,255,255,0.1);border-radius:6px;border-left:3px solid #fbbf24;">
                                    <strong>Un agent IA = un système d'information qui parle.</strong><br/>
                                    <span style="font-size:13px;color:#e0e7ff;">Mêmes exigences que tout SI critique : auth, droits, traçabilité, validation, supervision.</span>
                                </div>
                                <div style="margin-bottom:10px;padding:10px;background:rgba(255,255,255,0.1);border-radius:6px;border-left:3px solid #f87171;">
                                    <strong>Le vrai danger commence quand l'IA peut agir.</strong><br/>
                                    <span style="font-size:13px;color:#e0e7ff;">Répondre est une chose. Appeler un outil, une API ou un service en est une autre.</span>
                                </div>
                                <div style="margin-bottom:10px;padding:10px;background:rgba(255,255,255,0.1);border-radius:6px;border-left:3px solid #34d399;">
                                    <strong>La sécurité se joue en dehors du modèle.</strong><br/>
                                    <span style="font-size:13px;color:#e0e7ff;">Le prompt n'est pas une barrière de sécurité. Les contrôles doivent être dans une couche logicielle déterministe.</span>
                                </div>
                                <div style="padding:10px;background:rgba(255,255,255,0.1);border-radius:6px;border-left:3px solid #60a5fa;">
                                    <strong>Raisonner "blast radius".</strong><br/>
                                    <span style="font-size:13px;color:#e0e7ff;">Si l'agent est manipulé : que peut-il voir ? Que peut-il faire ? Quel est l'impact max ?</span>
                                </div>
                            </div>
                        </td>
                    </tr>

                    <!-- 2 Principes fondamentaux OWASP -->
                    <tr>
                        <td style="padding:0 40px 30px;">
                            <div style="background:#eff6ff;border-radius:8px;padding:25px;">
                                <h3 style="color:#1e40af;margin:0 0 15px;font-size:18px;">🛡️ Les 2 principes fondamentaux (OWASP)</h3>
                                <p style="margin:0 0 10px;color:#1e3a8a;font-size:14px;line-height:1.6;">
                                    <strong>Least Agency</strong> — Ne donner à un agent que l'autonomie strictement nécessaire. Moins d'outils, moins de droits, moins d'autonomie.
                                </p>
                                <p style="margin:0;color:#1e3a8a;font-size:14px;line-height:1.6;">
                                    <strong>Strong Observability</strong> — Monitorer en temps réel ce que fait l'agent, pourquoi, avec quels outils et quelles identités.
                                </p>
                                <p style="margin:10px 0 0;color:#3b82f6;font-size:13px;font-style:italic;">L'un sans l'autre ne suffit pas.</p>
                            </div>
                        </td>
                    </tr>

                    <!-- Chiffres marquants -->
                    <tr>
                        <td style="padding:0 40px 30px;">
                            <h3 style="color:#1f2937;margin:0 0 15px;font-size:18px;border-bottom:2px solid #e5e7eb;padding-bottom:10px;">📊 Chiffres marquants</h3>
                            <table width="100%" cellpadding="0" cellspacing="8">
                                <tr>
                                    <td style="padding:15px;background:#fef3c7;border-radius:8px;text-align:center;width:50%;">
                                        <div style="font-size:28px;font-weight:bold;color:#d97706;">82:1</div>
                                        <div style="font-size:12px;color:#92400e;margin-top:5px;">Identités machines vs humaines en entreprise (<a href="https://www.paloaltonetworks.com/blog/2025/11/2026-predictions-for-autonomous-ai/" style="color:#92400e;">Palo Alto Networks</a>)</div>
                                    </td>
                                    <td style="padding:15px;background:#fce7f3;border-radius:8px;text-align:center;width:50%;">
                                        <div style="font-size:28px;font-weight:bold;color:#db2777;">80%</div>
                                        <div style="font-size:12px;color:#9d174d;margin-top:5px;">Des organisations ont rencontré des comportements risqués d'agents (<a href="https://www.mintmcp.com/blog/ai-agent-security" style="color:#9d174d;">Kiteworks 2025</a>)</div>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding:15px;background:#fee2e2;border-radius:8px;text-align:center;width:50%;">
                                        <div style="font-size:14px;font-weight:bold;color:#dc2626;">Sept. 2025</div>
                                        <div style="font-size:12px;color:#991b1b;margin-top:5px;">Première cyberattaque orchestrée intégralement par des agents IA (<a href="https://www.anthropic.com/news/disrupting-AI-espionage" style="color:#991b1b;">Anthropic</a>)</div>
                                    </td>
                                    <td style="padding:15px;background:#ede9fe;border-radius:8px;text-align:center;width:50%;">
                                        <div style="font-size:28px;font-weight:bold;color:#7c3aed;">1 184</div>
                                        <div style="font-size:12px;color:#5b21b6;margin-top:5px;">Skills malveillantes détectées sur ClawHub, fév. 2026 (<a href="https://blog.cyberdesserts.com/ai-agent-security-risks/" style="color:#5b21b6;">Antiy CERT / Trend Micro</a>)</div>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- 10 Règles de sécurité -->
                    <tr>
                        <td style="padding:0 40px 30px;">
                            <div style="background:#f0fdf4;border-radius:8px;padding:25px;">
                                <h3 style="color:#166534;margin:0 0 15px;font-size:18px;">📋 Les 10 règles pour sécuriser vos agents</h3>
                                <ol style="margin:0;padding-left:20px;color:#14532d;line-height:2;font-size:13px;">
                                    <li><strong>Réduire l'agency</strong> — Moins d'outils, moins de droits, plusieurs agents spécialisés</li>
                                    <li><strong>Séparer raisonnement, vérification et action</strong> — Pas d'exécution directe sans contrôle</li>
                                    <li><strong>Garde-fous sur chaque outil</strong> — Allowlist, schéma strict, validation, journalisation</li>
                                    <li><strong>Tout contenu externe = non fiable</strong> — PDF, emails, tickets, sorties d'autres agents</li>
                                    <li><strong>Protéger secrets et contexte</strong> — Jamais de secret dans les prompts, coffre dédié</li>
                                    <li><strong>Encadrer la mémoire</strong> — TTL, validation avant persistance, séparation par tenant</li>
                                    <li><strong>Sécuriser RAG et bases vectorielles</strong> — Contrôle d'accès, provenance, segmentation</li>
                                    <li><strong>Human-in-the-loop pour actions sensibles</strong> — Finance, RH, juridique, production</li>
                                    <li><strong>Isoler les environnements d'exécution</strong> — Sandbox, conteneurs éphémères, kill switch</li>
                                    <li><strong>Red teamer avant production, surveiller en continu</strong> — Tester injection, exfiltration, dérives</li>
                                </ol>
                            </div>
                        </td>
                    </tr>

                    <!-- Checklist avant/en prod -->
                    <tr>
                        <td style="padding:0 40px 30px;">
                            <table width="100%" cellpadding="0" cellspacing="0">
                                <tr>
                                    <td style="padding:15px;background:#dbeafe;border-radius:8px 0 0 8px;vertical-align:top;width:50%;">
                                        <h4 style="color:#1e40af;margin:0 0 8px;font-size:14px;">✅ Avant mise en prod</h4>
                                        <p style="margin:0;color:#1e3a8a;font-size:12px;line-height:1.8;">
                                            Permissions minimales · Secrets hors prompts · Sources RAG approuvées · Human approval actions critiques · Sandbox · Logs activés · Tests d'injection · Kill switch
                                        </p>
                                    </td>
                                    <td style="width:5px;"></td>
                                    <td style="padding:15px;background:#fef9c3;border-radius:0 8px 8px 0;vertical-align:top;width:50%;">
                                        <h4 style="color:#854d0e;margin:0 0 8px;font-size:14px;">🔄 En production</h4>
                                        <p style="margin:0;color:#713f12;font-size:12px;line-height:1.8;">
                                            Monitorer coûts/outils/dérives · Revoir permissions · Auditer mémoires · Mettre à jour tests d'attaque
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- Ressources OWASP -->
                    <tr>
                        <td style="padding:0 40px 40px;">
                            <div style="background:#f9fafb;border:1px solid #e5e7eb;border-radius:8px;padding:20px;">
                                <h3 style="color:#1f2937;margin:0 0 12px;font-size:16px;">📚 Ressources pour aller plus loin</h3>
                                <ul style="margin:0;padding-left:20px;color:#4b5563;line-height:2;font-size:13px;">
                                    <li><a href="https://genai.owasp.org/llm-top-10/" style="color:#4f46e5;">OWASP Top 10 LLM Applications 2025</a></li>
                                    <li><a href="https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/" style="color:#4f46e5;">OWASP Top 10 Agentic Applications 2026</a></li>
                                    <li><a href="https://genai.owasp.org" style="color:#4f46e5;">Securing Agentic Applications Guide v1.0</a></li>
                                    <li><a href="https://genai.owasp.org/resource/a-practical-guide-for-secure-mcp-server-development/" style="color:#4f46e5;">Secure MCP Server Development Guide</a></li>
                                    <li><a href="https://www.youtube.com/watch?v=67fBGjTrrJc" style="color:#4f46e5;">🎬 Vidéo OCTO Technology — Sécurité des agents IA</a></li>
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
                                AIxperts - Grosse Conf 2026
                            </p>
                        </td>
                    </tr>

                </table>
            </td>
        </tr>
    </table>
</body>
</html>"""
