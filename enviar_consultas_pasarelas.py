"""
Script para enviar correos de consulta a pasarelas de pago
sobre tarifas y agendar llamadas para el viernes 10am-4pm
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import List, Dict
from datetime import datetime

# Configuración de correo (configurar con tus credenciales)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")  # Cambiar según tu proveedor
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
EMAIL_FROM = os.getenv("EMAIL_FROM", "")  # Tu correo electrónico
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")  # Tu contraseña o app password

# Información del contacto
TU_NOMBRE = os.getenv("TU_NOMBRE", "Tu Nombre")
TU_EMPRESA = os.getenv("TU_EMPRESA", "Tu Empresa")
TU_TELEFONO = os.getenv("TU_TELEFONO", "")

# Pasarelas prioritarias para contactar
PASARELAS_PRIORITARIAS = [
    {
        "nombre": "dLocal",
        "email": "sales@dlocal.com",  # Email genérico, verificar en su sitio
        "url": "https://www.dlocal.com",
        "notas": "Muy popular en LatAm para high-risk, tarifas negociables"
    },
    {
        "nombre": "EBANX",
        "email": "contact@ebanx.com",  # Email genérico, verificar en su sitio
        "url": "https://www.ebanx.com/en/",
        "notas": "Muy popular en LatAm, tarifas negociables"
    },
    {
        "nombre": "SegPay",
        "email": "sales@segpay.com",  # Email genérico, verificar en su sitio
        "url": "https://segpay.com/verticals/high-risk/",
        "notas": "Especializado en high-risk/apuestas"
    },
    {
        "nombre": "EasyPayDirect",
        "email": "info@easypaydirect.com",  # Email genérico, verificar en su sitio
        "url": "https://www.easypaydirect.com/merchant-accounts/high-risk-credit-card-processing",
        "notas": "Especializado en high-risk/apuestas"
    },
    {
        "nombre": "PayU México",
        "email": "mexico@payu.com",  # Email genérico, verificar en su sitio
        "url": "https://corporate.payu.com/mexico/",
        "notas": "Presencia específica en México"
    },
    {
        "nombre": "Adyen",
        "email": "sales@adyen.com",  # Email genérico, verificar en su sitio
        "url": "https://www.adyen.com",
        "notas": "Para alto volumen, tarifas muy competitivas (0.6%-1.5%)"
    },
    {
        "nombre": "Checkout.com",
        "email": "sales@checkout.com",  # Email genérico, verificar en su sitio
        "url": "https://www.checkout.com",
        "notas": "Para alto volumen, tarifas muy competitivas (0.8%-1.2%)"
    },
    {
        "nombre": "Mobbex",
        "email": "contacto@mobbex.com",  # Email genérico, verificar en su sitio
        "url": "https://www.mobbex.com",
        "notas": "Popular en Argentina, expandiéndose a LatAm"
    },
    {
        "nombre": "ePayco",
        "email": "ventas@epayco.com",  # Email genérico, verificar en su sitio
        "url": "https://epayco.com/tarifas/",
        "notas": "Popular en Colombia"
    },
    {
        "nombre": "ETPay",
        "email": "contacto@etpay.com",  # Email genérico, verificar en su sitio
        "url": "https://etpay.com/mx-es/tarifas",
        "notas": "Tiene sitio específico para México"
    },
    {
        "nombre": "Fiserv México",
        "email": "mexico@fiserv.com",  # Email genérico, verificar en su sitio
        "url": "https://www.fiserv.com.mx",
        "notas": "Soluciones empresariales"
    }
]

def crear_mensaje(pasarela: Dict, tu_email: str, tu_nombre: str, tu_empresa: str, tu_telefono: str) -> MIMEMultipart:
    """Crea el mensaje de correo para una pasarela"""
    
    mensaje = MIMEMultipart("alternative")
    mensaje["Subject"] = f"Consulta: Tarifas y Servicios para Industria de Apuestas en México - {pasarela['nombre']}"
    mensaje["From"] = tu_email
    mensaje["To"] = pasarela["email"]
    
    # Cuerpo del mensaje en texto plano
    texto = f"""
Estimado equipo de {pasarela['nombre']},

Espero que este mensaje les encuentre bien. Me dirijo a ustedes para solicitar información sobre sus servicios de procesamiento de pagos para nuestra empresa en México.

INFORMACIÓN DE NUESTRA EMPRESA:
- Nombre: {tu_empresa}
- Contacto: {tu_nombre}
- Email: {tu_email}
- Teléfono: {tu_telefono}
- Industria: Apuestas en línea / Gaming
- País de operación: México

