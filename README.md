# INVESTIGACIÓN APIS

# INTEGRANTES
- Tyron Morales (tayron.morales@unl.edu.ec) 
- Luis Blacio (luis.blacio@unl.edu.ec)
- Santiago Villamagua (santiago.villamagua@unl.edu.ec)
- Mathias Medina ( mathias.medina@unl.edu.ec )
# APIS A UTILIZAR EN EL MENUBOARD
- Api para delibery de dos funciones " PICKER "  https://www.pickerexpress.com/es/desarrollador/documentacion-api-delivery
- Api para pago con tarjetas de credito y facturación " RAMPAGO " https://rapidapi.com/RampagoHub/api/rampago-seamless-fiat-to-usdc-fiat-ramp

#  API PICKER 
La API Picker es una interfaz utilizada en aplicaciones web para permitir a los usuarios seleccionar archivos de su dispositivo o de servicios en la nube de manera eficiente.


Picker te permitirá conectar tus plataformas y/o comercios a distintos proveedores de delivery de la región en la que te encuentras. La integración con Picker a través de su API te ofrece las siguientes capacidades:

- Administración de locales.
- Automatizar la creación de pedidos desde tu plataforma.
- Realizar consultas de tarifas.
- Recibir en tiempo real las actualizaciones de tu pedido.

 Funciona en 2 partes, es decir 2 APIS en una sola, que se pueden usar y combinar a la vez:
 - Primera parte para crear un pedido
 - La segunda parte para calcuar el costo de entraga por pedido

# Crear un pedido
Para entender un poco la lógica que maneja Picker, una cuenta se la denomina Empresa. Cada empresa puede tener N locales (que pueden representar tiendas, restaurantes, puntos de despacho). Cada local obligatoriamente debe estar referenciado con una dirección y una geolocalización (se las requiere al momento de crearlas). Por ejemplo: Si tu empresa va a manejar 2 sucursales, deberás crear 2 locales, Todo pedido creado en la plataforma de Picker es determinado por un estado. El estado de un pedido es una parte importante del ciclo de vida del mismo. Estos estados pueden indicar si el pedido esta terminado, cancelado o aun en proceso. Es importante que en la integración que se vaya a desarrollar se mapeen todos los estados posibles, para que el cliente tenga muy claro lo que significa cada estado.

## Estados de Pedido

### ON_HOLD: 
Es el estado inicial del pedido si existe un tiempo de preparación. Durante este estado, el pedido aún no busca conductor. Pasa automáticamente a READY_FOR_PICKUP si:
- Se cumple el tiempo de preparación o cooktime.
- Se activa manualmente la búsqueda desde dashboard.
- Se activa mediante el endpoint de Start Search.


### READY_FOR_PICKUP

En este estado se inicia la búsqueda de motorizados en los distintos proveedores activados para el local. Este estado se puede disparar en los siguientes escenarios.

- Se termina tiempo de preparación de pedido en ON_HOLD
- Se inicia una búsqueda manualmente
- Si un pedido ya con conductor ejecuta una nueva búsqueda de conductores. (Por ejemplo: Pedido en ACCEPTED con conductor vuelve a READY_FOR_PICKUP).
- Si el pedido se crea sin tiempo de preparación, será el estado inicial del pedido.
   
### ACCEPTED
Este estado se guarda en el pedido al momento que un proveedor asigna un motorizado al pedido. Este estado únicamente llega por medio del webhook de DRIVER_ASSIGNED 

### ARRIVED_AT_PICKUP
Cuando el conductor notifica que el conductor llego al local y esta esperando que local le entregue el pedido

### WAY_TO_DELIVER
Cuando el conductor indica que abandono el local y va en dirección al punto de entrega

### ARRIVED_AT_DELIVERY
Cuando el conductor llega donde el cliente y esta por terminar el pedido

### COMPLETED
Pedido fue completado satisfactoriamente

### PROVIDER_NOT_FOUND
Cuando ningún proveedor activado para tu local no puede atender tu pedido. No se ejecuta ninguna búsqueda

### CANCELLED_BY_BUSINESS
Negocio dispara la cancelación del pedido. Esto puede suceder cuando:

- Pedido es cancelado desde dashboard
- Pedido es cancelado vía API por medio del endpoint de Cancel Booking

### CANCELLED_BY_ADMIN
Cuando la cancelación es disparada por el área de Soporte de Picker

### CANCELLED_BY_DELIVERY_PROVIDER
Cuando la cancelación es disparada por el proveedor de delivery


### NOT_DELIVERED
Cuando el pedido no pudo ser entregado al cliente; y el paquete de entrega no puede ser devuelto al negocio


### RETURNING
Cuando el pedido no pudo ser entregado al cliente y el pedido esta en camino a ser retornado al negocio

### RETURNED
Cuando el pedido fue retornado exitosamente al negocio

# Costo de Pedido
El endpoint de Pre Checkout te permitirá consultar precios y valores del pedido que necesites realizar. Además de eso, te indicará si es posible que podamos atender tu pedido (si el pedido cubre una distancia muy larga entre el local y el punto de entrega; o el punto de entrega esta fuera de cobertura, devolveremos un mensaje de error).

