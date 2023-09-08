# Generador de menús

## Introducción

La Aplicación de Generación de Menús es una aplicación web diseñada para permitir a los usuarios crear, administrar y compartir menús personalizados. La aplicación consta de un backend desarrollado en Python y un frontend desarrollado en React. Esta documentación proporciona una visión general de las pantallas y características principales de la aplicación, así como detalles técnicos sobre su funcionamiento.

## Pantallas y Características

### 1. Pantalla de Inicio de Sesión (Login)

- Descripción: Esta pantalla permite a los usuarios iniciar sesión en la aplicación utilizando sus credenciales.
- Funcionalidades:
  - Iniciar sesión con nombre de usuario y contraseña.
  - Recuperar contraseña (opción).
- Flujo de Uso: Los usuarios deben autenticarse antes de acceder a otras funcionalidades de la aplicación.

### 2. Pantalla de Inicio (Home)

- Descripción: La pantalla de inicio es la página principal de la aplicación después del inicio de sesión.
- Funcionalidades:
  - Mostrar los menús creados por el usuario.
  - Crear nuevos menús.
  - Actualizar automáticamente los precios de los menús en base al precio del dólar (opción).
- Flujo de Uso: Los usuarios pueden ver y gestionar sus menús desde esta pantalla.

### 3. Crear Menú

- Descripción: En esta pantalla, los usuarios pueden crear un nuevo menú personalizado.
- Funcionalidades:
  - Agregar productos con nombre, precio y una descripción, categoría e imagen opcionales.
  - Opción para habilitar la actualización automática de precios en función del cambio en el precio del dólar.
- Flujo de Uso: Los usuarios pueden crear menús personalizados y definir los detalles de los productos que lo componen.

### 4. Visualizar Menú

- Descripción: Esta pantalla permite a los usuarios ver un menú creado y realizar acciones relacionadas.
- Funcionalidades:
  - Compartir el menú mediante un QR o enlace.
  - Imprimir el menú.
  - Guardar el menú como PDF.
- Flujo de Uso: Los usuarios pueden acceder a esta pantalla desde la lista de menús y realizar acciones relacionadas con un menú específico.

## Características Extra

### Actualización Automática de Precios

- Descripción: Los menús pueden actualizarse automáticamente en base al precio del dólar si el usuario marca la opción correspondiente al crear el menú.
- Funcionalidad:
  - Los precios de los productos en el menú se actualizan automáticamente en función del cambio en el precio del dólar.
- Flujo de Uso: Los usuarios pueden habilitar esta opción al crear un menú, lo que asegura que los precios reflejen cambios en el valor del dólar.

## Tecnologías Utilizadas

- Backend: Python
- Frontend: React
- Base de Datos: MongoDB
- Otros componentes y bibliotecas (listar bibliotecas y herramientas adicionales utilizadas en el proyecto)

## Requisitos del Sistema

- Navegador web moderno con soporte para JavaScript habilitado.

## Conclusiones

La Aplicación de Generación de Menús es una herramienta versátil que permite a los usuarios crear, gestionar y compartir fácilmente menús personalizados. Con características adicionales como la actualización automática de precios, se asegura de que los menús siempre estén actualizados y reflejen cambios en el valor del dólar. Este documento proporciona una visión general de las características principales y la tecnología utilizada en la aplicación.