SOLICITUD DE INFORMACIÓN:
Estamos evaluando diferentes pasarelas de pago para integrar en nuestra plataforma y nos gustaría conocer:

1. Tarifas y comisiones actuales para procesamiento de pagos en México
2. Políticas y requisitos para trabajar con empresas del sector de apuestas/gaming
3. Métodos de pago disponibles (tarjetas, transferencias bancarias, efectivo, etc.)
4. Requisitos de volumen mínimo (si aplica)
5. Tiempos de integración y disponibilidad de documentación técnica
6. Términos de disponibilidad de fondos
7. Medidas de seguridad y prevención de fraude

AGENDA DE LLAMADA:
Nos gustaría agendar una llamada para discutir estos puntos en detalle. Estamos disponibles el viernes en el siguiente horario:
- Horario: 10:00 AM - 4:00 PM (hora de México)
- Preferencia: Llamada telefónica o videollamada

Por favor, indíquennos qué horario les conviene mejor dentro de este rango y nos pondremos en contacto para confirmar.

Agradezco de antemano su tiempo y atención. Quedo a la espera de su respuesta.

Saludos cordiales,
{tu_nombre}
{tu_empresa}
{tu_email}
{tu_telefono}
"""
    
    # Versión HTML del mensaje
    html = f"""
    <html>
      <body>
        <p>Estimado equipo de <strong>{pasarela['nombre']}</strong>,</p>
        
        <p>Espero que este mensaje les encuentre bien. Me dirijo a ustedes para solicitar información sobre sus servicios de procesamiento de pagos para nuestra empresa en México.</p>
        
        <h3>INFORMACIÓN DE NUESTRA EMPRESA:</h3>
        <ul>
          <li><strong>Nombre:</strong> {tu_empresa}</li>
          <li><strong>Contacto:</strong> {tu_nombre}</li>
          <li><strong>Email:</strong> {tu_email}</li>
          <li><strong>Teléfono:</strong> {tu_telefono}</li>
          <li><strong>Industria:</strong> Apuestas en línea / Gaming</li>
          <li><strong>País de operación:</strong> México</li>
        </ul>
        
        <h3>SOLICITUD DE INFORMACIÓN:</h3>
        <p>Estamos evaluando diferentes pasarelas de pago para integrar en nuestra plataforma y nos gustaría conocer:</p>
        <ol>
          <li>Tarifas y comisiones actuales para procesamiento de pagos en México</li>
          <li>Políticas y requisitos para trabajar con empresas del sector de apuestas/gaming</li>
          <li>Métodos de pago disponibles (tarjetas, transferencias bancarias, efectivo, etc.)</li>
          <li>Requisitos de volumen mínimo (si aplica)</li>
          <li>Tiempos de integración y disponibilidad de documentación técnica</li>
          <li>Términos de disponibilidad de fondos</li>
          <li>Medidas de seguridad y prevención de fraude</li>
        </ol>
        
        <h3>AGENDA DE LLAMADA:</h3>
        <p>Nos gustaría agendar una llamada para discutir estos puntos en detalle. Estamos disponibles el <strong>viernes</strong> en el siguiente horario:</p>
        <ul>
          <li><strong>Horario:</strong> 10:00 AM - 4:00 PM (hora de México)</li>
          <li><strong>Preferencia:</strong> Llamada telefónica o videollamada</li>
        </ul>
        <p>Por favor, indíquennos qué horario les conviene mejor dentro de este rango y nos pondremos en contacto para confirmar.</p>
        
        <p>Agradezco de antemano su tiempo y atención. Quedo a la espera de su respuesta.</p>
        
        <p>Saludos cordiales,<br>
        <strong>{tu_nombre}</strong><br>
        {tu_empresa}<br>
        {tu_email}<br>
        {tu_telefono}</p>
      </body>
    </html>
    """
    
    parte_texto = MIMEText(texto, "plain", "utf-8")
    parte_html = MIMEText(html, "html", "utf-8")
    
    mensaje.attach(parte_texto)
    mensaje.attach(parte_html)
    
    return mensaje

def enviar_correos(pasarelas: List[Dict], tu_email: str, tu_password: str, 
                   tu_nombre: str, tu_empresa: str, tu_telefono: str, 
                   solo_preview: bool = True):
    """Envía correos a las pasarelas especificadas"""
    
    if not tu_email or not tu_password:
        print("❌ ERROR: Debes configurar EMAIL_FROM y EMAIL_PASSWORD")
        print("\nPuedes configurarlos como variables de entorno:")
        print("export EMAIL_FROM='tu_email@gmail.com'")
        print("export EMAIL_PASSWORD='tu_password'")
        return
    
    print(f"\n{'='*70}")
    print(f"ENVÍO DE CORREOS A PASARELAS DE PAGO")
    print(f"{'='*70}\n")
    print(f"De: {tu_email}")
    print(f"Nombre: {tu_nombre}")
    print(f"Empresa: {tu_empresa}")
    print(f"Teléfono: {tu_telefono}")
    print(f"\nTotal de pasarelas: {len(pasarelas)}")
    print(f"Modo: {'PREVIEW (no se enviarán)' if solo_preview else 'ENVÍO REAL'}\n")
    
    if solo_preview:
        print("⚠️  MODO PREVIEW - Los correos NO se enviarán realmente")
        print("   Para enviar realmente, ejecuta con solo_preview=False\n")
    
    resultados = []
    
    for i, pasarela in enumerate(pasarelas, 1):
        print(f"\n[{i}/{len(pasarelas)}] {pasarela['nombre']}")
        print(f"   Email: {pasarela['email']}")
        print(f"   URL: {pasarela['url']}")
        
        try:
            mensaje = crear_mensaje(pasarela, tu_email, tu_nombre, tu_empresa, tu_telefono)
            
            if solo_preview:
                print(f"   ✅ Mensaje creado (PREVIEW)")
                print(f"   Asunto: {mensaje['Subject']}")
                resultados.append({"pasarela": pasarela["nombre"], "estado": "PREVIEW OK"})
            else:
                # Enviar correo real
                with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as servidor:
                    servidor.starttls()
                    servidor.login(tu_email, tu_password)
                    servidor.send_message(mensaje)
                
                print(f"   ✅ Correo enviado exitosamente")
                resultados.append({"pasarela": pasarela["nombre"], "estado": "ENVIADO"})
        
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            resultados.append({"pasarela": pasarela["nombre"], "estado": f"ERROR: {str(e)}"})
    
    # Resumen
    print(f"\n{'='*70}")
    print("RESUMEN")
    print(f"{'='*70}")
    for resultado in resultados:
        estado_icono = "✅" if "OK" in resultado["estado"] or "ENVIADO" in resultado["estado"] else "❌"
        print(f"{estado_icono} {resultado['pasarela']}: {resultado['estado']}")
    
    print(f"\n{'='*70}\n")

def main():
    """Función principal"""
    print("="*70)
    print("ENVÍO DE CONSULTAS A PASARELAS DE PAGO")
    print("="*70)
    print("\nEste script enviará correos a las pasarelas de pago para solicitar")
    print("información sobre tarifas y agendar llamadas para el viernes 10am-4pm.\n")
    
    # Obtener configuración
    tu_email = EMAIL_FROM or input("Tu correo electrónico: ").strip()
    tu_password = EMAIL_PASSWORD or input("Tu contraseña (o app password): ").strip()
    tu_nombre = TU_NOMBRE if TU_NOMBRE != "Tu Nombre" else input("Tu nombre: ").strip()
    tu_empresa = TU_EMPRESA if TU_EMPRESA != "Tu Empresa" else input("Nombre de tu empresa: ").strip()
    tu_telefono = TU_TELEFONO or input("Tu teléfono (opcional): ").strip()
    
    if not tu_email or not tu_password:
        print("\n❌ Error: Se requiere correo y contraseña")
        return
    
    # Confirmar antes de enviar
    print(f"\n{'='*70}")
    print("CONFIGURACIÓN:")
    print(f"  Email: {tu_email}")
    print(f"  Nombre: {tu_nombre}")
    print(f"  Empresa: {tu_empresa}")
    print(f"  Teléfono: {tu_telefono}")
    print(f"  Pasarelas a contactar: {len(PASARELAS_PRIORITARIAS)}")
    print(f"{'='*70}\n")
    
    # Primero hacer preview
    print("Primero se mostrará un PREVIEW de los correos...\n")
    enviar_correos(PASARELAS_PRIORITARIAS, tu_email, tu_password, 
                   tu_nombre, tu_empresa, tu_telefono, solo_preview=True)
    
    # Preguntar si enviar realmente
    respuesta = input("\n¿Deseas enviar los correos realmente? (s/n): ").strip().lower()
    
    if respuesta == 's':
        print("\n⚠️  ENVIANDO CORREOS REALES...\n")
        enviar_correos(PASARELAS_PRIORITARIAS, tu_email, tu_password, 
                       tu_nombre, tu_empresa, tu_telefono, solo_preview=False)
        print("\n✅ Proceso completado!")
    else:
        print("\n✅ Preview completado. Los correos NO se enviaron.")

if __name__ == "__main__":
    main()


