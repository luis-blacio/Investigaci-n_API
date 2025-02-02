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