Para este endpoint es obligatorio la locación del punto de entrega. La ubicación del local ya la obtenemos automáticamente por el Api Key del negocio que usas en la autorización.

Otros datos que puedes ingresar en este endpoint son:

- paymentMethod: Es el método de pago que usarás para el pedido. En el caso que exista un pago en efectivo al momento de entregar el pedido, deberás usar CASH. Caso contrario, si no hay ningún pago de por medio y el conductor unicamente tiene que recoger el pedido y entregarle al cliente, deberás usar CARD.  
- carName: Indicá el tipo de vehículo que necesitas para tu pedido. Si es un pedido de dimensiones pequeñas y necesitas una moto, debes ingresar aquí BIKE. Si tu pedido es de mayores dimensiones y necesitas un coche, deberás usar LITE.

# API RAMPAGO

La API de Rampago es una herramienta diseñada para facilitar la conversión de moneda fiduciaria (fiat) a USDC (USD Coin). Esta API es especialmente útil para aplicaciones que requieren integrar la compra o conversión de criptomonedas de manera sencilla y segura, ofreciendo una interfaz programática para interactuar con el servicio de Rampago. Permitiendo una variedad de transacciones entre diferentes tipos de moneda/ criptomoneda, y operar de manera sencilla con los mismos, por medio de las conversiones y/o transacciones de cualquier tipo por medio de una moneda USDC como intermediario en las operaciones

## Endpoints Principales de la API

La API de Rampago ofrece varios endpoints clave para interactuar con su servicio tales y como:

1. Obtener una lista de bancos soportados, usando el método GET, para obtener como resultado, los bancos disponibles para efectuar la transacción a realizarse
2. Iniciar una Transacción empleando el método POST ya habiendo revisado el banco, los datos del usuario y la moneda a convertir, para devolver como resultado una lista de detalles para completar el pago 
3. Verificar Estado de una Transacción, usando el método GET, y como dato de ingreso la ID de la transacción, y emitiendo una respuesta como pendiente, completada o fallida
4. Obtener Tasas de Conversión entre monedas empleando el método GET y una serie de fórmulas entre los diferentes tipos de moneda como euros o dólares, y convertirlos en otro tipo de moneda y otra posible cantidad de moneda establecida bajo una serie de conversiones detalladas en el resultado

## AUTENTICACIONES

La API de Rampago requiere de realizar algunas autenticaciones, usando API Keys en el encabezado de las solicitudes realizadas, empleando los siguientes encabezados
- X-RapidAPI-Key que identifica la clave API del usuario para validar la autenticación.
- X-RapidAPI-Host que define el host de la API de Rampago para direccionar la solicitud correctamente.

 ## INTEGRACIÓN DE LIBRERIAS PARA SOLICITUDES
 
Para realizar cualquier interacción entre la API usando Django, se requiere de una librería que permita realizar cualquier solicitud HTTP con la información mencionada en la sección de los endpoints, algunas como httpx o requests que facilitan las solicitudes.

## PROCESOS DE INTEGRACIÓN CLAVE
Una vez completado ese hito, comenzamos los procesos de la integración que determinan las acciones a realizarse dentro del proyecto Django, primero se inicia una transacción enviando una solicitud a la API para crear una nueva, esta parte del proceso considera los datos iniciales de una transacción como el banco al que se realizara su transacción, la cantidad y la moneda que se manejarán y los datos personales del usuario. El objetivo del proceso es enviar los datos principales de la API, respondiendo con el estado de la misma, empleada en el siguiente proceso que es la verificación del estado, proceso necesario para determinar si la transacción fue aprobada, sigue procesándose, o si fue rechazada y para ello se emplea la ID de la transacción generada por medio de los datos personales y mantener una verificación del estado de la operación, estos dos son los pilares básicos en la integración de procesos en Django.

## CONFIGURACIÓN DE RUTAS

Luego se debe continuar configurando las rutas en Django para definir los accesos a las funciones de la aplicación en las URL, las rutas se configuran en el archivo urls.py de la aplicación, definiendo el archivo principal, el de rutas y las vistas asociadas a cada ruta, para configurar rutas en django se debe crear o editar el archivo urls.py en la aplicación usando path() o re_path(). Luego incluimos las rutas en el archivo para que sean accesibles de forma global, finalmente podemos probar el funcionamiento ejecutando el servidor de desarrollo usando las URLs definidas.

## CONSIDERACIONES ADICIONALES

Hay que considerar algunos detalles a la hora de implementar la API en un proyecto Django, para garantizar seguridad, estabilidad y funcionalidad como No exponer la clave API en el frontend, ya que Las API keys son privadas, si se exponen pueden ser robadas, para ello se debe usar la clave solo en el backend y no en los archivos que el usuario pueda acceder y manejar la comunicación con la API exclusivamente en el servidor. También es buena opción Almacenar la clave API en variables de entorno(Archivo .env), para evitar que las claves se registren en el control de versiones, así como almacenar claves sin alterar el código, por último se debe gestionar los errores de la manera lo más adecuada para evitar fallos en la aplicación, para ello se deben validar los datos antes de enviarlos a la API, manejar las respuestas HTTP bajo errores, proceder a reintentar después de atravesar un fallo al cabo de un tiempo y registrar los errores para futuros análisis
