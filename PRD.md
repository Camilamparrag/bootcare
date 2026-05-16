# Documento de Requisitos del Producto (PRD)
# MVP — Red Social para Bootcamp
## Proyecto: BootcampConnect

**Versión:** 1.0  
**Estado:** MVP  
**Framework Principal:** Django 6.0 / Django 5.2+  
**Base de Datos:** SQLite (MVP) / PostgreSQL (Producción)  
**Fecha:** Mayo 2026  

---

# 1. Resumen Ejecutivo

BootcampConnect es una red social privada diseñada exclusivamente para estudiantes, graduados e instructores de un bootcamp tecnológico.  

La plataforma busca mejorar el engagement, la colaboración y la comunicación dentro de la comunidad educativa mediante funcionalidades sociales modernas inspiradas en plataformas como Instagram y Discord.

Además, incorpora una sección anónima llamada:

> **“Lo que callamos en el Bootcamp”**

donde los estudiantes podrán compartir frustraciones, experiencias y desahogos sin exponer su identidad públicamente.

---

# 2. Objetivos del Producto

## Objetivos Principales

- Incrementar la participación de estudiantes dentro del ecosistema del bootcamp.
- Generar comunidad entre alumnos, graduados e instructores.
- Facilitar la comunicación directa mediante chats privados.
- Permitir compartir avances, proyectos y experiencias técnicas.
- Crear un espacio seguro y anónimo para expresión emocional y feedback interno.

---

# 3. Alcance del MVP

El MVP se enfocará únicamente en las funcionalidades esenciales para validar el producto rápidamente.

## Incluye

- Registro e inicio de sesión
- Perfil de usuario
- Sistema de seguidores
- Feed de publicaciones
- Likes y comentarios
- Publicaciones anónimas
- Chats privados 1 a 1
- Subida de imágenes
- Feed personalizado

## No Incluye (Post-MVP)

- Notificaciones push
- Historias estilo Instagram
- Streaming
- Video llamadas
- Reacciones avanzadas
- Moderación automática con IA
- Aplicación móvil nativa

---

# 4. User Personas

## 4.1 Diego — Estudiante Estresado

### Perfil
- Estudiante de programación
- Pasa más de 10 horas al día programando
- Vive frustraciones constantes con entregas y bugs

### Necesidades
- Compartir avances
- Ver proyectos de compañeros
- Recibir apoyo de la comunidad
- Tener un espacio seguro para desahogarse

---

## 4.2 Seba — Instructor/Mentor

### Perfil
- Instructor técnico del bootcamp
- Supervisa proyectos y progreso de alumnos

### Necesidades
- Publicar anuncios
- Compartir contenido educativo
- Resolver dudas
- Mantener interacción constante con estudiantes

---

# 5. Requisitos Funcionales

# 5.1 Gestión de Usuarios y Autenticación

## Funcionalidades

### Registro de usuarios
- Registro mediante email
- Validación de credenciales
- Restricción mediante invitación o dominio permitido

### Inicio de sesión
- Sistema de autenticación nativo de Django
- Manejo de sesiones

### Perfil de usuario
Cada usuario tendrá:

- Username
- Avatar
- Biografía
- Link de GitHub
- Link de LinkedIn
- Contador de seguidores
- Contador de seguidos

---

# 5.2 Sistema de Seguidores

## Funcionalidades

- Seguir usuarios
- Dejar de seguir usuarios
- Ver seguidores
- Ver seguidos
- Construcción dinámica del feed según usuarios seguidos

## Relación Técnica

ManyToMany asimétrica hacia el modelo User.

---

# 5.3 Feed de Publicaciones

## Funcionalidades

### Crear publicación
- Imagen
- Descripción
- Fecha automática
- Hashtags opcionales

### Interacciones
- Dar Like
- Quitar Like
- Comentar publicaciones

---

# 5.4 Sección Anónima
## “Lo que callamos en el Bootcamp”

## Objetivo

Permitir que estudiantes puedan expresar frustraciones o experiencias sin revelar su identidad.

