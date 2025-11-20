# Instrucciones para Enviar Consultas a Pasarelas de Pago

## Archivos Creados

1. **pasarelas_filtradas.txt** - Lista filtrada y ordenada de pasarelas de pago según tus criterios
2. **enviar_consultas_pasarelas.py** - Script para enviar correos automáticamente

## Pasos para Enviar los Correos

### Opción 1: Usar Variables de Entorno (Recomendado)

```bash
# Configurar tus credenciales
export EMAIL_FROM="tu_email@gmail.com"
export EMAIL_PASSWORD="tu_app_password"  # Para Gmail, usa App Password
export TU_NOMBRE="Tu Nombre"
export TU_EMPRESA="Nombre de tu Empresa"
export TU_TELEFONO="+52 55 1234 5678"

# Ejecutar el script
python enviar_consultas_pasarelas.py
```

### Opción 2: Ejecutar Interactivamente

```bash
python enviar_consultas_pasarelas.py
```

El script te pedirá la información necesaria.

## Configuración de Gmail

Si usas Gmail, necesitarás crear una "App Password":

1. Ve a tu cuenta de Google: https://myaccount.google.com/
2. Seguridad → Verificación en 2 pasos (debe estar activada)
3. Contraseñas de aplicaciones → Generar nueva
4. Usa esa contraseña como `EMAIL_PASSWORD`

## Configuración para Otros Proveedores de Email

### Outlook/Hotmail
```bash
export SMTP_SERVER="smtp-mail.outlook.com"
export SMTP_PORT="587"
```

### Yahoo
```bash
export SMTP_SERVER="smtp.mail.yahoo.com"
export SMTP_PORT="587"
```

### Otros proveedores
Consulta la configuración SMTP de tu proveedor de email.

## Verificar Direcciones de Email

⚠️ **IMPORTANTE**: Las direcciones de email en el script son genéricas. Antes de enviar, verifica las direcciones correctas de contacto en los sitios web de cada pasarela:

1. **dLocal**: https://www.dlocal.com/contact/
2. **EBANX**: https://www.ebanx.com/en/contact/
3. **SegPay**: https://segpay.com/contact/
4. **EasyPayDirect**: https://www.easypaydirect.com/contact/
5. **PayU México**: https://corporate.payu.com/mexico/contacto/
6. **Adyen**: https://www.adyen.com/contact
7. **Checkout.com**: https://www.checkout.com/contact
8. **Mobbex**: https://www.mobbex.com/contacto
9. **ePayco**: https://epayco.com/contacto/
10. **ETPay**: https://etpay.com/contacto
11. **Fiserv México**: https://www.fiserv.com.mx/contacto

## Pasarelas Prioritarias para Contactar

El script enviará correos a estas 11 pasarelas prioritarias:

1. **dLocal** - Muy popular en LatAm para high-risk
2. **EBANX** - Muy popular en LatAm
3. **SegPay** - Especializado en high-risk/apuestas
4. **EasyPayDirect** - Especializado en high-risk/apuestas
5. **PayU México** - Presencia específica en México
6. **Adyen** - Para alto volumen (tarifas 0.6%-1.5%)
7. **Checkout.com** - Para alto volumen (tarifas 0.8%-1.2%)
8. **Mobbex** - Popular en Argentina, expandiéndose
9. **ePayco** - Popular en Colombia
10. **ETPay** - Tiene sitio específico para México
11. **Fiserv México** - Soluciones empresariales

## Contenido del Correo

El correo incluye:
- Información de tu empresa
- Solicitud de tarifas y comisiones
- Consulta sobre políticas para industria de apuestas
- Solicitud para agendar llamada el viernes 10am-4pm (hora de México)

## Modo Preview

El script primero muestra un PREVIEW de todos los correos sin enviarlos. Solo después de revisar, puedes confirmar el envío real.

## Solución de Problemas

### Error de autenticación
- Verifica que tu contraseña sea correcta
- Para Gmail, usa App Password, no tu contraseña normal
- Asegúrate de tener habilitada la verificación en 2 pasos

### Error de conexión SMTP
- Verifica que SMTP_SERVER y SMTP_PORT sean correctos
- Algunos proveedores requieren conexión segura (TLS/SSL)

### Correos no llegan
- Verifica que las direcciones de email sean correctas
- Revisa tu carpeta de spam
- Algunas pasarelas pueden tener filtros anti-spam estrictos

## Próximos Pasos

1. Revisa el archivo `pasarelas_filtradas.txt` para ver todas las opciones
2. Verifica las direcciones de email antes de enviar
3. Ejecuta el script en modo preview primero
4. Revisa los correos antes de enviar
5. Confirma el envío
6. Monitorea las respuestas y agenda las llamadas

## Notas Adicionales

- Las pasarelas pueden tardar 1-3 días hábiles en responder
- Algunas pueden requerir información adicional antes de dar tarifas
- Prepara información sobre tu volumen de transacciones esperado
- Ten lista documentación de tu empresa si la solicitan