## Reglas de Privacidad

### IMPORTANTE
Aunque el sistema podrá almacenar internamente el autor real por motivos administrativos:

- Nunca deberá exponerse públicamente.
- La API jamás retornará información del autor.
- Las vistas siempre mostrarán:

```text
Autor: Anónimo
```

## Funcionalidades

- Publicaciones anónimas
- Comentarios anónimos
- Likes anónimos visibles públicamente

---

# 5.5 Sistema de Chats

## Chat Privado 1 a 1

### MVP Inicial
Implementación basada en:

- HTTP tradicional
- AJAX Polling

### Tecnologías Futuras
- Django Channels
- WebSockets
- Redis

---

# 6. Arquitectura Técnica

# Stack Principal

| Componente | Tecnología |
|---|---|
| Backend | Django 6 |
| Base de Datos | SQLite  |
| Frontend | Django Templates |
| CSS | TailwindCSS |
| ORM | Django ORM |
| Autenticación | django.contrib.auth |
| Manejo de Imágenes | Pillow |

---

# 7. Modelo de Datos (Django ORM)

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    github_url = models.URLField(blank=True)

    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )


class Post(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    image = models.ImageField(upload_to='posts/')
    caption = models.TextField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(
        User,
        related_name='liked_posts',
        blank=True
    )


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)


class AnonymousConfession(models.Model):

    # Usuario oculto para moderación interna
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='confessions'
    )

    content = models.TextField(max_length=2000)

    created_at = models.DateTimeField(auto_now_add=True)

    likes = models.ManyToManyField(
        User,
        related_name='liked_confessions',
        blank=True
    )


class AnonymousComment(models.Model):

    confession = models.ForeignKey(
        AnonymousConfession,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)


class ChatMessage(models.Model):

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )

    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )

    message = models.TextField()

    is_read = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now_add=True)
```

---

# 8. Requisitos No Funcionales

## Rendimiento
- Optimización ORM con:
  - `select_related()`
  - `prefetch_related()`

## Seguridad
- Protección CSRF
- Validación de formularios
- Restricción de acceso
- Sanitización de inputs

## Almacenamiento de Medios
- Desarrollo local:
  - MEDIA_ROOT
  - MEDIA_URL

- Producción:
  - AWS S3
  - Cloudinary

---

# 9. Estructura Inicial del Proyecto

```text
bootcampconnect/
│
├── accounts/
├── posts/
├── comments/
├── confessions/
├── chat/
├── core/
│
├── media/
├── static/
│
├── templates/
│
├── manage.py
└── requirements.txt
```

---

# 10. Métricas de Éxito del MVP

## KPIs Principales

### Adopción
- 70% de alumnos activos registrados durante la primera semana

### Engagement
- Número de publicaciones diarias
- Likes promedio por publicación
- Cantidad de comentarios

### Uso de la Sección Anónima
- Actividad constante
- Participación recurrente

---

# 11. Roadmap Post-MVP

## Futuras Funcionalidades

### Tiempo Real
- Django Channels
- WebSockets

### Moderación Inteligente
- Filtro de palabras prohibidas
- Moderación mediante IA

### Integraciones
- Discord
- Slack
- GitHub

### Sistema de Notificaciones
- Push notifications
- Alertas en tiempo real

---

# 12. Riesgos Técnicos

| Riesgo | Mitigación |
|---|---|
| Exposición accidental de identidad anónima | Revisiones estrictas de serializers y templates |
| Problemas de rendimiento en el feed | Optimización ORM |
| Escalabilidad de imágenes | Uso futuro de CDN |
| Spam o abuso | Moderación y reportes |

---

# 13. Conclusión

BootcampConnect busca convertirse en el núcleo social del bootcamp, combinando:

- Comunidad
- Aprendizaje
- Networking
- Comunicación
- Expresión emocional segura

El MVP prioriza velocidad de desarrollo, simplicidad técnica y validación temprana del engagement estudiantil.
